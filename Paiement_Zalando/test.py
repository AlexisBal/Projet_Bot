import json
import re

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from user_agent import generate_user_agent
from bs4 import BeautifulSoup


# Réglage des "Timeouts"
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 5
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


# Réglage des "Retries"
retries = Retry(total=8, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

# Désactivation des messages d'avertissement
urllib3.disable_warnings()

with requests.Session() as session:
    # Réglage des paramètres de la session
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    url = 'https://bizz4.com'
    a = requests.get(url, verify=False)
    soup = BeautifulSoup(a.content, 'html.parser')
    test = soup.find(string=re.compile("var et_pb_custom"))
    print(test.find({'name': 'config.accessToken'})['value'])
    session.close()