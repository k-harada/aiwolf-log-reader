from collections import deque
import csv
import pandas as pd


from game_info import base_info_15
from game_setting import game_setting_15


class GameServer:

    def __init__(self):
        self.n_players = -1
        self.game_setting = game_setting_15
        self.game_info = base_info_15
        self.request = "NAME"

    def initialize(self, n_players, role_map):
        self.n_players = n_players
        # TODO: if n_players == 15:
        self.game_setting = game_setting_15
        self.game_info = base_info_15
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

    def day_start(self):
        self.game_info["day"] += 1
        self.game_info["talkList"] = []
        self.game_info["whisperList"] = []
        self.game_info["voteList"] = self.game_info["latestVoteList"]
        self.game_info["latestVoteList"] = []
        self.game_info["attackVoteList"] = self.game_info["latestAttackVoteList"]
        self.game_info["latestAttackVoteList"] = []
        self.game_info["executedAgent"] = self.game_info["latestExecutedAgent"]
        self.game_info["latestExecutedAgent"] = -1

    def day_finish(self):
        self.game_info["divineResult"] = None
        self.game_info["guardedAgent"] = -1
        self.game_info["mediumResult"] = None

    def push_contents(self, request, contents):
        if request == "TALK":
            self.game_info["talkList"].append(contents)
        elif request == "WHISPER":
            self.game_info["whisperList"].append(contents)
        elif request == "VOTE":
            self.game_info["latestVoteList"].append(contents)
        elif request == "ATTACK":
            self.game_info["latestAttackVoteList"].append(contents)
        elif request == "INITIALIZE":
            pass
        elif request == "DAILY_INITIALIZE":
            pass
        elif request == "DAILY_FINISH":
            pass
        elif request == "DIVINE":
            self.game_info["divineResult"] = contents
        elif request == "GUARD":
            self.game_info["guardedAgent"] = contents["target"]
        elif request == "RUN_ATTACK":
            if contents["result"] == "true":
                self.game_info["lastDeadAgentList"].append(contents["target"])
            self.game_info["attackedAgent"] = contents["target"]
        elif request == "EXECUTE":
            self.game_info["executedAgent"] = contents["target"]
        elif request == "FINISH":
            pass
        else:
            raise NotImplementedError(f"request: {request}, contents: {contents}")
        if self.game_info["day"] <= 2:
            print(self.game_info)
        return None

    def create_packet(self):
        pass

    def _update(self):
        pass
