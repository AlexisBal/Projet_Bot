import json
import time
import re
import random
from threading import Thread
from colorama import Back, Fore, Style, deinit, init

import requests
import urllib3
import urllib
from urllib.parse import quote
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from user_agent import generate_user_agent
from password_generator import PasswordGenerator
from bs4 import BeautifulSoup
from licensing.models import *
from licensing.methods import Key, Helpers
from datetime import datetime


# Définition de la classe "Compte"
class Compte:
    def __init__(self, **compte_attributes):
        for attr_name, attr_value in compte_attributes.items():
            setattr(self, attr_name, attr_value)


# Définition de la classe "Carte"
class Carte:
    def __init__(self, **carte_attributes):
        for attr_name, attr_value in carte_attributes.items():
            setattr(self, attr_name, attr_value)


# Réglage des "Timeouts"
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 4
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
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

# Désactivation des messages d'avertissement
urllib3.disable_warnings()


# -----------------------------------------------------------Affichage horloge-------------------------------------------------------------------------#

def horloge():
    now = datetime.now()
    heures = now.hour
    heures = str(heures)
    minutes = now.minute
    minutes = str(minutes)
    secondes = now.second
    secondes = str(secondes)
    milisecondes = now.microsecond
    milisecondes = str(milisecondes)
    milisecondes = milisecondes[0] + milisecondes[1] + milisecondes[2]
    horloge = "[" + heures + ":" + minutes + ":" + secondes + "." + milisecondes + "]"
    print(Fore.RED + Style.BRIGHT + horloge, end="")


# ------------------------------------------------------------------------------------------------------------------------------------------------#

