import _datetime

date = datetime.datetime.now().strftime("%x")
heure = datetime.datetime.now().strftime("%X")
tasklist = [date, heure]
print(tasklist)