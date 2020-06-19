import json

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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
retries = Retry(total=10, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

# Désactivation des messages d'avertissement
urllib3.disable_warnings()


# Création des objets "Compte" et de la liste d'objet "compte_objet_list"
def creation_objet_compte():
    acces_fichier = open("Comptes.json", "r")
    compte_objet_list = []
    for compte_attributes in json.load(acces_fichier):
        compte_objet = Compte(**compte_attributes)
        compte_objet_list.append(compte_objet)
    acces_fichier.close()
    return compte_objet_list


def checkout():
    with requests.Session() as session:
        # Réglage des paramètres de la session
        session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
            }
        )

        # Connexion à la page d'accueil de Zalando
        url_home = "https://www.zalando.fr"
        home = session.get(url_home, verify=False)

        # Récupération des cookies de la session
        cookies = session.cookies.get_dict()

        # Connexion à la page de connexion
        url_get = "https://www.zalando.fr/login/?view=login"
        session.get(url_get, verify=False)

        # Récupérations des paramètres requis par le serveur de Zalando
        session.headers["x-xsrf-token"] = cookies["frsx"]
        session.headers["x-zalando-client-id"] = cookies["Zalando-Client-Id"]
        session.headers["x-zalando-render-page-uri"] = "/"
        session.headers["x-zalando-request-uri"] = "/"
        session.headers["x-flow-id"] = home.headers["X-Flow-Id"]
        session.headers["Accept"] = "application/json"

        # Connexion à la page du produit
        url_produit = "https://www.zalando.fr/levisr-t-shirt-imprime-white-le226g005-a11.html"
        session.get(url_produit, verify=False)

        # Mise dans le panier
        url_panier = 'https://www.zalando.fr/api/pdp/cart'
        article = 'LE226G005-A11004A000'
        panier = {
            'simpleSku': article,
            'anonymous': False
        }
        session.post(url_panier, json=panier, verify=False)

        # Requetes anti-bot
        url_1 = 'https://www.zalando.fr/api/navigation/cart-count'
        url_2 = 'https://www.zalando.fr/api/cart/details'
        url_3 = 'https://www.zalando.fr/cart'
        url_4 = 'https://www.zalando.fr/checkout/confirm'
        url_5 = 'https://www.zalando.fr/welcomenoaccount/true'
        session.get(url_1, verify=False)
        session.get(url_2, verify=False)
        session.get(url_3, verify=False)
        session.get(url_4, verify=False)
        session.get(url_5, verify=False)

        # Connexion au compte Zalando
        url_connexion_get = "https://www.zalando.fr/api/reef/login/schema"
        url_connextion_post1 = 'https://www.zalando.fr/api/rr/e'
        url_connexion_post2 = "https://www.zalando.fr/api/reef/login"
        login = {
            'username': 'tom.challete@gmail.com',
            'password': 'w?CnM9Ww',
            'wnaMode': 'checkout'
        }
        data = {
            'event': 'event_tracking',
            'eventCategory': 'checkout',
            'eventAction': 'click',
            'eventLabel': 'log in',
            'flowId': home.headers["X-Flow-Id"],
            'host': 'www.zalando.fr',
            'pathname': '/welcomenoaccount/true',
            'referrer': 'https://www.zalando.fr/cart/',
            'accept_language': 'fr-FR'
        }
        a = session.get(url_connexion_get, verify=False)
        session.headers["Origin"] = "https://www.zalando.fr"
        b = session.post(url_connextion_post1, json=data, verify=False)
        c = session.post(url_connexion_post2, json=login, verify=False)
        print(a.status_code)
        print(b.status_code)
        print(c.status_code)


checkout()


