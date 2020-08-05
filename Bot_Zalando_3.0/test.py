import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from user_agent import generate_user_agent
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import urllib3


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
        # Ouverture de la session
        with requests.Session() as session:
            # Réglage des paramètres de la session
            retries_2 = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
            session.mount("https://", TimeoutHTTPAdapter(max_retries=retries_2))
            session.headers.update(
                {"User-Agent": generate_user_agent(),
                 "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            )
            # Réglage du proxy
            if len(x) == 4:
                session.proxies = {"https": "https://%s:%s@%s:%s/" % (x[2], x[3], x[0], x[1])}
                # Connexion à la page d'accueil de Zalando
                url_home = 'https://whatismyipaddress.com/fr/mon-ip'
                test = session.get(url_home, verify=False)
                # Test du proxy
                soupbis_3 = BeautifulSoup(test.content, "html.parser")
                print(soupbis_3)

            else:
                session.proxies = {"https": "https://%s" % (x[0] + ":" + x[1])}
                # Connexion à la page d'accueil de Zalando
                url_home = 'https://whatismyipaddress.com/fr/mon-ip'
                test = session.get(url_home, verify=False)
                # Test du proxy
                soupbis_3 = BeautifulSoup(test.content, "html.parser")
                print(soupbis_3)
            print(session.proxies)
        session.close()


urllib3.disable_warnings()
VerificationProxys()

