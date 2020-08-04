import requests
import urllib3
from datetime import datetime
from datetime import date

urllib3.disable_warnings()

# Réglages Discord Webhook Paypal
now = datetime.utcnow()
print(now)