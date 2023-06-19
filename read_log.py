import csv


def read_log(game_file_path):

    with open(game_file_path, newline='') as csvfile:
        log_reader = csv.reader(csvfile, delimiter=',')
        log = []
        for row in log_reader:
            if row[1] == "status":
                log.append({
                    "type": "status", "contents": {
                        "agent": int(row[2]), "day": int(row[0]), "name": row[5], "role": row[3], "status": row[4]
                    }
                })
            elif row[1] == "talk":
                log.append({
                    "type": "talk", "contents": {
                        "agent": int(row[4]), "day": int(row[0]), "idx": int(row[2]),
                        "text": row[5], "turn": int(row[3])
                    }
                })
            elif row[1] == "whisper":
                log.append({
                    "type": "whisper", "contents": {
                        "agent": int(row[4]), "day": int(row[0]), "idx": int(row[2]),
                        "text": row[5], "turn": int(row[3])
                    }
                })
            elif row[1] == "vote":
                log.append({
                    "type": "vote", "contents": {
                        "agent": int(row[2]), "day": int(row[0]), "target": int(row[3])
                    }
                })
            elif row[1] == "attackVote":
                log.append({
                    "type": "attack_vote", "contents": {
                        "agent": int(row[2]), "day": int(row[0]), "target": int(row[3])
                    }
                })
            elif row[1] == "divine":
                log.append({
                    "type": "divine", "contents": {
                        "agent": int(row[2]), "day": int(row[0]), "target": int(row[3]), "result": row[4]
                    }
                })
            elif row[1] == "execute":
                log.append({
                    "type": "execute", "contents": {
                        "day": int(row[0]), "target": int(row[2]), "result": row[3]
                    }
                })
            elif row[1] == "guard":
                log.append({
                    "type": "guard", "contents": {
                        "agent": int(row[2]), "day": int(row[0]), "target": int(row[3]), "result": row[4]
                    }
                })
            elif row[1] == "attack":
                log.append({
                    "type": "attack", "contents": {
                        "day": int(row[0]), "target": int(row[2]), "result": row[3]
                    }
                })
            elif row[1] == "result":
                log.append({
                    "type": "result", "contents": {
                        "day": int(row[0]), "n_human": int(row[2]), "n_werewolves": int(row[3]), "winner": row[4]
                    }
                })
            else:
                raise ValueError(f"Unknown Log format: {row}")
    return log
