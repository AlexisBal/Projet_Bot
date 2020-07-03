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

# Fonction proxy
def proxy():
    with open('Generateur_Comptes_Zalando_V2/Data/proxy.txt', 'w') as f:
        liste_proxys = []
        for ligne in f:
            data = f.read()
            print(data)
            liste_proxys = liste_proxys.append(data)

        if not liste_proxys:
            print("Vous n'avez spécifié aucun proxy.")
            print("Entrer l'adresse des serveurs proxy dans le fichier proxy.txt")

        return liste_proxys


# Saisie des informations personnelles et du nombre de comptes souhaité
def SaisieInformations():
    # Création d'une liste "liste_compte" vide
    liste_comptes = []

    # Saisie des informations
    prenom = input("Entrer votre prenom :")
    nom = input("Entrer votre nom :")
    cp = input("Entrer votre code postal :")
    ville = input("Entrer votre ville (sans accents) :")
    adresse = input("Entrer votre adresse (sans accents) :")
    complement = input("Complément d'adresse (cliquer sur entrer pour passer) :")
    telephone = input("Entrer un numéro de téléphone mobile :")
    nombrecompte = int(
        input(
            "Entrer le nombre de comptes souhaité (1 adresse mail valide par compte) :"
        )
    )
    for i in range(0, nombrecompte):
        email = input("Entrer une adresse mail valide :")
        i = {
            "prenom": prenom,
            "nom": nom,
            "email": email,
            "motdepasse": "",
            "codepostal": cp,
            "ville": ville,
            "adresse": adresse,
            "complement_adresse": complement,
            "id_adresse": '',
            "telephone": telephone
        }
        # Création d'un mot de passe aléatoire et sécurisé
        pwo = PasswordGenerator()
        i["motdepasse"] = pwo.generate()
        # Insertion des comptes dans la liste "liste_compte"
        liste_comptes.append(i)

    # Insertion des comptes dans la base de données "Comptes.json"
    with open("Data/Comptes.json", "w") as f:
        json.dump(liste_comptes, f, indent=4)
    f.close()

    # Message de confimation
    print("Vos informations ont bien été sauvegardées !")


# Création des objets "Compte" et de la liste d'objet "compte_objet_list"
def creation_objet_compte():
    acces_fichier = open("Data/Comptes.json", "r")
    compte_objet_list = []
    for compte_attributes in json.load(acces_fichier):
        compte_objet = Compte(**compte_attributes)
        compte_objet_list.append(compte_objet)
    acces_fichier.close()
    return compte_objet_list


