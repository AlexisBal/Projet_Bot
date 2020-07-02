import json

import requests
import urllib3
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


def Paiement_Zalando(compte_objet_list):

    liste_proxys = [
        '195.154.42.163'
    ]

    # Comptage du nombre de comptes présents dans la base de données
    nombrecompte = len(compte_objet_list)

    # Achat du produit pour chaque objet "Compte" présent dans la base de données
    for compte in range(0, nombrecompte):
        x = 0
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
                del session.cookies['mpulseinject']
                session.cookies['mpulseinject'] = 'false'

                # Connexion à la page de connexion
                url_connexion_1 = "https://www.zalando.fr/login/?view=login"
                login = session.get(url_connexion_1, verify=False)

                # Requetes anti-bot
                url_bot = 'https://www.zalando.fr/resources/35692132da2028b315fc23b805e921'
                data1 = {
                    'sensor_data': '7a74G7m23Vrp0o5c9178011.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392127,8356226,1440,900,1440,900,1440,513,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.903443507451,796854178112.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,375,887,490;1,1,633,804,295;2,1,682,803,292;3,1,825,803,292;4,1,826,700,270;5,1,831,696,270;6,1,891,691,270;7,1,906,678,278;8,1,912,676,279;9,1,917,676,280;10,1,927,674,280;11,1,954,674,281;12,1,969,672,281;13,1,999,671,281;14,3,1046,671,281,1466;15,1,1090,671,281;16,4,1093,671,281,1466;17,2,1119,671,281,1466;18,1,1410,671,281;19,1,14210,654,237;20,1,14230,654,237;21,1,14231,655,236;22,1,14234,657,236;23,1,14235,657,236;24,1,14242,659,236;25,1,14242,659,236;26,1,14249,662,236;27,1,14250,662,236;28,1,14257,664,236;29,1,14258,664,236;30,1,14267,671,236;31,1,14267,671,236;32,1,14276,677,236;33,1,14282,683,236;34,1,14283,683,236;35,1,14289,688,236;36,1,14290,688,236;37,1,14299,694,236;38,1,14300,694,236;39,1,14305,699,238;40,1,14306,699,238;41,1,14314,707,240;42,1,14315,707,240;43,1,14321,712,243;44,1,14321,712,243;45,1,14329,718,247;46,1,14329,718,247;47,1,14337,725,253;48,1,14338,725,253;49,1,14344,731,259;50,1,14345,731,259;51,1,14353,737,267;52,1,14354,737,267;53,1,14361,742,275;54,1,14362,742,275;55,1,14369,746,284;56,1,14370,746,284;57,1,14376,748,292;58,1,14376,748,292;59,1,14384,748,297;60,1,14385,748,297;61,1,14392,749,304;62,1,14393,749,304;63,1,14401,749,311;64,1,14401,749,311;65,1,14408,749,315;66,1,14408,749,315;67,1,14416,749,319;68,1,14416,749,319;69,1,14423,749,322;70,1,14424,749,322;71,1,14431,747,323;72,1,14432,747,323;73,1,14439,745,324;74,1,14440,745,324;75,1,14447,743,325;76,1,14447,743,325;77,1,14455,738,325;78,1,14455,738,325;79,1,14463,734,325;80,1,14464,734,325;81,1,14470,730,323;82,1,14471,730,323;83,1,14478,724,317;84,1,14479,724,317;85,1,14486,718,311;86,1,14486,718,311;87,1,14494,709,303;88,1,14495,709,303;89,1,14502,702,295;90,1,14503,702,295;91,1,14511,692,284;92,1,14512,692,284;93,1,14518,689,280;94,1,14519,689,280;95,1,14525,683,271;96,1,14526,683,271;97,1,14534,678,265;98,1,14534,678,265;99,1,14543,675,260;100,1,14544,675,260;101,1,14550,673,256;102,1,14551,673,256;186,3,15449,606,280,1466;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,1003;0,1740;2,1939;1,13685;3,14207;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,1,1349798,32,0,0,0,1349766,15449,0,1593708356225,40,17049,0,187,2841,3,0,15451,1241425,0,F47B7ACD62E06613840912E4B0FF4D34~-1~YAAQDex7XHjKERBzAQAA4adrEAQVKC4G5DWTwiDbd99QE0TG/CZ/X7/0id5k5Wx002o9cnpldjg2VaUQLUT7xhQ16xAXRWtpmFjanwsvOKrPuOhteppYDYFUsR7dmXHIQ068VDYGjPmJ3s1QezU6/OK7qU/7z0Xzvw9HMdvSPwXK3yDBL3Xn5VCqcupRCesCB0vUZ37uYYJJv8rx1GdciMHQXlb1zg7waQUUQjLQM7oZUeI7QqqXoiPdQMPP/FSWoCe1fGoDA7+05Ur96s4rsR99wfKdfjv3wrPr71c+IetpJ2aONaAL0HHVhSeEeTzNST4NF0JAIB+KtncIoMXcQToOfVY7~-1~-1~-1,32020,851,1050434953,26018161,PiZtE,53346,121-1,2,-94,-106,1,3-1,2,-94,-119,200,0,0,0,0,0,0,0,200,0,0,600,200,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,25068636-1,2,-94,-118,188046-1,2,-94,-121,;4;10;0' % session.headers["User-Agent"]
                }
                data2 = {
                    'sensor_data': '7a74G7m23Vrp0o5c9178011.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392127,8356226,1440,900,1440,900,1440,513,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.883221105441,796854178112.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,15627,91,0,2,1466;1,1,15699,86,0,2,1466;2,3,15701,118,0,2,1466;3,2,15848,-2,0,0,1466;-1,2,-94,-110,0,1,375,887,490;1,1,633,804,295;2,1,682,803,292;3,1,825,803,292;4,1,826,700,270;5,1,831,696,270;6,1,891,691,270;7,1,906,678,278;8,1,912,676,279;9,1,917,676,280;10,1,927,674,280;11,1,954,674,281;12,1,969,672,281;13,1,999,671,281;14,3,1046,671,281,1466;15,1,1090,671,281;16,4,1093,671,281,1466;17,2,1119,671,281,1466;18,1,1410,671,281;19,1,14210,654,237;20,1,14230,654,237;21,1,14231,655,236;22,1,14234,657,236;23,1,14235,657,236;24,1,14242,659,236;25,1,14242,659,236;26,1,14249,662,236;27,1,14250,662,236;28,1,14257,664,236;29,1,14258,664,236;30,1,14267,671,236;31,1,14267,671,236;32,1,14276,677,236;33,1,14282,683,236;34,1,14283,683,236;35,1,14289,688,236;36,1,14290,688,236;37,1,14299,694,236;38,1,14300,694,236;39,1,14305,699,238;40,1,14306,699,238;41,1,14314,707,240;42,1,14315,707,240;43,1,14321,712,243;44,1,14321,712,243;45,1,14329,718,247;46,1,14329,718,247;47,1,14337,725,253;48,1,14338,725,253;49,1,14344,731,259;50,1,14345,731,259;51,1,14353,737,267;52,1,14354,737,267;53,1,14361,742,275;54,1,14362,742,275;55,1,14369,746,284;56,1,14370,746,284;57,1,14376,748,292;58,1,14376,748,292;59,1,14384,748,297;60,1,14385,748,297;61,1,14392,749,304;62,1,14393,749,304;63,1,14401,749,311;64,1,14401,749,311;65,1,14408,749,315;66,1,14408,749,315;67,1,14416,749,319;68,1,14416,749,319;69,1,14423,749,322;70,1,14424,749,322;71,1,14431,747,323;72,1,14432,747,323;73,1,14439,745,324;74,1,14440,745,324;75,1,14447,743,325;76,1,14447,743,325;77,1,14455,738,325;78,1,14455,738,325;79,1,14463,734,325;80,1,14464,734,325;81,1,14470,730,323;82,1,14471,730,323;83,1,14478,724,317;84,1,14479,724,317;85,1,14486,718,311;86,1,14486,718,311;87,1,14494,709,303;88,1,14495,709,303;89,1,14502,702,295;90,1,14503,702,295;91,1,14511,692,284;92,1,14512,692,284;93,1,14518,689,280;94,1,14519,689,280;95,1,14525,683,271;96,1,14526,683,271;97,1,14534,678,265;98,1,14534,678,265;99,1,14543,675,260;100,1,14544,675,260;101,1,14550,673,256;102,1,14551,673,256;186,3,15449,606,280,1466;188,4,15550,606,280,1466;189,2,15556,606,280,1466;313,3,16356,666,346,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,1003;0,1740;2,1939;1,13685;3,14207;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,69052,1400743,32,0,0,0,1469762,16356,0,1593708356225,40,17049,4,314,2841,5,0,16358,1351762,0,F47B7ACD62E06613840912E4B0FF4D34~-1~YAAQDex7XLvLERBzAQAAFeBrEATcL5sl0zgV7hXa6IvZO2QT3hLEasdPcX9ezDCTjChowIfAFvx+Q+T7cQAWoFaW8RNof/+Z2OvHog5F8Td4/XBLFqEK9M3PsonioZ47Sx2j75amRQH4X/7OhwhX40SICYOPfBxaCcv4fZNwPI7TplOsJMIljBeOdTTKwCF2Cffu4oo1vqAqpFGWNzbSdqTZ18b+ZK+uYAbdraJtzi336EFKc9KGa2kTrIrp+y5pM2ZCk8FvVv288O43kXM35qnl+Egs1SA3YM4mU/I0rPeJMjgeOp95XiDDQUbeRDMFiCykPrq5JXhcqTMNxIHi0sXXBg3t~-1~-1~-1,31936,851,1050434953,26018161,PiZtE,23794,107-1,2,-94,-106,1,4-1,2,-94,-119,200,0,0,0,0,0,0,0,200,0,0,600,200,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,25068636-1,2,-94,-118,196289-1,2,-94,-121,;2;10;0' % session.headers["User-Agent"]
                }
                session.headers["Accept"] = "*/*"
                session.headers["Content-Type"] = 'text/plain;charset=UTF-8'
                session.headers["Origin"] = 'https://www.zalando.fr'
                session.headers["Referer"] = 'https://www.zalando.fr/login/?view=login'
                session.post(url_bot, json=data1, verify=False)
                session.post(url_bot, json=data2, verify=False)
                del session.headers["Content-Type"]
                del session.headers["Origin"]
                del session.headers["Referer"]

                # Connexion au compte
                url_connexion_2 = 'https://www.zalando.fr/api/reef/login/schema'
                url_connexion_3 = 'https://www.zalando.fr/api/reef/login'
                url_compte = 'https://www.zalando.fr/myaccount/'
                identifiants = {
                    "username": compte_objet_list[compte].email,
                    "password": compte_objet_list[compte].motdepasse,
                    "wnaMode": "shop"
                }
                session.headers["x-xsrf-token"] = cookies["frsx"]
                session.headers["x-zalando-client-id"] = cookies["Zalando-Client-Id"]
                session.headers["x-zalando-render-page-uri"] = "/login/?view=login"
                session.headers["x-zalando-request-uri"] = "/login/?view=login"
                session.headers["x-flow-id"] = login.headers["X-Zalando-Child-Request-Id"]
                session.headers["Content-Type"] = "application/json"
                session.headers["Accept"] = "application/json"
                session.headers['Referer'] = 'https://www.zalando.fr/login/?view=login'
                session.get(url_connexion_2, verify=False)
                session.headers["Origin"] = "https://www.zalando.fr"
                session.headers['Content-Length'] = '76'
                session.post(url_connexion_3, json=identifiants, verify=False)
                del session.headers["x-xsrf-token"]
                del session.headers["x-zalando-client-id"]
                del session.headers["x-zalando-render-page-uri"]
                del session.headers["x-zalando-request-uri"]
                del session.headers["x-flow-id"]
                del session.headers['Content-Length']
                session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                session.get(url_compte, verify=False)

                # Validation du panier et checkout
                url_panier_1 = 'https://www.zalando.fr/cart/'
                url_panier_2 = 'https://www.zalando.fr/checkout/confirm'
                url_panier_3 = 'https://www.zalando.fr/checkout/address'
                url_panier_4 = 'https://www.zalando.fr/api/checkout/search-pickup-points-by-address'
                checkout = {
                    'address': {
                        'id': compte_objet_list[compte].id_adresse,
                        'salutation': 'Mr',
                        'first_name': compte_objet_list[compte].prenom,
                        'last_name': compte_objet_list[compte].nom,
                        'zip': compte_objet_list[compte].codepostal,
                        'city': compte_objet_list[compte].ville,
                        'country_code': 'FR',
                        'street': compte_objet_list[compte].adresse,
                        'additional': compte_objet_list[compte].complement_adresse
                    }
                }
                session.headers["Referer"] = "https://www.zalando.fr/myaccount/"
                session.get(url_panier_1, verify=False)
                session.headers["Referer"] = "https://www.zalando.fr/cart"
                session.get(url_panier_2, verify=False)
                session.get(url_panier_3, verify=False)
                session.post(url_panier_4, json=checkout, verify=False)

                # Requetes anti-bot
                url_botbis = 'https://www.zalando.fr/resources/35692132da2028b315fc23b805e921'
                data1bis = {
                    'sensor_data': '7a74G7m23Vrp0o5c9178851.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392105,5498227,1440,900,1440,900,1440,525,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.273584619136,796807749113.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,-1,2,-94,-102,-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/checkout/address-1,2,-94,-115,1,32,32,0,0,0,0,745,0,1593615498227,29,17048,0,0,2841,0,0,746,0,0,EBC16C32565FCC85852E046D0E13B03E~-1~YAAQLux7XBkXm/JyAQAASr3iCgSs+3joFRndDLyPCe5cbv0A8AknzYLWTBk244SQmgBCzZN6cq21YGyWvCsv4nKgaED8Go0IiEuEhdhY4sKY2R5HRrNnxyaD5skYqQwq0ffv2FqM+HpL++ZzD9+NS5B+ymWwkdDuo4kCbgKB8tN4E0deTM8Z7AABSlVxPSxnOga/rvkVc/GRBThbODhSxoDEXldjaulI3knTbe+2m4XYaLkTOljAzBUWnCC+a/B5T6zDjwUwQcKWlYaFc2qUFmt5WSHgX6pFTF7FkKGdN4ErI87HLQtAPdYgVgrrzYZ0BA9FMCYQzxGJgDbflRH+W+mjMu0=~-1~-1~-1,32365,97,-378114461,26018161,PiZtE,92130,68-1,2,-94,-106,9,1-1,2,-94,-119,200,0,200,0,0,200,0,0,0,200,200,2200,800,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,148451781-1,2,-94,-118,82368-1,2,-94,-121,;1;7;0' % session.headers["User-Agent"]
                }
                data2bis = {
                    'sensor_data': '7a74G7m23Vrp0o5c9178851.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392105,5498227,1440,900,1440,900,1440,525,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.273584619136,796807749113.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,-1,2,-94,-102,-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/checkout/address-1,2,-94,-115,1,32,32,0,0,0,0,745,0,1593615498227,29,17048,0,0,2841,0,0,746,0,0,EBC16C32565FCC85852E046D0E13B03E~-1~YAAQLux7XBkXm/JyAQAASr3iCgSs+3joFRndDLyPCe5cbv0A8AknzYLWTBk244SQmgBCzZN6cq21YGyWvCsv4nKgaED8Go0IiEuEhdhY4sKY2R5HRrNnxyaD5skYqQwq0ffv2FqM+HpL++ZzD9+NS5B+ymWwkdDuo4kCbgKB8tN4E0deTM8Z7AABSlVxPSxnOga/rvkVc/GRBThbODhSxoDEXldjaulI3knTbe+2m4XYaLkTOljAzBUWnCC+a/B5T6zDjwUwQcKWlYaFc2qUFmt5WSHgX6pFTF7FkKGdN4ErI87HLQtAPdYgVgrrzYZ0BA9FMCYQzxGJgDbflRH+W+mjMu0=~-1~-1~-1,32365,97,-378114461,26018161,PiZtE,92130,68-1,2,-94,-106,9,1-1,2,-94,-119,200,0,200,0,0,200,0,0,0,200,200,2200,800,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,148451781-1,2,-94,-118,82368-1,2,-94,-121,;1;7;0' % session.headers["User-Agent"]
                }
                session.headers["Accept"] = "*/*"
                session.headers["Content-Type"] = 'text/plain;charset=UTF-8'
                session.headers["Origin"] = 'https://www.zalando.fr'
                session.headers["Referer"] = 'https://www.zalando.fr/login/?view=login'
                session.post(url_botbis, json=data1bis, verify=False)
                session.post(url_botbis, json=data2bis, verify=False)
                del session.headers["Content-Type"]
                del session.headers["Origin"]
                del session.headers["Referer"]
                del session.headers["Content-Length"]

                # Adresse de livraison
                url_checkout_1 = 'https://www.zalando.fr/api/checkout/address/%s/default' % compte_objet_list[compte].id_adresse
                url_checkout_2 = 'https://www.zalando.fr/api/checkout/next-step'
                data_checkout = {
                    'isDefaultShipping': True
                }
                session.headers["Accept"] = "application/json"
                session.headers['Content-Type'] = 'application/json'
                session.headers['Origin'] = 'https://www.zalando.fr'
                session.headers['Referer'] = 'https://www.zalando.fr/checkout/address'
                session.headers['x-zalando-footer-mode'] = 'desktop'
                session.headers['x-zalando-checkout-app'] = 'web'
                session.headers['x-xsrf-token'] = cookies["frsx"]
                session.headers['x-zalando-header-mode'] = 'desktop'
                session.post(url_checkout_1, json=data_checkout, verify=False)
                session.get(url_checkout_2, verify=False)
                del session.headers['x-zalando-footer-mode']
                del session.headers['x-zalando-checkout-app']
                del session.headers['x-xsrf-token']
                del session.headers['x-zalando-header-mode']

                # Mode de Paiement
                url_pay = 'https://checkout.payment.zalando.com/selection?show=true'
                url_pay_2 = 'https://card-entry-service.zalando-payments.com/contexts/checkout/cards'
                cb = {
                    "card_holder": "alexis balayre",
                    "pan": "4974 0182 7975 2162 ",
                    "cvv": "492",
                    "expiry_month": "8",
                    "expiry_year": "2022",
                    "options": {
                        "selected": ["store_for_reuse"],
                        "not_selected": []
                    }
                }
                session.headers['Host'] = 'checkout.payment.zalando.com'
                a = session.get(url_pay, verify=False)
                print(a.status_code)

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
Paiement_Zalando(comptes)