from collections import deque
import csv
import pandas as pd

from read_log import read_log
from game_setting import game_setting_15, base_info_15


sample_15_path = "./sample_data/local_test/AIWolf20230614182753.log"


class GameServer:

    def __init__(self, n_players):
        self.n_players = n_players
        self.agent_idx = 1
        self.day = 0
        self.log = dict()
        # TODO: if n_players == 15:
        self.game_setting = game_setting_15
        self.game_info = base_info_15
        self.request = "NAME"
        self.talk_history = []
        self.whisper_history = []
        self.reader = 0

    def read_log(self, game_file_path):
        self.log = read_log(game_file_path)
        self.game_info = base_info_15
        self.game_info["roleMap"] = {
            int(self.log["agent"][i]): str(self.log["text"][i].split()[-1]) for i in range(self.n_players)
        }
        self.request = "INITIALIZE"
        self.agent_idx = 1
        self.day = 0

    def current_step(self):
        return self.request, self.agent_idx

    def next_step(self):
        if self.request == "NAME":
            self.agent_idx = self.next_alive()
            if self.agent_idx == -1:
                self.request = "READ_LOG"
                self.agent_idx = -1
        elif self.request == "ROLE":
            self.agent_idx = self.next_alive()
            if self.agent_idx == -1:
                self.request = "INITIALIZE"
                self.agent_idx = self.first_alive()
        elif self.request == "INITIALIZE":
            self.agent_idx = self.next_alive()
            if self.agent_idx == -1:
                self.request = "DAILY_INITIALIZE"
                self.agent_idx = self.first_alive()
        elif self.request == "DAILY_INITIALIZE":
            self.agent_idx = self.next_alive()
            if self.agent_idx == -1:
                if self.day == 0:
                    self.request = "DAILY_FINISH"
                    self.agent_idx = self.first_alive()
                else:
                    self.request = "TALK"
                self.agent_idx = 1
        return None

    def next_alive(self):
        for i in range(self.agent_idx + 1, self.n_players + 1):
            if self.game_info["statusMap"][str(i)] == "ALIVE":
                return i
        return -1

    def first_alive(self):
        for i in range(1, self.n_players + 1):
            if self.game_info["statusMap"][str(i)] == "ALIVE":
                return i
        return -1

    def create_packet(self):
        pass

    def _update(self):
        pass


if __name__ == "__main__":
    gs = GameServer(15)
    gs.read_log(sample_15_path)
    for _ in range(15):
        print(gs.current_step())
        gs.next_step()
    print(gs.game_info)
