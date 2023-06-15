game_setting_15 = {
  "enableNoAttack": False,
  "enableNoExecution": False,
  "enableRoleRequest": False,
  "maxAttackRevote": 1,
  "maxRevote": 1,
  "maxSkip": 2,
  "maxTalk": 10,
  "maxTalkTurn": 20,
  "maxWhisper": 10,
  "maxWhisperTurn": 20,
  "playerNum": 15,
  "randomSeed": 42,
  "roleNumMap": {
    'WEREWOLF': 3, 'FOX': 0, 'FREEMASON': 0, 'MEDIUM': 1, 'POSSESSED': 1,
    'VILLAGER': 8, 'ANY': 0, 'BODYGUARD': 1, 'SEER': 1
  },
  'talkOnFirstDay': False,
  'timeLimit': -1,
  'validateUtterance': True,
  'votableInFirstDay': False,
  'voteVisible': True,
  'whisperBeforeRevote': False
}

base_info_15 = {
  'agent': -1, 'attackVoteList': [], 'attackedAgent': -1, 'cursedFox': -1,
  'day': 0, 'divineResult': None, 'executedAgent': -1, 'existingRoleList': [
    'BODYGUARD', 'MEDIUM', 'POSSESSED', 'SEER', 'VILLAGER', 'WEREWOLF'
  ], 'guardedAgent': -1, 'lastDeadAgentList': [], 'latestAttackVoteList': [],
  'latestExecutedAgent': -1, 'latestVoteList': [], 'mediumResult': None,
  'remainTalkMap': {str(i + 1): game_setting_15["maxTalk"] for i in range(15)},
  'remainWhisperMap': dict(), 'roleMap': dict(),
  'statusMap': {str(i + 1): 'ALIVE' for i in range(15)},
  'talkList': [], 'voteList': [], 'whisperList': []
}
