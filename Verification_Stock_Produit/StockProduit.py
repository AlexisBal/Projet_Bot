import json
import time
import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.parse
from user_agent import generate_user_agent


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
retries = Retry(total=6, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

# Désactivation des messages d'avertissement
urllib3.disable_warnings()


def DisponibiliteProduit():
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

                # Réglage du Proxy
                liste_proxy = [
                    'pt32.nordvpn.com',
                    'ie69.nordvpn.com',
                    'hk139.nordvpn.com',
                    'jp491.nordvpn.com',
                    'au443.nordvpn.com'
                ]
                print(liste_proxy[x])
                session.proxies = {
                    'https': 'https://alexis.balayre@gmail.com:worwaj-8kemXi-gogqes@%s:80/' % liste_proxy[x]
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
                del session.cookies['mpulseinject']
                session.cookies['mpulseinject'] = 'false'

                # Connexion à la page du produit
                url_produit = 'https://www.zalando.fr/pier-one-baskets-basses-white-pi915o00k-a11.html'
                session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                produit_session = session.get(url_produit, verify=False)

                # Diversion anti-bot
                url_bot = 'https://www.zalando.fr/resources/35692132da201d42d0a3ba96882c7b'
                data_bot = {
                    'sensor_data': '7a74G7m23Vrp0o5c9178231.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392058,5583660,1440,816,1440,900,1440,457,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.310461937155,796712791830,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1136,-1,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1136,-1,0;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/reebok-classic-club-c-85-baskets-basses-whitedark-greenchalk-white-re015o075-a11.html-1,2,-94,-115,1,32,32,0,0,0,0,1,0,1593425583660,-999999,17046,0,0,2841,0,0,2,0,0,AD852DA9CB75216A40393C9EA4B27CA9~-1~YAAQLux7XEmFhfJyAQAA99qQ/wSQeuSr3yA2nUWFM355G9Au4k+JM7EsIxUEh2qBoJucheaV8nK4A7qzhqSTeRkqZmCARZtx49bK2n7Yp4WukXx0R69NrR+2q6VKAUVuGLvIi5xh3yU0oRYCSPryGSabiW3mhyrr8H+fPR8si9AU9vlhW00znwELGASR7UZzoJEB2kLR+0FBqQR2TxiK63dFJfppynpweN0GJHNXgAzWWEWBH5cAPljF1HUmYsum6zn2qMlPytR20miWUC7oUnvNMbOfYSN66+bePb5+PLjc2w/lma8ZW4PFT8UGkkZ77oa7HDRfAzPORuamSL1XvY2+QCE=~0~-1~-1,32125,-1,-1,26018161,NVFO,124,-1-1,2,-94,-106,0,0-1,2,-94,-119,-1-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,-1-1,2,-94,-80,94-1,2,-94,-116,150758334-1,2,-94,-118,88956-1,2,-94,-121,;1;-1;0'
                }
                session.headers["Accept"] = "*/*"
                session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                session.headers["Origin"] = "https://www.zalando.fr"
                session.headers["Content-Length"] = '1452'
                session.headers["Referer"] = url_produit
                session.post(url_bot, json=data_bot, verify=False)

                # Accès aux informations
                del session.headers["Content-Type"]
                del session.headers["Content-Length"]
                del session.headers["Origin"]
                session.headers["x-xsrf-token"] = cookies["frsx"]
                flowid_produit = urllib.parse.quote(produit_session.headers["X-Flow-Id"])
                url_get_2 = (
                        "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=1" % flowid_produit
                )
                a = session.get(url_get_2, verify=False)

                # Récupération de la liste du stock
                objet = json.loads(a.text)
                stock = objet['gtm']['productSizeAvailability']

            session.close()

            # Séparation des valeurs
            liste_stock = stock.split('|')
            liste_stock_bis = []

            # Séparation des pointures et du stock
            for valeur in liste_stock:
                y = valeur.split('_')
                liste_stock_bis.extend(y)

            # Détermination de la position de la pointure et du stock
            position_pointure = liste_stock_bis.index('38')
            position_stock = position_pointure + 1

            # Affichage du stock de la pointure concernée
            if liste_stock_bis[position_stock] == '1':
                return True
            else:
                time.sleep(1800)

        except:
            pass

        finally:
            x = x + 1
            if x == 5:
                x = 0


Dispo = DisponibiliteProduit()
print(Dispo)
