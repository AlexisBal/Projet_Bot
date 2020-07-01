import json

import requests
import urllib3
from password_generator import PasswordGenerator
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from user_agent import generate_user_agent


# Définition de la classe "Compte"
class Compte:
    def __init__(self, **compte_attributes):
        for attr_name, attr_value in compte_attributes.items():
            setattr(self, attr_name, attr_value)


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


# Création des objets "Compte" et de la liste d'objet "compte_objet_list"
def creation_objet_compte():
    acces_fichier = open("../Data/Comptes.json", "r")
    compte_objet_list = []
    for compte_attributes in json.load(acces_fichier):
        compte_objet = Compte(**compte_attributes)
        compte_objet_list.append(compte_objet)
    acces_fichier.close()
    return compte_objet_list


def Paiement_Zalando(liste_proxys):
    x = 0
    while True:
        try:
            # Ouverture de la Session
            with requests.Session() as session:
                # Réglage des paramètres de la session
                session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))

                session.headers.update(
                    {
                        'User-Agent': generate_user_agent(os=('mac', 'linux'))
                    }
                )

                # Réglage du proxy
                session.proxies = {
                    'https': 'https://%s' % liste_proxys[x]
                }

                # Connexion à la page d'accueil de Zalando
                url_google = 'https://www.google.com/?client=safari'
                url_home = 'https://www.zalando.fr'
                session.get(url_google, verify=False)
                session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                session.headers["Accept-Language"] = "fr-fr"
                session.headers["Accept-Encoding"] = "gzip, deflate, br"
                session.get(url_home, verify=False)

                # Récupération et modification des cookies de la session
                cookies = session.cookies.get_dict()

            # Fermeture de la Session
            session.close()

        # Gestion des exceptions
        except:
            pass

        finally:
            x = x + 1
            if x == (len(liste_proxys) + 1):
                x = 0


url_1 = 'https://www.zalando.fr/cart'
url_2 = 'https://www.zalando.fr/checkout/address'
url_2_bis = 'https://www.zalando.fr/api/checkout/search-pickup-points-by-address'
url_3 = 'https://www.zalando.fr/checkout/confirm'

