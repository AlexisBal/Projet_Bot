import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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
retries = Retry(total=8, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

# Désactivation des messages d'avertissement
urllib3.disable_warnings()

def MiseDansLePanier():
    # Ouverture de la Session
    with requests.Session() as session:
        # Réglage des paramètres de la session
        session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
        headers = {
            "Host": "www.zalando.fr",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.97 Safari/537.36",
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

        # Connexion à la page du produit
        del session.headers["Upgrade-Insecure-Requests"]
        session.get('https://www.zalando.fr/reebok-classic-club-c-85-baskets-basses-whitedark-greenchalk-white-re015o075-a11.html', verify=False)

        # Envoie de requetes pour éviter les sécurités anti-bot
        session.headers["x-xsrf-token"] = cookies["frsx"]


        # Mise dans le panier
        url_panier = "https://www.zalando.fr/api/pdp/cart"
        panier = {"simpleSku": 'RE015O075-A110009000', "anonymous": False}
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
            "sensor_data": "7a74G7m23Vrp0o5c9175921.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391853,4809209,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.970703120485,796297404604,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,-1,2407,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,-1,2407,0;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/cart-1,2,-94,-115,1,32,32,0,0,0,0,1,0,1592594809208,-999999,17037,0,0,2839,0,0,2,0,0,532BDDF92D2792A84D6D104030676E0D~-1~YAAQL+x7XB4Cl4RyAQAAuD4MzgSx3Lv1ABbT/zOiBCoPbgw/BaVzFR5eZ51uxxL4OXmQwVusXrmmp0UQoY91EL8XZjGXZrMEVcbc6xs9RqNoPQT9cmEBDv6P7YDcyruKTOSfhsAg/woWK0b0ajzRcS3F1Dg2bZPIIsoK7d19YVZavIIDPCXt1sCGFl530XhBLlaCEKwtzHQfUSlhF3NQVd9SWOJ6WAvgyXp7mUGeObHiBoSF9sPgFIepOlHRzq0UZmssedn+bhEtz/0FJ/TRMiWS1AM6/gAtbIJwvCzTjnba/L6/uJgtimiQUyrkIuBGq4gAvPc8f9hJW6SIlR4mU+2fpt4=~-1~-1~-1,32514,-1,-1,26018161,NVVO,124,-1-1,2,-94,-106,0,0-1,2,-94,-119,-1-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,-1-1,2,-94,-80,94-1,2,-94,-116,14427678-1,2,-94,-118,82036-1,2,-94,-121,;1;-1;0"
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
        url_connexion = "https://www.zalando.fr/welcomenoaccount/true"
        session.get(url_connexion, verify=False)

        # Sécurité anti-bot
        url_get_2 = (
                "https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=2"
                % home.headers["X-Flow-Id"]
        )
        url_post1 = (
            "https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b"
        )
        sensor_data = {
            "sensor_data": "7a74G7m23Vrp0o5c9175921.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391853,4814181,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.650518738325,796297407090.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,466,1098,525;1,1,510,1094,525;2,1,621,455,214;3,1,691,323,150;4,1,870,323,152;5,1,915,323,152;6,1,927,354,198;7,1,937,383,245;8,1,971,390,256;9,1,1011,431,333;10,1,1041,440,352;11,1,1066,441,353;12,1,1122,440,352;13,1,1133,439,350;14,1,1142,437,347;15,1,1150,435,345;16,1,1151,434,343;17,1,1165,432,341;18,1,1168,430,339;19,1,1183,427,334;20,1,1184,425,331;21,1,1190,421,327;22,1,1191,421,327;23,1,1199,418,323;24,1,1200,418,323;25,1,1207,414,318;26,1,1207,414,318;27,1,1215,412,316;28,1,1216,412,316;29,1,1222,410,313;30,1,1222,410,313;31,1,1233,407,309;32,1,1236,407,309;33,1,1239,404,305;34,1,1240,404,305;35,1,1249,402,303;36,1,1249,402,303;37,1,1255,400,301;38,1,1255,400,301;39,1,1265,399,300;40,1,1266,399,300;41,1,1271,398,299;42,1,1272,398,299;43,1,1283,397,298;44,1,1286,397,298;45,1,1287,397,298;46,1,1301,397,297;47,1,1303,397,297;48,1,1318,397,297;49,1,1319,397,297;50,1,1332,397,297;51,1,1332,397,297;52,1,1336,397,297;53,1,1337,397,297;54,1,1349,396,296;55,1,1352,396,296;56,1,1367,396,295;57,1,1371,395,293;58,1,1381,395,292;59,1,1384,394,290;60,1,1399,394,287;61,1,1403,392,285;62,1,1414,392,282;63,1,1416,391,280;64,1,1424,391,279;65,1,1425,391,279;66,1,1434,390,278;67,1,1434,390,278;68,1,1441,390,277;69,1,1442,390,277;70,1,1450,390,277;71,1,1451,390,277;72,1,1458,390,277;73,1,1459,390,277;74,1,1474,390,276;75,1,1475,390,276;76,1,1499,390,276;77,1,1499,390,276;78,3,1570,390,276,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/welcomenoaccount/true-1,2,-94,-115,1,157693,32,0,0,0,157661,1570,0,1592594814181,30,17037,0,79,2839,1,0,1572,97728,0,532BDDF92D2792A84D6D104030676E0D~-1~YAAQL+x7XGsCl4RyAQAAVVcMzgT8JqlM2ih46/XQ2qYQMxHvaSPQRX2kpvPCVKqrQtQU9V/vFR1MmPEXJf9SmdvOwAkfJImjhgWtg5Qe8TGeuBXznDTznEbLt4H84jeMFHF7HqEOhDVMpIx3WMrRGjPSkRBFYse5UyFG3sp6mv+YX1eTFNnYyFIhKvbMRUFQ2DtEC86yfleq6nBgQuuANy97ge5fStvq8KY1Py33TUYcLQRXFYNwnGjRi4PKcf/NkFtEHlsJukzXJxDUpiE/qsNo6E8KEceJBBEJVmr/MaxcTIcQXweubzRoH+kFchl/1stvlH0jJK9wMuo++pfPPifylAk=~-1~-1~-1,32904,607,-1122583492,26018161,NVVO,124,-1-1,2,-94,-106,1,2-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,200,800,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,649914741-1,2,-94,-118,158953-1,2,-94,-121,;2;5;0"
        }
        sensor_data_bis = {
            "sensor_data": "7a74G7m23Vrp0o5c9175921.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391853,4814181,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.668405617334,796297407090.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,4184,undefined,0,0,1103,0;1,2,4195,undefined,0,0,1103,0;2,1,4231,undefined,0,0,1103,0;3,2,4238,undefined,0,0,1103,0;4,1,4825,13,0,0,1466;-1,2,-94,-110,0,1,466,1098,525;1,1,510,1094,525;2,1,621,455,214;3,1,691,323,150;4,1,870,323,152;5,1,915,323,152;6,1,927,354,198;7,1,937,383,245;8,1,971,390,256;9,1,1011,431,333;10,1,1041,440,352;11,1,1066,441,353;12,1,1122,440,352;13,1,1133,439,350;14,1,1142,437,347;15,1,1150,435,345;16,1,1151,434,343;17,1,1165,432,341;18,1,1168,430,339;19,1,1183,427,334;20,1,1184,425,331;21,1,1190,421,327;22,1,1191,421,327;23,1,1199,418,323;24,1,1200,418,323;25,1,1207,414,318;26,1,1207,414,318;27,1,1215,412,316;28,1,1216,412,316;29,1,1222,410,313;30,1,1222,410,313;31,1,1233,407,309;32,1,1236,407,309;33,1,1239,404,305;34,1,1240,404,305;35,1,1249,402,303;36,1,1249,402,303;37,1,1255,400,301;38,1,1255,400,301;39,1,1265,399,300;40,1,1266,399,300;41,1,1271,398,299;42,1,1272,398,299;43,1,1283,397,298;44,1,1286,397,298;45,1,1287,397,298;46,1,1301,397,297;47,1,1303,397,297;48,1,1318,397,297;49,1,1319,397,297;50,1,1332,397,297;51,1,1332,397,297;52,1,1336,397,297;53,1,1337,397,297;54,1,1349,396,296;55,1,1352,396,296;56,1,1367,396,295;57,1,1371,395,293;58,1,1381,395,292;59,1,1384,394,290;60,1,1399,394,287;61,1,1403,392,285;62,1,1414,392,282;63,1,1416,391,280;64,1,1424,391,279;65,1,1425,391,279;66,1,1434,390,278;67,1,1434,390,278;68,1,1441,390,277;69,1,1442,390,277;70,1,1450,390,277;71,1,1451,390,277;72,1,1458,390,277;73,1,1459,390,277;74,1,1474,390,276;75,1,1475,390,276;76,1,1499,390,276;77,1,1499,390,276;78,3,1570,390,276,1103;79,4,1676,390,276,1103;80,2,1676,390,276,1103;81,1,1846,390,277;82,1,1847,390,277;83,1,1852,390,278;84,1,1853,390,278;85,1,1860,390,281;86,1,1861,390,281;87,1,1869,390,284;88,1,1870,390,284;89,1,1877,390,287;90,1,1878,390,287;91,1,1886,390,290;92,1,1887,390,290;93,1,1894,390,293;94,1,1894,390,293;95,1,1902,390,295;96,1,1903,390,295;97,1,1910,390,298;98,1,1912,390,298;99,1,1920,390,300;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,2,2624;3,4215;-1,2,-94,-112,https://www.zalando.fr/welcomenoaccount/true-1,2,-94,-115,NaN,212868,32,0,0,0,NaN,4825,0,1592594814181,30,17037,5,100,2839,2,0,4826,158474,0,532BDDF92D2792A84D6D104030676E0D~-1~YAAQL+x7XHoCl4RyAQAAJFsMzgQxUa6eRJ/ks9509lAH146yDbJhRzidCLZOUD8YcIwt5VMlKH9E5gL5nVGGA2kZDBn/WP7q3ijhG6TIEjzeR73Q5f6JxSgvZMCiRSy80sLppaVpERI1blHB1CwKtu+osvqd1Fvpo/0aMndGdm2FWAjEPxFM7G4KHVSvh0H7hWTeLzA8Jhm7Vplau+PfW8mPSXHP8TAOQkmj/CQottmRpsMZRq7JHYedpFnHgARYANo4maBb9V3+Z3/dZ9vRQ/W8gXjnJ6dZLN8g5JFJQvRxVLvpIlaQ949VUAHTckFxiyjfCD3+JZXygTJ3rkX+4yKofU0=~-1~-1~-1,31935,607,-1122583492,26018161,NVVO,124,-1-1,2,-94,-106,3,3-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,200,800,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,649914741-1,2,-94,-118,187600-1,2,-94,-121,;1;5;0"
        }
        session.headers["Accept"] = "*/*"
        session.headers["x-xsrf-token"] = cookies["frsx"]
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
            "x-xsrf-token": cookies["frsx"],
            "Accept-Language": "fr-fr",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.97 Safari/537.36",
            "Referer": "https://www.zalando.fr/welcomenoaccount/true",
            "x-flow-id": home.headers["X-Flow-Id"],
            "x-zalando-client-id": cookies["Zalando-Client-Id"],
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }
        identifiants = {
            "username": 'tom.challete@gmail.com',
            "password": 'w?CnM9Ww',
            "wnaMode": "checkout",
        }
        session.headers.update(headers_2)
        session.get(url_connexion_get, verify=False)
        session.headers["Origin"] = "https://www.zalando.fr"
        session.post(url_connexion_post2, json=identifiants, verify=False)
        session.get(url_checkout_1, verify=False)

    # Fermeture de la session
    session.close()


def VerificationArticle():
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

        # Mise à jour du headers
        session.headers["x-xsrf-token"] = cookies["frsx"]
        session.headers["x-zalando-client-id"] = cookies["Zalando-Client-Id"]
        session.headers["x-zalando-render-page-uri"] = "/"
        session.headers["x-zalando-request-uri"] = "/"
        session.headers["x-flow-id"] = home.headers["X-Flow-Id"]
        session.headers["Accept"] = "application/json"

        # Requetes anti-bot
        url_post_data1 = (
            "https://www.zalando.fr/resources/557a587d1e201d42d0a3ba96882c7b"
        )
        data1 = {
            "sensor_data": "7a74G7m23Vrp0o5c9176891.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391930,6614291,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.683202938341,796453307145.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,211,762,1;1,1,221,762,19;2,1,223,762,29;3,1,234,765,40;4,1,248,773,64;5,1,270,776,76;6,1,321,783,106;7,1,326,798,178;8,1,330,799,181;9,1,335,800,188;10,1,347,802,194;11,1,380,803,198;12,1,465,805,206;13,1,467,805,210;14,1,584,805,210;15,1,659,805,210;16,1,661,805,210;17,1,666,805,211;18,1,667,805,211;19,1,674,805,213;20,1,674,805,213;21,1,682,804,215;22,1,683,804,215;23,1,690,802,216;24,1,691,802,216;25,1,699,801,219;26,1,699,801,219;27,1,706,798,221;28,1,708,798,221;29,1,715,795,222;30,1,832,773,225;31,1,841,772,225;32,1,856,771,224;33,1,871,770,224;34,1,1121,770,223;35,1,1147,740,243;36,1,1425,712,212;37,1,1439,710,217;38,1,1443,710,219;39,1,1483,709,222;40,1,1593,701,239;41,1,1603,701,239;42,1,1639,701,239;43,1,1675,700,239;44,1,1697,700,239;45,1,1704,700,239;46,3,1752,700,239,-1;47,4,2006,700,239,-1;48,2,2006,700,239,-1;49,1,2166,700,239;50,1,2167,700,239;51,1,2170,699,237;52,1,2170,699,237;53,1,2178,697,233;54,1,2178,697,233;55,1,2188,695,231;56,1,2188,695,231;57,1,2195,694,229;58,1,2195,694,229;59,1,2203,693,227;60,1,2203,693,227;61,1,2211,692,226;62,1,2212,692,226;63,1,2219,689,222;64,1,2220,689,222;65,1,2227,685,219;66,1,2229,685,219;67,1,2237,683,216;68,1,2237,683,216;69,1,2243,682,215;70,1,2244,682,215;71,1,2251,680,213;72,1,2252,680,213;73,1,2258,679,212;74,1,2259,679,212;75,1,2267,678,210;76,1,2268,678,210;77,1,2275,677,210;78,1,2275,677,210;79,1,2284,676,210;80,1,2285,676,210;81,1,2292,675,209;82,1,2292,675,209;83,1,2299,675,209;84,1,2300,675,209;85,1,2307,675,209;86,1,2307,675,209;87,1,2316,675,208;88,1,2317,675,208;89,1,2324,674,208;90,1,2325,674,208;91,1,2342,674,208;92,1,2343,674,208;93,1,2347,674,208;94,1,2348,674,208;95,1,2363,674,208;96,1,2364,674,208;97,1,2371,673,208;98,1,2371,673,208;99,1,2387,673,208;100,1,2388,673,208;101,1,2413,673,208;102,1,2413,673,208;134,3,2681,671,218,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,465;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,1,269753,32,0,0,0,269721,2681,0,1592906614291,11,17040,0,135,2840,3,0,2682,167733,0,CEDFA92C631F235A19893F4D8FBB215E~-1~YAAQtKtkX+rEqcNyAQAA8wyi4ATu6Gl7b3N82og0BBhx45EL/91CglVPx/waxhCK7OF0Oi33DZ22ei7XasjwKlfmDyTH97Oi6UAMN1v7Gbdg4Y5ylD6Mzg8XS36C/CCCybXS9L+TUG7jxXtbmEgGnsK4itTCubBeaqiquQ/Y9sVSBupLyp18/BWC02iYA/3lCVyP7B3yP0DMMQPBZ4ikCS8R2kAzByKOhSyKFGsvLbv7ImcxDtlcYoboSbC2G7fyhhObig6yt037FvHdDvDAJEoVkuEqGSnHfsfIff593OYZVqoZvuJBrMbR8FlZ8SG7Pfu09cyJEZC1HS4UAUmKbm4yogE=~-1~-1~-1,32098,550,782898681,26018161,NWtO,124,-1-1,2,-94,-106,1,3-1,2,-94,-119,2000,200,0,0,0,0,0,0,0,2000,2600,600,800,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,99214506-1,2,-94,-118,180123-1,2,-94,-121,;1;3;0"
        }
        data2 = {
            "sensor_data": "7a74G7m23Vrp0o5c9176891.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391930,6614291,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.16559469682,796453307145.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,4569,undefined,0,0,1103,0;1,2,4580,undefined,0,0,1103,0;2,1,4621,undefined,0,0,1103,0;3,2,4627,undefined,0,0,1103,0;4,1,5015,13,0,0,1466;-1,2,-94,-110,0,1,211,762,1;1,1,221,762,19;2,1,223,762,29;3,1,234,765,40;4,1,248,773,64;5,1,270,776,76;6,1,321,783,106;7,1,326,798,178;8,1,330,799,181;9,1,335,800,188;10,1,347,802,194;11,1,380,803,198;12,1,465,805,206;13,1,467,805,210;14,1,584,805,210;15,1,659,805,210;16,1,661,805,210;17,1,666,805,211;18,1,667,805,211;19,1,674,805,213;20,1,674,805,213;21,1,682,804,215;22,1,683,804,215;23,1,690,802,216;24,1,691,802,216;25,1,699,801,219;26,1,699,801,219;27,1,706,798,221;28,1,708,798,221;29,1,715,795,222;30,1,832,773,225;31,1,841,772,225;32,1,856,771,224;33,1,871,770,224;34,1,1121,770,223;35,1,1147,740,243;36,1,1425,712,212;37,1,1439,710,217;38,1,1443,710,219;39,1,1483,709,222;40,1,1593,701,239;41,1,1603,701,239;42,1,1639,701,239;43,1,1675,700,239;44,1,1697,700,239;45,1,1704,700,239;46,3,1752,700,239,-1;47,4,2006,700,239,-1;48,2,2006,700,239,-1;49,1,2166,700,239;50,1,2167,700,239;51,1,2170,699,237;52,1,2170,699,237;53,1,2178,697,233;54,1,2178,697,233;55,1,2188,695,231;56,1,2188,695,231;57,1,2195,694,229;58,1,2195,694,229;59,1,2203,693,227;60,1,2203,693,227;61,1,2211,692,226;62,1,2212,692,226;63,1,2219,689,222;64,1,2220,689,222;65,1,2227,685,219;66,1,2229,685,219;67,1,2237,683,216;68,1,2237,683,216;69,1,2243,682,215;70,1,2244,682,215;71,1,2251,680,213;72,1,2252,680,213;73,1,2258,679,212;74,1,2259,679,212;75,1,2267,678,210;76,1,2268,678,210;77,1,2275,677,210;78,1,2275,677,210;79,1,2284,676,210;80,1,2285,676,210;81,1,2292,675,209;82,1,2292,675,209;83,1,2299,675,209;84,1,2300,675,209;85,1,2307,675,209;86,1,2307,675,209;87,1,2316,675,208;88,1,2317,675,208;89,1,2324,674,208;90,1,2325,674,208;91,1,2342,674,208;92,1,2343,674,208;93,1,2347,674,208;94,1,2348,674,208;95,1,2363,674,208;96,1,2364,674,208;97,1,2371,673,208;98,1,2371,673,208;99,1,2387,673,208;100,1,2388,673,208;101,1,2413,673,208;102,1,2413,673,208;134,3,2681,671,218,1103;135,4,2799,671,218,1103;136,2,2799,671,218,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,465;2,3689;3,4604;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,NaN,277406,32,0,0,0,NaN,5015,0,1592906614291,11,17040,5,143,2840,4,0,5016,196743,0,CEDFA92C631F235A19893F4D8FBB215E~-1~YAAQtKtkX/DEqcNyAQAAmBCi4AT8g4Cz62+qOUad8n7/NZFgbFy51CXnltt3yvuA4RVfp2XNNKTGF4fNyiTYZP6vnQvNpQRip3tLZmtqygrcddqmvaiB49808zOFCVwGgDs0Mm/h4kbTrDicok4ORHi+N96alsxijsWFJn2mU+4UGzaleuyyOE1wV9x1+Fw/UpHPTDiS/sGI3gjIcdIDglmuB4bdznaKrJjhnP1DRF1mATAbCfoe8vXZJqNVkzOUJF0yrYvtnARFftOGsxGs+PDE05Mw/bnnX9E5HpEni10atwAn9VavsKi+pdfo1lACq9R82w9bCrFE7yiBz9El5orRJlg=~-1~-1~-1,32960,550,782898681,26018161,NWtO,124,-1-1,2,-94,-106,3,4-1,2,-94,-119,2000,200,0,0,0,0,0,0,0,2000,2600,600,800,600,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,99214506-1,2,-94,-118,193109-1,2,-94,-121,;1;3;0"
        }
        session.headers["Accept"] = "*/*"
        session.headers["Content-Type"] = "text/plain;charset=UTF-8"
        del session.headers["x-xsrf-token"]
        session.headers["Content-Type"] = "text/plain;charset=UTF-8"
        session.post(url_post_data1, json=data1, verify=False)
        session.post(url_post_data1, json=data2, verify=False)

        # Connexion au compte Zalando
        url_connexion_get = "https://www.zalando.fr/api/reef/login/schema"
        url_connexion_post2 = "https://www.zalando.fr/api/reef/login"
        url_checkout_1 = "https://www.zalando.fr/myaccount"
        headers_2 = {
            "Host": "www.zalando.fr",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "x-zalando-request-uri": "/login/?view=login",
            "x-zalando-render-page-uri": "/login/?view=login",
            "x-xsrf-token": cookies["frsx"],
            "Accept-Language": "fr-fr",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.97 Safari/537.36",
            "Referer": "https://www.zalando.fr/welcomenoaccount/true",
            "x-flow-id": home.headers["X-Flow-Id"],
            "x-zalando-client-id": cookies["Zalando-Client-Id"],
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }
        identifiants = {
            "username": 'tom.challete@gmail.com',
            "password": 'w?CnM9Ww',
            "wnaMode": "shop",
        }
        session.headers.update(headers_2)
        session.get(url_connexion_get, verify=False)
        session.headers["Origin"] = "https://www.zalando.fr"
        session.post(url_connexion_post2, json=identifiants, verify=False)
        session.get(url_checkout_1, verify=False)

        # Accès au panier
        url_panier_1 = 'https://www.zalando.fr/cart'
        url_panier_2 = 'https://www.zalando.fr/api/navigation'
        url_panier_3 = 'https://www.zalando.fr/checkout/confirm'
        a = session.get(url_panier_1, verify=False)
        b = session.get(url_panier_2, verify=False)
        c = session.get(url_panier_3, verify=False)
        print(a.status_code)
        print(b.status_code)
        print(c.status_code)

    session.close()


MiseDansLePanier()
VerificationArticle()
