import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from user_agent import generate_user_agent
import random


# Réglage des "Timeouts"
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 8
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
retries = Retry(total=3, backoff_factor=0, status_forcelist=[429, 500, 502, 503, 504])
urllib3.disable_warnings()
headers = {
    "User-Agent": generate_user_agent()
}
with requests.Session() as session:
    # Réglage des paramètres de la session
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    diversion_1 = random.choice(['https://www.bing.com/',
                                 'https://www.google.com/',
                                 'https://duckduckgo.com',
                                 'https://fr.yahoo.com/'
                                 ])
    session.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'User-Agent': generate_user_agent(),
        "Accept-Language": "fr-fr",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": diversion_1
    }
    session.get('https://www.zalando.fr/', verify=False)
    session.auth = ('bopiy98340@icanav.net', 'Dubai007')
    session.get('https://www.zalando.fr/login?target=/myaccount/', verify=False)
    session.get('https://www.zalando.fr/myaccount/', verify=False)
    session.get('https://www.zalando.fr/myaccount/checkout/confirm', verify=False)
    session.get('https://www.zalando.fr/checkout/address', verify=False)
    session.close()
