import datetime
import csv

def process_csv_row(row: list):

    date_string = row[0]
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    
    return {
        "action": row[2],
        "date": date,
        "user": row[1],
        "before": {
            "channel": row[4],
            "server": row[3]
        },
        "after": {
            "channel": row[6],
            "server": row[5]
        }
    }


def process_log():

    active_sessions = {}
    total_time = {}

    with open("db/vc_activity.csv", mode="r", encoding="UTF-8") as f:
        reader = csv.reader(f)
        next(reader) # skip header

        for row in reader:

            entry = process_csv_row(row)

            user = entry["user"]

            if user not in active_sessions:
                active_sessions[user] = {}
            if user not in total_time:
                total_time[user] = 0
            
            if entry["action"] == "join":
                active_sessions[user]["channel"] = entry["after"]
                active_sessions[user]["status"] = "unmuted"
                active_sessions[user]["date"] = entry["date"]
            
            elif entry["action"] == "leave":
                if entry["before"] == active_sessions[user]["channel"]:
                    time_spent = (entry["date"] - active_sessions[user]["date"]).total_seconds()
                    total_time[user] += time_spent
                    del active_sessions[user]
            
            elif entry["action"] == "switch":
                time_spent = (entry["date"] - active_sessions[user]["date"]).total_seconds()
                total_time[user] += time_spent
                active_sessions[user]["date"] = entry["date"]

                if entry["before"] == entry["after"]:
                    if entry["after"] == active_sessions[user]["channel"]:
                        if active_sessions[user]["status"] == "unmuted":
                            active_sessions[user]["status"] = "muted"
                        else:
                            active_sessions[user]["status"] = "unmuted"
                else:
                    active_sessions[user]["channel"] = entry["after"]

        
        for user, data in active_sessions.items():
            timestamp = datetime.datetime.now()
            time_spent = (timestamp - data["date"]).total_seconds()
            total_time[user] += time_spent

        total_minutes = {}
        for user, seconds in total_time.items():
            total_minutes[user] = round(seconds / 60)

        return total_minutes

        # sorted_hours = dict(sorted(total_minutes.items(), key=lambda item: item[1], reverse=True))
        # print(json.dumps(sorted_hours, indent=4))


if __name__ == "__main__":
    process_log()