from datetime import date
from datetime import datetime


today = date.today()
now = datetime.now()
date = today.strftime("%b-%d-%Y")
heure = now.strftime("%H:%M:%S")
tasklist = [date, heure]
print(tasklist)