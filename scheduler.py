from datetime import timedelta, datetime
import json

followups = {
    "still_there": timedelta(hours=4)
    , "last_warning": timedelta(hours=16)
    , "delete": timedelta(days=1)
}
schedule_file = "test_file.json"

def gen_reminders(channel_name):
    now = datetime.now()
    reminders = [(f[0], int((now+f[1]).timestamp()), channel_name) for f in followups.items()]
    return reminders

def add_reminders(reminders):
    try:
        with open(schedule_file, "r") as s:
            schedule = json.load(s)
    except FileNotFoundError:
        schedule = []
    with open(schedule_file, "w") as s:
        json.dump(schedule + [reminders], s)

def get_reminders():
    pass

if __name__ == "__main__":
    print(gen_reminders("test"))
    add_reminders(gen_reminders("test2"))