class RechercheCommande(Thread):
    def __init__(self, compte_objet_list, carte_objet_list, liste_proxys, taille_produit, url_produit):
        Thread.__init__(self)
        self.carte_objet_list = carte_objet_list
        self.compte_objet_list = compte_objet_list
        self.taille_produit = taille_produit
        self.url_produit = url_produit
        self.liste_proxys = liste_proxys

    def run(self):
        # Récupération du Sku
        while True:
            headers = {
                "User-Agent": generate_user_agent(os=("mac", "linux"))
            }
            url = self.url_produit
            requete_1 = requests.get(url, headers=headers, verify=False, allow_redirects=False)
            soup_1 = BeautifulSoup(requete_1.content, "html.parser")
            reponse_1 = soup_1.find(type="application/json", class_="re-1-1")
            if reponse_1 is not None:
                reponsebis_1 = reponse_1.contents
                reponsebis2_1 = json.loads(reponsebis_1[0])
                id_produit = reponsebis2_1['enrichedEntity']['id']
                sku_list = reponsebis2_1['graphqlCache'][
                    '{"id":"79b404b0f26a318349c1b29b57e789da91cb39a541a668c96c2f4945bc7df528","variables":{"id":"%s"}}' % id_produit][
                    'data']['product']['simples']
                liste_sku = []
                for n in range(0, len(sku_list)):
                    liste_sku.append(sku_list[n]['sku'])
                    liste_sku.append(sku_list[n]['size'])
                position_taille = liste_sku.index(self.taille_produit)
                sku = liste_sku[position_taille - 1]
                break

        # Verification du stock
        while True:
            requete_2 = requests.get(self.url_produit, headers=headers, verify=False, allow_redirects=False)
            soup_2 = BeautifulSoup(requete_2.content, "html.parser")
            reponse_2 = soup_2.find(type="application/ld+json")
            if reponse_2 is not None:
                reponsebis_2 = reponse_2.contents
                reponsebis2_2 = json.loads(reponsebis_2[0])
                stock_list = reponsebis2_2['offers']
                liste_stock = []
                for n in range(0, len(stock_list)):
                    liste_stock.append(stock_list[n]['sku'])
                    liste_stock.append(stock_list[n]['availability'])
                position_sku = liste_stock.index(self.url_produit)
                stock_schema = liste_stock[position_sku + 1]
                if stock_schema == 'http://schema.org/InStock':
                    print('Le produit est disponible !')
                    break
                else:
                    time.sleep(0.2)

        # Mise dans le panier du produit
        nombrecompte = len(self.compte_objet_list)
        for compte in range(0, nombrecompte):
            while True:
                try:
                    # Ouverture de la Session
                    with requests.Session() as session:
                        # Réglage des paramètres de la session
                        session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))

                        # Réglage du proxy
                        session.proxies = {
                            'https': 'https://%s' % random.choice(self.liste_proxys)
                        }

                        # Connexion à la page d'accueil de Zalando
                        url_home = "https://www.zalando.fr"
                        headers_2 = {
                            "Host": "www.zalando.fr",
                            "User-Agent": generate_user_agent(os=('mac', 'linux')),
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                            "Accept-Language": "fr-fr",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Connection": "keep-alive",
                            "Upgrade-Insecure-Requests": "1",
                        }
                        session.headers.update(headers_2)
                        home_1 = session.get(url_home, verify=False)

                        # Récupération des cookies de la session
                        cookies_1 = session.cookies.get_dict()

                        # Connexion à la page du produit
                        del session.headers["Upgrade-Insecure-Requests"]
                        session.get(self.url_produit, verify=False)

                        # Envoie de requetes pour éviter les sécurités anti-bot
                        url_get_1 = (
                                "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=1"
                                % home_1.headers["X-Flow-Id"]
                        )
                        session.headers["Accept"] = "*/*"
                        session.headers["x-xsrf-token"] = cookies_1["frsx"]
                        session.get(url_get_1, verify=False)

                        # Mise dans le panier
                        url_panier = "https://www.zalando.fr/api/pdp/cart"
                        panier = {"simpleSku": sku, "anonymous": False}
                        session.headers["Accept"] = "application/json"
                        session.headers["Content-Type"] = "application/json"
                        session.post(url_panier, json=panier, verify=False)

                        # Requetes anti-bot
                        url_1 = "https://www.zalando.fr/api/navigation/cart-count"
                        url_2 = "https://www.zalando.fr/api/cart/details"
                        url_3 = "https://www.zalando.fr/cart"
                        url_post_data1 = (
                            "https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b"
                        )
                        url_4 = "https://www.zalando.fr/checkout/confirm"
                        data1 = {
                            "sensor_data": "7a74G7m23Vrp0o5c9175921.59-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391853,4809209,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.970703120485,796297404604,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,-1,2407,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,-1,2407,0;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/cart-1,2,-94,-115,1,32,32,0,0,0,0,1,0,1592594809208,-999999,17037,0,0,2839,0,0,2,0,0,532BDDF92D2792A84D6D104030676E0D~-1~YAAQL+x7XB4Cl4RyAQAAuD4MzgSx3Lv1ABbT/zOiBCoPbgw/BaVzFR5eZ51uxxL4OXmQwVusXrmmp0UQoY91EL8XZjGXZrMEVcbc6xs9RqNoPQT9cmEBDv6P7YDcyruKTOSfhsAg/woWK0b0ajzRcS3F1Dg2bZPIIsoK7d19YVZavIIDPCXt1sCGFl530XhBLlaCEKwtzHQfUSlhF3NQVd9SWOJ6WAvgyXp7mUGeObHiBoSF9sPgFIepOlHRzq0UZmssedn+bhEtz/0FJ/TRMiWS1AM6/gAtbIJwvCzTjnba/L6/uJgtimiQUyrkIuBGq4gAvPc8f9hJW6SIlR4mU+2fpt4=~-1~-1~-1,32514,-1,-1,26018161,NVVO,124,-1-1,2,-94,-106,0,0-1,2,-94,-119,-1-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,-1-1,2,-94,-80,94-1,2,-94,-116,14427678-1,2,-94,-118,82036-1,2,-94,-121,;1;-1;0" %
                                           session.headers["User-Agent"]
                        }
                        session.headers["Accept"] = "*/*"
                        del session.headers["Content-Type"]
                        session.get(url_1, verify=False)
                        session.get(url_2, verify=False)
                        del session.headers["x-xsrf-token"]
                        session.headers[
                            "Accept"
                        ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                        session.get(url_3, verify=False)
                        session.headers["Accept"] = "*/*"
                        session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                        session.post(url_post_data1, json=data1, verify=False)
                        session.headers[
                            "Accept"
                        ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                        del session.headers["Content-Type"]
                        session.get(url_4, verify=False)

                        # Ouverture de la page de connexion
                        url_connexion_1 = "https://www.zalando.fr/welcomenoaccount/true"
                        session.get(url_connexion_1, verify=False)

                        # Sécurité anti-bot
                        url_get_2 = (
                                "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=2"
                                % home_1.headers["X-Flow-Id"]
                        )
                        url_post1 = (
                            "https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b"
                        )
                        sensor_data = {
                            "sensor_data": "7a74G7m23Vrp0o5c9175921.59-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391853,4814181,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.650518738325,796297407090.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,466,1098,525;1,1,510,1094,525;2,1,621,455,214;3,1,691,323,150;4,1,870,323,152;5,1,915,323,152;6,1,927,354,198;7,1,937,383,245;8,1,971,390,256;9,1,1011,431,333;10,1,1041,440,352;11,1,1066,441,353;12,1,1122,440,352;13,1,1133,439,350;14,1,1142,437,347;15,1,1150,435,345;16,1,1151,434,343;17,1,1165,432,341;18,1,1168,430,339;19,1,1183,427,334;20,1,1184,425,331;21,1,1190,421,327;22,1,1191,421,327;23,1,1199,418,323;24,1,1200,418,323;25,1,1207,414,318;26,1,1207,414,318;27,1,1215,412,316;28,1,1216,412,316;29,1,1222,410,313;30,1,1222,410,313;31,1,1233,407,309;32,1,1236,407,309;33,1,1239,404,305;34,1,1240,404,305;35,1,1249,402,303;36,1,1249,402,303;37,1,1255,400,301;38,1,1255,400,301;39,1,1265,399,300;40,1,1266,399,300;41,1,1271,398,299;42,1,1272,398,299;43,1,1283,397,298;44,1,1286,397,298;45,1,1287,397,298;46,1,1301,397,297;47,1,1303,397,297;48,1,1318,397,297;49,1,1319,397,297;50,1,1332,397,297;51,1,1332,397,297;52,1,1336,397,297;53,1,1337,397,297;54,1,1349,396,296;55,1,1352,396,296;56,1,1367,396,295;57,1,1371,395,293;58,1,1381,395,292;59,1,1384,394,290;60,1,1399,394,287;61,1,1403,392,285;62,1,1414,392,282;63,1,1416,391,280;64,1,1424,391,279;65,1,1425,391,279;66,1,1434,390,278;67,1,1434,390,278;68,1,1441,390,277;69,1,1442,390,277;70,1,1450,390,277;71,1,1451,390,277;72,1,1458,390,277;73,1,1459,390,277;74,1,1474,390,276;75,1,1475,390,276;76,1,1499,390,276;77,1,1499,390,276;78,3,1570,390,276,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/welcomenoaccount/true-1,2,-94,-115,1,157693,32,0,0,0,157661,1570,0,1592594814181,30,17037,0,79,2839,1,0,1572,97728,0,532BDDF92D2792A84D6D104030676E0D~-1~YAAQL+x7XGsCl4RyAQAAVVcMzgT8JqlM2ih46/XQ2qYQMxHvaSPQRX2kpvPCVKqrQtQU9V/vFR1MmPEXJf9SmdvOwAkfJImjhgWtg5Qe8TGeuBXznDTznEbLt4H84jeMFHF7HqEOhDVMpIx3WMrRGjPSkRBFYse5UyFG3sp6mv+YX1eTFNnYyFIhKvbMRUFQ2DtEC86yfleq6nBgQuuANy97ge5fStvq8KY1Py33TUYcLQRXFYNwnGjRi4PKcf/NkFtEHlsJukzXJxDUpiE/qsNo6E8KEceJBBEJVmr/MaxcTIcQXweubzRoH+kFchl/1stvlH0jJK9wMuo++pfPPifylAk=~-1~-1~-1,32904,607,-1122583492,26018161,NVVO,124,-1-1,2,-94,-106,1,2-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,200,800,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,649914741-1,2,-94,-118,158953-1,2,-94,-121,;2;5;0" %
                                           session.headers["User-Agent"]
                        }
                        sensor_data_bis = {
                            "sensor_data": "7a74G7m23Vrp0o5c9175921.59-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391853,4814181,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.668405617334,796297407090.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,4184,undefined,0,0,1103,0;1,2,4195,undefined,0,0,1103,0;2,1,4231,undefined,0,0,1103,0;3,2,4238,undefined,0,0,1103,0;4,1,4825,13,0,0,1466;-1,2,-94,-110,0,1,466,1098,525;1,1,510,1094,525;2,1,621,455,214;3,1,691,323,150;4,1,870,323,152;5,1,915,323,152;6,1,927,354,198;7,1,937,383,245;8,1,971,390,256;9,1,1011,431,333;10,1,1041,440,352;11,1,1066,441,353;12,1,1122,440,352;13,1,1133,439,350;14,1,1142,437,347;15,1,1150,435,345;16,1,1151,434,343;17,1,1165,432,341;18,1,1168,430,339;19,1,1183,427,334;20,1,1184,425,331;21,1,1190,421,327;22,1,1191,421,327;23,1,1199,418,323;24,1,1200,418,323;25,1,1207,414,318;26,1,1207,414,318;27,1,1215,412,316;28,1,1216,412,316;29,1,1222,410,313;30,1,1222,410,313;31,1,1233,407,309;32,1,1236,407,309;33,1,1239,404,305;34,1,1240,404,305;35,1,1249,402,303;36,1,1249,402,303;37,1,1255,400,301;38,1,1255,400,301;39,1,1265,399,300;40,1,1266,399,300;41,1,1271,398,299;42,1,1272,398,299;43,1,1283,397,298;44,1,1286,397,298;45,1,1287,397,298;46,1,1301,397,297;47,1,1303,397,297;48,1,1318,397,297;49,1,1319,397,297;50,1,1332,397,297;51,1,1332,397,297;52,1,1336,397,297;53,1,1337,397,297;54,1,1349,396,296;55,1,1352,396,296;56,1,1367,396,295;57,1,1371,395,293;58,1,1381,395,292;59,1,1384,394,290;60,1,1399,394,287;61,1,1403,392,285;62,1,1414,392,282;63,1,1416,391,280;64,1,1424,391,279;65,1,1425,391,279;66,1,1434,390,278;67,1,1434,390,278;68,1,1441,390,277;69,1,1442,390,277;70,1,1450,390,277;71,1,1451,390,277;72,1,1458,390,277;73,1,1459,390,277;74,1,1474,390,276;75,1,1475,390,276;76,1,1499,390,276;77,1,1499,390,276;78,3,1570,390,276,1103;79,4,1676,390,276,1103;80,2,1676,390,276,1103;81,1,1846,390,277;82,1,1847,390,277;83,1,1852,390,278;84,1,1853,390,278;85,1,1860,390,281;86,1,1861,390,281;87,1,1869,390,284;88,1,1870,390,284;89,1,1877,390,287;90,1,1878,390,287;91,1,1886,390,290;92,1,1887,390,290;93,1,1894,390,293;94,1,1894,390,293;95,1,1902,390,295;96,1,1903,390,295;97,1,1910,390,298;98,1,1912,390,298;99,1,1920,390,300;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,2,2624;3,4215;-1,2,-94,-112,https://www.zalando.fr/welcomenoaccount/true-1,2,-94,-115,NaN,212868,32,0,0,0,NaN,4825,0,1592594814181,30,17037,5,100,2839,2,0,4826,158474,0,532BDDF92D2792A84D6D104030676E0D~-1~YAAQL+x7XHoCl4RyAQAAJFsMzgQxUa6eRJ/ks9509lAH146yDbJhRzidCLZOUD8YcIwt5VMlKH9E5gL5nVGGA2kZDBn/WP7q3ijhG6TIEjzeR73Q5f6JxSgvZMCiRSy80sLppaVpERI1blHB1CwKtu+osvqd1Fvpo/0aMndGdm2FWAjEPxFM7G4KHVSvh0H7hWTeLzA8Jhm7Vplau+PfW8mPSXHP8TAOQkmj/CQottmRpsMZRq7JHYedpFnHgARYANo4maBb9V3+Z3/dZ9vRQ/W8gXjnJ6dZLN8g5JFJQvRxVLvpIlaQ949VUAHTckFxiyjfCD3+JZXygTJ3rkX+4yKofU0=~-1~-1~-1,31935,607,-1122583492,26018161,NVVO,124,-1-1,2,-94,-106,3,3-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,200,800,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,649914741-1,2,-94,-118,187600-1,2,-94,-121,;1;5;0" %
                                           session.headers["User-Agent"]
                        }
                        session.headers["Accept"] = "*/*"
                        session.headers["x-xsrf-token"] = cookies_1["frsx"]
                        session.get(url_get_2, verify=False)
                        del session.headers["x-xsrf-token"]
                        session.post(url_post1, json=sensor_data, verify=False)
                        session.post(url_post1, json=sensor_data_bis, verify=False)

                        # Connexion au compte Zalando
                        url_connexion_get = "https://www.zalando.fr/api/reef/login/schema"
                        url_connexion_post2 = "https://www.zalando.fr/api/reef/login"
                        url_checkout_1 = "https://www.zalando.fr/checkout/confirm"
                        headers_2 = {
                            "Host": "www.zalando.fr",
                            "Accept": "application/json",
                            "Accept-Encoding": "gzip, deflate, br",
                            "x-zalando-request-uri": "/welcomenoaccount/true",
                            "x-zalando-render-page-uri": "/welcomenoaccount/true",
                            "x-xsrf-token": cookies_1["frsx"],
                            "Accept-Language": "fr-fr",
                            "User-Agent": generate_user_agent(os=('mac', 'linux')),
                            "Referer": "https://www.zalando.fr/welcomenoaccount/true",
                            "x-flow-id": home_1.headers["X-Flow-Id"],
                            "x-zalando-client-id": cookies_1["Zalando-Client-Id"],
                            "Connection": "keep-alive",
                            "Content-Type": "application/json"
                        }
                        identifiants_1 = {
                            "username": self.compte_objet_list[compte].email,
                            "password": self.compte_objet_list[compte].motdepasse,
                            "wnaMode": "checkout"
                        }
                        session.headers.update(headers_2)
                        session.get(url_connexion_get, verify=False)
                        session.headers["Origin"] = "https://www.zalando.fr"
                        session.post(url_connexion_post2, json=identifiants_1, verify=False)
                        session.get(url_checkout_1, verify=False)

                    # Fermeture de la session
                    session.close()

                    # Message de confimation pour chaque compte configuré
                    print(
                        "Le produit a bien été mis dans le panier du compte ",
                        self.compte_objet_list[compte].email
                    )

                    # Fin de la boucle
                    break

                # Gestion des exceptions
                except:
                    pass

        # Commande du produit si checkout automatique activé
        if self.carte_objet_list:
            for compte in range(0, nombrecompte):
                while True:
                    try:
                        # Ouverture de la Session
                        with requests.Session() as session:
                            # Réglage des paramètres de la session
                            session.mount("http://", TimeoutHTTPAdapter(max_retries=retries))

                            session.headers.update(
                                {"User-Agent": generate_user_agent(os=("mac", "linux"))}
                            )

                            # Réglage du proxy
                            session.proxies = {"https": 'https://%s' % random.choice(self.liste_proxys)}

                            # Connexion à la page d'accueil de Zalando
                            url_google = "https://www.google.com/?client=safari"
                            url_home = "https://www.zalando.fr"
                            session.get(url_google, verify=False)
                            session.headers[
                                "Accept"
                            ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                            session.headers["Accept-Language"] = "fr-fr"
                            session.headers["Accept-Encoding"] = "gzip, deflate, br"
                            home_2 = session.get(url_home, verify=False)

                            # Récupération et modification des cookies de la session
                            cookies_2 = session.cookies.get_dict()
                            del session.cookies['mpulseinject']
                            session.cookies['mpulseinject'] = 'false'
                            session.headers["Accept"] = "*/*"
                            session.headers["x-xsrf-token"] = cookies_2["frsx"]
                            url_div = "https://www.zalando.fr/api/navigation/banners?gender=unisex&membership=non-eligible&url=https%3A%2F%2Fwww.zalando.fr%2F"
                            url_div2 = "https://www.zalando.fr/api/navigation"
                            url_div3 = (
                                    "https://www.zalando.fr/api/t/js_pixel?flowId=%s&cid=%s&js=true&ga=true"
                                    % (home_2.headers["X-Flow-Id"], home_2.cookies["Zalando-Client-Id"])
                            )
                            session.get(url_div, verify=False)
                            session.get(url_div2, verify=False)
                            session.headers[
                                "Accept"
                            ] = "image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5"
                            del session.headers["x-xsrf-token"]
                            session.get(url_div3, verify=False)

                            # Connexion à la page de connexion
                            url_connexion_1 = "https://www.zalando.fr/login/?view=login"
                            login = session.get(url_connexion_1, verify=False)

                            # Requetes anti-bot
                            url_bot_2 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                            data1_2 = {
                                "sensor_data": "7a74G7m23Vrp0o5c9178011.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392127,8356226,1440,900,1440,900,1440,513,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.903443507451,796854178112.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,375,887,490;1,1,633,804,295;2,1,682,803,292;3,1,825,803,292;4,1,826,700,270;5,1,831,696,270;6,1,891,691,270;7,1,906,678,278;8,1,912,676,279;9,1,917,676,280;10,1,927,674,280;11,1,954,674,281;12,1,969,672,281;13,1,999,671,281;14,3,1046,671,281,1466;15,1,1090,671,281;16,4,1093,671,281,1466;17,2,1119,671,281,1466;18,1,1410,671,281;19,1,14210,654,237;20,1,14230,654,237;21,1,14231,655,236;22,1,14234,657,236;23,1,14235,657,236;24,1,14242,659,236;25,1,14242,659,236;26,1,14249,662,236;27,1,14250,662,236;28,1,14257,664,236;29,1,14258,664,236;30,1,14267,671,236;31,1,14267,671,236;32,1,14276,677,236;33,1,14282,683,236;34,1,14283,683,236;35,1,14289,688,236;36,1,14290,688,236;37,1,14299,694,236;38,1,14300,694,236;39,1,14305,699,238;40,1,14306,699,238;41,1,14314,707,240;42,1,14315,707,240;43,1,14321,712,243;44,1,14321,712,243;45,1,14329,718,247;46,1,14329,718,247;47,1,14337,725,253;48,1,14338,725,253;49,1,14344,731,259;50,1,14345,731,259;51,1,14353,737,267;52,1,14354,737,267;53,1,14361,742,275;54,1,14362,742,275;55,1,14369,746,284;56,1,14370,746,284;57,1,14376,748,292;58,1,14376,748,292;59,1,14384,748,297;60,1,14385,748,297;61,1,14392,749,304;62,1,14393,749,304;63,1,14401,749,311;64,1,14401,749,311;65,1,14408,749,315;66,1,14408,749,315;67,1,14416,749,319;68,1,14416,749,319;69,1,14423,749,322;70,1,14424,749,322;71,1,14431,747,323;72,1,14432,747,323;73,1,14439,745,324;74,1,14440,745,324;75,1,14447,743,325;76,1,14447,743,325;77,1,14455,738,325;78,1,14455,738,325;79,1,14463,734,325;80,1,14464,734,325;81,1,14470,730,323;82,1,14471,730,323;83,1,14478,724,317;84,1,14479,724,317;85,1,14486,718,311;86,1,14486,718,311;87,1,14494,709,303;88,1,14495,709,303;89,1,14502,702,295;90,1,14503,702,295;91,1,14511,692,284;92,1,14512,692,284;93,1,14518,689,280;94,1,14519,689,280;95,1,14525,683,271;96,1,14526,683,271;97,1,14534,678,265;98,1,14534,678,265;99,1,14543,675,260;100,1,14544,675,260;101,1,14550,673,256;102,1,14551,673,256;186,3,15449,606,280,1466;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,1003;0,1740;2,1939;1,13685;3,14207;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,1,1349798,32,0,0,0,1349766,15449,0,1593708356225,40,17049,0,187,2841,3,0,15451,1241425,0,F47B7ACD62E06613840912E4B0FF4D34~-1~YAAQDex7XHjKERBzAQAA4adrEAQVKC4G5DWTwiDbd99QE0TG/CZ/X7/0id5k5Wx002o9cnpldjg2VaUQLUT7xhQ16xAXRWtpmFjanwsvOKrPuOhteppYDYFUsR7dmXHIQ068VDYGjPmJ3s1QezU6/OK7qU/7z0Xzvw9HMdvSPwXK3yDBL3Xn5VCqcupRCesCB0vUZ37uYYJJv8rx1GdciMHQXlb1zg7waQUUQjLQM7oZUeI7QqqXoiPdQMPP/FSWoCe1fGoDA7+05Ur96s4rsR99wfKdfjv3wrPr71c+IetpJ2aONaAL0HHVhSeEeTzNST4NF0JAIB+KtncIoMXcQToOfVY7~-1~-1~-1,32020,851,1050434953,26018161,PiZtE,53346,121-1,2,-94,-106,1,3-1,2,-94,-119,200,0,0,0,0,0,0,0,200,0,0,600,200,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,25068636-1,2,-94,-118,188046-1,2,-94,-121,;4;10;0"
                                               % session.headers["User-Agent"]
                            }
                            data2_2 = {
                                "sensor_data": "7a74G7m23Vrp0o5c9178011.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392127,8356226,1440,900,1440,900,1440,513,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.883221105441,796854178112.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,15627,91,0,2,1466;1,1,15699,86,0,2,1466;2,3,15701,118,0,2,1466;3,2,15848,-2,0,0,1466;-1,2,-94,-110,0,1,375,887,490;1,1,633,804,295;2,1,682,803,292;3,1,825,803,292;4,1,826,700,270;5,1,831,696,270;6,1,891,691,270;7,1,906,678,278;8,1,912,676,279;9,1,917,676,280;10,1,927,674,280;11,1,954,674,281;12,1,969,672,281;13,1,999,671,281;14,3,1046,671,281,1466;15,1,1090,671,281;16,4,1093,671,281,1466;17,2,1119,671,281,1466;18,1,1410,671,281;19,1,14210,654,237;20,1,14230,654,237;21,1,14231,655,236;22,1,14234,657,236;23,1,14235,657,236;24,1,14242,659,236;25,1,14242,659,236;26,1,14249,662,236;27,1,14250,662,236;28,1,14257,664,236;29,1,14258,664,236;30,1,14267,671,236;31,1,14267,671,236;32,1,14276,677,236;33,1,14282,683,236;34,1,14283,683,236;35,1,14289,688,236;36,1,14290,688,236;37,1,14299,694,236;38,1,14300,694,236;39,1,14305,699,238;40,1,14306,699,238;41,1,14314,707,240;42,1,14315,707,240;43,1,14321,712,243;44,1,14321,712,243;45,1,14329,718,247;46,1,14329,718,247;47,1,14337,725,253;48,1,14338,725,253;49,1,14344,731,259;50,1,14345,731,259;51,1,14353,737,267;52,1,14354,737,267;53,1,14361,742,275;54,1,14362,742,275;55,1,14369,746,284;56,1,14370,746,284;57,1,14376,748,292;58,1,14376,748,292;59,1,14384,748,297;60,1,14385,748,297;61,1,14392,749,304;62,1,14393,749,304;63,1,14401,749,311;64,1,14401,749,311;65,1,14408,749,315;66,1,14408,749,315;67,1,14416,749,319;68,1,14416,749,319;69,1,14423,749,322;70,1,14424,749,322;71,1,14431,747,323;72,1,14432,747,323;73,1,14439,745,324;74,1,14440,745,324;75,1,14447,743,325;76,1,14447,743,325;77,1,14455,738,325;78,1,14455,738,325;79,1,14463,734,325;80,1,14464,734,325;81,1,14470,730,323;82,1,14471,730,323;83,1,14478,724,317;84,1,14479,724,317;85,1,14486,718,311;86,1,14486,718,311;87,1,14494,709,303;88,1,14495,709,303;89,1,14502,702,295;90,1,14503,702,295;91,1,14511,692,284;92,1,14512,692,284;93,1,14518,689,280;94,1,14519,689,280;95,1,14525,683,271;96,1,14526,683,271;97,1,14534,678,265;98,1,14534,678,265;99,1,14543,675,260;100,1,14544,675,260;101,1,14550,673,256;102,1,14551,673,256;186,3,15449,606,280,1466;188,4,15550,606,280,1466;189,2,15556,606,280,1466;313,3,16356,666,346,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,1003;0,1740;2,1939;1,13685;3,14207;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,69052,1400743,32,0,0,0,1469762,16356,0,1593708356225,40,17049,4,314,2841,5,0,16358,1351762,0,F47B7ACD62E06613840912E4B0FF4D34~-1~YAAQDex7XLvLERBzAQAAFeBrEATcL5sl0zgV7hXa6IvZO2QT3hLEasdPcX9ezDCTjChowIfAFvx+Q+T7cQAWoFaW8RNof/+Z2OvHog5F8Td4/XBLFqEK9M3PsonioZ47Sx2j75amRQH4X/7OhwhX40SICYOPfBxaCcv4fZNwPI7TplOsJMIljBeOdTTKwCF2Cffu4oo1vqAqpFGWNzbSdqTZ18b+ZK+uYAbdraJtzi336EFKc9KGa2kTrIrp+y5pM2ZCk8FvVv288O43kXM35qnl+Egs1SA3YM4mU/I0rPeJMjgeOp95XiDDQUbeRDMFiCykPrq5JXhcqTMNxIHi0sXXBg3t~-1~-1~-1,31936,851,1050434953,26018161,PiZtE,23794,107-1,2,-94,-106,1,4-1,2,-94,-119,200,0,0,0,0,0,0,0,200,0,0,600,200,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,25068636-1,2,-94,-118,196289-1,2,-94,-121,;2;10;0"
                                               % session.headers["User-Agent"]
                            }
                            session.headers["Accept"] = "*/*"
                            session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                            session.headers["Origin"] = "https://www.zalando.fr"
                            session.headers[
                                "Referer"
                            ] = "https://www.zalando.fr/login/?view=login"
                            session.post(url_bot_2, json=data1_2, verify=False)
                            session.post(url_bot_2, json=data2_2, verify=False)
                            del session.headers["Content-Type"]
                            del session.headers["Origin"]
                            del session.headers["Referer"]

                            # Connexion au compte
                            url_connexion_2 = "https://www.zalando.fr/api/reef/login/schema"
                            url_connexion_3 = "https://www.zalando.fr/api/reef/login"
                            url_compte = "https://www.zalando.fr/myaccount"
                            identifiants_2 = {
                                "username": self.compte_objet_list[compte].email,
                                "password": self.compte_objet_list[compte].motdepasse,
                                "wnaMode": "shop",
                            }
                            session.headers["x-xsrf-token"] = cookies_2["frsx"]
                            session.headers["x-zalando-client-id"] = cookies_2[
                                "Zalando-Client-Id"
                            ]
                            session.headers["x-zalando-render-page-uri"] = "/login/?view=login"
                            session.headers["x-zalando-request-uri"] = "/login/?view=login"
                            session.headers["x-flow-id"] = login.headers[
                                "X-Zalando-Child-Request-Id"
                            ]
                            session.headers["Content-Type"] = "application/json"
                            session.headers["Accept"] = "application/json"
                            session.headers[
                                "Referer"
                            ] = "https://www.zalando.fr/login/?view=login"
                            session.get(url_connexion_2, verify=False)
                            session.headers["Origin"] = "https://www.zalando.fr"
                            session.headers["Content-Length"] = "76"
                            session.post(url_connexion_3, json=identifiants_2, verify=False)
                            del session.headers["x-xsrf-token"]
                            del session.headers["x-zalando-client-id"]
                            del session.headers["x-zalando-render-page-uri"]
                            del session.headers["x-zalando-request-uri"]
                            del session.headers["x-flow-id"]
                            del session.headers["Content-Length"]
                            del session.headers["Content-Type"]
                            del session.headers["Origin"]
                            session.headers[
                                "Accept"
                            ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                            accueil = session.get(url_compte, verify=False)

                            # Validation du panier et checkout
                            bot_2_2 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                            bot_3_2 = "https://www.zalando.fr/api/cart/details"
                            bot_4_2 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                            bot_5_2 = "https://www.zalando.fr/api/rr/e"
                            url_panier_1 = "https://www.zalando.fr/cart/"
                            url_panier_2 = "https://www.zalando.fr/checkout/confirm"
                            url_panier_3 = "https://www.zalando.fr/checkout/address"
                            bot_6 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                            url_panier_4 = "https://www.zalando.fr/api/checkout/search-pickup-points-by-address"
                            data_bot2_2 = {
                                "sensor_data": "7a74G7m23Vrp0o5c9179211.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392145,8120368,1440,900,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.253321588126,796889060184,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1075,-1,1;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1075,-1,1;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/myaccount-1,2,-94,-115,1,32,32,0,0,0,0,1,0,1593778120368,-999999,17049,0,0,2841,0,0,2,0,0,83B56B14F8791DE4459B2C8598D943FC~-1~YAAQDex7XFuSJxBzAQAAhxmUFARw88kisNpiFVwyQs7ReWEop16qPFMe+VyLWUTZrCy7SZ1/IeDafSHu/HwSxhuIH5iGZEC59iHXo+lhFihkHwcQUHKIe+IFNX9AqswJqkpjhRIqOqzEp8rzefrlVv/QZ8+TlE3agC6k7axpxToHECu4Uu+HS6sgG9SVQu/j6SkLmiQYHbLDoWkeWc//d6ukSGArsYcNEJTOilWs6UEd+JwOCeA2H1k+Ag+qYpTKXxlXW3fKPAwyTeCDng32+lX2lUbGLoZnWtK9Pj2lADYgVfMEVRSqJ23Qdb47qz8u+U4lRRJcY3kxsCio55JsKXjPn/0=~-1~-1~-1,32638,-1,-1,26018161,PiZtE,38925,90-1,2,-94,-106,0,0-1,2,-94,-119,-1-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,-1-1,2,-94,-80,94-1,2,-94,-116,219249894-1,2,-94,-118,82726-1,2,-94,-121,;3;-1;0"
                                               % session.headers["User-Agent"]
                            }
                            data_bot4_2 = {
                                "sensor_data": "7a74G7m23Vrp0o5c9179211.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392145,8120368,1440,900,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.987229521493,796889060184,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1075,-1,1;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1075,-1,1;-1,2,-94,-108,-1,2,-94,-110,0,1,5356,662,355;1,1,5357,662,355;2,1,5363,666,354;3,1,5364,666,354;4,1,5369,671,353;5,1,5370,671,353;6,1,5378,677,349;7,1,5379,677,349;8,1,5385,687,343;9,1,5386,687,343;10,1,5395,704,332;11,1,5395,704,332;12,1,5401,718,321;13,1,5402,718,321;14,1,5423,735,310;15,1,5427,762,290;16,1,5436,795,269;17,1,5442,817,256;18,1,5450,839,243;19,1,5451,839,243;20,1,5457,848,239;21,1,5458,848,239;22,1,5464,869,230;23,1,5465,869,230;24,1,5472,889,222;25,1,5472,889,222;26,1,5480,907,215;27,1,5481,907,215;28,1,5489,926,208;29,1,5489,926,208;30,1,5495,943,203;31,1,5496,943,203;32,1,5503,961,196;33,1,5504,961,196;34,1,5511,977,189;35,1,5522,992,183;36,1,5527,1008,176;37,1,5536,1022,169;38,1,5543,1033,162;39,1,5544,1033,162;40,1,5552,1045,155;41,1,5553,1045,155;42,1,5559,1056,148;43,1,5560,1056,148;44,1,5566,1066,142;45,1,5567,1066,142;46,1,5574,1074,135;47,1,5575,1074,135;48,1,5582,1083,129;49,1,5583,1083,129;50,1,5591,1090,123;51,1,5592,1090,123;52,1,5598,1098,117;53,1,5598,1098,117;54,1,5606,1104,112;55,1,5606,1104,112;56,1,5624,1111,106;57,1,5625,1117,102;58,1,5630,1123,98;59,1,5631,1123,98;60,1,5637,1126,96;61,1,5638,1126,96;62,1,5648,1130,92;63,1,5649,1130,92;64,1,5655,1135,89;65,1,5655,1135,89;66,1,5662,1140,87;67,1,5662,1140,87;68,1,5669,1143,85;69,1,5670,1143,85;70,1,5679,1146,83;71,1,5680,1146,83;72,1,5686,1149,81;73,1,5687,1149,81;74,1,5694,1151,80;75,1,5694,1151,80;76,1,5700,1154,78;77,1,5701,1154,78;78,1,5709,1157,77;79,1,5710,1157,77;80,1,5718,1159,75;81,1,5718,1159,75;82,1,5724,1162,74;83,1,5725,1162,74;84,1,5732,1164,72;85,1,5733,1164,72;86,1,5740,1167,70;87,1,5741,1167,70;88,1,5750,1169,69;89,1,5750,1169,69;90,1,5757,1171,67;91,1,5757,1171,67;92,1,5764,1174,66;93,1,5764,1174,66;94,1,5772,1176,64;95,1,5773,1176,64;96,1,5779,1179,63;97,1,5780,1179,63;98,1,5789,1181,61;99,1,5790,1181,61;205,3,6324,1256,56,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/myaccount-1,2,-94,-115,1,688232,32,0,0,0,688200,6324,0,1593778120368,110,17049,0,206,2841,1,0,6326,564474,0,83B56B14F8791DE4459B2C8598D943FC~-1~YAAQDex7XNWSJxBzAQAALCuUFARpiI+esYkf8lYdpjdLCeXpGHJ9+vnM6kEHHFvxY7T3yfNiygvtsQijxoB0yNuYl9wZotLwIwuoC9bI17FAhvUdRcyXL+l0Ge888pkyWFzJAH3M+C2Kp6Gd707Y65BbzbnblYpOVxKrIuiYQ77TdYjt9j85/zP5/tbklZ300b0M5/G4heKt5UOVncp1KtlqCNj9THUFEgo4ANkwaLOE1/K9PohfRbC90hyz7hzdxY3JGKGZuQ7uKN9p/ETblQXE3kwGtZDiPLgQ4nGGYzOT0iwZkVYPZOzRXBFruRu2U32RmNm4eOHksmzrFcYnCk212yM=~-1~-1~-1,32589,130,-829678606,26018161,PiZtE,72737,94-1,2,-94,-106,1,2-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,0,400,600,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,219249894-1,2,-94,-118,178607-1,2,-94,-121,;3;4;0"
                                               % session.headers["User-Agent"]
                            }
                            data_bot5_2 = {
                                "event": "event_tracking",
                                "eventCategory": "cart",
                                "eventAction": "view",
                                "eventLabel": "overlay.opened by hover",
                                "flowId": accueil.headers["X-Zalando-Child-Request-Id"],
                                "host": "www.zalando.fr",
                                "pathname": "/myaccount",
                                "referrer": "https://www.zalando.fr/login/?view=login",
                                "accept_language": "fr-FR",
                                "timestamp": "",
                            }
                            data_bot5bis_2 = {
                                "event": "event_tracking",
                                "eventCategory": "header",
                                "eventAction": "click",
                                "eventLabel": "cart",
                                "flowId": accueil.headers["X-Zalando-Child-Request-Id"],
                                "host": "www.zalando.fr",
                                "pathname": "/myaccount",
                                "referrer": "https://www.zalando.fr/login/?view=login",
                                "accept_language": "fr-FR",
                                "timestamp": "",
                            }
                            data_bot6_2 = {
                                "sensor_data": "7a74G7m23Vrp0o5c9179231.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392147,6416884,1440,900,1440,900,1440,338,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.772422311386,796893208442,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,-1,2,-94,-102,-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/checkout/address-1,2,-94,-115,1,32,32,0,0,0,0,818,0,1593786416884,25,17049,0,0,2841,0,0,819,0,0,6E7A8BB6ED1A8AB786D6512DC1ED4DB1~-1~YAAQNOx7XOEjEQ1zAQAA7L4SFQTDTAWYNVhRFWiIO+dsppVcEdLR8OJRi7qC9jIKE/1/yVQ8wwFceE79rVsV16vQTlhCjf6m3sJxsVFse1aLT8Yv483jeNiR/2r4xL9+9tp6dlT/UkgJ6G3LfubwSQFH5GdebR0fyceZWp6OQgmhi04d2gKJQSlBsjppZM5wME1IGtdl3qKsjsjZ2ldmGdUX4ElaslapCGdZy06b5toxd1dcPEVCdsbyhBXgjixLYPWH8h0790FxzL57Q5zQgWjavp8z48Y8xzcc8tH5gaRZNTzWZn6RRHh+tOdfwtmx23p/FogeywZifk8efVVAcZ11UMw=~-1~-1~-1,32721,333,-388728882,26018161,PiZtE,50292,83-1,2,-94,-106,9,1-1,2,-94,-119,0,200,0,0,200,0,0,200,800,2600,200,2400,2200,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,7796514045-1,2,-94,-118,82939-1,2,-94,-121,;2;4;0"
                                               % session.headers["User-Agent"]
                            }
                            checkout_2 = {
                                "address": {
                                    "id": self.compte_objet_list[compte].id_adresse,
                                    "salutation": "Mr",
                                    "first_name": self.compte_objet_list[compte].prenom,
                                    "last_name": self.compte_objet_list[compte].nom,
                                    "zip": self.compte_objet_list[compte].codepostal,
                                    "city": self.compte_objet_list[compte].ville,
                                    "country_code": "FR",
                                    "street": self.compte_objet_list[compte].adresse,
                                    "additional": self.compte_objet_list[compte].complement_adresse,
                                }
                            }
                            session.headers["Accept"] = "*/*"
                            session.headers["Referer"] = "https://www.zalando.fr/myaccount"
                            session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                            session.post(bot_2_2, json=data_bot2_2, verify=False)
                            del session.headers["Content-Type"]
                            session.headers["Accept"] = "*/*"
                            session.headers["x-xsrf-token"] = cookies_2["frsx"]
                            session.get(bot_3_2, verify=False)
                            del session.headers["x-xsrf-token"]
                            session.headers["Accept"] = "*/*"
                            session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                            session.headers["Referer"] = "https://www.zalando.fr/myaccount"
                            session.headers["Origin"] = "https://www.zalando.fr"
                            session.post(bot_4_2, json=data_bot4_2, verify=False)
                            session.post(bot_5_2, json=data_bot5_2, verify=False)
                            session.post(bot_5_2, json=data_bot5bis_2, verify=False)
                            del session.headers["Origin"]
                            del session.headers["Content-Type"]
                            session.headers[
                                "Accept"
                            ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                            session.get(url_panier_1, verify=False)
                            session.headers["Referer"] = "https://www.zalando.fr/cart"
                            session.get(url_panier_2, verify=False)
                            session.get(url_panier_3, verify=False)
                            session.headers["Accept"] = "*/*"
                            session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                            session.headers["Origin"] = "https://www.zalando.fr"
                            session.headers[
                                "Referer"
                            ] = "https://www.zalando.fr/checkout/address"
                            session.post(bot_6, json=data_bot6_2, verify=False)
                            del session.headers["Content-Type"]
                            session.headers["Accept"] = "application/json"
                            session.headers["x-zalando-footer-mode"] = "desktop"
                            session.headers["x-zalando-checkout-app"] = "web"
                            session.headers["x-xsrf-token"] = cookies_2["frsx"]
                            session.headers["x-zalando-header-mode"] = "desktop"
                            session.post(url_panier_4, json=checkout_2, verify=False)

                            # Adresse de livraison
                            url_checkout_1 = (
                                    "https://www.zalando.fr/api/checkout/address/%s/default"
                                    % self.compte_objet_list[compte].id_adresse
                            )
                            url_bot_1_2 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                            url_checkout_2_2 = "https://www.zalando.fr/api/checkout/next-step"
                            data_checkout_2 = {"isDefaultShipping": True}
                            bot = {
                                "sensor_data": "7a74G7m23Vrp0o5c9179241.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392147,8581193,1440,900,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.390034960195,796894290596.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,-1,2,-94,-102,0,-1,0,0,-1,-1,1;-1,2,-94,-108,-1,2,-94,-110,0,1,657,1080,411;1,1,660,1075,411;2,1,666,1064,411;3,1,668,1056,411;4,1,677,1040,411;5,1,677,1040,411;6,1,690,1027,411;7,1,691,1027,411;8,1,700,1004,411;9,1,701,1004,411;10,1,711,988,410;11,1,711,988,410;12,1,724,967,410;13,1,724,967,410;14,1,734,948,409;15,1,736,948,409;16,1,745,934,409;17,1,745,934,409;18,1,760,916,407;19,1,762,916,407;20,1,769,902,407;21,1,770,902,407;22,1,783,880,405;23,1,793,865,404;24,1,794,865,404;25,1,801,842,403;26,1,801,842,403;27,1,812,820,401;28,1,813,820,401;29,1,825,805,401;30,1,826,805,401;31,1,835,784,400;32,1,836,784,400;33,1,849,771,399;34,1,850,771,399;35,1,859,751,399;36,1,859,751,399;37,1,868,740,399;38,1,869,740,399;39,1,882,727,399;40,1,883,727,399;41,1,894,718,399;42,1,895,718,399;43,1,904,714,399;44,1,905,714,399;45,1,913,710,399;46,1,914,710,399;47,1,926,709,399;48,1,927,709,399;49,1,965,709,399;50,1,965,709,399;51,1,970,709,398;52,1,971,709,398;53,1,982,710,398;54,1,983,710,398;55,1,996,709,398;56,1,996,709,398;57,1,3418,709,398;58,1,3430,707,398;59,1,3436,707,398;60,1,3446,707,398;61,1,3451,707,398;62,1,3457,706,398;63,1,3467,706,397;64,1,3472,706,397;65,1,3480,707,397;66,1,3484,707,397;67,1,3490,708,395;68,1,3494,708,395;69,1,3502,710,392;70,1,3506,710,392;71,1,3514,712,389;72,1,3520,712,389;73,1,3526,717,382;74,1,3535,724,374;75,1,3551,724,374;76,1,3599,737,356;77,1,3707,795,293;78,1,3752,811,282;79,1,4005,823,277;80,1,4069,863,260;81,1,4195,863,260;82,1,4226,863,260;83,3,4312,863,260,-1;84,4,4489,863,260,-1;85,1,7670,861,261;86,1,7671,861,261;87,1,7677,858,261;88,1,7681,858,261;89,1,7688,857,262;90,1,7689,857,262;91,1,7699,856,263;92,1,7700,856,263;93,1,7713,854,264;94,1,7714,854,264;95,1,7722,852,265;96,1,7723,852,265;97,1,7732,851,265;98,1,7733,851,265;99,1,7745,849,266;100,1,7745,849,266;101,1,7757,847,267;204,3,8588,789,264,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/checkout/address-1,2,-94,-115,1,416497,32,0,0,0,416465,8588,0,1593788581193,15,17049,0,205,2841,3,0,8589,288802,0,76260A165DC066A281E308D22442E210~-1~YAAQDex7XEniKhBzAQAAv90zFQRgLX+H525FNSJA+PWv3mymWCgXUW580xaXcmKBPWhYINfvGdhIS/F039c2iPvffQzIIxVPbFbiaDkeoKEFjS1mkS0iI4dzN3bizDcLlWilXfCJLKlXbiobWfkI/ep3LTzlRiFrOyEfWdNFgZGvd02CTOFsgbLFR/+RRoZVYNPcwHxvjANKHPThPx92XQwkthmMJ0bkDzrKjPwzZhrvSzA+8C8F59/9YHxpAdj0zHzFnc7m8t4LZXtsDk5MdsFOg04sIIbbUCoZFbOhnfxcpSMV9PUG+wA/XyEyd9goPiawwLG0YkESoP58BTucyV6ynbE=~-1~-1~-1,32761,971,1563747676,26018161,PiZtE,83370,83-1,2,-94,-106,1,3-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,0,800,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,231692481-1,2,-94,-118,175938-1,2,-94,-121,;2;2;0"
                                               % session.headers["User-Agent"]
                            }
                            session.headers["Accept"] = "application/json"
                            session.headers["Content-Type"] = "application/json"
                            session.headers["Origin"] = "https://www.zalando.fr"
                            session.headers["Referer"
                            ] = "https://www.zalando.fr/checkout/address"
                            session.headers["x-zalando-footer-mode"] = "desktop"
                            session.headers["x-zalando-checkout-app"] = "web"
                            session.headers["x-xsrf-token"] = cookies_2["frsx"]
                            session.headers["x-zalando-header-mode"] = "desktop"
                            session.post(url_checkout_1, json=data_checkout_2, verify=False)
                            del session.headers["x-xsrf-token"]
                            del session.headers["x-zalando-header-mode"]
                            del session.headers["x-zalando-checkout-app"]
                            del session.headers["x-zalando-footer-mode"]
                            del session.headers["Content-Type"]
                            del session.headers["Origin"]
                            session.headers["Accept"] = "*/*"
                            session.post(url_bot_1_2, json=bot, verify=False)
                            session.headers["Accept"] = "*/*"
                            session.headers["Referer"] = "https://www.zalando.fr/checkout/address"
                            session.headers["x-zalando-footer-mode"] = "desktop"
                            session.headers["x-zalando-checkout-app"] = "web"
                            session.headers["x-xsrf-token"] = cookies_2["frsx"]
                            session.headers["x-zalando-header-mode"] = "desktop"
                            reponse_livraison = session.get(url_checkout_2_2, verify=False)
                            pay_ini = json.loads(reponse_livraison.text)
                            url_pay_ini = str(pay_ini["url"])
                            del session.headers["x-zalando-footer-mode"]
                            del session.headers["x-zalando-checkout-app"]
                            del session.headers["x-xsrf-token"]
                            del session.headers["x-zalando-header-mode"]
                            session.headers[
                                "Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                            session.headers["Host"] = "checkout.payment.zalando.com"
                            session.headers["Referer"] = "https://www.zalando.fr/checkout/address"
                            session.get(url_pay_ini, verify=False, allow_redirects=False)

                            # Paiement Partie 1
                            url_pay = "https://checkout.payment.zalando.com/selection"
                            url_pay_2 = "https://card-entry-service.zalando-payments.com/contexts/checkout/cards"
                            data_cb = {
                                "card_holder": self.carte_objet_list.nom,
                                "pan": self.carte_objet_list.numero,
                                "cvv": self.carte_objet_list.criptogramme,
                                "expiry_month": self.carte_objet_list.mois,
                                "expiry_year": self.carte_objet_list.annee,
                                "options": {
                                    "selected": [],
                                    "not_selected": ["store_for_reuse"],
                                },
                            }
                            a_2 = session.get(url_pay, verify=False, allow_redirects=False)
                            if self.liste_proxys != ['paypal']:
                                session_id_2 = session.cookies["Session-ID"]
                                soup_3 = BeautifulSoup(a_2.text, "html.parser")
                                objet_token_ini = soup_3.find(string=re.compile("config.accessToken"))
                                token_ini = objet_token_ini.split("'")
                                token = token_ini[1]
                                session.headers["Accept"] = "*/*"
                                session.headers["Origin"] = "https://card-entry-service.zalando-payments.com"
                                session.headers["Content-Type"] = "application/json"
                                session.headers["Host"] = "card-entry-service.zalando-payments.com"
                                del session.cookies['mpulseinject']
                                session.headers["Authorization"] = "Bearer %s" % token
                                reponsepay = session.post(
                                    url_pay_2, json=data_cb, verify=False, allow_redirects=False
                                )
                                reponsepaybis = json.loads(reponsepay.text)

                                # Paiement Partie 2
                                url_pay_3 = (
                                        "https://checkout.payment.zalando.com/payment-method-selection-session/%s/selection?"
                                        % session_id_2
                                )
                                data_pay_3 = (
                                        "payz_selected_payment_method=CREDIT_CARD&payz_credit_card_former_payment_method_id=-1&iframe_funding_source_id=%s"
                                        % reponsepaybis["id"]
                                )
                                del session.headers["Authorization"]
                                session.headers["Referer"] = "https://checkout.payment.zalando.com/selection"
                                session.headers[
                                    "Accept"
                                ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                                session.headers["Origin"] = "https://checkout.payment.zalando.com"
                                session.headers[
                                    "Content-Type"
                                ] = "application/x-www-form-urlencoded"
                                session.headers["Host"] = "checkout.payment.zalando.com"
                                session.post(url_pay_3, data=data_pay_3, verify=False)

                                # Paiement Partie 3
                                url_pay_4 = "https://www.zalando.fr/checkout/payment-complete"
                                del session.headers["Content-Type"]
                                del session.headers["Origin"]
                                session.headers["Host"] = "www.zalando.fr"
                                session.headers[
                                    "Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                                b = session.get(url_pay_4, verify=False)
                                soupbis_3 = BeautifulSoup(b.content, "html.parser")
                                reponsefinale_3 = soupbis_3.find(attrs={"data-props": re.compile('eTag')})
                                reponsefinale1_3 = reponsefinale_3['data-props']
                                reponsefinale2_3 = json.loads(reponsefinale1_3)
                                checkout_id = reponsefinale2_3['model']['checkoutId']
                                etagini = reponsefinale2_3['model']['eTag']

                                # Paiement FIN
                                url_pay_bot = 'https://www.zalando.fr/resources/35692132da2028b315fc23b805e921'
                                url_pay_fin = 'https://www.zalando.fr/api/checkout/buy-now'
                                data_bot_pay = {
                                    'sensor_data': 'a74G7m23Vrp0o5c9179431.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392164,7588656,1920,1080,1920,1080,1920,1017,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.967902033483,796928794328,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,-1,3960,0;-1,2,-94,-102,0,-1,0,0,-1,3960,0;-1,2,-94,-108,-1,2,-94,-110,0,1,260,839,528;1,1,261,839,528;2,1,274,839,528;3,1,281,839,528;4,1,283,838,529;5,1,289,837,529;6,1,290,837,529;7,1,303,834,530;8,1,304,834,530;9,1,312,828,531;10,1,312,828,531;11,1,324,818,533;12,1,325,818,533;13,1,335,810,534;14,1,338,810,534;15,1,346,799,534;16,1,348,799,534;17,1,359,790,534;18,1,360,790,534;19,1,368,781,535;20,1,380,774,535;21,1,397,766,535;22,1,398,766,535;23,1,402,758,535;24,1,403,758,535;25,1,435,755,535;26,1,437,747,536;27,1,448,744,536;28,1,449,744,536;29,1,462,743,536;30,1,462,743,536;31,1,471,741,536;32,1,472,741,536;33,1,482,740,536;34,1,483,740,536;35,1,494,740,536;36,1,495,740,536;37,1,572,740,536;38,1,572,740,536;39,1,584,742,535;40,1,584,742,535;41,1,593,744,535;42,1,594,744,535;43,1,606,746,535;44,1,606,746,535;45,1,616,750,534;46,1,618,750,534;47,1,627,757,534;48,1,628,757,534;49,1,642,764,535;50,1,643,764,535;51,1,651,771,535;52,1,652,771,535;53,1,663,783,536;54,1,664,783,536;55,1,675,800,537;56,1,676,800,537;57,1,684,816,538;58,1,685,816,538;59,1,695,850,540;60,1,704,850,540;61,1,849,895,546;62,1,871,1120,587;63,1,874,1126,589;64,1,878,1128,590;65,1,887,1129,591;66,1,888,1129,591;67,1,1121,1133,593;68,1,1130,1139,593;69,1,1141,1140,593;70,1,1170,1140,593;71,1,1171,1140,593;72,1,1416,1139,593;73,1,1423,1138,592;74,1,1438,1137,592;75,1,1443,1136,592;76,1,1449,1136,591;77,1,1451,1136,591;78,1,1485,1136,591;79,1,1485,1137,590;80,1,1494,1137,588;81,1,1495,1137,588;82,1,1504,1138,585;83,1,1505,1138,585;84,1,1516,1140,583;85,1,1517,1140,583;86,1,1532,1141,581;87,1,1538,1141,581;88,1,1541,1142,579;89,1,1549,1144,577;90,1,1550,1144,577;91,1,1562,1145,576;92,1,1562,1145,576;93,1,1572,1146,575;94,1,1573,1146,575;95,1,1583,1147,574;96,1,1587,1147,574;97,1,1596,1148,574;98,1,1598,1148,574;99,1,1618,1148,573;256,3,5106,1244,954,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/checkout/confirm-1,2,-94,-115,1,242493,32,0,0,0,242461,5106,0,1593857588656,12,17050,0,257,2841,1,0,5108,87744,0,76260A165DC066A281E308D22442E210~-1~YAAQNOx7XOg6hBVzAQAARcBQGQSyvSFbFGXl59iNajFhHhapCF6BkxAA0sqDaoD9MZ0sqZZZGU0QvNo4YzuehT+HCCZ+QcgR83ZMGQxqQpnXCIGFbPQ9lpbkkovEK8nocdwGx5GAqGaxWsVOHLXej4YT0gcTiqqlZg+6Z/Y6dVuzxBr7tkSnSODv52r6Sd9cr/U3w/VJTDmT2MpPwSWFHNx/PjOERknhjj1NY6yNNn9Df8Ih+lL8L7jIhNaMnur9afb0scBr7NhG0AVH/0qWz+O5+Zmxwi0s1ASNjAeh2jJHlr25uReBJ2l20pa5pUEB4UaqHwmCv4s4kYmORGswxW3u65E=~-1~-1~-1,32325,146,-242715172,26018161,PiZtE,81065,44-1,2,-94,-106,1,2-1,2,-94,-119,200,0,0,0,0,0,200,0,0,200,200,2200,1000,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,1844041464-1,2,-94,-118,175375-1,2,-94,-121,;3;6;0' %
                                                   session.headers['User-Agent']
                                }
                                data_pay_fin = {
                                    'checkoutId': checkout_id,
                                    'eTag': etagini
                                }
                                session.headers["Host"] = "www.zalando.fr"
                                session.headers["Accept"] = "*/*"
                                session.headers["Referer"] = "https://www.zalando.fr/checkout/confirm"
                                session.headers["Origin"] = 'https://www.zalando.fr'
                                session.headers['Content-Type'] = 'text/plain;charset=UTF-8'
                                session.post(url_pay_bot, json=data_bot_pay, verify=False)
                                session.headers["Accept"] = "application/json"
                                session.headers["x-zalando-footer-mode"] = "desktop"
                                session.headers["x-zalando-checkout-app"] = "web"
                                session.headers["x-xsrf-token"] = cookies_2["frsx"]
                                session.headers['Content-Type'] = 'application/json'
                                session.headers['x-zalando-header-mode'] = 'desktop'
                                session.post(url_pay_fin, json=data_pay_fin, verify=False)

                        # Fermeture de la Session
                        session.close()
                        print("The product has been ordered !")
                        break

                    # Gestion des exceptions
                    except:
                        pass

        else:
            print("Fin de tâche")


def titre():
    print(Fore.RED + Style.BRIGHT + "  ___                     _     __     ______    ___ ")
    print(Fore.RED + Style.BRIGHT + "/ ___|  ___ ___  ___   __| |   /  \   |_    _| /  _  \ ")
    print(Fore.RED + Style.BRIGHT + "\___ \ / __|  _|/ _ \ / _' |  / /\ \    |  |  |  / \  |")
    print(Fore.RED + Style.BRIGHT + " ___) | (__| | |  __/| ( | | / /__\ \  _|  |_ |  \_/  |")
    print(Fore.RED + Style.BRIGHT + "|____/ \___|_|  \___| \_.__|/_/    \_\|______| \_____/")
    print("\n")


# ----------------------------------------------------------------------------------Fonction licenses--------------------------------------------------------------#

# Informations du propriétaire
RSAPubKey = "<RSAKeyValue><Modulus>zGKjhD1u4eZQg+U2oZgX8inZ1SLvb83jD+oKD20GplwpYcqquQZMAPokGXTs8FMD5X2sc6FtiNKg/wcapvkuyS9KRTauaoQib/B2SW7e9b4zkfpg3hJHW8zm9CZ3F2xbH5E8aXOlm0Knu9lOxjE+e7IogTQGk5RvyO4TO6QRO71bc9dW9h44KWdzku6lcF1VBHM646E6F10ziq7beGhmyLt/dbz88Yt9VP5CKBRH+/QDafbV+KD86WFTQ69p/j+k/h1QF2LYY2tVOhz9TL0iF9zpb8e4mR/vL1RGU3T3ztS21AwGwyCI2j1xc8KvWsUWnPgfDsIr4SRi6EH0d5joxQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyIyOTQ2NiIsInBGK1diMVN2TnhPd3ZZTnNxczNXd3MvZS8xT3hKK2RKZk9wbklBT1ciXQ=="


# Fonction de vérification les liscences en ligne. (https://cryptolens.io/)
def VerificationLicense():
    with open("Data/License.txt", "r") as f:
        License = f.read()
        if License == "":
            print("Enter your License key in file : License.txt\n")
            exit()

    result = Key.activate(token=auth,
                          rsa_pub_key=RSAPubKey,
                          product_id=6868,
                          key=License,
                          machine_code=Helpers.GetMachineCode())

    if result[0] is None or not Helpers.IsOnRightMachine(result[0]):
        print("ERREUR: {0}".format(result[1]))

        print("\nYour License is invalid.\n")
        exit()

    else:
        print("Your license is valid.\n")
        pass


# ------------------------------------------------------------------------------------------------------------------------------------------------#


# Création des objets "Compte" et de la liste d'objet "compte_objet_list"
def creation_objet_compte():
    acces_fichier = open("../Data/Comptes.json", "r")
    compte_objet_list = []
    for compte_attributes in json.load(acces_fichier):
        compte_objet = Compte(**compte_attributes)
        compte_objet_list.append(compte_objet)
    acces_fichier.close()
    return compte_objet_list


# Récupérations des proxies
def proxy():
    with open('../Data/proxy.txt', 'r') as f:
        liste_proxys = []
        for ligne in f:
            if ligne.strip('\n') != '':
                liste_proxys.append(ligne.strip('\n'))

        if not liste_proxys:
            print("You did not specify any proxy.")
            print("Enter the address of the proxy servers in the proxy.txt file.")

        return liste_proxys


# Saisie des informations personnelles et du nombre de comptes souhaité
def SaisieInformations():
    # Création d'une liste "liste_compte" vide
    liste_comptes = []

    # Saisie des informations
    print("Welcome to the Zalando account generator !")
    prenom = input("Enter your first name:")
    nom = input("Enter your name :")
    cp = input("Enter your postal code :")
    ville = input("Enter your city of residence (without accents) :")
    adresse = input("Enter your address (without accents) :")
    complement = input("Complément d'adresse (cliquer sur entrer pour passer) :")
    telephone = input("Enter a mobile phone number :")
    nombrecompte = int(
        input(
            "Enter the desired number of accounts (1 valid email address per account) :"
        )
    )
    for i in range(0, nombrecompte):
        email = input("Enter a valid email address:")
        i = {
            "id_liste": "",
            "prenom": prenom,
            "nom": nom,
            "email": email,
            "motdepasse": "",
            "codepostal": cp,
            "ville": ville,
            "adresse": adresse,
            "complement_adresse": complement,
            "id_adresse": "",
            "telephone": telephone,
        }
        # Création d'un mot de passe aléatoire et sécurisé
        pwo = PasswordGenerator()
        i["motdepasse"] = pwo.generate()
        # Insertion des comptes dans la liste "liste_compte"
        liste_comptes.append(i)

    # Insertion des comptes dans la base de données "Comptes.json"
    with open("../Data/Comptes.json", "w") as f:
        json.dump(liste_comptes, f, indent=4)
    f.close()

    # Message de confimation
    print("Your personal information has been saved !")


def ModePaiement():
    # Création d'une liste "liste_paiement" vide
    liste_paiement = []

    # Saisie des informations
    nombrecb = int(
        input(
            "Entrer le nombre de carte bancaire à saisir :"
        )
    )
    for i in range(0, nombrecb):
        nom = input('Entrer le nom sur la carte (DUPOND Jean) :')
        num = input('Entrer le numéro de la carte avec espaces (3233 3288 3222 3333) :')
        mois = input("Entrer le mois d'expiration sans '0' devant (8) :")
        annee = input("Entrer l'année d'expliration (2023) : ")
        cripto = input('Entrer le cryptogramme visuel (134) :')
        i = {
            "nom": nom,
            "numero": num,
            "mois": mois,
            "annee": annee,
            "criptogramme": cripto
        }

        # Insertion des comptes dans la liste "liste_compte"
        liste_paiement.append(i)

    # Insertion des comptes dans la base de données "Comptes.json"
    with open("../Data/Paiement.json", "w") as f:
        json.dump(liste_paiement, f, indent=4)
    f.close()

    # Message de confimation
    print("Vos informations bancaires ont bien été sauvegardées !")


# Création des objets "Carte" et de la liste d'objet "carte_objet_list"
def creation_objet_carte():
    acces_fichier = open("../Data/Paiement.json", "r")
    carte_objet_list = []
    for carte_attributes in json.load(acces_fichier):
        carte_objet = Carte(**carte_attributes)
        carte_objet_list.append(carte_objet)
    acces_fichier.close()
    return carte_objet_list


# Création des comptes à partir des attributs de chaque objet "Compte"
def CreationComptes(compte_objet_list, liste_proxys):
    # Comptage du nombre de comptes présents dans la base de données
    nombrecompte = len(compte_objet_list)

    # Création d'un compte pour chaque objet "Compte" présent dans la base de données
    for compte in range(0, nombrecompte):
        x = 0
        while True:
            try:
                # Ouverture de la session
                with requests.Session() as session:
                    # Réglage des paramètres de la session
                    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
                    session.headers.update(
                        {"User-Agent": generate_user_agent(os=("mac", "linux"))}
                    )

                    # Réglage du proxy
                    session.proxies = {"https": "https://%s" % liste_proxys[x]}

                    # Connexion à la page d'accueil de Zalando
                    url_home = "https://www.zalando.fr"
                    home = session.get(url_home, verify=False)

                    # Récupération des cookies de la session
                    cookies = session.cookies.get_dict()

                    # Connexion à la page d'inscription
                    url_get = "https://www.zalando.fr/login/?view=register"
                    session.get(url_get, verify=False)

                    # Mise à jour du headers
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.headers["x-zalando-client-id"] = cookies[
                        "Zalando-Client-Id"
                    ]
                    session.headers["x-zalando-render-page-uri"] = "/"
                    session.headers["x-zalando-request-uri"] = "/"
                    session.headers["x-flow-id"] = home.headers["X-Flow-Id"]
                    session.headers["Accept"] = "application/json"

                    # Envoie de requetes pour éviter les sécurités anti-bot
                    url_get_2 = "https://www.zalando.fr/resources/a6c5863f92201d42d0a3ba96882c7b"
                    url_get_3 = (
                            "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=1"
                            % home.headers["X-Flow-Id"]
                    )
                    url_post1 = "https://www.zalando.fr/resources/a6c5863f921840dbe8f36578d86f32"
                    sensor_data = {
                        "sensor_data": "7a74G7m23Vrp0o5c9179861.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392194,6927070,1920,1080,1920,1080,1920,587,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.13311868866,796988463535,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,924,1884,0;0,-1,0,0,930,1768,0;0,1,0,0,1044,1435,0;1,-1,0,0,2163,1798,0;-1,2,-94,-102,0,-1,0,0,998,1884,1;0,-1,0,0,949,1768,1;0,1,0,0,1144,1435,1;1,-1,0,0,2062,1798,0;-1,2,-94,-108,0,1,218339,-2,0,0,1884;1,3,218340,-2,0,0,1884;2,1,218411,-2,0,0,1884;3,3,218411,-2,0,0,1884;4,2,218440,-2,0,0,1884;5,2,218495,-2,0,0,1884;6,1,218507,-2,0,0,1884;7,3,218508,-2,0,0,1884;8,1,218608,-2,0,0,1884;9,3,218608,-2,0,0,1884;10,2,218641,-2,0,0,1884;11,2,218675,-2,0,0,1884;12,1,220597,-2,0,0,1768;13,3,220598,-2,0,0,1768;14,1,220676,-2,0,0,1768;15,3,220677,-2,0,0,1768;16,2,220707,-2,0,0,1768;17,2,220752,-2,0,0,1768;18,1,220773,-2,0,0,1768;19,3,220774,-2,0,0,1768;20,1,220837,-2,0,0,1768;21,3,220838,-2,0,0,1768;22,2,220889,-2,0,0,1768;23,2,220909,-2,0,0,1768;24,1,223485,-2,0,0,1435;25,3,223486,-2,0,0,1435;26,2,223577,-2,0,0,1435;27,1,223581,-2,0,0,1435;28,3,223581,-2,0,0,1435;29,2,223652,-2,0,0,1435;30,1,223670,-2,0,0,1435;31,3,223671,-2,0,0,1435;32,1,223810,-2,0,0,1435;33,3,223811,-2,0,0,1435;34,2,223835,-2,0,0,1435;35,2,223879,-2,0,0,1435;36,1,224067,-2,0,0,1435;37,3,224067,-2,0,0,1435;38,2,224201,-2,0,0,1435;39,1,224703,-2,0,0,1435;40,3,224703,-2,0,0,1435;41,2,224775,-2,0,0,1435;42,1,225010,-2,0,0,1435;43,3,225011,-2,0,0,1435;44,2,225099,-2,0,0,1435;45,1,225182,-2,0,0,1435;46,3,225183,-2,0,0,1435;47,2,225259,-2,0,0,1435;48,1,225313,-2,0,0,1435;49,3,225313,-2,0,0,1435;50,2,225376,-2,0,0,1435;51,1,225490,-2,0,0,1435;52,3,225491,-2,0,0,1435;53,2,225550,-2,0,0,1435;54,1,225590,16,0,8,1435;55,1,225738,-2,0,8,1435;56,3,225739,-2,0,8,1435;57,2,225793,16,0,0,1435;58,2,225794,-2,0,0,1435;59,1,225952,-2,0,0,1435;60,3,225957,-2,0,0,1435;61,1,226032,-2,0,0,1435;62,3,226032,-2,0,0,1435;63,2,226059,-2,0,0,1435;64,2,226115,-2,0,0,1435;65,1,226179,-2,0,0,1435;66,3,226180,-2,0,0,1435;67,2,226273,-2,0,0,1435;-1,2,-94,-110,0,1,11,921,87;1,1,2420,526,927;2,1,2424,526,927;3,1,2427,538,912;4,1,2438,546,898;5,1,2444,549,888;6,1,2454,551,875;7,1,2461,551,856;8,1,2470,551,843;9,1,2477,543,827;10,1,2487,530,809;11,1,2493,515,792;12,1,2502,495,770;13,1,2510,484,760;14,1,2520,465,741;15,1,2524,449,725;16,1,2535,444,721;17,1,2544,435,714;18,1,2550,429,708;19,1,2558,425,705;20,1,2566,423,702;21,1,2575,422,701;22,1,2584,421,701;23,1,2590,421,701;24,3,2615,421,701,-1;25,4,2732,421,701,-1;26,2,2732,421,701,-1;27,1,2972,421,702;28,1,2974,421,702;29,1,2979,417,708;30,1,2979,417,708;31,1,2986,413,717;32,1,2987,413,717;33,1,2993,407,726;34,1,2993,407,726;35,1,3001,402,736;36,1,3002,402,736;37,1,3012,397,745;38,1,3013,397,745;39,1,3018,382,770;40,1,3019,382,770;41,1,3026,369,792;42,1,3027,369,792;43,1,3036,354,817;44,1,3036,354,817;45,1,3043,336,844;46,1,3044,336,844;47,1,3050,321,869;48,1,3051,321,869;49,1,3058,305,897;50,1,3059,305,897;51,1,3068,299,906;52,1,3069,299,906;53,1,4633,219,905;54,1,4636,214,870;55,1,4643,205,836;56,1,4650,194,800;57,1,4661,178,764;58,1,4667,158,725;59,1,4676,137,691;60,1,4685,112,660;61,1,4692,82,628;62,1,4699,51,603;63,1,4708,14,579;64,1,16166,5,574;65,1,16172,5,574;66,1,16176,37,568;67,1,16189,83,562;68,1,16202,138,557;69,1,16211,171,555;70,1,16223,206,553;71,1,16237,236,553;72,1,16245,261,554;73,1,16256,278,554;74,1,16270,294,555;75,1,16277,305,557;76,1,16291,312,558;77,1,16303,319,559;78,1,16326,326,560;79,1,16338,327,560;80,1,16346,328,560;81,1,16357,328,560;82,1,16383,328,560;83,1,16396,328,560;84,1,16406,328,560;85,1,16414,328,560;86,1,16425,329,560;87,1,16439,329,560;88,1,16446,331,560;89,1,16459,336,560;90,1,16472,342,560;91,1,16481,348,560;92,1,16493,358,560;93,1,16507,369,561;94,1,16516,380,562;95,1,16526,396,564;96,1,16540,414,567;97,1,16549,427,570;98,1,16560,431,572;99,1,16574,435,574;100,1,16583,437,575;101,1,16593,439,577;102,1,16608,440,578;329,4,56092,1433,431,-1;468,3,207362,522,266,-1,3;565,3,216020,834,402,1884;566,4,216119,834,402,1884;567,2,216125,834,402,1884;600,3,219228,852,500,-1;601,4,219315,852,500,-1;602,2,219315,852,500,-1;643,3,219809,1095,471,1768;645,4,219944,1096,471,1768;646,2,219944,1096,471,1768;772,3,222232,934,618,1435;774,4,222403,934,618,1435;775,2,222404,934,618,1435;955,3,226947,1047,710,1798;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,2626;2,3975;3,55999;2,135087;3,202399;2,204275;2,209387;3,216078;-1,2,-94,-112,https://www.zalando.fr/login/?view=register-1,2,-94,-115,15277576,4101469,32,0,0,0,19379012,226947,0,1593976927070,49,17051,68,956,2841,12,0,226949,19125976,0,76260A165DC066A281E308D22442E210~-1~YAAQVex7XApf3+5yAQAAtxdxIATyF8XdNicO4+Pe+pODGAYF1dJVsyGmLnGUfB/xBSRu8VgbMjYcawGfsII8LoBH51JMuQa4cYXmrtMZ+Md1/vCFoUhCaPB+2eYPesZXyQfDahs3h0iIiT56Cq6d3ViMgSa18H6dPc5wdXk2/n0ddaeU0wSySgtS1u5HGWP89HgsSHGtgGee6ABA2CUM/L70WINMLZpnx1glWYP2ax9f+9kCVbOHSfT0c8+zvZa/o7mn64zZIt6tE/MXGRuNvcbw+OeiksaI4iZJbWIRJ5duQQ9Gg9PO9P3NHt0dwuGA9F43tuQfoWF8RJqa5PKmjOGvmKc=~-1~-1~-1,31840,588,1200352557,26018161,PiZtE,66948,66-1,2,-94,-106,1,8-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,0,800,1200,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,20781153-1,2,-94,-118,290061-1,2,-94,-121,;2;4;0" %
                                       session.headers["User-Agent"]
                    }
                    sensor_data_bis = {
                        "sensor_data": "7a74G7m23Vrp0o5c9179861.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392194,6927070,1920,1080,1920,1080,1920,587,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.457866288228,796988463535,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,924,1884,0;0,-1,0,0,930,1768,0;0,1,0,0,1044,1435,0;1,-1,0,0,2163,1798,0;-1,2,-94,-102,0,-1,0,0,975,1884,1;0,-1,0,0,984,1768,1;0,1,0,0,1094,1435,1;1,-1,0,0,2053,1798,1;-1,2,-94,-108,0,1,218339,-2,0,0,1884;1,3,218340,-2,0,0,1884;2,1,218411,-2,0,0,1884;3,3,218411,-2,0,0,1884;4,2,218440,-2,0,0,1884;5,2,218495,-2,0,0,1884;6,1,218507,-2,0,0,1884;7,3,218508,-2,0,0,1884;8,1,218608,-2,0,0,1884;9,3,218608,-2,0,0,1884;10,2,218641,-2,0,0,1884;11,2,218675,-2,0,0,1884;12,1,220597,-2,0,0,1768;13,3,220598,-2,0,0,1768;14,1,220676,-2,0,0,1768;15,3,220677,-2,0,0,1768;16,2,220707,-2,0,0,1768;17,2,220752,-2,0,0,1768;18,1,220773,-2,0,0,1768;19,3,220774,-2,0,0,1768;20,1,220837,-2,0,0,1768;21,3,220838,-2,0,0,1768;22,2,220889,-2,0,0,1768;23,2,220909,-2,0,0,1768;24,1,223485,-2,0,0,1435;25,3,223486,-2,0,0,1435;26,2,223577,-2,0,0,1435;27,1,223581,-2,0,0,1435;28,3,223581,-2,0,0,1435;29,2,223652,-2,0,0,1435;30,1,223670,-2,0,0,1435;31,3,223671,-2,0,0,1435;32,1,223810,-2,0,0,1435;33,3,223811,-2,0,0,1435;34,2,223835,-2,0,0,1435;35,2,223879,-2,0,0,1435;36,1,224067,-2,0,0,1435;37,3,224067,-2,0,0,1435;38,2,224201,-2,0,0,1435;39,1,224703,-2,0,0,1435;40,3,224703,-2,0,0,1435;41,2,224775,-2,0,0,1435;42,1,225010,-2,0,0,1435;43,3,225011,-2,0,0,1435;44,2,225099,-2,0,0,1435;45,1,225182,-2,0,0,1435;46,3,225183,-2,0,0,1435;47,2,225259,-2,0,0,1435;48,1,225313,-2,0,0,1435;49,3,225313,-2,0,0,1435;50,2,225376,-2,0,0,1435;51,1,225490,-2,0,0,1435;52,3,225491,-2,0,0,1435;53,2,225550,-2,0,0,1435;54,1,225590,16,0,8,1435;55,1,225738,-2,0,8,1435;56,3,225739,-2,0,8,1435;57,2,225793,16,0,0,1435;58,2,225794,-2,0,0,1435;59,1,225952,-2,0,0,1435;60,3,225957,-2,0,0,1435;61,1,226032,-2,0,0,1435;62,3,226032,-2,0,0,1435;63,2,226059,-2,0,0,1435;64,2,226115,-2,0,0,1435;65,1,226179,-2,0,0,1435;66,3,226180,-2,0,0,1435;67,2,226273,-2,0,0,1435;68,1,228357,16,0,8,1798;69,1,228603,-2,0,8,1798;70,3,228609,-2,0,8,1798;71,2,228667,-2,0,8,1798;72,2,228742,16,0,0,1798;73,1,228882,-2,0,0,1798;74,3,228882,-2,0,0,1798;75,2,228962,-2,0,0,1798;76,1,229105,-2,0,0,1798;77,3,229106,-2,0,0,1798;78,2,229189,-2,0,0,1798;79,1,229229,-2,0,0,1798;80,3,229230,-2,0,0,1798;81,1,229582,16,0,8,1798;82,2,230306,16,0,0,1798;-1,2,-94,-110,0,1,11,921,87;1,1,2420,526,927;2,1,2424,526,927;3,1,2427,538,912;4,1,2438,546,898;5,1,2444,549,888;6,1,2454,551,875;7,1,2461,551,856;8,1,2470,551,843;9,1,2477,543,827;10,1,2487,530,809;11,1,2493,515,792;12,1,2502,495,770;13,1,2510,484,760;14,1,2520,465,741;15,1,2524,449,725;16,1,2535,444,721;17,1,2544,435,714;18,1,2550,429,708;19,1,2558,425,705;20,1,2566,423,702;21,1,2575,422,701;22,1,2584,421,701;23,1,2590,421,701;24,3,2615,421,701,-1;25,4,2732,421,701,-1;26,2,2732,421,701,-1;27,1,2972,421,702;28,1,2974,421,702;29,1,2979,417,708;30,1,2979,417,708;31,1,2986,413,717;32,1,2987,413,717;33,1,2993,407,726;34,1,2993,407,726;35,1,3001,402,736;36,1,3002,402,736;37,1,3012,397,745;38,1,3013,397,745;39,1,3018,382,770;40,1,3019,382,770;41,1,3026,369,792;42,1,3027,369,792;43,1,3036,354,817;44,1,3036,354,817;45,1,3043,336,844;46,1,3044,336,844;47,1,3050,321,869;48,1,3051,321,869;49,1,3058,305,897;50,1,3059,305,897;51,1,3068,299,906;52,1,3069,299,906;53,1,4633,219,905;54,1,4636,214,870;55,1,4643,205,836;56,1,4650,194,800;57,1,4661,178,764;58,1,4667,158,725;59,1,4676,137,691;60,1,4685,112,660;61,1,4692,82,628;62,1,4699,51,603;63,1,4708,14,579;64,1,16166,5,574;65,1,16172,5,574;66,1,16176,37,568;67,1,16189,83,562;68,1,16202,138,557;69,1,16211,171,555;70,1,16223,206,553;71,1,16237,236,553;72,1,16245,261,554;73,1,16256,278,554;74,1,16270,294,555;75,1,16277,305,557;76,1,16291,312,558;77,1,16303,319,559;78,1,16326,326,560;79,1,16338,327,560;80,1,16346,328,560;81,1,16357,328,560;82,1,16383,328,560;83,1,16396,328,560;84,1,16406,328,560;85,1,16414,328,560;86,1,16425,329,560;87,1,16439,329,560;88,1,16446,331,560;89,1,16459,336,560;90,1,16472,342,560;91,1,16481,348,560;92,1,16493,358,560;93,1,16507,369,561;94,1,16516,380,562;95,1,16526,396,564;96,1,16540,414,567;97,1,16549,427,570;98,1,16560,431,572;99,1,16574,435,574;100,1,16583,437,575;101,1,16593,439,577;102,1,16608,440,578;329,4,56092,1433,431,-1;468,3,207362,522,266,-1,3;565,3,216020,834,402,1884;566,4,216119,834,402,1884;567,2,216125,834,402,1884;600,3,219228,852,500,-1;601,4,219315,852,500,-1;602,2,219315,852,500,-1;643,3,219809,1095,471,1768;645,4,219944,1096,471,1768;646,2,219944,1096,471,1768;772,3,222232,934,618,1435;774,4,222403,934,618,1435;775,2,222404,934,618,1435;955,3,226947,1047,710,1798;956,4,227047,1047,710,1798;957,2,227048,1047,710,1798;1099,3,232121,1052,1107,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,2626;2,3975;3,55999;2,135087;3,202399;2,204275;2,209387;3,216078;-1,2,-94,-112,https://www.zalando.fr/login/?view=register-1,2,-94,-115,18741232,4796379,32,0,0,0,23537578,232121,0,1593976927070,49,17051,83,1100,2841,14,0,232123,23247643,0,76260A165DC066A281E308D22442E210~-1~YAAQVex7XDVf3+5yAQAAJCpxIASIK/u4VSyLlkilJT4PJrci3bIdwCoE657nvaF54+VGyUjPunq+pvPREKEqEvcmQ4w0iAdhne5yNzDZevX5c7I+Ewdj1xEHzbHX/jBmJBEPabObjz5thzNaH8qpEyteVNtT5ajmOJj6T6NMnkPZBCh1WaDWbk9kCujfHBIEmXWeKigoCwJA3rIzJHA7/mmzwNkdUyIMMHZw3ha0hnJiK3sBqa7EWYVLVgUQyNbVtL4QeC6RstjtUMiihAJeEHqDP47JN4meEsAY6o/VGicxdCWN7Vj+0+Z9jFrvrxCmCiBQWgEZ8bV2ni5pgQy982cOE0g=~-1~-1~-1,32589,588,1200352557,26018161,PiZtE,41164,43-1,2,-94,-106,1,9-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,0,800,1200,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,20781153-1,2,-94,-118,313027-1,2,-94,-121,;3;4;0" %
                                       session.headers["User-Agent"]
                    }
                    session.get(url_get_2, verify=False)
                    session.get(url_get_3, verify=False)
                    session.post(url_post1, json=sensor_data, verify=False)
                    session.post(url_post1, json=sensor_data_bis, verify=False)

                    # Préparation et envoie de la requete POST d'inscription
                    url_get2 = "https://www.zalando.fr/api/reef/register/schema"
                    url_post2 = "https://www.zalando.fr/api/reef/register"
                    register = {
                        "newCustomerData": {
                            "firstname": compte_objet_list[compte].prenom,
                            "lastname": compte_objet_list[compte].nom,
                            "email": compte_objet_list[compte].email,
                            "password": compte_objet_list[compte].motdepasse,
                            "fashion_preference": [],
                            "subscribe_to_news_letter": False,
                            "accepts_terms_and_conditions": True,
                            "date_of_birth": "",
                        },
                        "wnaMode": "shop",
                    }
                    session.get(url_get2, verify=False)
                    session.headers["Origin"] = "https://www.zalando.fr"
                    session.post(url_post2, json=register, verify=False)

                # Fermeture de la session
                session.close()

                # Message de confirmation pour chaque compte créé
                print(
                    "Le compte de", compte_objet_list[compte].email, "a bien été créé !"
                )
                break

            # Gestion des exceptions
            except:
                pass

            finally:
                x = x + 1
                if x == (len(liste_proxys) + 1):
                    x = 0


def Configuration(compte_objet_list, liste_proxys):
    # Comptage du nombre de compte présents dans la base de données
    nombrecompte = len(compte_objet_list)

    # Création d'un compte pour chaque objet "Compte" présent dans la base de données
    for y in range(0, nombrecompte):
        x = 0
        while True:
            try:
                with requests.Session() as session:
                    # Réglage des paramètres de la session
                    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
                    headers = {
                        "Host": "www.zalando.fr",
                        "User-Agent": generate_user_agent(os=("mac", "linux")),
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language": "fr-fr",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                    }
                    session.headers.update(headers)

                    # Réglage du proxy
                    session.proxies = {"https": "https://%s" % liste_proxys[x]}

                    # Connexion à la page d'accueil de Zalando
                    url_home = "https://www.zalando.fr"
                    home = session.get(url_home, verify=False)

                    # Récupération des cookies de la session
                    cookies = session.cookies.get_dict()

                    # Connexion à la page de connexion
                    url_get = "https://www.zalando.fr/login/?view=login"
                    del session.headers["Upgrade-Insecure-Requests"]
                    session.get(url_get, verify=False)

                    # Envoie de requetes pour éviter les sécurités anti-bot
                    url_get_1 = (
                            "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=1"
                            % home.headers["X-Flow-Id"]
                    )
                    session.get(url_get_1, verify=False)

                    # Envoie de requetes pour éviter les sécurités anti-bot
                    url_get_2 = (
                            "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=3"
                            % home.headers["X-Flow-Id"]
                    )
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.get(url_get_2, verify=False)

                    # Envoie de requetes pour éviter les sécurités anti-bot
                    url_post1 = "https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b"
                    sensor_data = {
                        "sensor_data": "7a74G7m23Vrp0o5c9175981.59-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391850,1658105,1440,814,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.294628793147,796290829052.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,617,939,3;1,1,622,939,3;2,1,624,946,6;3,1,633,955,10;4,1,635,955,10;5,1,639,965,15;6,1,639,965,15;7,1,647,976,19;8,1,648,976,19;9,1,657,991,24;10,1,657,991,24;11,1,663,1008,28;12,1,665,1008,28;13,1,672,1025,33;14,1,674,1025,33;15,1,679,1056,40;16,1,680,1056,40;17,1,688,1076,44;18,1,689,1076,44;19,1,696,1087,46;20,1,697,1087,46;21,1,703,1109,51;22,1,703,1109,51;23,1,712,1129,55;24,1,713,1129,55;25,1,720,1148,59;26,1,722,1148,59;27,1,727,1166,66;28,1,728,1166,66;29,1,736,1180,71;30,1,736,1180,71;31,1,744,1196,77;32,1,744,1196,77;33,1,753,1212,85;34,1,754,1212,85;35,1,760,1226,94;36,1,760,1226,94;37,1,769,1236,102;38,1,770,1236,102;39,1,775,1249,112;40,1,776,1249,112;41,1,787,1258,121;42,1,787,1258,121;43,1,791,1265,130;44,1,792,1265,130;45,1,802,1273,138;46,1,802,1273,138;47,1,808,1279,147;48,1,809,1279,147;49,1,818,1283,154;50,1,819,1283,154;51,1,825,1284,157;52,1,826,1284,157;53,1,832,1290,168;54,1,835,1290,168;55,1,840,1291,176;56,1,841,1291,176;57,1,850,1292,183;58,1,861,1293,190;59,1,864,1293,198;60,1,865,1293,198;61,1,873,1293,206;62,1,873,1293,206;63,1,882,1293,213;64,1,883,1293,213;65,1,889,1290,220;66,1,892,1290,220;67,1,897,1284,227;68,1,898,1284,227;69,1,908,1270,241;70,1,915,1255,250;71,1,918,1255,250;72,1,921,1239,258;73,1,922,1239,258;74,1,929,1216,267;75,1,929,1216,267;76,1,937,1190,274;77,1,938,1190,274;78,1,946,1162,282;79,1,947,1162,282;80,1,953,1130,287;81,1,954,1130,287;82,1,962,1096,293;83,1,962,1096,293;84,1,970,1061,296;85,1,970,1061,296;86,1,978,1022,298;87,1,979,1022,298;88,1,986,987,300;89,1,986,987,300;90,1,994,948,302;91,1,994,948,302;92,1,1005,917,304;93,1,1012,904,304;94,1,1013,904,304;95,1,1019,876,304;96,1,1020,876,304;97,1,1026,853,304;98,1,1026,853,304;99,1,1034,847,304;217,3,2758,739,188,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,329;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,1,220704,32,0,0,0,220672,2758,0,1592581658105,16,17036,0,218,2839,1,0,2759,84978,0,544D198E0F1B1CB2C191909E5A431D4A~-1~YAAQI5HdWON0Wa1yAQAAIJhDzQSs2DaHi3VWlNasxDo6Ll1h+oPs9Arg4f8DmMXtm7anSErvR5n9n2pO+UMTG/IVcwHpfi9Wi/ZDhjSRktF/01XyTRMeCqjaeI0/prETWeQeJkJTEUT7q7Lp9d7aH30hB2IihOsBdiBvSwqh9UbB/o6n5EgkZgrD6PRQwpDic6VG2QZ9k5czxOMXhm2LdiLG+/uKxYYkLkarftjuMKCgYsG+w4No1YL0WTXRpGFiEoZrP1PWYltbpu2Q2NBlWPFovn4VW0knih51voTZCUXpt52d7hsTVn2TdnQglcPVYqHyg6Goubm3of/HY6EI/ryzWoo=~-1~-1~-1,32678,285,1682362911,26018161,NVVN,124,-1-1,2,-94,-106,1,2-1,2,-94,-119,200,2200,0,0,0,0,0,0,0,200,0,3000,2600,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,44769069-1,2,-94,-118,176741-1,2,-94,-121,;1;4;0" %
                                       session.headers["User-Agent"]
                    }
                    sensor_data_bis = {
                        "sensor_data": "7a74G7m23Vrp0o5c9175981.59-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391850,1658105,1440,814,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.347127751173,796290829052.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,6662,undefined,0,0,1103,0;1,2,6677,undefined,0,0,1103,0;2,1,6716,undefined,0,0,1103,0;3,2,6726,undefined,0,0,1103,0;4,1,7287,13,0,0,1466;-1,2,-94,-110,0,1,617,939,3;1,1,622,939,3;2,1,624,946,6;3,1,633,955,10;4,1,635,955,10;5,1,639,965,15;6,1,639,965,15;7,1,647,976,19;8,1,648,976,19;9,1,657,991,24;10,1,657,991,24;11,1,663,1008,28;12,1,665,1008,28;13,1,672,1025,33;14,1,674,1025,33;15,1,679,1056,40;16,1,680,1056,40;17,1,688,1076,44;18,1,689,1076,44;19,1,696,1087,46;20,1,697,1087,46;21,1,703,1109,51;22,1,703,1109,51;23,1,712,1129,55;24,1,713,1129,55;25,1,720,1148,59;26,1,722,1148,59;27,1,727,1166,66;28,1,728,1166,66;29,1,736,1180,71;30,1,736,1180,71;31,1,744,1196,77;32,1,744,1196,77;33,1,753,1212,85;34,1,754,1212,85;35,1,760,1226,94;36,1,760,1226,94;37,1,769,1236,102;38,1,770,1236,102;39,1,775,1249,112;40,1,776,1249,112;41,1,787,1258,121;42,1,787,1258,121;43,1,791,1265,130;44,1,792,1265,130;45,1,802,1273,138;46,1,802,1273,138;47,1,808,1279,147;48,1,809,1279,147;49,1,818,1283,154;50,1,819,1283,154;51,1,825,1284,157;52,1,826,1284,157;53,1,832,1290,168;54,1,835,1290,168;55,1,840,1291,176;56,1,841,1291,176;57,1,850,1292,183;58,1,861,1293,190;59,1,864,1293,198;60,1,865,1293,198;61,1,873,1293,206;62,1,873,1293,206;63,1,882,1293,213;64,1,883,1293,213;65,1,889,1290,220;66,1,892,1290,220;67,1,897,1284,227;68,1,898,1284,227;69,1,908,1270,241;70,1,915,1255,250;71,1,918,1255,250;72,1,921,1239,258;73,1,922,1239,258;74,1,929,1216,267;75,1,929,1216,267;76,1,937,1190,274;77,1,938,1190,274;78,1,946,1162,282;79,1,947,1162,282;80,1,953,1130,287;81,1,954,1130,287;82,1,962,1096,293;83,1,962,1096,293;84,1,970,1061,296;85,1,970,1061,296;86,1,978,1022,298;87,1,979,1022,298;88,1,986,987,300;89,1,986,987,300;90,1,994,948,302;91,1,994,948,302;92,1,1005,917,304;93,1,1012,904,304;94,1,1013,904,304;95,1,1019,876,304;96,1,1020,876,304;97,1,1026,853,304;98,1,1026,853,304;99,1,1034,847,304;217,3,2758,739,188,1103;218,4,2893,739,188,1103;219,2,2893,739,188,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,329;2,4473;3,6695;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,NaN,228787,32,0,0,0,NaN,7287,0,1592581658105,16,17036,5,234,2839,2,0,7289,124832,0,544D198E0F1B1CB2C191909E5A431D4A~-1~YAAQI5HdWB11Wa1yAQAA5qBDzQSG6Pv/OSeYlJZ+5TdSTmLptNh6airlP5V/lfl0qZibNHdiWQexNK07iCtntsNCWGQHPYxIdWr4OhMwJ0i9iCooHr4ymTZvJOiehLUCEf20hGguVIpe5vO+tl8HNMUY7PGyvGkSCQeUF3LvyMptTNSG8CSY0BBnfap9mu2tyNqJrjG8Xea/jsk0hclFwXoOFGYut6G8PG3iNaLmer5R0671/1KuX41tQnpCg/f9510oCGeGVN2f1b3jSey1Ob7DjYTE+aUd5c5tuJsTW5eeK7Ce+eI43fC+QwqaWJz5TYZnz0IAjAGkEtDAFH4keWDUEZQ=~-1~-1~-1,32009,285,1682362911,26018161,NVVN,124,-1-1,2,-94,-106,3,3-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,0,600,200,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,44769069-1,2,-94,-118,188004-1,2,-94,-121,;2;4;0" %
                                       session.headers["User-Agent"]
                    }
                    session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                    session.headers["Accept"] = "*/*"
                    del session.headers["x-xsrf-token"]
                    session.post(url_post1, json=sensor_data, verify=False)
                    session.post(url_post1, json=sensor_data_bis, verify=False)

                    # Connexion au compte Zalando
                    url_connexion_get = "https://www.zalando.fr/api/reef/login/schema"
                    url_connexion_post2 = "https://www.zalando.fr/api/reef/login"
                    identifiants = {
                        "username": compte_objet_list[y].email,
                        "password": compte_objet_list[y].motdepasse,
                        "wnaMode": "shop",
                    }
                    session.headers["Accept"] = "application/json"
                    session.headers["x-zalando-request-uri"] = "/login/?view=login"
                    session.headers["x-zalando-render-page-uri"] = "/login/?view=login"
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.headers["x-flow-id"] = home.headers["X-Flow-Id"]
                    session.headers["x-zalando-client-id"] = cookies[
                        "Zalando-Client-Id"
                    ]
                    session.headers["Content-Type"] = "application/json"
                    session.get(url_connexion_get, verify=False)
                    session.headers["Origin"] = "https://www.zalando.fr"
                    session.post(url_connexion_post2, json=identifiants, verify=False)

                    # Affichage du profil
                    url_profil = "https://www.zalando.fr/myaccount"
                    session.get(url_profil, verify=False)

                    # Configuration du profil : Ajout d'un numéro de téléphone
                    url_informations_get = "https://www.zalando.fr/myaccount/details"
                    url_informations_post = (
                        "https://www.zalando.fr/api/user-account-details/details"
                    )
                    informations = {
                        "first_name": compte_objet_list[y].prenom,
                        "last_name": compte_objet_list[y].nom,
                        "fashion_category": [],
                        "birth_date": None,
                        "phone": compte_objet_list[y].telephone,
                    }
                    session.get(url_informations_get, verify=False)
                    session.post(url_informations_post, json=informations, verify=False)

                    # Configuration du profil : Ajout d'une adresse
                    url_profil_get = "https://www.zalando.fr/myaccount/addresses"
                    url_profil_post = (
                        "https://www.zalando.fr/api/user-account-address/addresses"
                    )
                    adresse = {
                        "type": "HomeAddress",
                        "city": compte_objet_list[y].ville,
                        "countryCode": "FR",
                        "firstname": compte_objet_list[y].prenom,
                        "lastname": compte_objet_list[y].nom,
                        "street": compte_objet_list[y].adresse,
                        "additional": compte_objet_list[y].complement_adresse,
                        "gender": "MALE",
                        "defaultBilling": True,
                        "defaultShipping": True,
                        "zip": compte_objet_list[y].codepostal,
                    }
                    session.get(url_profil_get, verify=False)
                    reponse = session.post(url_profil_post, json=adresse, verify=False)

                    # Récupération de l'id de d'adresse
                    objet = json.loads(reponse.text)
                    id_adresse = objet[0]["id"]
                    compte_objet_list[y].id_adresse = id_adresse

                # Fermeture de la session
                session.close()

                # Message de confimation pour chaque compte configuré
                print(
                    "Le compte de", compte_objet_list[y].email, "a bien été configuré !"
                )

                # Insertion des comptes actualisés dans la base de données "Comptes.json"
                liste_compte = []
                for b in range(0, len(compte_objet_list)):
                    liste_compte.append(compte_objet_list[b].__dict__)
                with open("../Data/Comptes.json", "w") as f:
                    json.dump(liste_compte, f, indent=4)
                f.close()

                break

            # Gestion des exceptions
            except:
                pass

            finally:
                x = x + 1
                if x == (len(liste_proxys) + 1):
                    x = 0


# Réglage du checkout automatique
def ModePaiementAutomatique(carte_objet_list):
    print("Bienvenu dans la recherche et commande de produit !")
    while True:
        print('Souhaitez-vous activer le checkout automatique ?')
        reponse = input('o / n :')

        if reponse == 'o':
            # Verification
            if len(carte_objet_list) == 0:
                print("Merci de saisir une carte bancaire !")
                break

            # Affichage des cartes bancaires disponibles
            print("Cartes bancaire disponibles : ")
            for carte in carte_objet_list:
                print("%s -" % carte, "Numéro de carte :", carte_objet_list[carte].numero)

            # Choix de la carte bancaire
            if len(carte_objet_list) == 1:
                rep_1 = input('Cliquer sur entrer pour valider ou taper sur une autre touche : ')
                if rep_1 == "" \
                            "":
                    return carte_objet_list
                else:
                    break
            else:
                rep_2 = int(input("Saisir le numéro de la carte souhaitée (2) ou cliquer sur entrer"))
                if rep_2 == "" \
                            "":
                    break
                else:
                    return carte_objet_list[rep_2]

        if reponse == 'n':
            break

        else:
            print('Entrer "o" ou "n"')


init()
titre()
horloge()
