from collections import deque

from read_log import read_log
from server import GameServer


sample_15_path = "./sample_data/local_test/AIWolf20230614182753.log"


class GameMaster:

    def __init__(self):
        self.log = dict()
        self.n_players = -1
        self.phase = "INITIALIZE"
        self.agent_idx = 1
        self.day = 0
        self.day_finish = -1
        self.position = 0
        self.server = GameServer()
        self.queue = deque([])
        self.role_map = dict()

    def read_log(self, game_file_path):
        self.log = read_log(game_file_path)
        self.n_players = 0
        for row in self.log:
            if row["type"] != "status":
                break
            else:
                self.n_players = max(self.n_players, row["contents"]["agent"])
        self.position = 0
        self.phase = "INITIALIZE"
        self.agent_idx = 1
        self.day = 0
        self.day_finish = self.log[-1]["contents"]["day"]
        self.role_map = dict()
        for i in range(self.n_players):
            contents = self.log[i]["contents"]
            self.role_map[str(contents["agent"])] = contents["role"]
        self.queue = deque([])
        for i in range(self.n_players):
            self.queue.append((i + 1, "INITIALIZE", None))
        self.server.initialize(self.n_players, self.role_map)

    def push_contents(self, request, contents):
        return self.server.push_contents(request, contents)

    def next_step(self):

        if len(self.queue) > 0:
            return self.queue.popleft()

        if self.position == len(self.log):
            return 0, "DONE", None

        # read log
        log_type, contents = self.log[self.position]["type"], self.log[self.position]["contents"]
        if log_type == "status":
            self.day = contents["day"]
            if self.day < self.day_finish:
                self.phase = "DAILY_INITIALIZE"
                if contents["status"] == 'ALIVE':
                    self.queue.append((contents["agent"], "DAILY_INITIALIZE", None))
            else:
                self.phase = "FINISH"
                self.queue.append((contents["agent"], "FINISH", None))
            self.position += 1
        elif log_type == "talk":
            self.queue.append((contents["agent"], "TALK", contents))
            self.phase = "TALK"
            self.position += 1
        elif log_type == "whisper":
            if self.day == 0 and self.phase == "DAILY_INITIALIZE":
                for i in range(self.n_players):
                    if self.server.game_info["statusMap"][str(i + 1)] == 'ALIVE':
                        self.queue.append((i + 1, "DAILY_FINISH", None))
                self.phase = "DAILY_FINISH"
            self.queue.append((contents["agent"], "WHISPER", contents))
            self.phase = "WHISPER"
            self.position += 1
        elif log_type == "vote":
            if self.phase != "VOTE":
                for i in range(self.n_players):
                    if self.server.game_info["statusMap"][str(i + 1)] == 'ALIVE':
                        self.queue.append((i + 1, "DAILY_FINISH", None))
                self.phase = "VOTE"
            else:
                self.queue.append((contents["agent"], "VOTE", contents))
                self.phase = "VOTE"
                self.position += 1
        elif log_type == "attackVote":
            self.queue.append((contents["agent"], "ATTACK", contents))
            self.phase = "ATTACK_VOTE"
            self.position += 1
        elif log_type == "divine":
            self.queue.append((contents["agent"], "DIVINE", contents))
            self.phase = "DIVINE"
            self.position += 1
        elif log_type == "execute":
            self.queue.append((0, "EXECUTE", contents))
            self.phase = "EXECUTE"
            self.position += 1
        elif log_type == "guard":
            self.queue.append((contents["agent"], "GUARD", contents))
            self.phase = "GUARD"
            self.position += 1
        elif log_type == "attack":
            self.queue.append((0, "RUN_ATTACK", contents))
            self.phase = "ATTACK"
            self.position += 1
        elif log_type == "result":
            self.phase = "RESULT"
            self.position += 1
        else:
            raise ValueError(f"Unknown Log format: {log_type}, {contents}")
        return self.next_step()


if __name__ == "__main__":
    gm = GameMaster()
    gm.read_log(sample_15_path)
    print(gm.server.game_info["roleMap"])
    while True:
        agent_, request_, contents_ = gm.next_step()
        if request_ == "DONE":
            break
        print(agent_, request_, contents_)
