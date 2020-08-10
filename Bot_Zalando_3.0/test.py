import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from user_agent import generate_user_agent
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import urllib3
import json


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


# Récupérations des proxies
def proxy():
    with open('Zalando/Tasks/Proxy.txt', 'r') as f:
        liste_proxys = []
        for ligne in f:
            if ligne.strip('\n') != '':
                liste_proxys.append(ligne.strip('\n').split(":"))

        if not liste_proxys:
            print(Fore.RED + "You have not specified any proxies !")
            print(Fore.RED + "Enter the address of the proxy servers in the Proxy.txt file.")

        return liste_proxys


def VerificationProxys():
    list_proxy = proxy()
    for x in list_proxy:
        try:
            # Ouverture de la session
            s = requests.Session()
            s.proxies = {}
            # Réglage des paramètres de la session
            retries_2 = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
            s.mount("https://", TimeoutHTTPAdapter(max_retries=retries_2))
            # Url Test IP
            url_test = 'https://www.zalando.fr'
            url_test2 = 'https://www.zalando.fr/login/?view=login'
            url3 = 'https://httpbin.org/ip'
            # Réglage du proxy
            if len(x) == 4:
                s.proxies['http'] = 'http://%s:%s@%s:%s/' % (x[2], x[3], x[0], x[1])
                s.proxies['https'] = 'http://%s:%s@%s:%s/' % (x[2], x[3], x[0], x[1])
                # Test du proxy
                s.headers = {"User-Agent": generate_user_agent(),
                             'Connection': 'keep-alive',
                             'Access-Control-Allow-Credentials:': 'true',
                             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                             'Accept-Language': 'fr-fr',
                             'Accept-Encoding': 'gzip, deflate, br'
                             }
                s.get(url_test, verify=False, proxies=s.proxies)
                test = s.get(url_test2, verify=False, proxies=s.proxies)
                iptest = s.get(url3, verify=False, proxies=s.proxies)
                # Affichage du résultat
                print(s.headers)
                print(s.cookies)
                print(iptest.json())
                s.close()

        # Gestion des exceptions
        except:
            raise


urllib3.disable_warnings()
VerificationProxys()
