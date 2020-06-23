import json
import time

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Compte:
    def __init__(self, **compte_attributes):
        for attr_name, attr_value in compte_attributes.items():
            setattr(self, attr_name, attr_value)


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
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    headers = {
        "Host": "www.zalando.fr",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "fr-fr",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    session.headers.update(headers)

    url_home = "https://www.zalando.fr"
    home = session.get(url_home, verify=False)

    cookies = session.cookies.get_dict()

    del session.headers["Upgrade-Insecure-Requests"]
    session.get('https://www.zalando.fr/sebago-docksides-portland-crazy-horse-chaussures-bateau-se212m00m-k11.html',
                verify=False)

    url_get_1 = (
            "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=1"
            % home.headers["X-Flow-Id"]
    )
    session.headers["Accept"] = "*/*"
    session.headers["x-xsrf-token"] = cookies["frsx"]
    a = session.get(url_get_1, verify=False)
    print(a.__getattribute__('gtm'))
