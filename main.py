import numpy as np
import pandas as pd

import aiwolf

from game_setting import game_setting_15


sample_15_path = "./sample_data/local_test/AIWolf20230614182753.log"


class DataHandler:

    def __init__(self, file_path, agent_idx):
        self.file_path = file_path
        self.agent_idx = agent_idx
        self.role_map = dict()
        self.game_info = None
        self.game_setting = None

    def _initialize(self):
        # find role
        roles = pd.read_csv(self.file_path, names=['_0', '_1', 'agent_idx', 'role', '_2', 'agent_name']).head(15)
        for _, row in roles.iterrows():
            self.role_map[int(row["agent_idx"])] = str(row["role"])

        _packet = dict()
        _packet['gameInfo'] = dict()
        _packet['gameInfo']['agent'] = self.agent_idx
        _packet['gameInfo']['attackVoteList'] = []
        _packet['gameInfo']['attackedAgent'] = -1
        _packet['gameInfo']['cursedFox'] = -1
        _packet['gameInfo']['day'] = 0
        _packet['gameInfo']['divineResult'] = None
        _packet['gameInfo']['executedAgent'] = -1
        _packet['gameInfo']['existingRoleList'] = ['BODYGUARD', 'MEDIUM', 'POSSESSED', 'SEER', 'VILLAGER', 'WEREWOLF']
        _packet['gameInfo']['guardedAgent'] = -1
        _packet['gameInfo']['lastDeadAgentList'] = []
        _packet['gameInfo']['latestAttackVoteList'] = []
        _packet['gameInfo']['latestExecutedAgent'] = -1
        _packet['gameInfo']['latestVoteList'] = []
        _packet['gameInfo']['mediumResult'] = None
        _packet['gameInfo']['remainTalkMap'] = {str(i): game_setting_15["maxTalk"] for i in range(1, 16)}
        _packet['gameInfo']['remainWhisperMap'] = dict()
        _packet['gameInfo']['roleMap'] = {str(self.agent_idx): self.role_map[int(self.agent_idx)]}
        # fill if the agent is WEREWOLF
        if self.role_map[int(self.agent_idx)] == "WEREWOLF":
            for i in range(1, 16):
                if self.role_map[i] == "WEREWOLF":
                    _packet['gameInfo']['remainWhisperMap'][str(i)] = game_setting_15["maxWhisper"]
                    _packet['gameInfo']['roleMap'][str(i)] = "WEREWOLF"
        _packet['gameInfo']['statusMap'] = {str(i): 'ALIVE' for i in range(1, 16)}
        _packet['gameInfo']['talkList'] = []
        _packet['gameInfo']['voteList'] = []
        _packet['gameInfo']['whisperList'] = []

        _packet['gameSetting'] = game_setting_15
        _packet['request'] = 'INITIALIZE'
        _packet['talkHistory'] = None
        _packet['whisperHistory'] = None
        print(_packet)
        self.game_info = aiwolf.GameInfo(_packet['gameInfo'])
        self.game_setting = aiwolf.GameSetting(_packet['gameSetting'])


if __name__ == "__main__":
    dh = DataHandler(sample_15_path, 15)
    dh._initialize()
