from collections import deque
import csv
import pandas as pd


from game_setting import game_setting_15, base_info_15


sample_15_path = "./sample_data/local_test/AIWolf20230614182753.log"


class GameServer:

    def __init__(self):
        self.n_players = -1
        self.game_setting = game_setting_15
        self.game_info = base_info_15
        self.request = "NAME"
        self.talk_history = []
        self.whisper_history = []

    def initialize(self, n_players, role_map):
        self.n_players = n_players
        # TODO: if n_players == 15:
        self.game_setting = game_setting_15
        self.game_info = base_info_15
        self.talk_history = []
        self.whisper_history = []
        for i in range(n_players):
            self.game_info["roleMap"][str(i + 1)] = role_map[str(i + 1)]

    def next_alive(self, agent_idx):
        for i in range(agent_idx + 1, self.n_players + 1):
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