# Création des comptes à partir des attributs de chaque objet "Compte"
def CreationComptes(compte_objet_list, liste_proxys):
    # Comptage du nombre de comptes présents dans la base de données
    nombrecompte = len(compte_objet_list)

    # Création d'un compte pour chaque objet "Compte" présent dans la base de données
    for compte in range(0, nombrecompte):
        # Ouverture de la session
        with requests.Session() as session:
            # Réglage des paramètres de la session
            session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
            session.headers.update(
                {
                    'User-Agent': generate_user_agent(os=('mac', 'linux'))
                }
            )

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
            session.headers["x-zalando-client-id"] = cookies["Zalando-Client-Id"]
            session.headers["x-zalando-render-page-uri"] = "/"
            session.headers["x-zalando-request-uri"] = "/"
            session.headers["x-flow-id"] = home.headers["X-Flow-Id"]
            session.headers["Accept"] = "application/json"

            # Envoie de requetes pour éviter les sécurités anti-bot
            url_get_2 = (
                "https://www.zalando.fr/resources/a6c5863f92201d42d0a3ba96882c7b"
            )
            url_get_3 = (
                "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=1"
                % home.headers["X-Flow-Id"]
            )
            url_post1 = (
                "https://www.zalando.fr/resources/a6c5863f921840dbe8f36578d86f32"
            )
            url_post1_bis = (
                "https://www.zalando.fr/resources/a6c5863f921840dbe8f36578d86f32"
            )
            sensor_data = {
                "sensor_data": "7a74G7m23Vrp0o5c9173031.54-1,2,-94,-100,Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362,"
                "uaend,12083,20030107,fr-FR,Gecko,1,0,0,0,391686,3056866,1280,680,1280,720,463,607,1295,,"
                "cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,9181,"
                "0.0117028775,795956630770,loc:-1,2,-94,-101,do_en,dm_en,t_dis-1,2,-94,-105,0,-1,0,0,1063,"
                "1884,0;0,-1,0,0,908,1768,0;0,1,0,0,981,1435,0;1,-1,0,0,2177,1798,0;-1,2,-94,-102,0,-1,0,0,"
                "972,1884,1;0,-1,0,0,925,1768,1;0,1,0,0,986,1435,1;1,-1,0,0,1995,1798,1;-1,2,-94,-108,-1,2,"
                "-94,-110,0,4,117,369,1226,-1;1,2,117,369,1226,-1;2,1,4892,374,1220;3,1,4900,393,1207;4,1,"
                "4906,409,1197;5,1,4913,428,1187;6,1,4921,480,1167;7,1,4929,521,1154;8,1,4936,539,1146;9,1,"
                "4942,623,1117;10,1,123816,545,1441;11,1,123822,572,1412;12,1,123829,605,1384;13,1,123838,620,"
                "1374;14,1,123844,632,1363;15,1,257501,521,1413;16,1,257508,520,1383;17,1,257515,516,1320;18,"
                "1,257522,513,1294;19,1,257530,509,1213;20,1,257537,505,1174;21,1,257545,501,1097;22,1,257552,"
                "496,1066;23,1,257560,496,1033;24,1,257567,496,993;25,1,257575,497,979;26,1,257582,497,967;27,"
                "1,257590,500,951;28,1,257597,503,939;29,1,257604,505,933;30,1,257612,507,927;31,1,257619,509,"
                "923;32,1,257626,511,920;33,1,257634,515,916;34,1,257643,527,909;35,1,257648,537,905;36,1,"
                "257659,548,904;37,1,257664,559,905;38,1,257671,578,907;39,1,257679,613,917;40,1,257686,627,"
                "922;41,1,298100,516,988;42,3,298110,516,988,-1;43,4,298230,516,986,-1;44,1,299551,557,874;45,"
                "3,299559,557,874,-1;46,4,299751,557,873,-1;47,1,300828,584,693;48,3,300837,584,693,-1;49,4,"
                "300989,584,693,-1;50,1,327987,643,409;51,1,327994,633,407;52,1,328001,626,405;53,1,328009,"
                "620,401;54,1,328016,615,399;55,1,328373,605,381;56,1,328381,599,372;57,1,328389,595,366;58,1,"
                "328395,589,357;59,1,328403,585,349;60,1,328410,579,339;61,1,328418,575,330;62,1,328425,571,"
                "321;63,1,328434,568,313;64,1,328440,565,305;65,1,328447,563,301;66,1,328455,559,292;67,1,"
                "328462,555,283;68,1,328470,552,271;69,1,328477,549,265;70,1,328484,547,260;71,1,328493,547,"
                "255;72,1,328501,547,254;73,1,328507,546,253;74,1,328514,546,252;75,1,328521,546,251;76,1,"
                "328529,546,251;77,1,328596,546,250;78,1,328604,546,249;79,1,328611,547,249;80,1,328619,550,"
                "249;81,1,328625,553,249;82,1,328635,557,252;83,1,328640,561,255;84,1,328650,563,257;85,1,"
                "328656,569,262;86,1,328663,571,265;87,1,328671,573,267;88,1,328678,577,271;89,1,328686,578,"
                "272;90,1,328692,579,273;91,1,328701,581,275;92,1,328708,581,275;93,1,328716,583,277;94,1,"
                "328722,583,277;95,1,328827,583,276;96,1,328835,583,273;97,1,328842,581,267;98,1,328851,579,"
                "263;99,1,328856,578,257;100,1,328864,576,254;101,1,328872,574,249;102,1,328879,572,247;103,1,"
                "328886,569,243;104,1,328894,565,239;105,1,340013,486,243;106,1,340013,486,243;107,1,340019,"
                "493,251;202,3,588503,895,479,-1,3;203,4,588555,895,479,-1,3;373,3,626799,242,1219,-1;374,4,"
                "627004,242,1219,-1;375,2,627005,242,1219,-1;557,3,921516,98,790,2366;558,4,921569,98,790,"
                "-1;560,3,929901,301,989,-1;561,4,929945,301,991,-1;563,3,938238,303,1186,-1;564,4,938317,303,"
                "1186,-1;565,2,938317,302,1186,-1;713,3,953189,346,1187,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,"
                "-94,-109,-1,2,-94,-114,1,3,298104,516,988;2,3,299552,556,874;3,3,300828,584,692;8,3,921512,"
                "98,790;9,3,929896,300,989;10,3,938233,302,1186;11,4,938317,302,1186;-1,2,-94,-103,3,2;2,"
                "9184;3,289774;2,292219;3,298101;2,302593;0,329903;1,339495;3,339547;2,339568;3,587988;2,"
                "630264;3,921510;2,923091;3,929894;2,934467;3,938233;2,948238;-1,2,-94,-112,"
                "https://www.zalando.fr/login/?view=register-1,2,-94,-115,1,39830069,32,0,0,4635871,44465908,"
                "953189,0,1591913261540,13,17029,0,714,2838,13,0,953191,48007072,1,"
                "70769C98B687B487EDB11AA876284490~-1~YAAQH3IRAkV4lpNyAQAADVx6pQQUjelrjmwRAe5bNDiLKh8PH+EI7lpuI"
                "+71UJ/j7niXkW90ZCQ9Oek6zv5CaX6+R2ANBcj4qQobgIP8fnA/a/JoOHQ"
                "/F7LEiUv0rTRig78FZtB1tfAH02lSej2Dtj6wGp/pXCJ4RWgR9YTZft0lE1gKhqxP6qaZgUPyN38JnSyWrqSsAfqve"
                "/ce1nm96vo/+d51AQ0R5c/XRDx+68E8rQbdF7yHaS0XEE5Sv5EjHtX3akEFs/I0Kg9fBwquT9QKl6QqG9AtZ"
                "/oDT2w8X7SVhKe+SpgYGjv2gMvM9/F+SKxFSh5MR0X8pls466RX4WE8gVM=~-1~-1~-1,31303,864,-119753953,"
                "27074993-1,2,-94,-106,1,15-1,2,-94,-119,20,60,40,60,80,40,20,40,20,20,20,260,280,80,-1,2,-94,"
                "-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,"
                "-359992563;-1439556030;dis;,23;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,"
                "5499-1,2,-94,-116,27511667-1,2,-94,-118,233033-1,2,-94,-121,;4;7;0 "
            }
            sensor_data_bis = {
                "sensor_data": "7a74G7m23Vrp0o5c9174241.54-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36,uaend,12147,"
                "20030107,fr-FR,Gecko,3,0,0,0,391704,8399265,1440,900,1440,900,1440,821,1440,,cpen:0,i1:0,"
                "dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:1,bat:1,x11:0,x12:1,8921,0.571005954285,"
                "795994199646,loc:-1,2,-94,-101,do_en,dm_en,t_en-1,2,-94,-105,0,-1,0,0,954,1884,0;0,-1,0,0,"
                "1041,1768,0;0,1,0,0,927,1435,0;1,-1,0,0,2091,1798,0;-1,2,-94,-102,0,-1,0,0,990,1884,1;0,-1,0,"
                "0,1031,1768,1;0,1,0,0,995,1435,1;1,-1,0,0,2037,1798,1;-1,2,-94,-108,0,1,3951,undefined,0,0,"
                "-1;1,2,3969,undefined,0,0,-1;2,1,3970,undefined,0,0,-1;3,2,3978,undefined,0,0,-1;4,1,5827,-2,"
                "0,0,1884;5,3,5828,-2,0,0,1884;6,2,5881,-2,0,0,1884;7,1,6246,-2,0,0,1884;8,3,6246,-2,0,0,"
                "1884;9,2,6321,-2,0,0,1884;10,1,6420,-2,0,0,1884;11,3,6420,-2,0,0,1884;12,2,6503,-2,0,0,"
                "1884;13,1,7712,-2,0,0,1768;14,3,7712,-2,0,0,1768;15,2,7796,-2,0,0,1768;16,1,7815,-2,0,0,"
                "1768;17,3,7815,-2,0,0,1768;18,2,7896,-2,0,0,1768;19,1,7910,-2,0,0,1768;20,3,7911,-2,0,0,"
                "1768;21,1,8031,-2,0,0,1768;22,3,8031,-2,0,0,1768;23,2,8082,-2,0,0,1768;24,2,8094,-2,0,0,"
                "1768;25,1,11003,8,0,0,1435;26,2,11112,8,0,0,1435;27,1,11329,-3,0,0,1435;28,2,11468,-3,0,0,"
                "1435;29,1,11618,8,0,0,1435;30,2,11713,8,0,0,1435;31,1,12274,-2,0,0,1435;32,3,12274,-2,0,0,"
                "1435;33,2,12333,-2,0,0,1435;34,1,12667,-2,0,0,1435;35,3,12667,-2,0,0,1435;36,2,12742,-2,0,0,"
                "1435;37,1,12833,-2,0,0,1435;38,3,12834,-2,0,0,1435;39,2,12922,-2,0,0,1435;40,1,13161,-2,0,0,"
                "1435;41,3,13162,-2,0,0,1435;42,2,13253,-2,0,0,1435;43,1,13277,-2,0,0,1435;44,3,13277,-2,0,0,"
                "1435;45,2,13355,-2,0,0,1435;46,1,13373,-2,0,0,1435;47,3,13373,-2,0,0,1435;48,1,13500,-2,0,0,"
                "1435;49,3,13501,-2,0,0,1435;50,2,13526,-2,0,0,1435;51,2,13568,-2,0,0,1435;52,1,16691,-3,0,0,"
                "1435;53,2,16838,-3,0,0,1435;54,1,17016,8,0,0,1435;55,2,17119,8,0,0,1435;56,1,17221,8,0,0,"
                "1435;57,2,17292,8,0,0,1435;58,1,17368,8,0,0,1435;59,2,17447,8,0,0,1435;60,1,17495,8,0,0,"
                "1435;61,2,17571,8,0,0,1435;62,1,17623,8,0,0,1435;63,2,17708,8,0,0,1435;64,1,18327,-2,0,0,"
                "1435;65,3,18328,-2,0,0,1435;66,1,18398,-2,0,0,1435;67,3,18399,-2,0,0,1435;68,2,18409,-2,0,0,"
                "1435;69,2,18478,-2,0,0,1435;70,1,18584,-2,0,0,1435;71,3,18584,-2,0,0,1435;72,1,18619,-2,0,0,"
                "1435;73,3,18620,-2,0,0,1435;74,2,18663,-2,0,0,1435;75,2,18683,-2,0,0,1435;76,1,20599,-2,0,0,"
                "1435;77,3,20600,-2,0,0,1435;78,1,20701,-2,0,0,1435;79,3,20701,-2,0,0,1435;80,2,20709,-2,0,0,"
                "1435;81,2,20790,-2,0,0,1435;82,1,20845,-2,0,0,1435;83,3,20846,-2,0,0,1435;84,2,20937,-2,0,0,"
                "1435;85,1,21070,-2,0,0,1435;86,3,21070,-2,0,0,1435;87,2,21171,-2,0,0,1435;88,1,21175,-2,0,0,"
                "1435;89,3,21175,-2,0,0,1435;90,2,21235,-2,0,0,1435;91,1,21321,-2,0,0,1435;92,3,21322,-2,0,0,"
                "1435;93,2,21393,-2,0,0,1435;94,1,21726,16,0,8,1435;95,1,22555,-2,0,8,1435;96,3,22555,-2,0,8,"
                "1435;97,2,22630,-2,0,8,1435;98,2,22727,16,0,0,1435;99,1,22861,-2,0,0,1435;100,3,22861,-2,0,0,"
                "1435;101,2,22928,-2,0,0,1435;102,1,22955,-2,0,0,1435;103,3,22956,-2,0,0,1435;104,2,23055,-2,"
                "0,0,1435;105,1,23148,-2,0,0,1435;106,3,23148,-2,0,0,1435;107,1,23203,-2,0,0,1435;108,3,23204,"
                "-2,0,0,1435;109,2,23217,-2,0,0,1435;110,2,23271,-2,0,0,1435;111,1,23433,-2,0,0,1435;112,3,"
                "23434,-2,0,0,1435;113,2,23509,-2,0,0,1435;114,1,23661,-2,0,0,1435;115,3,23661,-2,0,0,"
                "1435;116,2,23748,-2,0,0,1435;117,1,23793,-2,0,0,1435;118,3,23794,-2,0,0,1435;119,2,23881,-2,"
                "0,0,1435;120,1,25872,8,0,0,1435;121,2,25943,8,0,0,1435;122,1,27353,8,0,0,1435;123,2,27444,8,"
                "0,0,1435;124,1,27515,8,0,0,1435;125,2,27601,8,0,0,1435;126,1,27669,8,0,0,1435;127,2,27756,8,"
                "0,0,1435;128,1,28221,-2,0,0,1435;129,3,28222,-2,0,0,1435;130,2,28321,-2,0,0,1435;131,1,28400,"
                "-2,0,0,1435;132,3,28401,-2,0,0,1435;133,2,28484,-2,0,0,1435;134,1,29185,16,0,8,1798;135,1,"
                "29539,-2,0,8,1798;136,3,29539,-2,0,8,1798;137,2,29602,-2,0,8,1798;138,2,29735,16,0,0,"
                "1798;139,1,29884,-2,0,0,1798;140,3,29884,-2,0,0,1798;141,2,29959,-2,0,0,1798;142,1,30132,-2,"
                "0,0,1798;143,3,30132,-2,0,0,1798;144,2,30215,-2,0,0,1798;145,1,30244,-2,0,0,1798;146,3,30245,"
                "-2,0,0,1798;147,1,30623,16,0,8,1798;148,2,31438,16,0,0,1798;-1,2,-94,-110,0,1,2723,681,535;1,"
                "1,2726,698,552;2,1,2745,727,584;3,1,2765,746,606;4,1,2776,758,618;5,1,2832,788,657;6,1,2845,"
                "788,666;7,1,2886,783,713;8,1,3329,777,171;9,1,3347,769,170;10,1,3364,766,173;11,1,3499,704,"
                "304;12,1,3502,699,340;13,1,3510,698,346;14,1,3527,695,361;15,1,3544,694,371;16,1,3562,693,"
                "376;17,1,3577,692,378;18,1,3596,691,378;19,1,3610,690,379;20,1,3627,688,378;21,1,3646,686,"
                "376;22,1,3661,682,375;23,1,3677,682,375;24,1,3693,679,376;25,1,3710,677,376;26,1,3734,671,"
                "385;27,1,3743,670,386;28,1,3760,668,389;29,1,3776,665,391;30,1,3793,664,394;31,1,3810,661,"
                "396;32,1,3826,660,398;33,1,3857,658,400;34,1,3863,657,400;35,1,3894,656,402;36,1,3914,655,"
                "402;37,1,3928,655,403;38,1,3943,654,403;39,3,3979,654,403,1884;40,1,3988,654,403;41,4,4062,"
                "654,403,1884;42,2,4068,654,403,1884;43,1,6789,654,404;44,1,6801,651,416;45,1,6817,649,429;46,"
                "1,6833,649,439;47,1,6851,649,447;48,1,6867,649,456;49,1,6884,650,465;50,1,6900,651,470;51,1,"
                "6917,652,472;52,1,6933,652,473;53,1,6949,652,473;54,1,6967,652,474;55,1,6989,652,474;56,1,"
                "7034,652,474;57,1,7052,650,475;58,1,7067,647,478;59,1,7085,646,478;60,1,7100,644,482;61,1,"
                "7116,643,483;62,1,7134,642,484;63,3,7146,642,484,1768;64,1,7157,641,484;65,4,7282,641,484,"
                "1768;66,2,7287,641,484,1768;67,1,7305,641,484;68,1,8516,642,484;69,1,8536,658,484;70,1,8551,"
                "675,487;71,1,8567,688,496;72,1,8588,713,526;73,1,8601,717,535;74,1,8619,720,556;75,1,8636,"
                "720,585;76,1,8651,718,605;77,1,8667,717,624;78,1,8684,717,647;79,1,8700,717,658;80,1,8716,"
                "716,670;81,1,8733,713,677;82,1,8752,710,680;83,1,8767,708,682;84,1,8786,705,684;85,1,8802,"
                "704,684;86,1,8819,703,685;87,1,8833,703,685;88,1,8852,703,684;89,1,8868,702,681;90,1,8885,"
                "702,674;91,1,8900,702,670;92,1,8916,702,667;93,1,8934,704,665;94,1,8949,705,663;95,1,8967,"
                "705,663;96,1,8983,706,663;97,1,9000,706,663;98,1,9023,706,662;99,1,9037,706,662;100,1,9053,"
                "706,662;101,1,9069,704,661;102,1,9085,699,659;103,1,9101,694,658;104,1,9117,686,657;105,1,"
                "9134,671,657;155,3,10069,613,653,1435;169,4,10512,286,643,-1;170,2,10515,286,643,-1;289,3,"
                "16039,621,658,1435;290,4,16142,621,658,1435;291,2,16147,621,658,1435;332,3,19735,567,656,"
                "1435;341,4,19969,331,656,-1;342,2,19973,331,656,-1;410,3,25445,618,657,1435;411,4,25581,618,"
                "657,1435;412,2,25585,618,657,1435;446,3,26979,706,659,1435;447,4,27084,706,659,1435;448,2,"
                "27088,706,659,1435;470,3,28827,698,736,1798;481,4,29069,-1,-1,-1;482,2,29072,-1,-1,-1;518,3,"
                "35067,689,1129,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,"
                "-94,-112,https://www.zalando.fr/login/?view=register-1,2,-94,-115,NaN,1241948,32,0,0,0,NaN,"
                "35067,0,1591988399292,26,17030,149,519,2838,17,0,35071,3836867,0,"
                "B94B13408752796D9FA179CAE9B326F7~-1"
                "~YAAQtnIRAmAASppyAQAAA57nqQTTWkwggemyrCGrLGH6zIX9UVCPmrn8h2QUAUEj0lF29rBPzgtrr3jj5UR+sGK"
                "+yWtwHgK5PKrEczsUuy0vU4y4VqSql0liKBYIFZt3nczVvU/bk7MZGowQRAMx86YP4IE0jN8oqp+/2hnEhuzz1v"
                "/F1LmsrorvI+dkHwlJxvr1PtQztbz6t7Lu2VUZTzWjPiXOd6Cqf9FjpxbIYw"
                "+X4vRWL7hx1pGMG3TVz6Af5FBrUD52TihdEmqVEDfspLjDmsTcsrm+ukW8T7IxqPymb"
                "+6ciaUHfV7AoPBUPHdRkdThHLdjoBII1qsbNTApP0/BUIY=~-1~-1~-1,33155,954,-2009515897,30261693-1,2,"
                "-94,-106,1,11-1,2,-94,-119,58,64,63,93,103,132,92,47,12,9,9,1667,1915,510,-1,2,-94,-122,0,0,"
                "0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,11321144241322243122-1,2,"
                "-94,-70,-36060876;-1849314799;dis;,7,8;true;true;true;-120;true;30;30;true;false;-1-1,2,-94,"
                "-80,5578-1,2,-94,-116,8399281-1,2,-94,-118,386880-1,2,-94,-121,;10;31;0 "
            }
            session.get(url_get_2, verify=False)
            session.get(url_get_3, verify=False)
            session.post(url_post1, json=sensor_data, verify=False)
            session.post(url_post1_bis, json=sensor_data_bis, verify=False)

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

        # Message de confimation pour chaque compte créé
        print("Le compte de ", compte_objet_list[compte].email, "a bien été créé !")


