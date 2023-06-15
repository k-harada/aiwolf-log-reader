import csv


def read_log(game_file_path):

    with open(game_file_path, newline='') as csvfile:
        log_reader = csv.reader(csvfile, delimiter=',')
        log = {
            "agent": [], "day": [],
            "type": [], "idx": [],
            "turn": [], "text": [],
        }
        medium = 0
        for row in log_reader:
            if row[1] == "status" and int(row[0]) == 0:
                log["agent"].append(int(row[2])),
                log["day"].append(int(row[0])),
                log["type"].append('initialize'),
                log["idx"].append(int(row[2])),
                log["turn"].append(0),
                log["text"].append('COMINGOUT Agent[' + "{0:02d}".format(int(row[2])) + '] ' + row[3])
                # medium
                if row[3] == "MEDIUM":
                    medium = row[2]
            elif row[1] == "status":
                pass
            elif row[1] == "talk":
                log["agent"].append(int(row[4])),
                log["day"].append(int(row[0])),
                log["type"].append('talk'),
                log["idx"].append(int(row[2])),
                log["turn"].append(int(row[3])),
                log["text"].append(row[5])
            elif row[1] == "whisper":
                log["agent"].append(int(row[4])),
                log["day"].append(int(row[0])),
                log["type"].append('whisper'),
                log["idx"].append(int(row[2])),
                log["turn"].append(int(row[3])),
                log["text"].append(row[5])
            elif row[1] == "vote":
                log["agent"].append(int(row[3])),
                log["day"].append(int(row[0])),
                log["type"].append('vote'),
                log["idx"].append(int(row[2])),
                log["turn"].append(0),
                log["text"].append('VOTE Agent[' + "{0:02d}".format(int(row[3])) + ']')
            elif row[1] == "attackVote":
                log["agent"].append(int(row[3])),
                log["day"].append(int(row[0])),
                log["type"].append('attack_vote'),
                log["idx"].append(int(row[2])),
                log["turn"].append(0),
                log["text"].append('ATTACK Agent[' + "{0:02d}".format(int(row[3])) + ']')
            elif row[1] == "divine":
                log["agent"].append(int(row[3])),
                log["day"].append(int(row[0])),
                log["type"].append('divine'),
                log["idx"].append(int(row[2])),
                log["turn"].append(0),
                log["text"].append('DIVINED Agent[' + "{0:02d}".format(int(row[3])) + '] ' + row[4])
            elif row[1] == "execute":
                # for all
                log["agent"].append(int(row[2])),
                log["day"].append(int(row[0])),
                log["type"].append('execute'),
                log["idx"].append(0),
                log["turn"].append(0),
                log["text"].append('Over')
                # for medium
                res = 'HUMAN'
                if row[3] == 'WEREWOLF':
                    res = 'WEREWOLF'
                log["agent"].append(int(row[2])),
                log["day"].append(int(row[0])),
                log["type"].append('identify'),
                log["idx"].append(medium),
                log["turn"].append(0),
                log["text"].append('IDENTIFIED Agent[' + "{0:02d}".format(int(row[2])) + '] ' + res)
            elif row[1] == "guard":
                log["agent"].append(int(row[3])),
                log["day"].append(int(row[0])),
                log["type"].append('guard'),
                log["idx"].append(int(row[2])),
                log["turn"].append(0),
                log["text"].append('GUARDED Agent[' + "{0:02d}".format(int(row[3])) + ']')
            elif row[1] == "attack":
                log["agent"].append(int(row[2])),
                log["day"].append(int(row[0])),
                log["type"].append('attack'),
                log["idx"].append(0),
                log["turn"].append(0),
                log["text"].append('ATTACK Agent[' + "{0:02d}".format(int(row[2])) + ']')
                if row[3] == 'true':
                    # dead
                    log["agent"].append(int(row[2])),
                    log["day"].append(int(row[0])),
                    log["type"].append('dead'),
                    log["idx"].append(0),
                    log["turn"].append(0),
                    log["text"].append('Over')
            elif row[1] == "result":
                pass
            else:
                pass
    return log
