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


def Paiement_Zalando(liste_proxys, compte_objet_list):
    # Comptage du nombre de comptes présents dans la base de données
    nombrecompte = len(compte_objet_list)

    # Achat du produit pour chaque objet "Compte" présent dans la base de données
    for compte in range(0, nombrecompte):
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
                    home = session.get(url_home, verify=False)

                    # Récupération et modification des cookies de la session
                    cookies = session.cookies.get_dict()

                    # Connexion à la page de connexion
                    url_connexion_1 = "https://www.zalando.fr/login/?view=login"
                    session.get(url_connexion_1, verify=False)

                    # Connexion au compte
                    url_connexion_2 = 'https://www.zalando.fr/api/reef/login/schema'
                    url_connexion_3 = 'https://www.zalando.fr/api/reef/login'
                    identifiants = {
                        "username": compte_objet_list[compte].email,
                        "password": compte_objet_list[compte].motdepasse,
                        "wnaMode": "shop"
                    }
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.headers["x-zalando-client-id"] = cookies["Zalando-Client-Id"]
                    session.headers["x-zalando-render-page-uri"] = "/login/?view=login"
                    session.headers["x-zalando-request-uri"] = "/login/?view=login"
                    session.headers["x-flow-id"] = home.headers["X-Flow-Id"]
                    session.headers["Accept"] = "application/json"
                    session.get(url_connexion_2, verify=False)
                    session.headers["Origin"] = "https://www.zalando.fr"
                    session.post(url_connexion_3, json=identifiants, verify=False)

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


comptes = creation_objet_compte()
Paiement_Zalando(comptes)