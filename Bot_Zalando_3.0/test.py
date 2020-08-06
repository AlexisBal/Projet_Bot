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
            with requests.Session() as session:

                # Réglage des paramètres de la session
                retries_2 = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
                session.mount("https://", TimeoutHTTPAdapter(max_retries=retries_2))
                session.headers.update(
                    {"User-Agent": generate_user_agent()}
                )
                # Url Test IP
                url_test = 'https://httpbin.org/ip'
                # Récupération de l'ip de l'utilisateur
                temoin = session.get(url_test, verify=False)
                ip_user_prepa = temoin.json()
                ip_user = ip_user_prepa['origin']
                # Réglage du proxy
                if len(x) == 4:
                    proxi = {"https": "https://%s:%s@%s:%s/" % (x[2], x[3], x[0], x[1])}
                    # Test du proxy
                    test = session.get(url_test, proxies=proxi, verify=False)
                    ip_test_prepa = test.json()
                    ip_test = ip_test_prepa['origin']
                    # Affichage du résultat
                    if ip_test != ip_user:
                        print(Fore.GREEN + 'Proxy %s is OK !' % (x[0] + ":" + x[1] + ":" + x[2] + ":" + x[3]))
                    else:
                        print(Fore.RED + "Proxy %s doesn't work !" % (x[0] + ":" + x[1] + ":" + x[2] + ":" + x[3]),
                              Style.RESET_ALL)

                else:
                    proxie2 = {"https": "https://%s" % (x[0] + ":" + x[1])}
                    # Test du proxy
                    test = session.get(url_test, proxies=proxie2, verify=False)
                    ip_test_prepa = test.json()
                    ip_test = ip_test_prepa['origin']
                    # Affichage du résultat
                    if ip_test != ip_user:
                        print(Fore.GREEN + 'Proxy %s is OK !' % (x[0] + ":" + x[1]), Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Proxy %s doesn't work !" % (x[0] + ":" + x[1]), Style.RESET_ALL)
            session.close()

        # Gestion des exceptions
        except:
            if len(x) == 4:
                print(Fore.RED + "Proxy %s doesn't work !" % (x[0] + ":" + x[1] + ":" + x[2] + ":" + x[3]),
                      Style.RESET_ALL)
            else:
                print(Fore.RED + "Proxy %s doesn't work !" % (x[0] + ":" + x[1]), Style.RESET_ALL)


urllib3.disable_warnings()
VerificationProxys()

