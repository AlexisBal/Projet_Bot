import json
import re

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from user_agent import generate_user_agent
from bs4 import BeautifulSoup


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


# Fonction proxy
def proxy():
    with open("../Data/proxy.txt", "r") as f:
        liste_proxys = []
        for ligne in f:
            if ligne.strip("\n") != "":
                liste_proxys.append(ligne.strip("\n"))

        if not liste_proxys:
            print("Vous n'avez spécifié aucun proxy.")
            print("Entrer l'adresse des serveurs proxy dans le fichier proxy.txt")

        return liste_proxys


def Paiement_Zalando(compte_objet_list, liste_proxys):
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
                        {"User-Agent": generate_user_agent(os=("mac", "linux"))}
                    )

                    # Réglage du proxy
                    session.proxies = {"https": "https://%s" % liste_proxys[x]}

                    # Connexion à la page d'accueil de Zalando
                    url_google = "https://www.google.com/?client=safari"
                    url_home = "https://www.zalando.fr"
                    session.get(url_google, verify=False)
                    session.headers[
                        "Accept"
                    ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                    session.headers["Accept-Language"] = "fr-fr"
                    session.headers["Accept-Encoding"] = "gzip, deflate, br"
                    home = session.get(url_home, verify=False)

                    # Récupération et modification des cookies de la session
                    cookies = session.cookies.get_dict()
                    session.headers["Accept"] = "*/*"
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    url_div = "https://www.zalando.fr/api/navigation/banners?gender=unisex&membership=non-eligible&url=https%3A%2F%2Fwww.zalando.fr%2F"
                    url_div2 = "https://www.zalando.fr/api/navigation"
                    url_div3 = (
                        "https://www.zalando.fr/api/t/js_pixel?flowId=%s&cid=%s&js=true&ga=true"
                        % (home.headers["X-Flow-Id"], home.cookies["Zalando-Client-Id"])
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
                    url_bot = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                    data1 = {
                        "sensor_data": "7a74G7m23Vrp0o5c9178011.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392127,8356226,1440,900,1440,900,1440,513,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.903443507451,796854178112.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,375,887,490;1,1,633,804,295;2,1,682,803,292;3,1,825,803,292;4,1,826,700,270;5,1,831,696,270;6,1,891,691,270;7,1,906,678,278;8,1,912,676,279;9,1,917,676,280;10,1,927,674,280;11,1,954,674,281;12,1,969,672,281;13,1,999,671,281;14,3,1046,671,281,1466;15,1,1090,671,281;16,4,1093,671,281,1466;17,2,1119,671,281,1466;18,1,1410,671,281;19,1,14210,654,237;20,1,14230,654,237;21,1,14231,655,236;22,1,14234,657,236;23,1,14235,657,236;24,1,14242,659,236;25,1,14242,659,236;26,1,14249,662,236;27,1,14250,662,236;28,1,14257,664,236;29,1,14258,664,236;30,1,14267,671,236;31,1,14267,671,236;32,1,14276,677,236;33,1,14282,683,236;34,1,14283,683,236;35,1,14289,688,236;36,1,14290,688,236;37,1,14299,694,236;38,1,14300,694,236;39,1,14305,699,238;40,1,14306,699,238;41,1,14314,707,240;42,1,14315,707,240;43,1,14321,712,243;44,1,14321,712,243;45,1,14329,718,247;46,1,14329,718,247;47,1,14337,725,253;48,1,14338,725,253;49,1,14344,731,259;50,1,14345,731,259;51,1,14353,737,267;52,1,14354,737,267;53,1,14361,742,275;54,1,14362,742,275;55,1,14369,746,284;56,1,14370,746,284;57,1,14376,748,292;58,1,14376,748,292;59,1,14384,748,297;60,1,14385,748,297;61,1,14392,749,304;62,1,14393,749,304;63,1,14401,749,311;64,1,14401,749,311;65,1,14408,749,315;66,1,14408,749,315;67,1,14416,749,319;68,1,14416,749,319;69,1,14423,749,322;70,1,14424,749,322;71,1,14431,747,323;72,1,14432,747,323;73,1,14439,745,324;74,1,14440,745,324;75,1,14447,743,325;76,1,14447,743,325;77,1,14455,738,325;78,1,14455,738,325;79,1,14463,734,325;80,1,14464,734,325;81,1,14470,730,323;82,1,14471,730,323;83,1,14478,724,317;84,1,14479,724,317;85,1,14486,718,311;86,1,14486,718,311;87,1,14494,709,303;88,1,14495,709,303;89,1,14502,702,295;90,1,14503,702,295;91,1,14511,692,284;92,1,14512,692,284;93,1,14518,689,280;94,1,14519,689,280;95,1,14525,683,271;96,1,14526,683,271;97,1,14534,678,265;98,1,14534,678,265;99,1,14543,675,260;100,1,14544,675,260;101,1,14550,673,256;102,1,14551,673,256;186,3,15449,606,280,1466;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,1003;0,1740;2,1939;1,13685;3,14207;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,1,1349798,32,0,0,0,1349766,15449,0,1593708356225,40,17049,0,187,2841,3,0,15451,1241425,0,F47B7ACD62E06613840912E4B0FF4D34~-1~YAAQDex7XHjKERBzAQAA4adrEAQVKC4G5DWTwiDbd99QE0TG/CZ/X7/0id5k5Wx002o9cnpldjg2VaUQLUT7xhQ16xAXRWtpmFjanwsvOKrPuOhteppYDYFUsR7dmXHIQ068VDYGjPmJ3s1QezU6/OK7qU/7z0Xzvw9HMdvSPwXK3yDBL3Xn5VCqcupRCesCB0vUZ37uYYJJv8rx1GdciMHQXlb1zg7waQUUQjLQM7oZUeI7QqqXoiPdQMPP/FSWoCe1fGoDA7+05Ur96s4rsR99wfKdfjv3wrPr71c+IetpJ2aONaAL0HHVhSeEeTzNST4NF0JAIB+KtncIoMXcQToOfVY7~-1~-1~-1,32020,851,1050434953,26018161,PiZtE,53346,121-1,2,-94,-106,1,3-1,2,-94,-119,200,0,0,0,0,0,0,0,200,0,0,600,200,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,25068636-1,2,-94,-118,188046-1,2,-94,-121,;4;10;0"
                        % session.headers["User-Agent"]
                    }
                    data2 = {
                        "sensor_data": "7a74G7m23Vrp0o5c9178011.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392127,8356226,1440,900,1440,900,1440,513,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.883221105441,796854178112.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,15627,91,0,2,1466;1,1,15699,86,0,2,1466;2,3,15701,118,0,2,1466;3,2,15848,-2,0,0,1466;-1,2,-94,-110,0,1,375,887,490;1,1,633,804,295;2,1,682,803,292;3,1,825,803,292;4,1,826,700,270;5,1,831,696,270;6,1,891,691,270;7,1,906,678,278;8,1,912,676,279;9,1,917,676,280;10,1,927,674,280;11,1,954,674,281;12,1,969,672,281;13,1,999,671,281;14,3,1046,671,281,1466;15,1,1090,671,281;16,4,1093,671,281,1466;17,2,1119,671,281,1466;18,1,1410,671,281;19,1,14210,654,237;20,1,14230,654,237;21,1,14231,655,236;22,1,14234,657,236;23,1,14235,657,236;24,1,14242,659,236;25,1,14242,659,236;26,1,14249,662,236;27,1,14250,662,236;28,1,14257,664,236;29,1,14258,664,236;30,1,14267,671,236;31,1,14267,671,236;32,1,14276,677,236;33,1,14282,683,236;34,1,14283,683,236;35,1,14289,688,236;36,1,14290,688,236;37,1,14299,694,236;38,1,14300,694,236;39,1,14305,699,238;40,1,14306,699,238;41,1,14314,707,240;42,1,14315,707,240;43,1,14321,712,243;44,1,14321,712,243;45,1,14329,718,247;46,1,14329,718,247;47,1,14337,725,253;48,1,14338,725,253;49,1,14344,731,259;50,1,14345,731,259;51,1,14353,737,267;52,1,14354,737,267;53,1,14361,742,275;54,1,14362,742,275;55,1,14369,746,284;56,1,14370,746,284;57,1,14376,748,292;58,1,14376,748,292;59,1,14384,748,297;60,1,14385,748,297;61,1,14392,749,304;62,1,14393,749,304;63,1,14401,749,311;64,1,14401,749,311;65,1,14408,749,315;66,1,14408,749,315;67,1,14416,749,319;68,1,14416,749,319;69,1,14423,749,322;70,1,14424,749,322;71,1,14431,747,323;72,1,14432,747,323;73,1,14439,745,324;74,1,14440,745,324;75,1,14447,743,325;76,1,14447,743,325;77,1,14455,738,325;78,1,14455,738,325;79,1,14463,734,325;80,1,14464,734,325;81,1,14470,730,323;82,1,14471,730,323;83,1,14478,724,317;84,1,14479,724,317;85,1,14486,718,311;86,1,14486,718,311;87,1,14494,709,303;88,1,14495,709,303;89,1,14502,702,295;90,1,14503,702,295;91,1,14511,692,284;92,1,14512,692,284;93,1,14518,689,280;94,1,14519,689,280;95,1,14525,683,271;96,1,14526,683,271;97,1,14534,678,265;98,1,14534,678,265;99,1,14543,675,260;100,1,14544,675,260;101,1,14550,673,256;102,1,14551,673,256;186,3,15449,606,280,1466;188,4,15550,606,280,1466;189,2,15556,606,280,1466;313,3,16356,666,346,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,1003;0,1740;2,1939;1,13685;3,14207;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,69052,1400743,32,0,0,0,1469762,16356,0,1593708356225,40,17049,4,314,2841,5,0,16358,1351762,0,F47B7ACD62E06613840912E4B0FF4D34~-1~YAAQDex7XLvLERBzAQAAFeBrEATcL5sl0zgV7hXa6IvZO2QT3hLEasdPcX9ezDCTjChowIfAFvx+Q+T7cQAWoFaW8RNof/+Z2OvHog5F8Td4/XBLFqEK9M3PsonioZ47Sx2j75amRQH4X/7OhwhX40SICYOPfBxaCcv4fZNwPI7TplOsJMIljBeOdTTKwCF2Cffu4oo1vqAqpFGWNzbSdqTZ18b+ZK+uYAbdraJtzi336EFKc9KGa2kTrIrp+y5pM2ZCk8FvVv288O43kXM35qnl+Egs1SA3YM4mU/I0rPeJMjgeOp95XiDDQUbeRDMFiCykPrq5JXhcqTMNxIHi0sXXBg3t~-1~-1~-1,31936,851,1050434953,26018161,PiZtE,23794,107-1,2,-94,-106,1,4-1,2,-94,-119,200,0,0,0,0,0,0,0,200,0,0,600,200,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,25068636-1,2,-94,-118,196289-1,2,-94,-121,;2;10;0"
                        % session.headers["User-Agent"]
                    }
                    session.headers["Accept"] = "*/*"
                    session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                    session.headers["Origin"] = "https://www.zalando.fr"
                    session.headers[
                        "Referer"
                    ] = "https://www.zalando.fr/login/?view=login"
                    session.post(url_bot, json=data1, verify=False)
                    session.post(url_bot, json=data2, verify=False)
                    del session.headers["Content-Type"]
                    del session.headers["Origin"]
                    del session.headers["Referer"]

                    # Connexion au compte
                    url_connexion_2 = "https://www.zalando.fr/api/reef/login/schema"
                    url_connexion_3 = "https://www.zalando.fr/api/reef/login"
                    url_compte = "https://www.zalando.fr/myaccount"
                    identifiants = {
                        "username": compte_objet_list[compte].email,
                        "password": compte_objet_list[compte].motdepasse,
                        "wnaMode": "shop",
                    }
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.headers["x-zalando-client-id"] = cookies[
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
                    session.post(url_connexion_3, json=identifiants, verify=False)
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
                    bot_2 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                    bot_3 = "https://www.zalando.fr/api/cart/details"
                    bot_4 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                    bot_5 = "https://www.zalando.fr/api/rr/e"
                    url_panier_1 = "https://www.zalando.fr/cart/"
                    url_panier_2 = "https://www.zalando.fr/checkout/confirm"
                    url_panier_3 = "https://www.zalando.fr/checkout/address"
                    bot_6 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                    url_panier_4 = "https://www.zalando.fr/api/checkout/search-pickup-points-by-address"
                    data_bot2 = {
                        "sensor_data": "7a74G7m23Vrp0o5c9179211.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392145,8120368,1440,900,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.253321588126,796889060184,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1075,-1,1;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1075,-1,1;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/myaccount-1,2,-94,-115,1,32,32,0,0,0,0,1,0,1593778120368,-999999,17049,0,0,2841,0,0,2,0,0,83B56B14F8791DE4459B2C8598D943FC~-1~YAAQDex7XFuSJxBzAQAAhxmUFARw88kisNpiFVwyQs7ReWEop16qPFMe+VyLWUTZrCy7SZ1/IeDafSHu/HwSxhuIH5iGZEC59iHXo+lhFihkHwcQUHKIe+IFNX9AqswJqkpjhRIqOqzEp8rzefrlVv/QZ8+TlE3agC6k7axpxToHECu4Uu+HS6sgG9SVQu/j6SkLmiQYHbLDoWkeWc//d6ukSGArsYcNEJTOilWs6UEd+JwOCeA2H1k+Ag+qYpTKXxlXW3fKPAwyTeCDng32+lX2lUbGLoZnWtK9Pj2lADYgVfMEVRSqJ23Qdb47qz8u+U4lRRJcY3kxsCio55JsKXjPn/0=~-1~-1~-1,32638,-1,-1,26018161,PiZtE,38925,90-1,2,-94,-106,0,0-1,2,-94,-119,-1-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,-1-1,2,-94,-80,94-1,2,-94,-116,219249894-1,2,-94,-118,82726-1,2,-94,-121,;3;-1;0"
                        % session.headers["User-Agent"]
                    }
                    data_bot4 = {
                        "sensor_data": "7a74G7m23Vrp0o5c9179211.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392145,8120368,1440,900,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.987229521493,796889060184,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1075,-1,1;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1075,-1,1;-1,2,-94,-108,-1,2,-94,-110,0,1,5356,662,355;1,1,5357,662,355;2,1,5363,666,354;3,1,5364,666,354;4,1,5369,671,353;5,1,5370,671,353;6,1,5378,677,349;7,1,5379,677,349;8,1,5385,687,343;9,1,5386,687,343;10,1,5395,704,332;11,1,5395,704,332;12,1,5401,718,321;13,1,5402,718,321;14,1,5423,735,310;15,1,5427,762,290;16,1,5436,795,269;17,1,5442,817,256;18,1,5450,839,243;19,1,5451,839,243;20,1,5457,848,239;21,1,5458,848,239;22,1,5464,869,230;23,1,5465,869,230;24,1,5472,889,222;25,1,5472,889,222;26,1,5480,907,215;27,1,5481,907,215;28,1,5489,926,208;29,1,5489,926,208;30,1,5495,943,203;31,1,5496,943,203;32,1,5503,961,196;33,1,5504,961,196;34,1,5511,977,189;35,1,5522,992,183;36,1,5527,1008,176;37,1,5536,1022,169;38,1,5543,1033,162;39,1,5544,1033,162;40,1,5552,1045,155;41,1,5553,1045,155;42,1,5559,1056,148;43,1,5560,1056,148;44,1,5566,1066,142;45,1,5567,1066,142;46,1,5574,1074,135;47,1,5575,1074,135;48,1,5582,1083,129;49,1,5583,1083,129;50,1,5591,1090,123;51,1,5592,1090,123;52,1,5598,1098,117;53,1,5598,1098,117;54,1,5606,1104,112;55,1,5606,1104,112;56,1,5624,1111,106;57,1,5625,1117,102;58,1,5630,1123,98;59,1,5631,1123,98;60,1,5637,1126,96;61,1,5638,1126,96;62,1,5648,1130,92;63,1,5649,1130,92;64,1,5655,1135,89;65,1,5655,1135,89;66,1,5662,1140,87;67,1,5662,1140,87;68,1,5669,1143,85;69,1,5670,1143,85;70,1,5679,1146,83;71,1,5680,1146,83;72,1,5686,1149,81;73,1,5687,1149,81;74,1,5694,1151,80;75,1,5694,1151,80;76,1,5700,1154,78;77,1,5701,1154,78;78,1,5709,1157,77;79,1,5710,1157,77;80,1,5718,1159,75;81,1,5718,1159,75;82,1,5724,1162,74;83,1,5725,1162,74;84,1,5732,1164,72;85,1,5733,1164,72;86,1,5740,1167,70;87,1,5741,1167,70;88,1,5750,1169,69;89,1,5750,1169,69;90,1,5757,1171,67;91,1,5757,1171,67;92,1,5764,1174,66;93,1,5764,1174,66;94,1,5772,1176,64;95,1,5773,1176,64;96,1,5779,1179,63;97,1,5780,1179,63;98,1,5789,1181,61;99,1,5790,1181,61;205,3,6324,1256,56,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/myaccount-1,2,-94,-115,1,688232,32,0,0,0,688200,6324,0,1593778120368,110,17049,0,206,2841,1,0,6326,564474,0,83B56B14F8791DE4459B2C8598D943FC~-1~YAAQDex7XNWSJxBzAQAALCuUFARpiI+esYkf8lYdpjdLCeXpGHJ9+vnM6kEHHFvxY7T3yfNiygvtsQijxoB0yNuYl9wZotLwIwuoC9bI17FAhvUdRcyXL+l0Ge888pkyWFzJAH3M+C2Kp6Gd707Y65BbzbnblYpOVxKrIuiYQ77TdYjt9j85/zP5/tbklZ300b0M5/G4heKt5UOVncp1KtlqCNj9THUFEgo4ANkwaLOE1/K9PohfRbC90hyz7hzdxY3JGKGZuQ7uKN9p/ETblQXE3kwGtZDiPLgQ4nGGYzOT0iwZkVYPZOzRXBFruRu2U32RmNm4eOHksmzrFcYnCk212yM=~-1~-1~-1,32589,130,-829678606,26018161,PiZtE,72737,94-1,2,-94,-106,1,2-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,0,400,600,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,219249894-1,2,-94,-118,178607-1,2,-94,-121,;3;4;0"
                        % session.headers["User-Agent"]
                    }
                    data_bot5 = {
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
                    data_bot5bis = {
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
                    data_bot6 = {
                        "sensor_data": "7a74G7m23Vrp0o5c9179231.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392147,6416884,1440,900,1440,900,1440,338,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.772422311386,796893208442,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,-1,2,-94,-102,-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/checkout/address-1,2,-94,-115,1,32,32,0,0,0,0,818,0,1593786416884,25,17049,0,0,2841,0,0,819,0,0,6E7A8BB6ED1A8AB786D6512DC1ED4DB1~-1~YAAQNOx7XOEjEQ1zAQAA7L4SFQTDTAWYNVhRFWiIO+dsppVcEdLR8OJRi7qC9jIKE/1/yVQ8wwFceE79rVsV16vQTlhCjf6m3sJxsVFse1aLT8Yv483jeNiR/2r4xL9+9tp6dlT/UkgJ6G3LfubwSQFH5GdebR0fyceZWp6OQgmhi04d2gKJQSlBsjppZM5wME1IGtdl3qKsjsjZ2ldmGdUX4ElaslapCGdZy06b5toxd1dcPEVCdsbyhBXgjixLYPWH8h0790FxzL57Q5zQgWjavp8z48Y8xzcc8tH5gaRZNTzWZn6RRHh+tOdfwtmx23p/FogeywZifk8efVVAcZ11UMw=~-1~-1~-1,32721,333,-388728882,26018161,PiZtE,50292,83-1,2,-94,-106,9,1-1,2,-94,-119,0,200,0,0,200,0,0,200,800,2600,200,2400,2200,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,7796514045-1,2,-94,-118,82939-1,2,-94,-121,;2;4;0"
                        % session.headers["User-Agent"]
                    }
                    checkout = {
                        "address": {
                            "id": compte_objet_list[compte].id_adresse,
                            "salutation": "Mr",
                            "first_name": compte_objet_list[compte].prenom,
                            "last_name": compte_objet_list[compte].nom,
                            "zip": compte_objet_list[compte].codepostal,
                            "city": compte_objet_list[compte].ville,
                            "country_code": "FR",
                            "street": compte_objet_list[compte].adresse,
                            "additional": compte_objet_list[compte].complement_adresse,
                        }
                    }
                    session.headers["Accept"] = "*/*"
                    session.headers["Referer"] = "https://www.zalando.fr/myaccount"
                    session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                    session.post(bot_2, json=data_bot2, verify=False)
                    del session.headers["Content-Type"]
                    session.headers["Accept"] = "*/*"
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.get(bot_3, verify=False)
                    del session.headers["x-xsrf-token"]
                    session.headers["Accept"] = "*/*"
                    session.headers["Content-Type"] = "text/plain;charset=UTF-8"
                    session.headers["Referer"] = "https://www.zalando.fr/myaccount"
                    session.headers["Origin"] = "https://www.zalando.fr"
                    session.post(bot_4, json=data_bot4, verify=False)
                    session.post(bot_5, json=data_bot5, verify=False)
                    session.post(bot_5, json=data_bot5bis, verify=False)
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
                    session.post(bot_6, json=data_bot6, verify=False)
                    del session.headers["Content-Type"]
                    session.headers["Accept"] = "application/json"
                    session.headers["x-zalando-footer-mode"] = "desktop"
                    session.headers["x-zalando-checkout-app"] = "web"
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.headers["x-zalando-header-mode"] = "desktop"
                    session.post(url_panier_4, json=checkout, verify=False)

                    # Adresse de livraison
                    url_checkout_1 = (
                        "https://www.zalando.fr/api/checkout/address/%s/default"
                        % compte_objet_list[compte].id_adresse
                    )
                    url_bot_1 = "https://www.zalando.fr/resources/35692132da2028b315fc23b805e921"
                    url_checkout_2 = "https://www.zalando.fr/api/checkout/next-step"
                    data_checkout = {"isDefaultShipping": True}
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
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.headers["x-zalando-header-mode"] = "desktop"
                    session.post(url_checkout_1, json=data_checkout, verify=False)
                    del session.headers["x-xsrf-token"]
                    del session.headers["x-zalando-header-mode"]
                    del session.headers["x-zalando-checkout-app"]
                    del session.headers["x-zalando-footer-mode"]
                    del session.headers["Content-Type"]
                    del session.headers["Origin"]
                    session.headers["Accept"] = "*/*"
                    session.post(url_bot_1, json=bot, verify=False)
                    session.headers["Accept"] = "*/*"
                    session.headers["Referer"] = "https://www.zalando.fr/checkout/address"
                    session.headers["x-zalando-footer-mode"] = "desktop"
                    session.headers["x-zalando-checkout-app"] = "web"
                    session.headers["x-xsrf-token"] = cookies["frsx"]
                    session.headers["x-zalando-header-mode"] = "desktop"
                    reponse_livraison = session.get(url_checkout_2, verify=False)
                    pay_ini = json.loads(reponse_livraison.text)
                    url_pay_ini = str(pay_ini["url"])
                    del session.headers["x-zalando-footer-mode"]
                    del session.headers["x-zalando-checkout-app"]
                    del session.headers["x-xsrf-token"]
                    del session.headers["x-zalando-header-mode"]
                    session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                    session.headers["Host"] = "checkout.payment.zalando.com"
                    session.headers["Referer"] = "https://www.zalando.fr/checkout/address"
                    session.get(url_pay_ini, verify=False, allow_redirects=False)

                    # Paiement Partie 1
                    url_pay = "https://checkout.payment.zalando.com/selection"
                    url_pay_2 = "https://card-entry-service.zalando-payments.com/contexts/checkout/cards"
                    cb = {
                        "card_holder": "BALAYRE Alexis",
                        "pan": "4974 0182 7975 2162",
                        "cvv": "492",
                        "expiry_month": "8",
                        "expiry_year": "2022",
                        "options": {
                            "selected": [],
                            "not_selected": ["store_for_reuse"],
                        },
                    }
                    a = session.get(url_pay, verify=False, allow_redirects=False)
                    session_id = session.cookies["Session-ID"]
                    soup = BeautifulSoup(a.text, "html.parser")
                    objet_token_ini = soup.find(string=re.compile("config.accessToken"))
                    token_ini = objet_token_ini.split("'")
                    token = token_ini[1]
                    session.headers["Accept"] = "*/*"
                    session.headers["Origin"] = "https://card-entry-service.zalando-payments.com"
                    session.headers["Content-Type"] = "application/json"
                    session.headers["Host"] = "card-entry-service.zalando-payments.com"
                    session.headers["Authorization"] = "Bearer %s" % token
                    reponsepay = session.post(
                        url_pay_2, json=cb, verify=False, allow_redirects=False
                    )
                    reponsepaybis = json.loads(reponsepay.text)

                    # Paiement Partie 2
                    url_pay_3 = (
                        "https://checkout.payment.zalando.com/payment-method-selection-session/%s/selection?"
                        % session_id
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
                    session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                    b = session.get(url_pay_4, verify=False)
                    soupbis = BeautifulSoup(b.text, "html.parser")
                    dict_rep = soupbis.find("div", re.compile("data-props"))
                    print(dict_rep["data-props"])

                # Fermeture de la Session
                session.close()
                break

            # Gestion des exceptions
            except:
                pass

            finally:
                x = x + 1
                if x == (len(liste_proxys) + 1):
                    x = 0


comptes = creation_objet_compte()
proxies = proxy()
Paiement_Zalando(comptes, proxies)
