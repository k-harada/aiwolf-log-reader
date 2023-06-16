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
        self.position += self.n_players
        self.phase = "INITIALIZE"
        self.agent_idx = 1
        self.day = 0
        self.role_map = dict()
        for i in range(self.n_players):
            contents = self.log[i]["contents"]
            self.role_map[str(contents["agent"])] = contents["role"]
        self.queue = deque([])
        for i in range(self.n_players):
            self.queue.append((i + 1, "INITIALIZE"))
        self.server.initialize(self.n_players, self.role_map)

    def next_step(self):

        if len(self.queue) > 0:
            return self.queue.popleft()

        if self.phase == "INITIALIZE":
            self.phase = "DAILY_INITIALIZE"
            for i in range(self.n_players):
                self.queue.append((i + 1, "DAILY_INITIALIZE"))
        elif self.phase == "DAILY_INITIALIZE":
            if self.day == 0:
                self.phase = "DAILY_FINISH"
                for i in range(self.n_players):
                    self.queue.append((i + 1, "DAILY_INITIALIZE"))
            else:
                self.phase = "TALK"
        return self.queue.popleft()


if __name__ == "__main__":
    gm = GameMaster()
    gm.read_log(sample_15_path)
    print(gm.server.game_info["roleMap"])
    for _ in range(15):
        print(gm.next_step())
