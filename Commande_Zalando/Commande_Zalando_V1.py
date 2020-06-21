import json

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as bs


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

        # Connexion à la page du produit
        url_produit = "https://www.zalando.fr/levisr-t-shirt-imprime-white-le226g005-a11.html"
        del session.headers['Upgrade-Insecure-Requests']
        session.get(url_produit, verify=False)

        # Envoie de requetes pour éviter les sécurités anti-bot
        url_get_1 = (
                'https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=1' % home.headers["X-Flow-Id"]
        )
        session.headers["Accept"] = "*/*"
        session.headers["x-xsrf-token"] = cookies["frsx"]
        session.get(url_get_1, verify=False)

        # Mise dans le panier
        url_panier = 'https://www.zalando.fr/api/pdp/cart'
        article = 'LE226G005-A11004A000'
        panier = {
            'simpleSku': article,
            'anonymous': False
        }
        session.headers["Accept"] = "application/json"
        session.headers["Content-Type"] = "application/json"
        session.post(url_panier, json=panier, verify=False)

        # Requetes anti-bot
        url_1 = 'https://www.zalando.fr/api/navigation/cart-count'
        url_2 = 'https://www.zalando.fr/api/cart/details'
        url_3 = 'https://www.zalando.fr/cart'
        url_post_data1 = 'https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b'
        url_4 = 'https://www.zalando.fr/checkout/confirm'
        data1 = {
            "sensor_data": "7a74G7m23Vrp0o5c9175921.59-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.2 Safari/605.1.15,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,391853,4809209,1440,900,1440,900,1440,862,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.970703120485,796297404604,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,-1,2407,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,-1,2407,0;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.zalando.fr/cart-1,2,-94,-115,1,32,32,0,0,0,0,1,0,1592594809208,-999999,17037,0,0,2839,0,0,2,0,0,532BDDF92D2792A84D6D104030676E0D~-1~YAAQL+x7XB4Cl4RyAQAAuD4MzgSx3Lv1ABbT/zOiBCoPbgw/BaVzFR5eZ51uxxL4OXmQwVusXrmmp0UQoY91EL8XZjGXZrMEVcbc6xs9RqNoPQT9cmEBDv6P7YDcyruKTOSfhsAg/woWK0b0ajzRcS3F1Dg2bZPIIsoK7d19YVZavIIDPCXt1sCGFl530XhBLlaCEKwtzHQfUSlhF3NQVd9SWOJ6WAvgyXp7mUGeObHiBoSF9sPgFIepOlHRzq0UZmssedn+bhEtz/0FJ/TRMiWS1AM6/gAtbIJwvCzTjnba/L6/uJgtimiQUyrkIuBGq4gAvPc8f9hJW6SIlR4mU+2fpt4=~-1~-1~-1,32514,-1,-1,26018161,NVVO,124,-1-1,2,-94,-106,0,0-1,2,-94,-119,-1-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,-1-1,2,-94,-80,94-1,2,-94,-116,14427678-1,2,-94,-118,82036-1,2,-94,-121,;1;-1;0"
        }
        session.headers["Accept"] = "*/*"
        del session.headers["Content-Type"]
        session.get(url_1, verify=False)
        session.get(url_2, verify=False)
        del session.headers["x-xsrf-token"]
        session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        session.get(url_3, verify=False)
        session.headers["Accept"] = "*/*"
        session.headers["Content-Type"] = "text/plain;charset=UTF-8"
        session.post(url_post_data1, json=data1, verify=False)
        session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        del session.headers["Content-Type"]
        session.get(url_4, verify=False)

        # Ouverture de la page de connexion
        url_connexion = 'https://www.zalando.fr/welcomenoaccount/true'
        session.get(url_connexion, verify=False)

        # Sécurité anti-bot
        url_get_2 = (
                'https://www.zalando.fr/api/rr/pr/sajax?flowId=%s&try=2' % home.headers["X-Flow-Id"]
        )
        url_post1 = "https://www.zalando.fr/resources/1f2f569be9201d42d0a3ba96882c7b"
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
        '''url_connexion_get = "https://www.zalando.fr/api/reef/login/schema"
        url_connexion_post2 = "https://www.zalando.fr/api/reef/login"
        url_checkout_1 = 'https://www.zalando.fr/checkout/confirm'
        url_checkout_2 = 'https://www.zalando.fr/checkout/address'
        url_checkout_3 = 'https://www.zalando.fr/api/checkout/search-pickup-points-by-address'
        '''
        
        url_one = "https://www.zalando.fr/welcomenoaccount/true"
        url_two = "https://www.zalando.fr/checkout/address"
        url_three = "https://checkout.payment.zalando.com/selection"
        
        headers_2 = {
            'Host': 'www.zalando.fr',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'x-zalando-request-uri': '/welcomenoaccount/true',
            'x-zalando-render-page-uri': '/welcomenoaccount/true',
            'x-xsrf-token': cookies["frsx"],
            'Accept-Language': 'fr-fr',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'Referer': 'https://www.zalando.fr/welcomenoaccount/true',
            'x-flow-id': home.headers["X-Flow-Id"],
            'x-zalando-client-id': cookies["Zalando-Client-Id"],
            'Connection': 'keep-alive',
            'Content-Type': 'application/json'
        }
        identifiants = {
            'username': 'tom.challete@gmail.com',
            'password': 'w?CnM9Ww',
            'wnaMode': 'checkout'
        }
        adresse = {
            'address': {
                'id': '',
                'salutation': 'Mr',
                'first_name': 'Tom',
                'last_name': 'Challete',
                'zip': '78490',
                'city': 'Garancieres',
                'country_code': 'FR',
                'street': '8 rue du general leclerc',
                'additional': ''
            }
        }

        #-------------------------------------------------------------Connexion--------------------------------------------------#
        
        session.headers.update(headers_2)
        sensor_one = {"sensor_data":"7a74G7m23Vrp0o5c9176431.59-1,2,-94,-100,Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0,uaend,11059,20100101,fr,Gecko,1,0,0,0,391899,256437,1536,864,1536,864,1536,455,1550,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:1,sc:0,wrc:1,isc:73.5999984741211,vib:1,bat:0,x11:0,x12:1,5563,0.18513671292,796390128218.5,loc:-1,2,-94,-101,do_en,dm_en,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,-1,2,-94,-110,0,1,695,70,12;1,1,712,189,90;2,1,730,274,142;3,1,746,378,196;4,1,764,534,269;5,1,778,634,315;6,1,827,751,366;7,1,828,770,374;8,1,845,778,379;9,1,861,781,383;10,1,878,779,385;11,1,1245,833,490;12,1,1512,846,542;13,1,1744,874,538;14,1,1761,929,534;15,1,1778,982,532;16,1,1794,1007,530;17,1,1812,1023,527;18,1,1828,1038,520;19,1,1845,1042,515;20,1,1861,1049,502;21,1,1878,1052,497;22,1,1895,1055,493;23,1,1912,1057,490;24,1,1928,1058,490;25,3,2752,1058,490,-1,3;26,4,2940,1058,490,-1,3;27,1,4826,1055,496;28,1,4845,1049,510;29,1,4862,1034,536;30,1,4879,1026,552;31,1,4895,1017,566;32,1,4911,1006,590;33,1,4928,1001,605;34,1,4945,995,616;35,1,4962,992,622;36,1,4978,990,625;37,1,4995,989,631;38,1,5012,988,634;39,1,5028,988,640;40,1,5045,988,644;41,1,5062,988,646;42,1,5078,988,650;43,1,5094,988,652;44,1,5112,989,653;45,1,5145,990,653;46,1,5161,991,653;47,1,5178,994,652;48,1,5195,998,650;49,1,5211,1014,647;50,1,5228,1027,646;51,1,5245,1046,651;52,1,5262,1052,656;53,1,5271,1057,658;54,1,7095,1074,679;55,1,7112,1042,650;56,1,7129,974,605;57,1,7145,910,569;58,1,7161,801,524;59,1,7178,723,504;60,1,7195,648,497;61,1,7212,556,499;62,1,7228,527,505;63,1,7244,502,514;64,1,7261,495,517;65,1,7278,491,519;66,1,7295,490,523;67,1,7311,490,524;68,1,7328,490,525;69,1,7345,490,527;70,1,7361,490,528;71,1,7379,490,530;72,1,7395,490,532;73,1,7411,488,534;74,1,7428,486,535;75,1,7445,485,536;76,1,7461,484,537;77,1,7478,482,538;78,1,7495,476,542;79,1,7512,464,550;80,1,7529,458,554;81,1,7545,453,557;82,1,7561,450,559;83,3,8336,450,559,-1,3;84,4,8502,450,559,-1,3;85,1,9101,450,559;86,1,9112,451,559;87,1,9128,457,558;88,1,13011,494,566;89,1,13029,543,603;90,1,13044,604,636;91,1,13062,704,682;92,1,13079,835,728;93,1,13095,911,749;94,1,13104,942,757;95,1,13412,1094,761;96,1,13428,1182,740;97,1,13446,1336,713;98,1,13463,1417,705;99,1,13479,1468,705;100,1,13496,1502,705;101,1,13512,1510,705;102,1,13529,1513,705;103,1,13578,1513,706;173,3,18590,1166,500,-1,3;174,4,18764,1166,500,-1,3;297,3,38687,563,425,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,2,6054;3,8339;2,9897;3,17251;2,21424;-1,2,-94,-112,https://www.zalando.fr/welcomenoaccount/true-1,2,-94,-115,1,874844,32,0,0,0,874812,38687,0,1592780256437,7,17039,0,298,2839,7,0,38688,721006,0,B5CDF9F2189AC166430F432BC127478E~-1~YAAQJVNzaMu08KtyAQAA1Dca2QT05mHNQHolKq5pS/TTPISxlD4mau1hPheAXDoAOlxGbaHENnhQh8FMufhO0Q3Qux83MwEkdFgpCShq+6/7tQ0Pi8vG7TgJCqKUY5k984d0o9/fVN1xtVp7y/YBtobztns6Rg2xaLh+YlzvXSutMKUcA+aCA4BV8uxmJW5kIi7Az5oQnb5viZ6tVpo49vr6RIVyku32KVgYjiy9tBfg1ADGaCBE1fWsZZ/+weraYUsy/jQ/PY0LIybW9PL9VUl9UaZaIS14Ir+AzxUAwSwCn74FsOmQeXg+ufVQSFwKWR6ZML2ZDXahDUE9aak3SMICcBA=~-1~-1~-1,32193,110,1573915736,26067385,NWNN,124,-1-1,2,-94,-106,1,5-1,2,-94,-119,200,200,0,200,0,0,200,200,0,0,200,600,400,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,11133333331333333333-1,2,-94,-70,1436327638;1247333925;dis;,3;true;true;true;-120;true;24;24;true;false;unspecified-1,2,-94,-80,6550-1,2,-94,-116,3846372-1,2,-94,-118,188987-1,2,-94,-121,;2;3;0"}
        session.get(url_one, verify=False)
        session.headers["Origin"] = "https://www.zalando.fr"
        
        r= session.post(url_one, json=identifiants)
        #session.get(url_checkout_1, verify=False)

        print(r)
        
        
        #--------------------------------------------------------------------Adressse------------------------------------------------#
        
        '''session.get(url_checkout_2, verify=False)

        sensor_data_3 = {"sensor_data":"7a74G7m23Vrp0o5c9176431.59-1,2,-94,-100,Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0,uaend,11059,20100101,fr,Gecko,1,0,0,0,391899,9504254,1536,864,1536,864,1536,365,1550,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:1,sc:0,wrc:1,isc:73.5999984741211,vib:1,bat:0,x11:0,x12:1,5563,0.567790538283,796389752127,loc:-1,2,-94,-101,do_en,dm_en,t_dis-1,2,-94,-105,-1,2,-94,-102,0,-1,0,0,-1,-1,1;-1,2,-94,-108,-1,2,-94,-110,0,1,2166,514,105;1,1,2182,448,126;2,1,2199,385,160;3,1,2216,286,216;4,1,2233,179,277;5,1,2249,105,318;6,1,2265,69,338;7,1,2282,45,348;8,1,2299,39,350;9,1,2316,38,351;10,1,2333,38,352;11,1,2593,37,356;12,1,2599,36,359;13,1,3849,132,358;14,1,3866,289,328;15,1,3883,417,325;16,1,3899,518,329;17,1,3915,646,343;18,1,3933,687,350;19,1,3949,710,354;20,1,3966,714,354;21,1,4233,743,319;22,1,4249,776,291;23,1,4266,834,265;24,1,4282,874,258;25,1,4299,911,257;26,1,4315,926,260;27,1,4333,933,262;28,1,4349,936,264;29,1,4366,937,264;30,1,4400,938,265;31,3,5672,938,265,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,2,3240;-1,2,-94,-112,https://www.zalando.fr/checkout/address-1,2,-94,-115,1,135963,32,0,0,0,135931,5672,0,1592779504254,10,17039,0,32,2839,1,0,5672,109956,0,B5CDF9F2189AC166430F432BC127478E~-1~YAAQj9t6XJUgmsRyAQAAEncO2QQ4ENloRaR83IuVzK1aknanbK6/KievQAwYe14rLEC0XalUX8f998l0d0Kwr8GF1ijoxXWPBCR5OhauF17AzavmT+1jADboxCQ8RnHiqkFrqYCO2/rKMEYklbJdXxOuK+sAVXcDy/ToTNz7pxmMcC3gP/8EHVyzwc3igsMBWo3A7aDW+qehO+3Hzs6hGWhCnPD3fm/yVi+fgPNvJMPik8XCae9p+G/xqRMHkwNNnXj1KKRX+XchkaW4HrefLNQyuTFlGF1K7MXMm320IHKeW9kUA4hPmXI5+zBiamn9aSdteNuIdMNZNsuWZf8XTBmYAzs=~-1~-1~-1,32405,307,645824617,26067385,NWNP,124,-1-1,2,-94,-106,1,2-1,2,-94,-119,200,0,0,0,200,0,0,0,0,0,0,200,600,0,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,11133333331333333333-1,2,-94,-70,1436327638;1247333925;dis;,3;true;true;true;-120;true;24;24;true;false;unspecified-1,2,-94,-80,6550-1,2,-94,-116,712819095-1,2,-94,-118,110282-1,2,-94,-121,;0;4;0"}
        a = session.post(url_checkout_2, headers= headers_2, json = sensor_data_3, verify= False)
        
        print(a)'''
        


checkout()
