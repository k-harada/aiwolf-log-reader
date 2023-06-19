from game_setting import game_setting_15


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
