from collections import deque
import csv
import pandas as pd


sample_15_path = "./sample_data/local_test/AIWolf20230614182753.log"


class GameServer:

    def __init__(self, n_players):
        self.n_players = n_players
        self.role_map = None
        self.agent_idx = 1
        self.request = "NAME"
        self._packet = dict()
        self.log = {
            "agent": [], "day":  [],
            "type": [], "idx": [],
            "turn": [], "text": [],
        }

    def start_game(self, game_file_path):
        # read log
        with open(game_file_path, newline='') as csvfile:
            log_reader = csv.reader(csvfile, delimiter=',')
            self.log = {
                "agent": [], "day":  [],
                "type": [], "idx": [],
                "turn": [], "text": [],
            }
            medium = 0
            for row in log_reader:
                if row[1] == "status" and int(row[0]) == 0:
                    self.log["agent"].append(int(row[2])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('initialize'),
                    self.log["idx"].append(int(row[2])),
                    self.log["turn"].append(0),
                    self.log["text"].append('COMINGOUT Agent[' + "{0:02d}".format(int(row[2])) + '] ' + row[3])
                    # medium
                    if row[3] == "MEDIUM":
                        medium = row[2]
                elif row[1] == "status":
                    pass
                elif row[1] == "talk":
                    self.log["agent"].append(int(row[4])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('talk'),
                    self.log["idx"].append(int(row[2])),
                    self.log["turn"].append(int(row[3])),
                    self.log["text"].append(row[5])
                elif row[1] == "whisper":
                    self.log["agent"].append(int(row[4])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('whisper'),
                    self.log["idx"].append(int(row[2])),
                    self.log["turn"].append(int(row[3])),
                    self.log["text"].append(row[5])
                elif row[1] == "vote":
                    self.log["agent"].append(int(row[3])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('vote'),
                    self.log["idx"].append(int(row[2])),
                    self.log["turn"].append(0),
                    self.log["text"].append('VOTE Agent[' + "{0:02d}".format(int(row[3])) + ']')
                elif row[1] == "attackVote":
                    self.log["agent"].append(int(row[3])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('attack_vote'),
                    self.log["idx"].append(int(row[2])),
                    self.log["turn"].append(0),
                    self.log["text"].append('ATTACK Agent[' + "{0:02d}".format(int(row[3])) + ']')
                elif row[1] == "divine":
                    self.log["agent"].append(int(row[3])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('divine'),
                    self.log["idx"].append(int(row[2])),
                    self.log["turn"].append(0),
                    self.log["text"].append('DIVINED Agent[' + "{0:02d}".format(int(row[3])) + '] ' + row[4])
                elif row[1] == "execute":
                    # for all
                    self.log["agent"].append(int(row[2])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('execute'),
                    self.log["idx"].append(0),
                    self.log["turn"].append(0),
                    self.log["text"].append('Over')
                    # for medium
                    res = 'HUMAN'
                    if row[3] == 'WEREWOLF':
                        res = 'WEREWOLF'
                    self.log["agent"].append(int(row[2])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('identify'),
                    self.log["idx"].append(medium),
                    self.log["turn"].append(0),
                    self.log["text"].append('IDENTIFIED Agent[' + "{0:02d}".format(int(row[2])) + '] ' + res)
                elif row[1] == "guard":
                    self.log["agent"].append(int(row[3])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('guard'),
                    self.log["idx"].append(int(row[2])),
                    self.log["turn"].append(0),
                    self.log["text"].append('GUARDED Agent[' + "{0:02d}".format(int(row[3])) + ']')
                elif row[1] == "attack":
                    self.log["agent"].append(int(row[2])),
                    self.log["day"].append(int(row[0])),
                    self.log["type"].append('attack'),
                    self.log["idx"].append(0),
                    self.log["turn"].append(0),
                    self.log["text"].append('ATTACK Agent[' + "{0:02d}".format(int(row[2])) + ']')
                    if row[3] == 'true':
                        # dead
                        self.log["agent"].append(int(row[2])),
                        self.log["day"].append(int(row[0])),
                        self.log["type"].append('dead'),
                        self.log["idx"].append(0),
                        self.log["turn"].append(0),
                        self.log["text"].append('Over')
                elif row[1] == "result":
                    pass
                else:
                    pass
        # find role from log
        roles = pd.read_csv(
            game_file_path, names=['_0', '_1', 'agent_idx', 'role', '_2', 'agent_name']
        ).head(self.n_players)
        self.role_map = {int(row["agent_idx"]): str(row["role"]) for _, row in roles.iterrows()}
        self.request = "ROLE"
        self.agent_idx = 1

    def current_step(self):
        return self.request, self.agent_idx

    def next_step(self):
        if self.request == "NAME":
            if self.agent_idx < self.n_players:
                self.agent_idx += 1
            else:
                self.request = "DATA"
                self.agent_idx = -1
        elif self.request == "ROLE":
            if self.agent_idx < self.n_players:
                self.agent_idx += 1
            else:
                self.request = "INITIALIZE"
                self.agent_idx = 1

        return None

    def create_packet(self):
        pass

    def _update(self):
        pass




if __name__ == "__main__":
    gs = GameServer(15)
    for _ in range(15):
        print(gs.current_step())
        gs.next_step()
    gs.start_game(sample_15_path)
    for _ in range(15):
        print(gs.current_step())
        gs.next_step()