def Configuration(compte_objet_list, liste_proxys):
    # Comptage du nombre de compte présents dans la base de données
    nombrecompte = len(compte_objet_list)

    # Création d'un compte pour chaque objet "Compte" présent dans la base de données
    for y in range(0, nombrecompte):
        with requests.Session() as session:
            # Réglage des paramètres de la session
            session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
            headers = {
                "Host": "www.zalando.fr",
                "User-Agent": generate_user_agent(os=('mac', 'linux')),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "fr-fr",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
            session.headers.update(headers)

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
            url_post1 = (
                "https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b"
            )
            sensor_data = {
                "sensor_data": "7a74G7m23Vrp0o5c9175981.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391850,1658105,1440,814,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.294628793147,796290829052.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,617,939,3;1,1,622,939,3;2,1,624,946,6;3,1,633,955,10;4,1,635,955,10;5,1,639,965,15;6,1,639,965,15;7,1,647,976,19;8,1,648,976,19;9,1,657,991,24;10,1,657,991,24;11,1,663,1008,28;12,1,665,1008,28;13,1,672,1025,33;14,1,674,1025,33;15,1,679,1056,40;16,1,680,1056,40;17,1,688,1076,44;18,1,689,1076,44;19,1,696,1087,46;20,1,697,1087,46;21,1,703,1109,51;22,1,703,1109,51;23,1,712,1129,55;24,1,713,1129,55;25,1,720,1148,59;26,1,722,1148,59;27,1,727,1166,66;28,1,728,1166,66;29,1,736,1180,71;30,1,736,1180,71;31,1,744,1196,77;32,1,744,1196,77;33,1,753,1212,85;34,1,754,1212,85;35,1,760,1226,94;36,1,760,1226,94;37,1,769,1236,102;38,1,770,1236,102;39,1,775,1249,112;40,1,776,1249,112;41,1,787,1258,121;42,1,787,1258,121;43,1,791,1265,130;44,1,792,1265,130;45,1,802,1273,138;46,1,802,1273,138;47,1,808,1279,147;48,1,809,1279,147;49,1,818,1283,154;50,1,819,1283,154;51,1,825,1284,157;52,1,826,1284,157;53,1,832,1290,168;54,1,835,1290,168;55,1,840,1291,176;56,1,841,1291,176;57,1,850,1292,183;58,1,861,1293,190;59,1,864,1293,198;60,1,865,1293,198;61,1,873,1293,206;62,1,873,1293,206;63,1,882,1293,213;64,1,883,1293,213;65,1,889,1290,220;66,1,892,1290,220;67,1,897,1284,227;68,1,898,1284,227;69,1,908,1270,241;70,1,915,1255,250;71,1,918,1255,250;72,1,921,1239,258;73,1,922,1239,258;74,1,929,1216,267;75,1,929,1216,267;76,1,937,1190,274;77,1,938,1190,274;78,1,946,1162,282;79,1,947,1162,282;80,1,953,1130,287;81,1,954,1130,287;82,1,962,1096,293;83,1,962,1096,293;84,1,970,1061,296;85,1,970,1061,296;86,1,978,1022,298;87,1,979,1022,298;88,1,986,987,300;89,1,986,987,300;90,1,994,948,302;91,1,994,948,302;92,1,1005,917,304;93,1,1012,904,304;94,1,1013,904,304;95,1,1019,876,304;96,1,1020,876,304;97,1,1026,853,304;98,1,1026,853,304;99,1,1034,847,304;217,3,2758,739,188,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,329;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,1,220704,32,0,0,0,220672,2758,0,1592581658105,16,17036,0,218,2839,1,0,2759,84978,0,544D198E0F1B1CB2C191909E5A431D4A~-1~YAAQI5HdWON0Wa1yAQAAIJhDzQSs2DaHi3VWlNasxDo6Ll1h+oPs9Arg4f8DmMXtm7anSErvR5n9n2pO+UMTG/IVcwHpfi9Wi/ZDhjSRktF/01XyTRMeCqjaeI0/prETWeQeJkJTEUT7q7Lp9d7aH30hB2IihOsBdiBvSwqh9UbB/o6n5EgkZgrD6PRQwpDic6VG2QZ9k5czxOMXhm2LdiLG+/uKxYYkLkarftjuMKCgYsG+w4No1YL0WTXRpGFiEoZrP1PWYltbpu2Q2NBlWPFovn4VW0knih51voTZCUXpt52d7hsTVn2TdnQglcPVYqHyg6Goubm3of/HY6EI/ryzWoo=~-1~-1~-1,32678,285,1682362911,26018161,NVVN,124,-1-1,2,-94,-106,1,2-1,2,-94,-119,200,2200,0,0,0,0,0,0,0,200,0,3000,2600,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,44769069-1,2,-94,-118,176741-1,2,-94,-121,;1;4;0"
            }
            sensor_data_bis = {
                "sensor_data": "7a74G7m23Vrp0o5c9175981.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391850,1658105,1440,814,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.347127751173,796290829052.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,6662,undefined,0,0,1103,0;1,2,6677,undefined,0,0,1103,0;2,1,6716,undefined,0,0,1103,0;3,2,6726,undefined,0,0,1103,0;4,1,7287,13,0,0,1466;-1,2,-94,-110,0,1,617,939,3;1,1,622,939,3;2,1,624,946,6;3,1,633,955,10;4,1,635,955,10;5,1,639,965,15;6,1,639,965,15;7,1,647,976,19;8,1,648,976,19;9,1,657,991,24;10,1,657,991,24;11,1,663,1008,28;12,1,665,1008,28;13,1,672,1025,33;14,1,674,1025,33;15,1,679,1056,40;16,1,680,1056,40;17,1,688,1076,44;18,1,689,1076,44;19,1,696,1087,46;20,1,697,1087,46;21,1,703,1109,51;22,1,703,1109,51;23,1,712,1129,55;24,1,713,1129,55;25,1,720,1148,59;26,1,722,1148,59;27,1,727,1166,66;28,1,728,1166,66;29,1,736,1180,71;30,1,736,1180,71;31,1,744,1196,77;32,1,744,1196,77;33,1,753,1212,85;34,1,754,1212,85;35,1,760,1226,94;36,1,760,1226,94;37,1,769,1236,102;38,1,770,1236,102;39,1,775,1249,112;40,1,776,1249,112;41,1,787,1258,121;42,1,787,1258,121;43,1,791,1265,130;44,1,792,1265,130;45,1,802,1273,138;46,1,802,1273,138;47,1,808,1279,147;48,1,809,1279,147;49,1,818,1283,154;50,1,819,1283,154;51,1,825,1284,157;52,1,826,1284,157;53,1,832,1290,168;54,1,835,1290,168;55,1,840,1291,176;56,1,841,1291,176;57,1,850,1292,183;58,1,861,1293,190;59,1,864,1293,198;60,1,865,1293,198;61,1,873,1293,206;62,1,873,1293,206;63,1,882,1293,213;64,1,883,1293,213;65,1,889,1290,220;66,1,892,1290,220;67,1,897,1284,227;68,1,898,1284,227;69,1,908,1270,241;70,1,915,1255,250;71,1,918,1255,250;72,1,921,1239,258;73,1,922,1239,258;74,1,929,1216,267;75,1,929,1216,267;76,1,937,1190,274;77,1,938,1190,274;78,1,946,1162,282;79,1,947,1162,282;80,1,953,1130,287;81,1,954,1130,287;82,1,962,1096,293;83,1,962,1096,293;84,1,970,1061,296;85,1,970,1061,296;86,1,978,1022,298;87,1,979,1022,298;88,1,986,987,300;89,1,986,987,300;90,1,994,948,302;91,1,994,948,302;92,1,1005,917,304;93,1,1012,904,304;94,1,1013,904,304;95,1,1019,876,304;96,1,1020,876,304;97,1,1026,853,304;98,1,1026,853,304;99,1,1034,847,304;217,3,2758,739,188,1103;218,4,2893,739,188,1103;219,2,2893,739,188,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,329;2,4473;3,6695;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,NaN,228787,32,0,0,0,NaN,7287,0,1592581658105,16,17036,5,234,2839,2,0,7289,124832,0,544D198E0F1B1CB2C191909E5A431D4A~-1~YAAQI5HdWB11Wa1yAQAA5qBDzQSG6Pv/OSeYlJZ+5TdSTmLptNh6airlP5V/lfl0qZibNHdiWQexNK07iCtntsNCWGQHPYxIdWr4OhMwJ0i9iCooHr4ymTZvJOiehLUCEf20hGguVIpe5vO+tl8HNMUY7PGyvGkSCQeUF3LvyMptTNSG8CSY0BBnfap9mu2tyNqJrjG8Xea/jsk0hclFwXoOFGYut6G8PG3iNaLmer5R0671/1KuX41tQnpCg/f9510oCGeGVN2f1b3jSey1Ob7DjYTE+aUd5c5tuJsTW5eeK7Ce+eI43fC+QwqaWJz5TYZnz0IAjAGkEtDAFH4keWDUEZQ=~-1~-1~-1,32009,285,1682362911,26018161,NVVN,124,-1-1,2,-94,-106,3,3-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,0,600,200,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,44769069-1,2,-94,-118,188004-1,2,-94,-121,;2;4;0"
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
            session.headers["x-zalando-client-id"] = cookies["Zalando-Client-Id"]
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
            id_adresse = objet[0]['id']
            compte_objet_list[y].id_adresse = id_adresse

        # Fermeture de la session
        session.close()

        # Message de confimation pour chaque compte configuré
        print("Le compte de ", compte_objet_list[y].email, "a bien été configuré !")

        # Insertion des comptes actualisés dans la base de données "Comptes.json"
        liste_compte = []
        for b in range(0, len(compte_objet_list)):
            liste_compte.append(compte_objet_list[b].__dict__)
        with open("Data/Comptes.json", "w") as f:
            json.dump(liste_compte, f, indent=4)
        f.close()


SaisieInformations()
comptes = creation_objet_compte()
proxies = proxy()
CreationComptes(comptes, proxies)
Configuration(comptes, proxies)
