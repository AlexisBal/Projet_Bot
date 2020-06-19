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


def Configuration(compte_objet_list):
    # Comptage du nombre de compte présents dans la base de données
    nombrecompte = len(compte_objet_list)

    # Création d'un compte pour chaque objet "Compte" présent dans la base de données
    for x in range(0, nombrecompte):
        with requests.Session() as session:
            # Réglage des paramètres de la session
            session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
            headers = {
                'Host': 'www.zalando.fr',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/83.0.4103.97 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr-fr',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            session.headers.update(headers)

            # Connexion à la page d'accueil de Zalando
            url_home = "https://www.zalando.fr"
            home = session.get(url_home, verify=False)

            # Récupération des cookies de la session
            cookies = session.cookies.get_dict()

            # Modification du headers
            del session.headers['Upgrade-Insecure-Requests']

            # Connexion à la page de connexion
            url_get = "https://www.zalando.fr/login/?view=login"
            session.get(url_get, verify=False)

            # Envoie de requetes pour éviter les sécurités anti-bot
            url_get_1 = (
                    'https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=1' % home.headers["X-Flow-Id"]
            )
            session.get(url_get_1, verify=False)

            # Modification du headers
            session.headers["x-xsrf-token"] = cookies["frsx"]

            # Envoie de requetes pour éviter les sécurités anti-bot
            url_get_1 = (
                    'https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=3' % home.headers["X-Flow-Id"]
            )
            session.get(url_get_1, verify=False)

            # Modification du headers
            session.headers["Content-Type"] = "text/plain;charset=UTF-8"
            session.headers["Accept"] = "*/*"
            del session.headers["x-xsrf-token"]

            # Envoie de requetes pour éviter les sécurités anti-bot
            sensor_data = {
                "sensor_data": "7a74G7m23Vrp0o5c9175981.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391850,1658105,1440,814,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.294628793147,796290829052.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,617,939,3;1,1,622,939,3;2,1,624,946,6;3,1,633,955,10;4,1,635,955,10;5,1,639,965,15;6,1,639,965,15;7,1,647,976,19;8,1,648,976,19;9,1,657,991,24;10,1,657,991,24;11,1,663,1008,28;12,1,665,1008,28;13,1,672,1025,33;14,1,674,1025,33;15,1,679,1056,40;16,1,680,1056,40;17,1,688,1076,44;18,1,689,1076,44;19,1,696,1087,46;20,1,697,1087,46;21,1,703,1109,51;22,1,703,1109,51;23,1,712,1129,55;24,1,713,1129,55;25,1,720,1148,59;26,1,722,1148,59;27,1,727,1166,66;28,1,728,1166,66;29,1,736,1180,71;30,1,736,1180,71;31,1,744,1196,77;32,1,744,1196,77;33,1,753,1212,85;34,1,754,1212,85;35,1,760,1226,94;36,1,760,1226,94;37,1,769,1236,102;38,1,770,1236,102;39,1,775,1249,112;40,1,776,1249,112;41,1,787,1258,121;42,1,787,1258,121;43,1,791,1265,130;44,1,792,1265,130;45,1,802,1273,138;46,1,802,1273,138;47,1,808,1279,147;48,1,809,1279,147;49,1,818,1283,154;50,1,819,1283,154;51,1,825,1284,157;52,1,826,1284,157;53,1,832,1290,168;54,1,835,1290,168;55,1,840,1291,176;56,1,841,1291,176;57,1,850,1292,183;58,1,861,1293,190;59,1,864,1293,198;60,1,865,1293,198;61,1,873,1293,206;62,1,873,1293,206;63,1,882,1293,213;64,1,883,1293,213;65,1,889,1290,220;66,1,892,1290,220;67,1,897,1284,227;68,1,898,1284,227;69,1,908,1270,241;70,1,915,1255,250;71,1,918,1255,250;72,1,921,1239,258;73,1,922,1239,258;74,1,929,1216,267;75,1,929,1216,267;76,1,937,1190,274;77,1,938,1190,274;78,1,946,1162,282;79,1,947,1162,282;80,1,953,1130,287;81,1,954,1130,287;82,1,962,1096,293;83,1,962,1096,293;84,1,970,1061,296;85,1,970,1061,296;86,1,978,1022,298;87,1,979,1022,298;88,1,986,987,300;89,1,986,987,300;90,1,994,948,302;91,1,994,948,302;92,1,1005,917,304;93,1,1012,904,304;94,1,1013,904,304;95,1,1019,876,304;96,1,1020,876,304;97,1,1026,853,304;98,1,1026,853,304;99,1,1034,847,304;217,3,2758,739,188,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,329;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,1,220704,32,0,0,0,220672,2758,0,1592581658105,16,17036,0,218,2839,1,0,2759,84978,0,544D198E0F1B1CB2C191909E5A431D4A~-1~YAAQI5HdWON0Wa1yAQAAIJhDzQSs2DaHi3VWlNasxDo6Ll1h+oPs9Arg4f8DmMXtm7anSErvR5n9n2pO+UMTG/IVcwHpfi9Wi/ZDhjSRktF/01XyTRMeCqjaeI0/prETWeQeJkJTEUT7q7Lp9d7aH30hB2IihOsBdiBvSwqh9UbB/o6n5EgkZgrD6PRQwpDic6VG2QZ9k5czxOMXhm2LdiLG+/uKxYYkLkarftjuMKCgYsG+w4No1YL0WTXRpGFiEoZrP1PWYltbpu2Q2NBlWPFovn4VW0knih51voTZCUXpt52d7hsTVn2TdnQglcPVYqHyg6Goubm3of/HY6EI/ryzWoo=~-1~-1~-1,32678,285,1682362911,26018161,NVVN,124,-1-1,2,-94,-106,1,2-1,2,-94,-119,200,2200,0,0,0,0,0,0,0,200,0,3000,2600,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,44769069-1,2,-94,-118,176741-1,2,-94,-121,;1;4;0"
            }
            url_post1 = "https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b"
            session.post(url_post1, json=sensor_data, verify=False)

            sensor_data_bis = {
                "sensor_data": "7a74G7m23Vrp0o5c9175981.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391850,1658105,1440,814,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.347127751173,796290829052.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,6662,undefined,0,0,1103,0;1,2,6677,undefined,0,0,1103,0;2,1,6716,undefined,0,0,1103,0;3,2,6726,undefined,0,0,1103,0;4,1,7287,13,0,0,1466;-1,2,-94,-110,0,1,617,939,3;1,1,622,939,3;2,1,624,946,6;3,1,633,955,10;4,1,635,955,10;5,1,639,965,15;6,1,639,965,15;7,1,647,976,19;8,1,648,976,19;9,1,657,991,24;10,1,657,991,24;11,1,663,1008,28;12,1,665,1008,28;13,1,672,1025,33;14,1,674,1025,33;15,1,679,1056,40;16,1,680,1056,40;17,1,688,1076,44;18,1,689,1076,44;19,1,696,1087,46;20,1,697,1087,46;21,1,703,1109,51;22,1,703,1109,51;23,1,712,1129,55;24,1,713,1129,55;25,1,720,1148,59;26,1,722,1148,59;27,1,727,1166,66;28,1,728,1166,66;29,1,736,1180,71;30,1,736,1180,71;31,1,744,1196,77;32,1,744,1196,77;33,1,753,1212,85;34,1,754,1212,85;35,1,760,1226,94;36,1,760,1226,94;37,1,769,1236,102;38,1,770,1236,102;39,1,775,1249,112;40,1,776,1249,112;41,1,787,1258,121;42,1,787,1258,121;43,1,791,1265,130;44,1,792,1265,130;45,1,802,1273,138;46,1,802,1273,138;47,1,808,1279,147;48,1,809,1279,147;49,1,818,1283,154;50,1,819,1283,154;51,1,825,1284,157;52,1,826,1284,157;53,1,832,1290,168;54,1,835,1290,168;55,1,840,1291,176;56,1,841,1291,176;57,1,850,1292,183;58,1,861,1293,190;59,1,864,1293,198;60,1,865,1293,198;61,1,873,1293,206;62,1,873,1293,206;63,1,882,1293,213;64,1,883,1293,213;65,1,889,1290,220;66,1,892,1290,220;67,1,897,1284,227;68,1,898,1284,227;69,1,908,1270,241;70,1,915,1255,250;71,1,918,1255,250;72,1,921,1239,258;73,1,922,1239,258;74,1,929,1216,267;75,1,929,1216,267;76,1,937,1190,274;77,1,938,1190,274;78,1,946,1162,282;79,1,947,1162,282;80,1,953,1130,287;81,1,954,1130,287;82,1,962,1096,293;83,1,962,1096,293;84,1,970,1061,296;85,1,970,1061,296;86,1,978,1022,298;87,1,979,1022,298;88,1,986,987,300;89,1,986,987,300;90,1,994,948,302;91,1,994,948,302;92,1,1005,917,304;93,1,1012,904,304;94,1,1013,904,304;95,1,1019,876,304;96,1,1020,876,304;97,1,1026,853,304;98,1,1026,853,304;99,1,1034,847,304;217,3,2758,739,188,1103;218,4,2893,739,188,1103;219,2,2893,739,188,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,329;2,4473;3,6695;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,NaN,228787,32,0,0,0,NaN,7287,0,1592581658105,16,17036,5,234,2839,2,0,7289,124832,0,544D198E0F1B1CB2C191909E5A431D4A~-1~YAAQI5HdWB11Wa1yAQAA5qBDzQSG6Pv/OSeYlJZ+5TdSTmLptNh6airlP5V/lfl0qZibNHdiWQexNK07iCtntsNCWGQHPYxIdWr4OhMwJ0i9iCooHr4ymTZvJOiehLUCEf20hGguVIpe5vO+tl8HNMUY7PGyvGkSCQeUF3LvyMptTNSG8CSY0BBnfap9mu2tyNqJrjG8Xea/jsk0hclFwXoOFGYut6G8PG3iNaLmer5R0671/1KuX41tQnpCg/f9510oCGeGVN2f1b3jSey1Ob7DjYTE+aUd5c5tuJsTW5eeK7Ce+eI43fC+QwqaWJz5TYZnz0IAjAGkEtDAFH4keWDUEZQ=~-1~-1~-1,32009,285,1682362911,26018161,NVVN,124,-1-1,2,-94,-106,3,3-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,0,600,200,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,44769069-1,2,-94,-118,188004-1,2,-94,-121,;2;4;0"
            }
            url_post1_bis = 'https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b'
            session.post(url_post1_bis, json=sensor_data_bis, verify=False)

            # Modification du headers
            session.headers["Accept"] = "application/json"
            session.headers["x-zalando-request-uri"] = "/login/?view=login"
            session.headers["x-zalando-render-page-uri"] = "/login/?view=login"
            session.headers["x-xsrf-token"] = cookies["frsx"]
            session.headers["x-flow-id"] = home.headers["X-Flow-Id"]
            session.headers["x-zalando-client-id"] = cookies["Zalando-Client-Id"]
            session.headers["Content-Type"] = "application/json"

            # Connexion au compte Zalando
            url_connexion_get = "https://www.zalando.fr/api/reef/login/schema"
            url_connexion_post2 = "https://www.zalando.fr/api/reef/login"
            identifiants = {
                'username': compte_objet_list[x].email,
                'password': compte_objet_list[x].motdepasse,
                'wnaMode': 'shop'
            }
            session.get(url_connexion_get, verify=False)
            session.headers["Origin"] = "https://www.zalando.fr"
            session.post(url_connexion_post2, json=identifiants, verify=False)

            # Affichage du profil
            url_profil = 'https://www.zalando.fr/myaccount'
            session.get(url_profil, verify=False)

            # Configuration du profil : Ajout d'un numéro de téléphone
            url_informations_get = 'https://www.zalando.fr/myaccount/details'
            url_informations_post = 'https://www.zalando.fr/api/user-account-details/details'
            informations = {
                'first_name': compte_objet_list[x].prenom,
                'last_name': compte_objet_list[x].nom,
                'fashion_category': [],
                'birth_date': None,
                'phone': compte_objet_list[x].telephone
            }
            session.get(url_informations_get, verify=False)
            session.post(url_informations_post, json=informations, verify=False)

            # Configuration du profil : Ajout d'une adresse
            url_profil_get = 'https://www.zalando.fr/myaccount/addresses'
            url_profil_post = 'https://www.zalando.fr/api/user-account-address/addresses'
            adresse = {
                "type": "HomeAddress",
                "city": compte_objet_list[x].ville,
                "countryCode": "FR",
                "firstname": compte_objet_list[x].prenom,
                "lastname": compte_objet_list[x].nom,
                "street": compte_objet_list[x].adresse,
                "additional": compte_objet_list[x].complement_adresse,
                "gender": compte_objet_list[x].civilite,
                "defaultBilling": True,
                "defaultShipping": True,
                "zip": compte_objet_list[x].codepostal
            }
            session.get(url_profil_get, verify=False)
            session.post(url_profil_post, json=adresse, verify=False)


comptes = creation_objet_compte()
Configuration(comptes)
