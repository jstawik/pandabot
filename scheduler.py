from datetime import timedelta, datetime
import json

# Expected structure of the json file: list[list3[str, int, str]]

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
        with open(schedule_file, "r") as r:
            schedule = json.load(r)
    except FileNotFoundError:
        schedule = []
    with open(schedule_file, "w") as w:
        json.dump(schedule + reminders, w)

def get_reminders():
    try:
        with open(schedule_file, "r") as r:
            schedule = json.load(r)
            past, now, future = [], int(datetime.now().timestamp()), []
            [past.append(reminder) if reminder[1] < now else future.append(reminder) for reminder in schedule ]
        with open(schedule_file, "w") as w:
            json.dump(future, w)
        return past
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    print(gen_reminders("test"))
    add_reminders(gen_reminders(f"test2_{datetime.now().timestamp()}"))
    print(get_reminders())