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

                    # Requetes anti-bot
                    url_bot = 'https://www.zalando.fr/resources/35692132da2028b315fc23b805e921'
                    data1 = {
                        'sensor_data': '7a74G7m23Vrp0o5c9178731.6-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392103,7358435,1920,1057,1920,1080,1920,342,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.12281762661,796803679217,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,272,895,5;1,1,314,854,54;2,1,315,621,213;3,1,321,596,226;4,1,329,497,274;5,1,338,472,287;6,1,347,417,311;7,1,386,367,334;8,1,3079,411,336;9,1,3079,411,336;10,1,3085,470,324;11,1,3094,532,312;12,1,3101,561,309;13,1,3110,625,299;14,1,3120,684,294;15,1,3125,739,290;16,1,3133,789,286;17,1,3141,832,283;18,1,3151,847,283;19,1,3157,875,282;20,1,3165,900,280;21,1,3174,906,279;22,1,3185,919,278;23,1,3190,927,277;24,1,3198,933,277;25,1,3206,936,277;26,1,3215,938,276;27,1,3222,939,276;28,1,3230,939,276;29,1,3239,940,276;30,1,3249,940,276;31,1,3255,940,275;32,1,3262,940,275;33,1,3270,940,275;34,1,3280,936,273;35,1,3288,933,272;36,1,3296,929,270;37,1,3303,923,268;38,1,3313,916,264;39,1,3319,908,261;40,1,3328,900,258;41,1,3334,892,254;42,1,3346,885,250;43,1,3352,881,249;44,1,3360,875,245;45,1,3368,869,242;46,1,3377,864,239;47,1,3383,861,237;48,1,3392,858,235;49,1,3400,855,232;50,1,3409,853,230;51,1,3417,851,229;52,1,3424,850,227;53,1,3434,848,226;54,1,3441,847,224;55,1,3451,846,223;56,1,3457,845,222;57,1,3464,844,221;58,1,3472,843,220;59,1,3484,842,219;60,1,3488,842,218;61,1,3499,841,217;62,1,3506,840,217;63,1,3514,840,216;64,1,3521,840,215;65,1,3530,839,215;66,1,3538,838,214;67,1,3548,838,213;68,1,3554,838,213;69,1,3561,838,213;70,1,3571,837,212;71,1,3581,837,212;72,1,3585,837,212;73,1,3613,837,212;74,1,3654,837,212;75,1,3667,837,211;76,1,3686,837,211;77,1,3699,837,211;78,1,3726,837,211;79,1,3800,837,210;80,1,3896,837,211;81,1,3903,837,211;82,1,3908,837,211;83,1,6182,837,211;84,1,6189,837,209;85,1,6196,837,207;86,1,6204,837,206;87,1,6212,837,205;88,1,6223,837,204;89,1,6228,838,203;90,1,6235,838,202;91,1,6245,838,200;92,1,6254,838,199;93,1,6260,838,198;94,1,6269,838,197;95,1,6276,838,196;96,1,6286,838,195;97,1,6292,838,195;98,3,6312,838,195,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,1,465928,32,0,0,0,465896,6313,0,1593607358434,14,17047,0,99,2841,1,0,6314,356360,0,2CC3585D5F5E58B90C58E6D6DE13E22D~-1~YAAQO5HdWKgCGudyAQAA+olmCgQr7KfoRHodp8Batp157rgT6Qj7ulzDylDXMRIK0B9zhx5gqbZy18i5+msE1Xo08HmLbo0UE8c+j8S4M6E1VRjLhqNYpXIInPiZ2KeF41VLbM0tvQFpToVMglbB8n8wbAK0GFxvQ/SoNZDnlTnXeLk4TwcDL0snfqZb0Gl+KNfKYNWt1jiB6VsAxGahpYWGcxTqD8GsWPVGBxooePGKyk+t7TdNyTU0noF+/71TTL4io91ooFzoMy3u+fQFWlcfpK9pmENAN9u1SKzlZNhi4/XVIA9dMmhzVPtIFG2qAGxDF4S7fRqTb9vT8XnFwgrmmoc=~-1~-1~-1,32566,130,-829678606,26018161,PiZtE,46791,25-1,2,-94,-106,1,2-1,2,-94,-119,200,0,0,0,0,0,0,200,0,0,0,200,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,993389013-1,2,-94,-118,176685-1,2,-94,-121,;2;10;0'
                    }
                    data2 = {
                        'sensor_data': '7a74G7m23Vrp0o5c9178731.6-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392103,7358435,1920,1057,1920,1080,1920,342,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.364278565182,796803679217,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,8891,undefined,0,0,1103,0;1,2,8909,undefined,0,0,1103,0;2,1,8941,undefined,0,0,1103,0;3,2,8948,undefined,0,0,1103,0;-1,2,-94,-110,0,1,272,895,5;1,1,314,854,54;2,1,315,621,213;3,1,321,596,226;4,1,329,497,274;5,1,338,472,287;6,1,347,417,311;7,1,386,367,334;8,1,3079,411,336;9,1,3079,411,336;10,1,3085,470,324;11,1,3094,532,312;12,1,3101,561,309;13,1,3110,625,299;14,1,3120,684,294;15,1,3125,739,290;16,1,3133,789,286;17,1,3141,832,283;18,1,3151,847,283;19,1,3157,875,282;20,1,3165,900,280;21,1,3174,906,279;22,1,3185,919,278;23,1,3190,927,277;24,1,3198,933,277;25,1,3206,936,277;26,1,3215,938,276;27,1,3222,939,276;28,1,3230,939,276;29,1,3239,940,276;30,1,3249,940,276;31,1,3255,940,275;32,1,3262,940,275;33,1,3270,940,275;34,1,3280,936,273;35,1,3288,933,272;36,1,3296,929,270;37,1,3303,923,268;38,1,3313,916,264;39,1,3319,908,261;40,1,3328,900,258;41,1,3334,892,254;42,1,3346,885,250;43,1,3352,881,249;44,1,3360,875,245;45,1,3368,869,242;46,1,3377,864,239;47,1,3383,861,237;48,1,3392,858,235;49,1,3400,855,232;50,1,3409,853,230;51,1,3417,851,229;52,1,3424,850,227;53,1,3434,848,226;54,1,3441,847,224;55,1,3451,846,223;56,1,3457,845,222;57,1,3464,844,221;58,1,3472,843,220;59,1,3484,842,219;60,1,3488,842,218;61,1,3499,841,217;62,1,3506,840,217;63,1,3514,840,216;64,1,3521,840,215;65,1,3530,839,215;66,1,3538,838,214;67,1,3548,838,213;68,1,3554,838,213;69,1,3561,838,213;70,1,3571,837,212;71,1,3581,837,212;72,1,3585,837,212;73,1,3613,837,212;74,1,3654,837,212;75,1,3667,837,211;76,1,3686,837,211;77,1,3699,837,211;78,1,3726,837,211;79,1,3800,837,210;80,1,3896,837,211;81,1,3903,837,211;82,1,3908,837,211;83,1,6182,837,211;84,1,6189,837,209;85,1,6196,837,207;86,1,6204,837,206;87,1,6212,837,205;88,1,6223,837,204;89,1,6228,838,203;90,1,6235,838,202;91,1,6245,838,200;92,1,6254,838,199;93,1,6260,838,198;94,1,6269,838,197;95,1,6276,838,196;96,1,6286,838,195;97,1,6292,838,195;98,3,6312,838,195,1103;99,1,6325,838,195;100,4,6433,838,195,1103;101,2,6434,838,195,1103;102,1,7152,838,196;196,3,9936,852,346,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,6321;2,7949;3,8928;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,NaN,508148,32,0,0,0,NaN,9936,0,1593607358434,14,17047,4,197,2841,3,0,9938,428329,0,2CC3585D5F5E58B90C58E6D6DE13E22D~-1~YAAQO5HdWOACGudyAQAAmqBmCgRWq3Y8zYwaGJeZF0wq7+06oDr7dAtEuX2ZtTH1YUjRD+CqeE5+SuxiWp+3UOH/oDZb0P7f7k/vj94gyaUoxJ0ulFywnUos6WZPhwyrQuvJOgKanoe632gHwvUYti1kUW4M7rswglDHeqfMR/tpVubaWd956ZKM32EpASG+ZYjgnIMOf7QWlbM5FGPpux2updXK9fFS1iEWwj/mHLXIUodz1Guk3kg6xRAHSvsj6f/gGSYgnW9ViGcfwqCOq9aC5Ivor9JKYPwEG61n3hQjSDT5Gg9WbndM3mxwVoSTIXibnA98MSYjM1HvrUjlj1Llz2A=~-1~-1~-1,32838,130,-829678606,26018161,PiZtE,54403,52-1,2,-94,-106,1,3-1,2,-94,-119,200,0,0,0,0,0,0,200,0,0,0,200,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,993389013-1,2,-94,-118,191626-1,2,-94,-121,;2;10;0'
                    }
                    session.headers["Accept"] = "*/*"
                    session.headers["Content-Type"] = 'text/plain;charset=UTF-8'
                    session.headers["Origin"] = 'https://www.zalando.fr'
                    session.headers["Referer"] = 'https://www.zalando.fr/login/?view=login'
                    session.headers["Content-Length"] = '3298'
                    session.post(url_bot, json=data1, verify=False)
                    session.headers["Content-Length"] = '3547'
                    session.post(url_bot, json=data2, verify=False)
                    del session.headers["Content-Type"]
                    del session.headers["Origin"]
                    del session.headers["Referer"]
                    del session.headers["Content-Length"]

                    # Connexion au compte
                    url_connexion_2 = 'https://www.zalando.fr/api/reef/login/schema'
                    url_connexion_3 = 'https://www.zalando.fr/api/reef/login'
                    url_connexion_4 = 'https://www.zalando.fr/myaccount'
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
                    del session.headers["x-xsrf-token"]
                    del session.headers["x-zalando-client-id"]
                    del session.headers["x-zalando-render-page-uri"]
                    del session.headers["x-zalando-request-uri"]
                    del session.headers["x-flow-id"]
                    session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                    session.headers["Referer"] = "https://www.zalando.fr/login/?view=login"
                    session.get(url_connexion_4, verify=False)

                    # Validation du panier et checkout
                    url_panier_1 = 'https://www.zalando.fr/cart'
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
                    session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                    session.get(url_panier_1, verify=False)
                    session.headers["Referer"] = "https://www.zalando.fr/cart"
                    session.get(url_panier_2, verify=False)
                    session.get(url_panier_3, verify=False)
                    session.post(url_panier_4, json=checkout, verify=False)

                    # Requetes anti-bot
                    url_botbis = 'https://www.zalando.fr/resources/35692132da2028b315fc23b805e921'
                    data1bis = {
                        'sensor_data': '7a74G7m23Vrp0o5c9178851.6-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392105,5498227,1440,900,1440,900,1440,525,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.273584619136,796807749113.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,-1,2,-94,-102,-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/checkout/address-1,2,-94,-115,1,32,32,0,0,0,0,745,0,1593615498227,29,17048,0,0,2841,0,0,746,0,0,EBC16C32565FCC85852E046D0E13B03E~-1~YAAQLux7XBkXm/JyAQAASr3iCgSs+3joFRndDLyPCe5cbv0A8AknzYLWTBk244SQmgBCzZN6cq21YGyWvCsv4nKgaED8Go0IiEuEhdhY4sKY2R5HRrNnxyaD5skYqQwq0ffv2FqM+HpL++ZzD9+NS5B+ymWwkdDuo4kCbgKB8tN4E0deTM8Z7AABSlVxPSxnOga/rvkVc/GRBThbODhSxoDEXldjaulI3knTbe+2m4XYaLkTOljAzBUWnCC+a/B5T6zDjwUwQcKWlYaFc2qUFmt5WSHgX6pFTF7FkKGdN4ErI87HLQtAPdYgVgrrzYZ0BA9FMCYQzxGJgDbflRH+W+mjMu0=~-1~-1~-1,32365,97,-378114461,26018161,PiZtE,92130,68-1,2,-94,-106,9,1-1,2,-94,-119,200,0,200,0,0,200,0,0,0,200,200,2200,800,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,148451781-1,2,-94,-118,82368-1,2,-94,-121,;1;7;0'
                    }
                    data2bis = {
                        'sensor_data': '7a74G7m23Vrp0o5c9178851.6-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392105,5498227,1440,900,1440,900,1440,525,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.273584619136,796807749113.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,-1,2,-94,-102,-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/checkout/address-1,2,-94,-115,1,32,32,0,0,0,0,745,0,1593615498227,29,17048,0,0,2841,0,0,746,0,0,EBC16C32565FCC85852E046D0E13B03E~-1~YAAQLux7XBkXm/JyAQAASr3iCgSs+3joFRndDLyPCe5cbv0A8AknzYLWTBk244SQmgBCzZN6cq21YGyWvCsv4nKgaED8Go0IiEuEhdhY4sKY2R5HRrNnxyaD5skYqQwq0ffv2FqM+HpL++ZzD9+NS5B+ymWwkdDuo4kCbgKB8tN4E0deTM8Z7AABSlVxPSxnOga/rvkVc/GRBThbODhSxoDEXldjaulI3knTbe+2m4XYaLkTOljAzBUWnCC+a/B5T6zDjwUwQcKWlYaFc2qUFmt5WSHgX6pFTF7FkKGdN4ErI87HLQtAPdYgVgrrzYZ0BA9FMCYQzxGJgDbflRH+W+mjMu0=~-1~-1~-1,32365,97,-378114461,26018161,PiZtE,92130,68-1,2,-94,-106,9,1-1,2,-94,-119,200,0,200,0,0,200,0,0,0,200,200,2200,800,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,148451781-1,2,-94,-118,82368-1,2,-94,-121,;1;7;0'
                    }
                    session.headers["Accept"] = "*/*"
                    session.headers["Content-Type"] = 'text/plain;charset=UTF-8'
                    session.headers["Origin"] = 'https://www.zalando.fr'
                    session.headers["Referer"] = 'https://www.zalando.fr/login/?view=login'
                    session.headers["Content-Length"] = '3298'
                    session.post(url_botbis, json=data1bis, verify=False)
                    session.headers["Content-Length"] = '3547'
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
                    session.headers['Host'] = 'card-entry-service.zalando-payments.com'

                # Fermeture de la Session
                session.close()

            # Gestion des exceptions
            except:
                pass

            finally:
                x = x + 1
                if x == (len(liste_proxys) + 1):
                    x = 0


url_2_bis = 'https://www.zalando.fr/api/checkout/search-pickup-points-by-address'


comptes = creation_objet_compte()
Paiement_Zalando(comptes)