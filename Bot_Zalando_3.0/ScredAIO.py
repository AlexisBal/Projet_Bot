import json
import time
import timeit
import re
import random
from threading import Thread
from colorama import Fore, Style, init

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
from licensing.models import *
from licensing.methods import Key, Helpers
from datetime import datetime
from datetime import date
from discord_webhook import DiscordWebhook, DiscordEmbed
from pypresence import Presence


# Réglage des "Timeouts"
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 8
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
retries = Retry(total=3, backoff_factor=0, status_forcelist=[429, 500, 502, 503, 504])

# Désactivation des messages d'avertissement
urllib3.disable_warnings()


# Tasks
class RechercheCommande(Thread):
    def __init__(self, liste_proxys, List_profile, Liste_compte, url_produit,
                 taille_produit, Paiement, Mode, Task, List_Quick_Task, quantite):
        Thread.__init__(self)
        self.liste_proxys = liste_proxys
        self.Liste_profile = List_profile
        self.Liste_compte = Liste_compte
        self.url_produit = url_produit
        self.taille_produit = taille_produit
        self.Paiement = Paiement
        self.Mode = Mode
        self.Task = Task
        self.List_Quick_Task = List_Quick_Task
        self.quantite = quantite

    def run(self):
        try:
            # Choix du compte
            Liste_Compte = self.Liste_compte
            Task = self.Task
            compte = Liste_Compte[Task]

            # Choix au hasard d'un profil
            profil = self.Liste_profile

            # Identifiants
            if self.Mode == 'Quick':
                phone = self.List_Quick_Task[3].strip('\n').lstrip('"').rstrip('"')
                if phone[0] != '0':
                    phone = '0' + phone
                numero = self.List_Quick_Task[11].strip('\n').lstrip('"').rstrip('"')
                numerobis = numero[0] + numero[1] + numero[2] + numero[3] + " " + numero[4] + numero[5] + \
                            numero[6] + numero[7] + " " + numero[8] + numero[9] + numero[10] + numero[
                                11] + " " + numero[12] + numero[13] + numero[14] + numero[15] + " "
                data_cb = {
                    "card_holder": self.List_Quick_Task[10].strip('\n').lstrip('"').rstrip('"'),
                    "pan": numerobis,
                    "cvv": self.List_Quick_Task[14].strip('\n').lstrip('"').rstrip('"'),
                    "expiry_month": self.List_Quick_Task[12].strip('\n').lstrip('"').rstrip('"'),
                    "expiry_year": self.List_Quick_Task[13].strip('\n').lstrip('"').rstrip('"'),
                    "options": {
                        "selected": [],
                        "not_selected": ["store_for_reuse"],
                    },
                }
            else:
                phone = profil[2].strip('\n').lstrip('"').rstrip('"')
                if phone[0] != '0':
                    phone = '0' + phone
                numero = profil[10].strip('\n').lstrip('"').rstrip('"')
                numerobis = numero[0] + numero[1] + numero[2] + numero[3] + " " + numero[4] + numero[5] + \
                            numero[6] + numero[7] + " " + numero[8] + numero[9] + numero[10] + numero[
                                11] + " " + numero[12] + numero[13] + numero[14] + numero[15] + " "
                data_cb = {
                    "card_holder": profil[9].strip('\n').lstrip('"').rstrip('"'),
                    "pan": numerobis,
                    "cvv": profil[13].strip('\n').lstrip('"').rstrip('"'),
                    "expiry_month": profil[11].strip('\n').lstrip('"').rstrip('"'),
                    "expiry_year": profil[12].strip('\n').lstrip('"').rstrip('"'),
                    "options": {
                        "selected": [],
                        "not_selected": ["store_for_reuse"],
                    },
                }

            # Reglage du pays
            if self.Mode == 'Normal':
                Pays = profil[8].upper().lstrip('"').rstrip('"')
            else:
                Pays = self.List_Quick_Task[9].upper().lstrip('"').rstrip('"')
            if Pays == 'FR':
                site = 'https://www.zalando.fr'
            if Pays == 'CH':
                site = 'https://fr.zalando.ch'
            if Pays == 'BE':
                site = 'https://fr.zalando.be'
            if Pays == 'LU':
                site = 'https://fr.zalando.be/?clu=1'
            if Pays == 'DE':
                site = 'https://www.zalando.de'
            if Pays == 'AT':
                site = 'https://www.zalando.at'
            if Pays == 'NL':
                site = 'https://www.zalando.nl'
            if Pays == 'IT':
                site = 'https://www.zalando.it'
            if Pays == 'UK':
                site = 'https://www.zalando.co.uk'
            if Pays == 'ES':
                site = 'https://www.zalando.es'
            if Pays == 'SE':
                site = 'https://www.zalando.se'
            if Pays == 'DK':
                site = 'https://www.zalando.dk'
            if Pays == 'NO':
                site = 'https://www.zalando.no'
            if Pays == 'FI':
                site = 'https://www.zalando.fi'
            if Pays == 'PL':
                site = 'https://www.zalando.pl'

            payslist = ['FR', 'CH', 'BE', 'LU', 'DE', 'AT', 'NL', 'IT', 'UK', 'ES', 'SE', 'DK', 'NO', 'FI', 'PL']
            if Pays not in payslist:
                print(Fore.RED + 'Wrong country code !')
                print(Fore.YELLOW + 'Country code accepted :')
                print(Fore.YELLOW + 'FR, CH, BE, LU, DE, AT, NL, IT, UK, ES, SE, DK, NO, FI, PL')
                time.sleep(5)
                main()

            # Récupération du Sku
            while True:
                try:
                    headers = {
                        "User-Agent": generate_user_agent()
                    }
                    url = self.url_produit
                    requete_1 = requests.get(url, headers=headers, verify=False, allow_redirects=False)
                    soup_1 = BeautifulSoup(requete_1.content, "html.parser")
                    reponse_1 = soup_1.find(type="application/json", class_="re-1-1")
                    print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                          Style.RESET_ALL + "> Task %s - " % self.Task + Fore.RED + "Searching Product")
                    if reponse_1 is not None:
                        reponsebis_1 = reponse_1.contents
                        reponsebis2_1 = json.loads(reponsebis_1[0])
                        id_produit = reponsebis2_1['enrichedEntity']['id']
                        sku_list = reponsebis2_1['graphqlCache'][
                            '{"id":"060d7dee025024237a02b73f6e4436f4e57fdffb20016dc5fa67e817b5a2d682","variables":{"id":"%s"}}' % id_produit][
                            'data']['product']['simples']
                        link_photo = reponsebis2_1['graphqlCache'][
                            '{"id":"060d7dee025024237a02b73f6e4436f4e57fdffb20016dc5fa67e817b5a2d682","variables":{"id":"%s"}}' % id_produit][
                            'data']['product']['galleryThumbnails'][0]['uri']
                        name_product = reponsebis2_1['graphqlCache'][
                            '{"id":"060d7dee025024237a02b73f6e4436f4e57fdffb20016dc5fa67e817b5a2d682","variables":{"id":"%s"}}' % id_produit][
                            'data']['product']['name']
                        liste_sku = []
                        for n in range(0, len(sku_list)):
                            liste_sku.append(sku_list[n]['sku'])
                            liste_sku.append(sku_list[n]['size'])
                        position_taille = liste_sku.index(self.taille_produit.strip('\n').lstrip('"').rstrip('"'))
                        sku = liste_sku[position_taille - 1]
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> Task %s - " % self.Task + Fore.YELLOW + "Product Found")
                        break

                except:
                    print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                          Style.RESET_ALL + "> Task %s - " % self.Task + Fore.RED + 'There is a problem with the Sku !')
                    time.sleep(5)
                    main()

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
                    position_sku = liste_stock.index(sku)
                    stock_schema = liste_stock[position_sku + 1]
                    if stock_schema == 'http://schema.org/InStock':
                        break
                    else:
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> Task %s - " % self.Task + Fore.YELLOW + "Product out of stock - "
                                                                                           "Waiting for restock")
                        time.sleep(0.2)

            # Mise dans le panier du produit
            # Ouverture de la Session
            with requests.Session() as session:
                # Réglage des paramètres de la session
                session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))

                while True:
                    # Réglage du proxy
                    proxy = random.choice(self.liste_proxys)
                    diversion_1 = random.choice(['https://www.bing.com/',
                                                 'https://www.google.com/',
                                                 'https://duckduckgo.com',
                                                 'https://fr.yahoo.com/'
                                                 ])
                    headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        'User-Agent': generate_user_agent(),
                        "Accept-Language": "fr-fr",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Referer": diversion_1
                    }
                    diversion = random.choice(['https://www.zalando.fr/accueil-homme/',
                                               'https://www.zalando.fr/tiger-of-sweden-joran-sandales-dark-brown'
                                               '-ti512g002-o11.html',
                                               'https://www.zalando.fr/accueil-luxe-homme/',
                                               'https://www.zalando.fr/mode-homme/',
                                               'https://www.zalando.fr/pulls-gilets-homme/',
                                               'https://www.zalando.fr/accueil-femme/',
                                               'https://www.zalando.fr/mode-femme/',
                                               'https://www.zalando.fr/baskets-femme/',
                                               'https://www.zalando.fr/promo-femme/',
                                               'https://www.zalando.fr/soutien-gorge-femme/',
                                               'https://www.zalando.fr/chaussures-femme/'])
                    diversion_2 = 'https://www.zalando.fr/chaussures-homme/'
                    if len(proxy) == 4:
                        try:
                            session.proxies = {
                                "https": "https://%s:%s@%s:%s/" % (proxy[2], proxy[3], proxy[0], proxy[1])}
                            # Connexion à la page d'accueil de Zalando
                            session.headers.update(headers)
                            session.get(site, verify=False, timeout=0.5)
                        except:
                            session.proxies = {"http": "http://%s:%s@%s:%s/" % (proxy[2], proxy[3], proxy[0], proxy[1])}
                            # Connexion à la page d'accueil de Zalando
                            session.headers.update(headers)
                            session.get(site, verify=False)

                    else:
                        try:
                            session.proxies = {"https": "https://%s" % (proxy[0] + proxy[1])}
                            # Connexion à la page d'accueil de Zalando
                            session.headers.update(headers)
                            session.get(site, verify=False, timeout=0.5)
                        except:
                            session.proxies = {"http": "http://%s" % (proxy[0] + proxy[1])}
                            # Connexion à la page d'accueil de Zalando
                            session.headers.update(headers)
                            session.get(site, verify=False)

                    if session.cookies != '<RequestsCookieJar[]>':
                        session.headers['Referer'] = 'https://www.zalando.fr/'
                        session.get(diversion, verify=False)
                        session.headers['Referer'] = diversion
                        session.get(diversion_2, verify=False)
                        # Connexion à la page du produit
                        session.headers['Referer'] = diversion_2
                        login = session.get(self.url_produit, verify=False)
                        break

                # Lancement du chronomètre
                start_chrono = timeit.default_timer()

                # Récupération des cookies de la session
                cookies_2 = session.cookies.get_dict()

                # Connexion au compte
                url_bot_2 = "%s/resources/da6ea05bf5rn2028b315fc23b805e921" % site
                urlconex = 'https://www.zalando.fr/api/t/i'
                url_connexion_2 = "%s/api/reef/login/schema" % site
                url_connexion_3 = "%s/api/reef/login" % site
                data1_2 = {
                    "sensor_data": "7a74G7m23Vrp0o5c9185761.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392716,928274,1440,877,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.04270993621,798050464137,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1082,-1,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1082,-1,0;-1,2,-94,-108,-1,2,-94,-110,0,1,5,780,307;1,1,594,852,322;2,1,835,1027,242;3,1,848,1043,385;4,1,849,1041,391;5,1,935,1040,393;6,1,946,1033,401;7,1,1004,1033,401;8,1,1012,1029,404;9,1,1021,1028,405;10,1,1110,1026,406;11,1,1114,1014,419;12,1,1116,1013,420;13,1,1150,1012,422;14,1,1195,1008,426;15,1,1269,1003,432;16,1,1271,991,434;17,1,1326,989,434;18,1,1385,967,410;19,1,1396,959,314;20,1,1707,966,305;21,1,1724,1079,442;22,1,1726,1072,444;23,1,1730,1069,445;24,1,2080,1066,446;25,1,2087,1024,481;26,1,2146,1024,481;27,1,2160,1024,481;28,1,2502,1024,482;29,1,2589,1024,483;30,1,2596,1024,483;31,1,3252,1024,483;32,1,3265,1084,56;33,1,3285,1085,59;34,1,3291,1085,62;35,1,3427,1085,63;36,1,3430,1086,65;37,1,3502,1086,65;38,1,3504,1086,65;39,1,3795,1086,65;40,1,3881,1082,113;41,1,3956,1082,116;42,1,4035,1081,116;43,1,4110,1081,117;44,1,4429,1081,120;45,1,4506,1080,120;46,1,5013,1080,120;47,1,5015,1080,120;48,1,11328,1080,120;49,1,11332,1080,120;50,1,16706,1080,121;51,1,16709,1080,121;52,1,16712,1080,124;53,1,16718,1080,126;54,1,16720,1080,126;55,1,16726,1080,129;56,1,16727,1080,129;57,1,16734,1080,132;58,1,16735,1080,132;59,1,16747,1080,137;60,1,16749,1080,137;61,1,16751,1081,144;62,1,16759,1082,151;63,1,16761,1082,151;64,1,16766,1083,158;65,1,16767,1083,158;66,1,16779,1083,161;67,1,16780,1083,161;68,1,16787,1084,168;69,1,16795,1085,174;70,1,16799,1086,179;71,1,16803,1086,179;72,1,16807,1087,184;73,1,16813,1087,184;74,1,16815,1088,188;75,1,16822,1090,192;76,1,16827,1090,192;77,1,16831,1091,197;78,1,16831,1091,197;79,1,16839,1093,205;80,1,16844,1093,205;81,1,16847,1094,210;82,1,16848,1094,210;83,1,16855,1095,215;84,1,16861,1095,215;85,1,16863,1097,221;86,1,16863,1097,221;87,1,16872,1098,228;88,1,16873,1098,228;89,1,16879,1099,234;90,1,16880,1099,234;91,1,16887,1100,237;92,1,16888,1100,237;93,1,16896,1102,244;94,1,16897,1102,244;95,1,16905,1103,250;96,1,16906,1103,250;97,1,16911,1103,254;98,1,16912,1103,254;99,1,16920,1104,259;333,3,21741,985,479,-1;334,4,21992,985,479,-1;335,2,21992,985,479,-1;486,3,36533,1001,313,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,%s-1,2,-94,-115,1,1217637,32,0,0,0,1217605,36533,0,1596100928274,21,17074,0,487,2845,3,0,36534,1074764,0,8666435BCB20333DA4708699A3C8C57F~-1~YAAQHVNzaDPjQ4lzAQAAQrgHnwRg5DADyLhio7a9BiGqUvXeCxBA3NWskTMZ1jvRMLOHri5/vyI9dnA3MZYxEAXVz6iAv6SncI51P+6UWGSZauTb/r8umDjnkG6NRe6f/6EZxAhyiaK/wmfkbpz6Dw2YU6HVsEudpL/765TzzP5oYSWXiB537rU8rYvFzTT5NHTH/ktQtQztKLKRSqSrMkGAzBG7TWJOlrNYRVPHAyRGgqqfh61QUD9n6X7FOkdUvDd7MK/NdLDu/UmvgFcuQ2eJzLwflmQP+vu4UcWvyGMJ+qxNfX2VyZ33aFeahrOEry6mtNUeFGhFlc1SEiCoc08sti8=~-1~-1~-1,32707,992,-1522636444,26018161,PiZtE,38400,80-1,2,-94,-106,1,3-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,0,200,400,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,125316684-1,2,-94,-118,190375-1,2,-94,-121,;2;4;0" % (
                        session.headers["User-Agent"], self.url_produit)
                }
                data2_2 = {
                    "sensor_data": "7a74G7m23Vrp0o5c9185761.6-1,2,-94,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392716,928274,1440,877,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.11380621956,798050464137,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1082,-1,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1082,-1,0;0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,45247,undefined,0,0,1103,0;1,2,45250,undefined,0,0,1103,0;2,1,45277,undefined,0,0,1103,0;3,2,45280,undefined,0,0,1103,0;-1,2,-94,-110,0,1,5,780,307;1,1,594,852,322;2,1,835,1027,242;3,1,848,1043,385;4,1,849,1041,391;5,1,935,1040,393;6,1,946,1033,401;7,1,1004,1033,401;8,1,1012,1029,404;9,1,1021,1028,405;10,1,1110,1026,406;11,1,1114,1014,419;12,1,1116,1013,420;13,1,1150,1012,422;14,1,1195,1008,426;15,1,1269,1003,432;16,1,1271,991,434;17,1,1326,989,434;18,1,1385,967,410;19,1,1396,959,314;20,1,1707,966,305;21,1,1724,1079,442;22,1,1726,1072,444;23,1,1730,1069,445;24,1,2080,1066,446;25,1,2087,1024,481;26,1,2146,1024,481;27,1,2160,1024,481;28,1,2502,1024,482;29,1,2589,1024,483;30,1,2596,1024,483;31,1,3252,1024,483;32,1,3265,1084,56;33,1,3285,1085,59;34,1,3291,1085,62;35,1,3427,1085,63;36,1,3430,1086,65;37,1,3502,1086,65;38,1,3504,1086,65;39,1,3795,1086,65;40,1,3881,1082,113;41,1,3956,1082,116;42,1,4035,1081,116;43,1,4110,1081,117;44,1,4429,1081,120;45,1,4506,1080,120;46,1,5013,1080,120;47,1,5015,1080,120;48,1,11328,1080,120;49,1,11332,1080,120;50,1,16706,1080,121;51,1,16709,1080,121;52,1,16712,1080,124;53,1,16718,1080,126;54,1,16720,1080,126;55,1,16726,1080,129;56,1,16727,1080,129;57,1,16734,1080,132;58,1,16735,1080,132;59,1,16747,1080,137;60,1,16749,1080,137;61,1,16751,1081,144;62,1,16759,1082,151;63,1,16761,1082,151;64,1,16766,1083,158;65,1,16767,1083,158;66,1,16779,1083,161;67,1,16780,1083,161;68,1,16787,1084,168;69,1,16795,1085,174;70,1,16799,1086,179;71,1,16803,1086,179;72,1,16807,1087,184;73,1,16813,1087,184;74,1,16815,1088,188;75,1,16822,1090,192;76,1,16827,1090,192;77,1,16831,1091,197;78,1,16831,1091,197;79,1,16839,1093,205;80,1,16844,1093,205;81,1,16847,1094,210;82,1,16848,1094,210;83,1,16855,1095,215;84,1,16861,1095,215;85,1,16863,1097,221;86,1,16863,1097,221;87,1,16872,1098,228;88,1,16873,1098,228;89,1,16879,1099,234;90,1,16880,1099,234;91,1,16887,1100,237;92,1,16888,1100,237;93,1,16896,1102,244;94,1,16897,1102,244;95,1,16905,1103,250;96,1,16906,1103,250;97,1,16911,1103,254;98,1,16912,1103,254;99,1,16920,1104,259;333,3,21741,985,479,-1;334,4,21992,985,479,-1;335,2,21992,985,479,-1;486,3,36533,1001,313,-1;487,4,36539,1001,313,-1;488,2,36539,1001,313,-1;581,3,38397,1100,134,-1;582,4,38418,1100,134,-1;583,2,38422,1100,134,-1;689,3,46032,751,480,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,2,44073;3,45258;-1,2,-94,-112,%s-1,2,-94,-115,NaN,1462973,32,0,0,0,NaN,46032,0,1596100928274,21,17074,4,690,2845,7,0,46034,1490165,0,8666435BCB20333DA4708699A3C8C57F~-1~YAAQHVNzaKXlQ4lzAQAASvkHnwQYDMPH11YUvY5tLbpJ+rdUW5mJgr1iadePzYqvoU5UI95OGrwQ8jpm/7YMTXMe+warhVQztddAokahCSUa/UDakUAsmMWLnRnQpFZeGdYROZMuGXFf0pTz8eUxi9vWRgBMgQi+IOWz+M4BimE/RSZRZwKHdTuH4skBjZdPm7UDSCEdGJvOEcwKECkdsInbfCil7K3TQhI8+jGvCZN7hihG9Nzx6hj43Mzap1PzUOuca50ApNswkV1bI8+aHExUI/XmHs/3BYjS10By9XLd05n9Wngg3VGNnVHtWN+FwALdnG8443vRARMzIvcspvP7du0=~-1~-1~-1,32628,992,-1522636444,26018161,PiZtE,27368,80-1,2,-94,-106,1,5-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,0,200,400,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,125316684-1,2,-94,-118,208506-1,2,-94,-121,;2;4;0" % (
                        session.headers["User-Agent"], self.url_produit)
                }
                identifiants_2 = {
                    "username": compte[0].strip('\n').lstrip('"').rstrip('"'),
                    "password": compte[1].strip('\n').lstrip('"').rstrip('"'),
                    "wnaMode": "modal"
                }
                session.headers.update({
                    "Accept": "*/*",
                    "Content-Type": "text/plain;charset=UTF-8",
                    "Origin": site,
                    "Referer": self.url_produit
                })
                session.post(url_bot_2, json=data1_2, verify=False)
                session.post(url_bot_2, json=data2_2, verify=False)
                del session.headers["Origin"]
                session.headers.update({
                    "x-xsrf-token": cookies_2["frsx"],
                    "x-zalando-client-id": cookies_2["Zalando-Client-Id"],
                    "x-zalando-render-page-uri": self.url_produit.replace(site, ""),
                    "x-zalando-request-uri": self.url_produit.replace(site, ""),
                    "x-flow-id": login.headers["X-Zalando-Child-Request-Id"],
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Referer": self.url_produit
                })
                session.get(url_connexion_2, verify=False)
                session.headers["Origin"] = site
                connex = session.post(url_connexion_3, json=identifiants_2, verify=False)
                del session.headers["x-xsrf-token"]
                del session.headers["x-zalando-client-id"]
                del session.headers["x-zalando-render-page-uri"]
                del session.headers["x-zalando-request-uri"]
                del session.headers["x-flow-id"]
                del session.headers["Content-Type"]
                del session.headers["Origin"]

                if connex.status_code == 201:
                    print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                          Style.RESET_ALL + "> Task %s - " % self.Task + Fore.GREEN + "Account successfully logged")
                else:
                    print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                          Style.RESET_ALL + "> Task %s - " % self.Task + Fore.RED + "There is a problem with this "
                                                                                    "account. Stop the program and "
                                                                                    "try later !")
                    time.sleep(5)
                    main()

                # Connexion à la page du produit
                session.headers.update({
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Referer": self.url_produit
                })
                page_produit = session.get(self.url_produit, verify=False)
                impression = page_produit.headers['x-page-impression-id']

                # Mise dans le panier
                for quantite in range(0, int(self.quantite)):
                    url_bot_panier = '%s/resources/7be100d4c6rn2028b315fc23b805e921' % site
                    url_panier = "%s/api/graphql/" % site
                    bot_panier = {
                        'sensor_data': '7a74G7m23Vrp0o5c9183031.6-1,2,-94,-100,%s,uaend,11011,20030107,fr-fr,Gecko,1,0,0,0,392572,4143776,1440,900,1440,900,1440,353,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8824,0.896028632448,797757071888,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,926,-1,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,926,-1,0;-1,2,-94,-108,-1,2,-94,-110,0,1,47,981,8;1,1,6967,780,829;2,1,6976,1029,672;3,1,6979,1116,630;4,1,6995,1190,595;5,1,7005,1294,547;6,1,7016,1347,522;7,1,7027,1413,486;8,1,7227,1438,509;9,1,7373,1410,539;10,1,7390,1194,672;11,1,7669,1180,672;12,1,7724,1100,654;13,1,7749,1099,652;14,3,7954,1099,652,-1;15,4,8045,1099,652,-1;16,2,8045,1099,652,-1;17,1,8428,1099,862;18,1,9488,1099,862;19,1,9491,1098,863;20,1,9495,1098,865;21,1,9496,1098,865;22,1,9504,1097,865;23,1,9505,1097,865;24,1,9512,1096,866;25,1,9513,1096,866;26,1,9521,1095,867;27,1,9523,1095,867;28,1,9528,1094,868;29,1,9529,1094,868;30,1,9535,1094,869;31,1,9536,1094,869;32,1,9545,1092,870;33,1,9546,1092,870;34,1,9553,1091,871;35,1,9555,1091,871;36,1,9560,1090,873;37,1,9561,1090,873;38,1,9569,1087,875;39,1,9570,1087,875;40,1,9578,1085,877;41,1,9579,1085,877;42,1,9587,1081,880;43,1,9589,1081,880;44,1,9592,1080,880;45,1,9593,1080,880;46,1,9603,1073,885;47,1,9605,1073,885;48,1,9609,1069,888;49,1,9610,1069,888;50,1,9619,1063,892;51,1,9621,1063,892;52,1,9626,1056,896;53,1,9627,1056,896;54,1,9633,1048,901;55,1,9635,1048,901;56,1,9642,1041,904;57,1,9643,1041,904;58,1,9653,1034,909;59,1,9654,1034,909;60,1,9657,1026,913;61,1,9658,1026,913;62,1,9667,1023,914;63,1,9668,1023,914;64,1,9675,1016,917;65,1,9676,1016,917;66,1,9683,1012,918;67,1,9685,1012,918;68,1,9689,1006,920;69,1,9690,1006,920;70,1,9698,1002,920;71,1,9699,1002,920;72,1,9707,998,921;73,1,9708,998,921;74,1,9717,993,922;75,1,9719,993,922;76,1,9721,989,922;77,1,9722,989,922;78,1,9734,986,922;79,1,9735,986,922;80,1,9738,982,922;81,1,9739,982,922;82,1,9748,979,922;83,1,9750,979,922;84,1,9754,975,922;85,1,9755,975,922;86,1,9763,972,922;87,1,9764,972,922;88,1,9772,969,922;89,1,9773,969,922;90,1,9781,966,922;91,1,9783,966,922;92,1,9786,964,922;93,1,9787,964,922;94,1,9795,962,922;95,1,9796,962,922;96,1,9802,959,922;97,1,9803,959,922;98,1,9814,958,922;99,1,9816,958,922;100,1,9819,957,922;101,1,9828,955,922;102,1,9829,955,922;115,3,10159,953,923,-1;116,4,10252,953,923,-1;117,2,10252,953,923,-1;257,3,15150,967,660,-1;258,4,15279,967,660,-1;259,2,15279,967,660,-1;299,3,15937,948,935,-1;300,4,16087,948,935,-1;301,2,16088,948,935,-1;398,3,17326,924,653,-1;400,4,17453,924,653,-1;401,2,17454,924,653,-1;529,3,18354,895,813,-1;530,4,18490,895,813,-1;531,2,18490,895,813,-1;589,3,20264,936,732,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,7959;2,11828;3,15163;-1,2,-94,-112,%s/nike-sportswear-alpha-lite-baskets-basses-ni112o0am-c12.html-1,2,-94,-115,1,1434238,32,0,0,0,1434206,20264,0,1595514143776,29,17068,0,590,2844,13,0,20265,1199766,0,5A6236607E448865D7A432CE144FFDF5~-1~YAAQDOx7XNW7gy9zAQAA3AsOfAQdvNnRmPRtGD+Vbnvwj9sl5cWYzej2Z67I1GWl8oNQE+QRbxUAmccc7C4f/ocpHtggywIKYwIjTVW3cKwSMI7nafnSkUHDdovf3E7uuDE0tUx6r+Bedx2mXykaelOO5lU9iFXywnO62WqGyfMISIiJ4twTYgIajxKmwEd/yWHBWDun52B+NjTcH28QJb42WAFXK6uvxgasjoUkRdjY/iNI6/XFXhTydXPJ0hhCPgkciReOUiplcvVmVxJVln2wr7NoeVe11IiRaEKRkn5fp45VBOamY6JHMYvJb4BAe16bMfJqH2elZS9cQps8WVsjVTE=~-1~-1~-1,32986,147,1531999884,26018161,PiZtE,72271,62-1,2,-94,-106,1,8-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,0,200,200,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5341-1,2,-94,-116,62156235-1,2,-94,-118,209108-1,2,-94,-121,;2;3;0' %
                                       (session.headers['User-Agent'], site)
                    }
                    panier = [{
                        "id": 'e7f9dfd05f6b992d05ec8d79803ce6a6bcfb0a10972d4d9731c6b94f6ec75033',
                        "variables": {
                            "addToCartInput": {
                                "productId": sku,
                                "clientMutationId": "addToCartMutation"
                            }
                        }
                    }]
                    session.headers.update({
                        "Accept": "*/*",
                        "Content-Type": "text/plain;charset=UTF-8",
                        'Origin': site,
                        'Referer': self.url_produit
                    })
                    session.post(url_bot_panier, json=bot_panier, verify=False)
                    session.headers.update({
                        "x-page-impression-id": impression,
                        "Content-Type": "application/json",
                        'x-xsrf-token': cookies_2["frsx"],
                        'x-zalando-intent-context': 'navigationTargetGroup=MEN'
                    })
                    repPanier = session.post(url_panier, json=panier, verify=False)
                    stop_1 = timeit.default_timer()
                    del session.headers['x-zalando-intent-context']
                    del session.headers['x-page-impression-id']
                    if self.Paiement == 'CB' and repPanier.status_code == 200:
                        chronometre_1 = str(round(stop_1 - start_chrono, 5))
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> Task %s - " % self.Task + Fore.GREEN + "Article %s successfully "
                                                                                          "added to cart - size %s" % (
                                  quantite, self.taille_produit))
                    if self.Paiement == 'CB_Auto' or self.Paiement == 'Paypal' and repPanier.status_code == 200:
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> Task %s - " % self.Task + Fore.YELLOW + "Article %s successfully "
                                                                                           "added to cart - size %s" % (
                                  quantite, self.taille_produit))
                # Credit Card Autocheckout
                if self.Paiement == 'CB_Auto' or self.Paiement == 'Paypal':
                    print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                          Style.RESET_ALL + "> Task %s - " % self.Task + Fore.YELLOW + "Payment Process")

                    # Validation du panier et checkout
                    url_panier_1 = "%s/cart/" % site
                    url_panier_2 = "%s/checkout/confirm" % site
                    del session.headers["x-xsrf-token"]
                    del session.headers["Origin"]
                    del session.headers["Content-Type"]
                    session.headers.update({
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Referer": "%s/myaccount" % site,
                    })
                    session.get(url_panier_1, verify=False)
                    session.headers["Referer"] = "%s/cart/" % site
                    session.get(url_panier_2, verify=False)

                    if self.Mode == 'Quick':
                        # Addresse de livraison
                        url_adresse = '%s/api/checkout/validate-address' % site
                        url_panier_4 = '%s/api/checkout/create-or-update-address' % site
                        checkout_2_2 = {
                            'address': {
                                'address': {
                                    'city': self.List_Quick_Task[8].strip('\n').lstrip('"').rstrip('"'),
                                    'salutation': 'Mr',
                                    'first_name': self.List_Quick_Task[1].strip('\n').lstrip('"').rstrip('"'),
                                    'last_name': self.List_Quick_Task[2].strip('\n').lstrip('"').rstrip('"'),
                                    'country_code': Pays,
                                    'street': self.List_Quick_Task[4].strip('\n').lstrip('"').rstrip('"') + " " +
                                              self.List_Quick_Task[5].strip(
                                                  '\n').lstrip('"').rstrip('"'),
                                    'zip': self.List_Quick_Task[7].strip('\n').lstrip('"').rstrip('"')
                                }
                            }
                        }
                        data_panier4 = {
                            'address': {
                                'city': self.List_Quick_Task[8].strip('\n').lstrip('"').rstrip('"'),
                                'salutation': 'Mr',
                                'first_name': self.List_Quick_Task[1].strip('\n').lstrip('"').rstrip('"'),
                                'last_name': self.List_Quick_Task[2].strip('\n').lstrip('"').rstrip('"'),
                                'country_code': Pays,
                                'street': self.List_Quick_Task[4].strip('\n').lstrip('"').rstrip('"') + " " +
                                          self.List_Quick_Task[5].strip(
                                              '\n').lstrip('"').rstrip('"'),
                                'zip': self.List_Quick_Task[7].strip('\n').lstrip('"').rstrip('"')
                            },
                            'addressDestination': {
                                'destination': {
                                    'address': {
                                        'salutation': 'Mr',
                                        'first_name': self.List_Quick_Task[1].strip('\n').lstrip('"').rstrip('"'),
                                        'last_name': self.List_Quick_Task[2].strip('\n').lstrip('"').rstrip('"'),
                                        'country_code': Pays,
                                        'city': self.List_Quick_Task[8].strip('\n').lstrip('"').rstrip('"'),
                                        'zip': self.List_Quick_Task[7].strip('\n').lstrip('"').rstrip('"'),
                                        'street': self.List_Quick_Task[4].strip('\n').lstrip('"').rstrip('"') + " " +
                                                  self.List_Quick_Task[
                                                      5].strip('\n').lstrip('"').rstrip('"'),
                                        'additional': self.List_Quick_Task[6].strip('\n').lstrip('"').rstrip('"')
                                    }
                                },
                                'normalized_address': {
                                    'country_code': Pays,
                                    'city': self.List_Quick_Task[9].strip('\n').lstrip('"').rstrip('"'),
                                    'zip': self.List_Quick_Task[8].strip('\n').lstrip('"').rstrip('"'),
                                    'street': self.List_Quick_Task[6].strip('\n').lstrip('"').rstrip('"'),
                                    "additional": self.List_Quick_Task[7].strip('\n').lstrip('"').rstrip('"'),
                                    'house_number': self.List_Quick_Task[5].strip('\n').lstrip('"').rstrip('"')
                                },
                                'status': 'https://docs.riskmgmt.zalan.do/address/correct',
                                'blacklisted': 'false'
                            },
                            'isDefaultShipping': 'true',
                            'isDefaultBilling': 'true'

                        }
                        session.headers.update({
                            "Content-Type": 'application/json',
                            "Referer": "%s/checkout/address" % site,
                            "Accept": "application/json",
                            "x-zalando-footer-mode": "desktop",
                            "x-zalando-checkout-app": "web",
                            "x-xsrf-token": cookies_2["frsx"],
                            "x-zalando-header-mode": "desktop",
                            "Origin": site
                        })
                        session.post(url_adresse, json=checkout_2_2, verify=False)
                        session.post(url_panier_4, json=data_panier4, verify=False)

                        # Numero de telephone
                        url_phone = '%s/api/checkout/save-customer-phone-number' % site
                        data_phone = {"phoneNumber": phone}
                        session.post(url_phone, json=data_phone, verify=False)
                        del session.headers["x-xsrf-token"]
                        del session.headers["x-zalando-header-mode"]
                        del session.headers["x-zalando-checkout-app"]
                        del session.headers["x-zalando-footer-mode"]

                        # Next Step
                        url_bot_1_2 = '%s/resources/7be100d4c6rn2028b315fc23b805e921' % site
                        url_checkout_2_2 = '%s/api/checkout/next-step' % site
                        bot = {
                            'sensor_data': '7a74G7m23Vrp0o5c9183811.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392552,3616660,1440,900,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.15037313375,797716808330,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,-1,3665,1;0,-1,0,0,-1,3549,1;0,-1,0,0,1450,1450,0;0,-1,0,0,-1,4421,0;0,-1,0,0,1115,1115,0;0,-1,0,0,1373,1373,0;-1,2,-94,-102,0,-1,0,0,-1,-1,1;-1,2,-94,-108,0,1,1806,16,0,8,1450;1,1,2126,-2,0,8,1450;2,3,2126,-2,0,8,1450;3,2,2190,-2,0,8,1450;4,2,2291,16,0,0,1450;5,1,2310,-2,0,0,1450;6,3,2310,-2,0,0,1450;7,2,2385,-2,0,0,1450;8,1,2459,-2,0,0,1450;9,3,2459,-2,0,0,1450;10,2,2610,-2,0,0,1450;11,1,2614,-2,0,0,1450;12,3,2615,-2,0,0,1450;13,2,2700,-2,0,0,1450;14,1,2761,-2,0,0,1450;15,3,2762,-2,0,0,1450;16,2,2842,-2,0,0,1450;17,1,2843,-2,0,0,1450;18,3,2843,-2,0,0,1450;19,2,2919,-2,0,0,1450;20,1,3079,-2,0,0,1450;21,3,3079,-2,0,0,1450;22,2,3186,-2,0,0,1450;23,1,3239,-2,0,0,1450;24,3,3240,-2,0,0,1450;25,2,3301,-2,0,0,1450;26,1,3386,-2,0,0,1450;27,3,3387,-2,0,0,1450;28,2,3474,-2,0,0,1450;29,1,3603,-2,0,0,1450;30,3,3603,-2,0,0,1450;31,2,3678,-2,0,0,1450;32,1,3724,-2,0,0,1450;33,3,3724,-2,0,0,1450;34,2,3803,-2,0,0,1450;35,1,3866,-2,0,0,1450;36,3,3867,-2,0,0,1450;37,2,3905,-2,0,0,1450;38,1,3980,-2,0,0,1450;39,3,3981,-2,0,0,1450;40,2,4072,-2,0,0,1450;41,1,4244,-2,0,0,1450;42,3,4256,-2,0,0,1450;43,2,4359,-2,0,0,1450;44,1,4495,-2,0,0,1450;45,3,4495,-2,0,0,1450;46,1,4590,-2,0,0,1450;47,3,4590,-2,0,0,1450;48,2,4619,-2,0,0,1450;49,2,4677,-2,0,0,1450;50,1,5247,-2,0,0,1450;51,3,5248,-2,0,0,1450;52,2,5324,-2,0,0,1450;53,1,5486,-2,0,0,1450;54,3,5487,-2,0,0,1450;55,2,5570,-2,0,0,1450;56,1,5578,-2,0,0,1450;57,3,5579,-2,0,0,1450;58,2,5666,-2,0,0,1450;59,1,5760,-2,0,0,1450;60,3,5761,-2,0,0,1450;61,2,5845,-2,0,0,1450;62,1,5854,-2,0,0,1450;63,3,5854,-2,0,0,1450;64,2,5937,-2,0,0,1450;65,1,5956,-2,0,0,1450;66,3,5956,-2,0,0,1450;67,2,6068,-2,0,0,1450;68,1,6142,-2,0,0,1450;69,3,6143,-2,0,0,1450;70,2,6237,-2,0,0,1450;71,1,6347,-2,0,0,1450;72,3,6347,-2,0,0,1450;73,2,6451,-2,0,0,1450;74,1,7755,16,0,8,1115;75,1,8313,-2,0,8,1115;76,3,8313,-2,0,8,1115;77,2,8383,-2,0,8,1115;78,1,8461,-2,0,8,1115;79,3,8461,-2,0,8,1115;80,2,8524,-2,0,8,1115;81,1,8657,-2,0,8,1115;82,3,8657,-2,0,8,1115;83,2,8748,-2,0,8,1115;84,1,8829,-2,0,8,1115;85,3,8829,-2,0,8,1115;86,2,8931,-2,0,8,1115;87,2,9159,16,0,0,1115;88,1,10539,16,0,8,1115;89,1,10894,-2,0,8,1115;90,3,10895,-2,0,8,1115;91,2,10951,-2,0,8,1115;92,1,11329,8,0,8,1115;93,2,11426,8,0,8,1115;94,1,11857,-2,0,8,1115;95,3,11857,-2,0,8,1115;96,2,11901,-2,0,8,1115;97,2,12135,16,0,0,1115;98,1,14077,16,0,8,1373;99,1,14599,-2,0,8,1373;100,3,14600,-2,0,8,1373;101,2,14674,-2,0,8,1373;102,2,14736,16,0,0,1373;103,1,14777,-2,0,0,1373;104,3,14778,-2,0,0,1373;105,1,14874,-2,0,0,1373;106,3,14875,-2,0,0,1373;107,2,14904,-2,0,0,1373;108,2,14933,-2,0,0,1373;109,1,15046,-2,0,0,1373;110,3,15046,-2,0,0,1373;111,2,15117,-2,0,0,1373;112,1,15207,-2,0,0,1373;113,3,15207,-2,0,0,1373;114,2,15264,-2,0,0,1373;115,1,15398,-2,0,0,1373;116,3,15398,-2,0,0,1373;117,2,15461,-2,0,0,1373;118,1,15822,8,0,0,1373;119,2,15905,8,0,0,1373;120,1,15974,8,0,0,1373;121,2,16053,8,0,0,1373;122,1,16366,-2,0,0,1373;123,3,16366,-2,0,0,1373;124,2,16441,-2,0,0,1373;125,1,16482,-2,0,0,1373;126,3,16482,-2,0,0,1373;127,2,16580,-2,0,0,1373;128,1,16592,-2,0,0,1373;129,3,16593,-2,0,0,1373;130,2,16667,-2,0,0,1373;131,1,16753,-2,0,0,1373;132,3,16753,-2,0,0,1373;133,2,16980,-2,0,0,1373;134,1,17063,-2,0,0,1373;135,3,17063,-2,0,0,1373;136,2,17126,-2,0,0,1373;137,1,17191,-2,0,0,1373;138,3,17192,-2,0,0,1373;139,2,17294,-2,0,0,1373;140,1,17301,-2,0,0,1373;141,3,17301,-2,0,0,1373;142,2,17371,-2,0,0,1373;143,1,36470,16,0,8,-1;144,1,36934,-2,0,8,-1;145,3,36935,-2,0,8,-1;146,2,36999,-2,0,8,-1;147,1,37254,-2,0,8,-1;148,3,37255,-2,0,8,-1;149,2,37301,-2,0,8,-1;-1,2,-94,-110,0,1,642,1025,416;1,1,682,1025,416;2,1,683,954,446;3,1,723,941,451;4,1,762,832,458;5,1,919,798,456;6,1,963,698,465;7,1,1314,677,467;8,1,1325,627,608;9,1,1326,627,608;10,1,1419,626,608;11,1,1424,626,608;12,1,1426,626,608;13,1,1537,626,609;14,1,1541,626,609;15,3,1621,626,609,1450;16,1,1729,626,609;17,4,1744,626,609,1450;18,1,1802,626,609;19,1,2291,626,609;20,1,7044,625,787;21,1,7045,625,787;22,1,7049,622,787;23,1,7050,622,787;24,1,7056,619,788;25,1,7057,619,788;26,1,7068,616,789;27,1,7070,616,789;28,1,7073,612,791;29,1,7074,612,791;30,1,7084,608,792;31,1,7085,608,792;32,1,7089,605,794;33,1,7090,605,794;34,1,7096,598,796;35,1,7097,598,796;36,1,7105,593,799;37,1,7107,593,799;38,1,7117,589,800;39,1,7118,589,800;40,1,7121,585,802;41,1,7121,585,802;42,1,7129,581,804;43,1,7130,581,804;44,1,7137,578,806;45,1,7137,578,806;46,1,7145,574,809;47,1,7146,574,809;48,1,7153,570,814;49,1,7153,570,814;50,1,7163,569,815;51,1,7164,569,815;52,1,7169,568,818;53,1,7170,568,818;54,1,7179,567,821;55,1,7180,567,821;56,1,7185,566,823;57,1,7186,566,823;58,1,7193,565,824;59,1,7194,565,824;60,1,7202,565,825;61,1,7203,565,825;62,1,7211,565,825;63,1,7212,565,825;64,1,7218,565,825;65,1,7219,565,825;66,1,7236,564,825;67,1,7237,564,825;68,1,7244,564,825;69,1,7245,564,825;70,1,7277,564,825;71,1,7278,564,825;72,1,7372,564,825;73,1,7372,564,825;74,1,7380,564,824;75,1,7381,564,824;76,1,7387,564,821;77,1,7388,564,821;78,1,7395,563,820;79,1,7395,563,820;80,1,7404,563,818;81,1,7405,563,818;82,1,7412,563,816;83,1,7413,563,816;84,1,7419,562,815;85,1,7420,562,815;86,1,7428,562,814;87,1,7428,562,814;88,1,7436,562,813;89,1,7437,562,813;90,1,7445,562,813;91,1,7445,562,813;92,1,7452,562,812;93,1,7452,562,812;94,1,7460,562,812;95,1,7461,562,812;96,1,7470,562,811;97,1,7471,562,811;98,1,7479,562,811;99,1,7479,562,811;100,1,7494,562,811;101,1,7496,562,811;108,3,7534,562,810,1115;110,4,7652,562,810,1115;113,3,9303,562,810,1115;121,4,9401,535,810,1115;122,2,9401,535,810,1115;246,3,10257,419,801,1115;247,4,10353,419,801,1115;248,2,10353,419,801,1115;297,3,12864,477,869,1373;298,4,12929,477,869,1373;327,3,13449,548,873,1373;328,4,13603,548,873,1373;329,2,13603,548,873,1373;330,3,14010,548,873,1373;331,4,14017,548,873,1373;332,2,14017,548,873,1373;401,3,20535,667,967,0;402,4,20637,667,967,0;403,2,20637,667,967,0;519,4,29259,1255,368,-1;717,3,35782,402,426,-1;718,4,35927,402,426,-1;719,2,35928,402,426,-1;745,3,36249,404,432,-1;747,4,36367,404,432,-1;748,2,36367,404,432,-1;967,3,42305,965,260,0;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,2,13301;3,13451;0,18122;2,18347;1,19575;3,20125;2,28594;3,29163;-1,2,-94,-112,%s/checkout/address-1,2,-94,-115,1722474,1342876,32,0,0,0,3065317,42305,0,1595433616660,15,17067,175,968,2844,22,0,42307,2667949,0,79F5DDBDB01E6F260FCA83916C07C04B~-1~YAAQfsYcuGA7DVpzAQAAO5NBdwQZdVRg2FjI0qcV0Q/xMJwbpUuafeY/lRPefForqQ10jpdeTcgwi94B/qkWKOBLvWzAGnjWvsz12FE6xZEAH0r04gZtQonI89mfSm33K+mW7Qp1py92Oa6g5Z29clnlcE7G+jLEGK1l9hMhk/0MAGI9Ipe8UH3GzMc+w+mobrYZ9NibnDYcH5QIXj4bfjotDm/iAejYv5c+jcFR5NaQu9o92OMLGkWsZhO2CNXdBSaAv3jSwhr9RXFjxUPOvEUuDS/k9EsGzKsrn2W74rnBrNHCgGaJvhPbpGq53/J2oRlC7bAmfzbOnmnvIJv9jynpwiY=~-1~-1~-1,32617,6,-1634669391,26018161,PiZtE,25060,78-1,2,-94,-106,1,12-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,0,200,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,10849923-1,2,-94,-118,385921-1,2,-94,-121,;2;2;0' %
                                           (session.headers['User-Agent'], site)
                        }
                        session.headers.update({
                            "Referer": '%s/checkout/address' % site,
                            "Origin": site,
                            "Content-Type": 'text/plain;charset=UTF-8',
                            "Accept": "*/*"
                        })
                        session.post(url_bot_1_2, json=bot, verify=False)
                        session.headers.update({
                            "Referer": '%s/checkout/address' % site,
                            "Origin": site,
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "x-zalando-footer-mode": "desktop",
                            "x-zalando-checkout-app": "web",
                            "x-xsrf-token": cookies_2["frsx"],
                            "x-zalando-header-mode": "desktop"
                        })
                        session.get(url_checkout_2_2, verify=False)
                        del session.headers["x-zalando-footer-mode"]
                        del session.headers["x-zalando-checkout-app"]
                        del session.headers["x-xsrf-token"]
                        del session.headers["x-zalando-header-mode"]

                    else:
                        # Addresse de livraison
                        botvalidurl = '%s/resources/da6ea05bf5rn2028b315fc23b805e921' % site
                        url_adresse = '%s/api/checkout/validate-address' % site
                        url_panier_4 = '%s/api/checkout/create-or-update-address' % site
                        bot = {
                            'sensor_data': '7a74G7m23Vrp0o5c9186361.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392552,3616660,1440,900,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.15037313375,797716808330,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,-1,3665,1;0,-1,0,0,-1,3549,1;0,-1,0,0,1450,1450,0;0,-1,0,0,-1,4421,0;0,-1,0,0,1115,1115,0;0,-1,0,0,1373,1373,0;-1,2,-94,-102,0,-1,0,0,-1,-1,1;-1,2,-94,-108,0,1,1806,16,0,8,1450;1,1,2126,-2,0,8,1450;2,3,2126,-2,0,8,1450;3,2,2190,-2,0,8,1450;4,2,2291,16,0,0,1450;5,1,2310,-2,0,0,1450;6,3,2310,-2,0,0,1450;7,2,2385,-2,0,0,1450;8,1,2459,-2,0,0,1450;9,3,2459,-2,0,0,1450;10,2,2610,-2,0,0,1450;11,1,2614,-2,0,0,1450;12,3,2615,-2,0,0,1450;13,2,2700,-2,0,0,1450;14,1,2761,-2,0,0,1450;15,3,2762,-2,0,0,1450;16,2,2842,-2,0,0,1450;17,1,2843,-2,0,0,1450;18,3,2843,-2,0,0,1450;19,2,2919,-2,0,0,1450;20,1,3079,-2,0,0,1450;21,3,3079,-2,0,0,1450;22,2,3186,-2,0,0,1450;23,1,3239,-2,0,0,1450;24,3,3240,-2,0,0,1450;25,2,3301,-2,0,0,1450;26,1,3386,-2,0,0,1450;27,3,3387,-2,0,0,1450;28,2,3474,-2,0,0,1450;29,1,3603,-2,0,0,1450;30,3,3603,-2,0,0,1450;31,2,3678,-2,0,0,1450;32,1,3724,-2,0,0,1450;33,3,3724,-2,0,0,1450;34,2,3803,-2,0,0,1450;35,1,3866,-2,0,0,1450;36,3,3867,-2,0,0,1450;37,2,3905,-2,0,0,1450;38,1,3980,-2,0,0,1450;39,3,3981,-2,0,0,1450;40,2,4072,-2,0,0,1450;41,1,4244,-2,0,0,1450;42,3,4256,-2,0,0,1450;43,2,4359,-2,0,0,1450;44,1,4495,-2,0,0,1450;45,3,4495,-2,0,0,1450;46,1,4590,-2,0,0,1450;47,3,4590,-2,0,0,1450;48,2,4619,-2,0,0,1450;49,2,4677,-2,0,0,1450;50,1,5247,-2,0,0,1450;51,3,5248,-2,0,0,1450;52,2,5324,-2,0,0,1450;53,1,5486,-2,0,0,1450;54,3,5487,-2,0,0,1450;55,2,5570,-2,0,0,1450;56,1,5578,-2,0,0,1450;57,3,5579,-2,0,0,1450;58,2,5666,-2,0,0,1450;59,1,5760,-2,0,0,1450;60,3,5761,-2,0,0,1450;61,2,5845,-2,0,0,1450;62,1,5854,-2,0,0,1450;63,3,5854,-2,0,0,1450;64,2,5937,-2,0,0,1450;65,1,5956,-2,0,0,1450;66,3,5956,-2,0,0,1450;67,2,6068,-2,0,0,1450;68,1,6142,-2,0,0,1450;69,3,6143,-2,0,0,1450;70,2,6237,-2,0,0,1450;71,1,6347,-2,0,0,1450;72,3,6347,-2,0,0,1450;73,2,6451,-2,0,0,1450;74,1,7755,16,0,8,1115;75,1,8313,-2,0,8,1115;76,3,8313,-2,0,8,1115;77,2,8383,-2,0,8,1115;78,1,8461,-2,0,8,1115;79,3,8461,-2,0,8,1115;80,2,8524,-2,0,8,1115;81,1,8657,-2,0,8,1115;82,3,8657,-2,0,8,1115;83,2,8748,-2,0,8,1115;84,1,8829,-2,0,8,1115;85,3,8829,-2,0,8,1115;86,2,8931,-2,0,8,1115;87,2,9159,16,0,0,1115;88,1,10539,16,0,8,1115;89,1,10894,-2,0,8,1115;90,3,10895,-2,0,8,1115;91,2,10951,-2,0,8,1115;92,1,11329,8,0,8,1115;93,2,11426,8,0,8,1115;94,1,11857,-2,0,8,1115;95,3,11857,-2,0,8,1115;96,2,11901,-2,0,8,1115;97,2,12135,16,0,0,1115;98,1,14077,16,0,8,1373;99,1,14599,-2,0,8,1373;100,3,14600,-2,0,8,1373;101,2,14674,-2,0,8,1373;102,2,14736,16,0,0,1373;103,1,14777,-2,0,0,1373;104,3,14778,-2,0,0,1373;105,1,14874,-2,0,0,1373;106,3,14875,-2,0,0,1373;107,2,14904,-2,0,0,1373;108,2,14933,-2,0,0,1373;109,1,15046,-2,0,0,1373;110,3,15046,-2,0,0,1373;111,2,15117,-2,0,0,1373;112,1,15207,-2,0,0,1373;113,3,15207,-2,0,0,1373;114,2,15264,-2,0,0,1373;115,1,15398,-2,0,0,1373;116,3,15398,-2,0,0,1373;117,2,15461,-2,0,0,1373;118,1,15822,8,0,0,1373;119,2,15905,8,0,0,1373;120,1,15974,8,0,0,1373;121,2,16053,8,0,0,1373;122,1,16366,-2,0,0,1373;123,3,16366,-2,0,0,1373;124,2,16441,-2,0,0,1373;125,1,16482,-2,0,0,1373;126,3,16482,-2,0,0,1373;127,2,16580,-2,0,0,1373;128,1,16592,-2,0,0,1373;129,3,16593,-2,0,0,1373;130,2,16667,-2,0,0,1373;131,1,16753,-2,0,0,1373;132,3,16753,-2,0,0,1373;133,2,16980,-2,0,0,1373;134,1,17063,-2,0,0,1373;135,3,17063,-2,0,0,1373;136,2,17126,-2,0,0,1373;137,1,17191,-2,0,0,1373;138,3,17192,-2,0,0,1373;139,2,17294,-2,0,0,1373;140,1,17301,-2,0,0,1373;141,3,17301,-2,0,0,1373;142,2,17371,-2,0,0,1373;143,1,36470,16,0,8,-1;144,1,36934,-2,0,8,-1;145,3,36935,-2,0,8,-1;146,2,36999,-2,0,8,-1;147,1,37254,-2,0,8,-1;148,3,37255,-2,0,8,-1;149,2,37301,-2,0,8,-1;-1,2,-94,-110,0,1,642,1025,416;1,1,682,1025,416;2,1,683,954,446;3,1,723,941,451;4,1,762,832,458;5,1,919,798,456;6,1,963,698,465;7,1,1314,677,467;8,1,1325,627,608;9,1,1326,627,608;10,1,1419,626,608;11,1,1424,626,608;12,1,1426,626,608;13,1,1537,626,609;14,1,1541,626,609;15,3,1621,626,609,1450;16,1,1729,626,609;17,4,1744,626,609,1450;18,1,1802,626,609;19,1,2291,626,609;20,1,7044,625,787;21,1,7045,625,787;22,1,7049,622,787;23,1,7050,622,787;24,1,7056,619,788;25,1,7057,619,788;26,1,7068,616,789;27,1,7070,616,789;28,1,7073,612,791;29,1,7074,612,791;30,1,7084,608,792;31,1,7085,608,792;32,1,7089,605,794;33,1,7090,605,794;34,1,7096,598,796;35,1,7097,598,796;36,1,7105,593,799;37,1,7107,593,799;38,1,7117,589,800;39,1,7118,589,800;40,1,7121,585,802;41,1,7121,585,802;42,1,7129,581,804;43,1,7130,581,804;44,1,7137,578,806;45,1,7137,578,806;46,1,7145,574,809;47,1,7146,574,809;48,1,7153,570,814;49,1,7153,570,814;50,1,7163,569,815;51,1,7164,569,815;52,1,7169,568,818;53,1,7170,568,818;54,1,7179,567,821;55,1,7180,567,821;56,1,7185,566,823;57,1,7186,566,823;58,1,7193,565,824;59,1,7194,565,824;60,1,7202,565,825;61,1,7203,565,825;62,1,7211,565,825;63,1,7212,565,825;64,1,7218,565,825;65,1,7219,565,825;66,1,7236,564,825;67,1,7237,564,825;68,1,7244,564,825;69,1,7245,564,825;70,1,7277,564,825;71,1,7278,564,825;72,1,7372,564,825;73,1,7372,564,825;74,1,7380,564,824;75,1,7381,564,824;76,1,7387,564,821;77,1,7388,564,821;78,1,7395,563,820;79,1,7395,563,820;80,1,7404,563,818;81,1,7405,563,818;82,1,7412,563,816;83,1,7413,563,816;84,1,7419,562,815;85,1,7420,562,815;86,1,7428,562,814;87,1,7428,562,814;88,1,7436,562,813;89,1,7437,562,813;90,1,7445,562,813;91,1,7445,562,813;92,1,7452,562,812;93,1,7452,562,812;94,1,7460,562,812;95,1,7461,562,812;96,1,7470,562,811;97,1,7471,562,811;98,1,7479,562,811;99,1,7479,562,811;100,1,7494,562,811;101,1,7496,562,811;108,3,7534,562,810,1115;110,4,7652,562,810,1115;113,3,9303,562,810,1115;121,4,9401,535,810,1115;122,2,9401,535,810,1115;246,3,10257,419,801,1115;247,4,10353,419,801,1115;248,2,10353,419,801,1115;297,3,12864,477,869,1373;298,4,12929,477,869,1373;327,3,13449,548,873,1373;328,4,13603,548,873,1373;329,2,13603,548,873,1373;330,3,14010,548,873,1373;331,4,14017,548,873,1373;332,2,14017,548,873,1373;401,3,20535,667,967,0;402,4,20637,667,967,0;403,2,20637,667,967,0;519,4,29259,1255,368,-1;717,3,35782,402,426,-1;718,4,35927,402,426,-1;719,2,35928,402,426,-1;745,3,36249,404,432,-1;747,4,36367,404,432,-1;748,2,36367,404,432,-1;967,3,42305,965,260,0;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,2,13301;3,13451;0,18122;2,18347;1,19575;3,20125;2,28594;3,29163;-1,2,-94,-112,%s/checkout/address-1,2,-94,-115,1722474,1342876,32,0,0,0,3065317,42305,0,1595433616660,15,17067,175,968,2844,22,0,42307,2667949,0,79F5DDBDB01E6F260FCA83916C07C04B~-1~YAAQfsYcuGA7DVpzAQAAO5NBdwQZdVRg2FjI0qcV0Q/xMJwbpUuafeY/lRPefForqQ10jpdeTcgwi94B/qkWKOBLvWzAGnjWvsz12FE6xZEAH0r04gZtQonI89mfSm33K+mW7Qp1py92Oa6g5Z29clnlcE7G+jLEGK1l9hMhk/0MAGI9Ipe8UH3GzMc+w+mobrYZ9NibnDYcH5QIXj4bfjotDm/iAejYv5c+jcFR5NaQu9o92OMLGkWsZhO2CNXdBSaAv3jSwhr9RXFjxUPOvEUuDS/k9EsGzKsrn2W74rnBrNHCgGaJvhPbpGq53/J2oRlC7bAmfzbOnmnvIJv9jynpwiY=~-1~-1~-1,32617,6,-1634669391,26018161,PiZtE,25060,78-1,2,-94,-106,1,12-1,2,-94,-119,200,0,0,0,0,0,0,0,0,0,0,200,400,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,10849923-1,2,-94,-118,385921-1,2,-94,-121,;2;2;0' %
                                           (session.headers['User-Agent'], site)
                        }
                        botvalidbis = {
                            'sensor_data': '7a74G7m23Vrp0o5c9186361.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392605,7351935,1440,900,1440,900,1440,837,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.441784385220,797823675967,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,-1,3665,1;0,-1,0,0,-1,3549,1;0,-1,0,0,1450,1450,0;0,-1,0,0,-1,4421,0;0,-1,0,0,1115,1115,0;0,-1,0,0,1373,1373,0;-1,2,-94,-102,0,-1,0,0,-1,-1,0;-1,2,-94,-108,0,1,3198,16,0,8,1450;1,1,3685,-2,0,8,1450;2,3,3686,-2,0,8,1450;3,2,3764,-2,0,8,1450;4,2,3805,16,0,0,1450;5,1,3921,-2,0,0,1450;6,3,3921,-2,0,0,1450;7,2,4011,-2,0,0,1450;8,1,4035,-2,0,0,1450;9,3,4035,-2,0,0,1450;10,2,4147,-2,0,0,1450;11,1,4213,-2,0,0,1450;12,3,4213,-2,0,0,1450;13,2,4269,-2,0,0,1450;14,1,4349,-2,0,0,1450;15,3,4349,-2,0,0,1450;16,1,4449,-2,0,0,1450;17,3,4449,-2,0,0,1450;18,2,4552,-2,0,0,1450;19,2,4553,-2,0,0,1450;20,1,4820,8,0,0,1450;21,2,4921,8,0,0,1450;22,1,4993,8,0,0,1450;23,2,5080,8,0,0,1450;24,1,5136,8,0,0,1450;25,2,5243,8,0,0,1450;26,1,5635,-2,0,0,1450;27,3,5635,-2,0,0,1450;28,2,5713,-2,0,0,1450;29,1,5729,-2,0,0,1450;30,3,5730,-2,0,0,1450;31,2,5838,-2,0,0,1450;32,1,5840,-2,0,0,1450;33,3,5841,-2,0,0,1450;34,2,5913,-2,0,0,1450;35,1,5996,-2,0,0,1450;36,3,5996,-2,0,0,1450;37,2,6104,-2,0,0,1450;38,1,6290,-2,0,0,1450;39,3,6290,-2,0,0,1450;40,2,6374,-2,0,0,1450;41,1,6654,8,0,0,1450;42,2,6755,8,0,0,1450;43,1,7110,-2,0,0,1450;44,3,7110,-2,0,0,1450;45,2,7210,-2,0,0,1450;46,1,7301,-2,0,0,1450;47,3,7301,-2,0,0,1450;48,2,7394,-2,0,0,1450;49,1,8189,-2,0,0,1450;50,3,8189,-2,0,0,1450;51,2,8283,-2,0,0,1450;52,1,8338,-2,0,0,1450;53,3,8338,-2,0,0,1450;54,2,8459,-2,0,0,1450;55,1,8511,-2,0,0,1450;56,3,8511,-2,0,0,1450;57,2,8585,-2,0,0,1450;58,1,8644,-2,0,0,1450;59,3,8644,-2,0,0,1450;60,2,8749,-2,0,0,1450;61,1,8898,-2,0,0,1450;62,3,8899,-2,0,0,1450;63,2,9002,-2,0,0,1450;64,1,9231,-2,0,0,1450;65,3,9232,-2,0,0,1450;66,2,9409,-2,0,0,1450;67,1,9430,-2,0,0,1450;68,3,9430,-2,0,0,1450;69,2,9492,-2,0,0,1450;70,1,9669,-2,0,0,1450;71,3,9670,-2,0,0,1450;72,2,9709,-2,0,0,1450;73,1,9857,-2,0,0,1450;74,3,9857,-2,0,0,1450;75,2,9935,-2,0,0,1450;76,1,9969,-2,0,0,1450;77,3,9969,-2,0,0,1450;78,2,10074,-2,0,0,1450;79,1,10196,-2,0,0,1450;80,3,10196,-2,0,0,1450;81,2,10319,-2,0,0,1450;82,1,10360,-2,0,0,1450;83,3,10361,-2,0,0,1450;84,2,10436,-2,0,0,1450;85,1,10477,-2,0,0,1450;86,3,10477,-2,0,0,1450;87,2,10593,-2,0,0,1450;88,1,10676,-2,0,0,1450;89,3,10676,-2,0,0,1450;90,2,10793,-2,0,0,1450;91,1,10939,-2,0,0,1450;92,3,10939,-2,0,0,1450;93,2,11086,-2,0,0,1450;94,1,12481,16,0,8,1115;95,1,12889,-2,0,8,1115;96,3,12889,-2,0,8,1115;97,2,12926,-2,0,8,1115;98,1,13086,-2,0,8,1115;99,3,13086,-2,0,8,1115;100,2,13169,-2,0,8,1115;101,1,13288,-2,0,8,1115;102,3,13288,-2,0,8,1115;103,2,13372,-2,0,8,1115;104,1,13509,-2,0,8,1115;105,3,13509,-2,0,8,1115;106,2,13659,-2,0,8,1115;107,1,13765,-2,0,8,1115;108,3,13765,-2,0,8,1115;109,2,13874,-2,0,8,1115;110,2,14095,16,0,0,1115;111,1,15703,16,0,8,1373;112,1,16229,-2,0,8,1373;113,3,16229,-2,0,8,1373;114,2,16302,-2,0,8,1373;115,2,16314,16,0,0,1373;116,1,16376,-2,0,0,1373;117,3,16376,-2,0,0,1373;118,1,16505,-2,0,0,1373;119,3,16506,-2,0,0,1373;120,2,16532,-2,0,0,1373;121,2,16583,-2,0,0,1373;122,1,16627,-2,0,0,1373;123,3,16628,-2,0,0,1373;124,2,16724,-2,0,0,1373;125,1,16867,-2,0,0,1373;126,3,16868,-2,0,0,1373;127,2,16931,-2,0,0,1373;128,1,16999,-2,0,0,1373;129,3,16999,-2,0,0,1373;130,2,17111,-2,0,0,1373;131,1,17181,-2,0,0,1373;132,3,17182,-2,0,0,1373;133,2,17248,-2,0,0,1373;134,1,17298,-2,0,0,1373;135,3,17299,-2,0,0,1373;136,2,17422,-2,0,0,1373;137,1,17522,-2,0,0,1373;138,3,17523,-2,0,0,1373;139,2,17608,-2,0,0,1373;140,1,17617,-2,0,0,1373;141,3,17617,-2,0,0,1373;142,2,17719,-2,0,0,1373;143,1,17738,-2,0,0,1373;144,3,17739,-2,0,0,1373;145,2,17885,-2,0,0,1373;146,1,18308,8,0,0,1373;147,2,18396,8,0,0,1373;148,1,18474,8,0,0,1373;149,2,18554,8,0,0,1373;-1,2,-94,-110,0,1,31,907,182;1,1,49,924,196;2,1,51,951,213;3,1,86,965,220;4,1,103,1007,240;5,1,108,1044,255;6,1,118,1061,262;7,1,119,1061,262;8,1,128,1074,266;9,1,129,1074,266;10,1,141,1083,267;11,1,143,1083,267;12,1,151,1092,269;13,1,152,1092,269;14,1,162,1100,270;15,1,163,1100,270;16,1,176,1104,271;17,1,177,1104,271;18,1,185,1108,271;19,1,190,1108,271;20,1,196,1108,271;21,1,207,1108,271;22,1,257,1102,269;23,1,258,1102,269;24,1,272,1087,267;25,1,274,1061,262;26,1,285,1038,260;27,1,285,1038,260;28,1,297,1007,257;29,1,308,1007,257;30,1,310,982,256;31,1,320,968,256;32,1,323,968,256;33,1,330,949,257;34,1,332,949,257;35,1,341,935,259;36,1,342,935,259;37,1,354,927,261;38,1,356,927,261;39,1,364,924,263;40,1,364,924,263;41,1,375,920,267;42,1,376,920,267;43,1,387,917,271;44,1,391,917,271;45,1,398,916,276;46,1,398,916,276;47,1,494,915,286;48,1,514,934,365;49,1,626,934,369;50,1,705,886,420;51,1,731,832,452;52,1,786,808,464;53,1,962,800,467;54,1,999,793,444;55,1,1005,792,441;56,1,1406,578,386;57,1,1408,572,410;58,1,1479,571,412;59,1,1483,571,413;60,1,1651,571,413;61,1,1681,571,413;62,1,1694,571,414;63,1,1695,571,414;64,1,1702,571,415;65,1,1704,571,415;66,1,1714,571,416;67,1,1715,571,416;68,1,1727,571,417;69,1,1727,571,417;70,1,1736,570,420;71,1,1737,570,420;72,1,1749,569,424;73,1,1750,569,424;74,1,1759,568,429;75,1,1759,568,429;76,1,1770,566,435;77,1,1772,566,435;78,1,1786,563,445;79,1,1789,563,445;80,1,1792,560,455;81,1,1794,560,455;82,1,1806,556,464;83,1,1807,556,464;84,1,1819,551,478;85,1,1823,551,478;86,1,1826,547,492;87,1,1829,547,492;88,1,1838,544,502;89,1,1839,544,502;90,1,1851,541,513;91,1,1852,541,513;92,1,1860,539,523;93,1,1861,539,523;94,1,1872,538,530;95,1,1873,538,530;96,1,1887,538,537;97,1,1888,538,537;98,1,1893,538,542;99,1,1896,538,542;210,3,2940,543,614,1450;212,4,3043,544,614,1450;446,3,12201,469,795,1115;447,4,12308,469,795,1115;619,3,15427,891,869,1373;620,4,15572,891,869,1373;817,3,20729,794,981,-1;818,4,20808,794,981,-1;819,2,20809,794,981,-1;1097,3,25381,472,449,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,%s/checkout/address-1,2,-94,-115,1804030,386330,32,0,0,0,2190327,25381,0,1595647351934,16,17069,161,1098,2844,9,0,25382,1828242,0,EFDE55E3CB9D90A4821B78F3B53D16D1~-1~YAAQfiMVAkVo+39zAQAA4a3+gwSdqttmjbWTIbAoANCTf1tZKaWebTb3TiHq2l1yC1CRz0UEarlE9lLJRbb/zE6dRNWgeaX6GiJhw/+JXY4XLX4fKccnMovtS/or0St+iYkXRo/dngvoTsYTzUX+3beyIZLt3nCLgx6ocrdnYagWcf35iCcLgp+u3/NXJ3rB23CHMYa1MJrfrVyTF+A1IUOB1N5JXuMTVFSZe/hezZ0wcKs+jlSu+Q6/FZFMsDsFUOekOkhZRHqouHWjL18OTSa3ZQWpHk6qwX6cjftCDdYAsgrDSobwdNed2Fb8u97CxYofXjuftDHVOY+dTapR/sMwiUA=~-1~-1~-1,32777,184,-1829503388,26018161,PiZtE,42007,69-1,2,-94,-106,1,6-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,0,400,200,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,22055865-1,2,-94,-118,358982-1,2,-94,-121,;2;8;0' % (
                                session.headers['User-Agent'], site)
                        }
                        checkout_2_2 = {
                            'address': {
                                'address': {
                                    'city': profil[7].strip('\n').lstrip('"').rstrip('"'),
                                    'salutation': 'Mr',
                                    'first_name': profil[0].strip('\n').lstrip('"').rstrip('"'),
                                    'last_name': profil[1].strip('\n').lstrip('"').rstrip('"'),
                                    'country_code': Pays,
                                    'street': profil[3].strip('\n').lstrip('"').rstrip('"') + " " + profil[4].strip(
                                        '\n').lstrip('"').rstrip('"'),
                                    'zip': profil[6].strip('\n').lstrip('"').rstrip('"')
                                }
                            }
                        }
                        data_panier4 = {
                            'address': {
                                'city': profil[7].strip('\n').lstrip('"').rstrip('"'),
                                'salutation': 'Mr',
                                'first_name': profil[0].strip('\n').lstrip('"').rstrip('"'),
                                'last_name': profil[1].strip('\n').lstrip('"').rstrip('"'),
                                'country_code': Pays,
                                'street': profil[3].strip('\n').lstrip('"').rstrip('"') + " " + profil[4].strip(
                                    '\n').lstrip('"').rstrip('"'),
                                'zip': profil[6].strip('\n').lstrip('"').rstrip('"')
                            },
                            'addressDestination': {
                                'destination': {
                                    'address': {
                                        'salutation': 'Mr',
                                        'first_name': profil[0].strip('\n').lstrip('"').rstrip('"'),
                                        'last_name': profil[1].strip('\n').lstrip('"').rstrip('"'),
                                        'country_code': Pays,
                                        'city': profil[7].strip('\n').lstrip('"').rstrip('"'),
                                        'zip': profil[6].strip('\n').lstrip('"').rstrip('"'),
                                        'street': profil[3].strip('\n').lstrip('"').rstrip('"') + " " + profil[4].strip(
                                            '\n').lstrip('"').rstrip('"'),
                                        "additional": profil[5].strip('\n').lstrip('"').rstrip('"')
                                    }
                                },
                                'normalized_address': {
                                    'country_code': Pays,
                                    'city': profil[7].strip('\n').lstrip('"').rstrip('"'),
                                    'zip': profil[6].strip('\n').lstrip('"').rstrip('"'),
                                    'street': profil[4].strip('\n').lstrip('"').rstrip('"'),
                                    "additional": profil[5].strip('\n').lstrip('"').rstrip('"'),
                                    'house_number': profil[3].strip('\n').lstrip('"').rstrip('"')
                                },
                                'status': 'https://docs.riskmgmt.zalan.do/address/correct',
                                'blacklisted': 'false'
                            },
                            'isDefaultShipping': 'true',
                            'isDefaultBilling': 'true'

                        }
                        session.headers.update({
                            "Referer": '%s/checkout/address' % site,
                            "Origin": site,
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "x-zalando-footer-mode": "desktop",
                            "x-zalando-checkout-app": "web",
                            "x-xsrf-token": cookies_2["frsx"],
                            "x-zalando-header-mode": "desktop"
                        })
                        session.post(url_adresse, json=checkout_2_2, verify=False)
                        session.post(url_panier_4, json=data_panier4, verify=False)
                        del session.headers["x-xsrf-token"]
                        del session.headers["x-zalando-header-mode"]
                        del session.headers["x-zalando-checkout-app"]
                        del session.headers["x-zalando-footer-mode"]
                        session.headers.update({
                            "Referer": '%s/checkout/address' % site,
                            "Origin": site,
                            "Content-Type": "text/plain;charset=UTF-8",
                            "Accept": "*/*"
                        })
                        session.post(botvalidurl, json=botvalidbis, verify=False)
                        session.post(botvalidurl, json=bot, verify=False)

                        # Numero de telephone
                        url_phone = '%s/api/checkout/save-customer-phone-number' % site
                        data_phone = {"phoneNumber": phone}
                        session.headers.update({
                            "Referer": '%s/checkout/address' % site,
                            "Origin": site,
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "x-zalando-footer-mode": "desktop",
                            "x-zalando-checkout-app": "web",
                            "x-xsrf-token": cookies_2["frsx"],
                            "x-zalando-header-mode": "desktop"
                        })
                        session.post(url_phone, json=data_phone, verify=False)

                        # Next Step
                        url_checkout_2_2 = '%s/api/checkout/next-step' % site
                        session.headers["Accept"] = "application/json"
                        session.headers["Content-Type"] = "application/json"
                        del session.headers["Origin"]
                        url_pay = session.get(url_checkout_2_2, verify=False)
                        url_pay_2 = json.loads(url_pay.text)
                        url_pay_3 = url_pay_2['url']
                        del session.headers["x-zalando-footer-mode"]
                        del session.headers["x-zalando-checkout-app"]
                        del session.headers["x-xsrf-token"]
                        del session.headers["x-zalando-header-mode"]
                        del session.headers["Content-Type"]

                    # Paiement Partie 1
                    url_select = 'https://checkout.payment.zalando.com/selection'
                    url_pay_2 = "https://card-entry-service.zalando-payments.com/contexts/checkout/cards"

                    # Paiement par carte bancaire
                    if self.Paiement != 'Paypal':
                        session.get(url_pay_3, verify=False)
                        session.headers['Referer'] = 'https://www.zalando.fr/checkout/confirm'
                        session.get(url_pay_3 + "?show=true", verify=False)
                        selecrequete = session.get(url_select, verify=False, allow_redirects=False)
                        soup_3 = BeautifulSoup(selecrequete.text, "html.parser")
                        objet_token_ini = soup_3.find(string=re.compile("config.accessToken"))
                        token_ini = objet_token_ini.split("'")
                        token = token_ini[1]
                        session.headers.update({
                            "Referer": '%s/checkout/address' % site,
                            "Origin": "https://card-entry-service.zalando-payments.com",
                            "Content-Type": "application/json",
                            "Accept": "*/*",
                            "Host": "card-entry-service.zalando-payments.com",
                            "Authorization": "Bearer %s" % token
                        })
                        reponsepay = session.post(
                            url_pay_2, json=data_cb, verify=False, allow_redirects=False
                        )
                        reponsepaybis = json.loads(reponsepay.text)

                        # Paiement Partie 2
                        data_pay_3 = (
                                "payz_selected_payment_method=CREDIT_CARD_PAY_LATER&payz_credit_card_pay_later_former_payment_method_id=-1&payz_credit_card_former_payment_method_id=-1&iframe_funding_source_id=%s"
                                % reponsepaybis["id"]
                        )
                        del session.headers["Authorization"]
                        session.headers.update({
                            "Referer": 'https://checkout.payment.zalando.com/selection',
                            "Origin": "https://checkout.payment.zalando.com",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Host": "card-entry-service.zalando-payments.com",
                            "Authorization": "Bearer %s" % token
                        })
                        session.post(url_pay_3 + "?show=true", data=data_pay_3, verify=False)

                        # Paiement Partie 3
                        url_pay_4 = "%s/checkout/payment-complete" % site
                        del session.headers["Content-Type"]
                        del session.headers["Origin"]
                        session.headers["Host"] = site.strip('https://')
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
                        url_pay_bot = '%s/resources/da6ea05bf5rn2028b315fc23b805e921' % site
                        url_pay_fin = '%s/api/checkout/buy-now' % site
                        data_bot_pay = {
                            'sensor_data': 'a74G7m23Vrp0o5c9179431.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392164,7588656,1920,1080,1920,1080,1920,1017,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.967902033483,796928794328,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,-1,3960,0;-1,2,-94,-102,0,-1,0,0,-1,3960,0;-1,2,-94,-108,-1,2,-94,-110,0,1,260,839,528;1,1,261,839,528;2,1,274,839,528;3,1,281,839,528;4,1,283,838,529;5,1,289,837,529;6,1,290,837,529;7,1,303,834,530;8,1,304,834,530;9,1,312,828,531;10,1,312,828,531;11,1,324,818,533;12,1,325,818,533;13,1,335,810,534;14,1,338,810,534;15,1,346,799,534;16,1,348,799,534;17,1,359,790,534;18,1,360,790,534;19,1,368,781,535;20,1,380,774,535;21,1,397,766,535;22,1,398,766,535;23,1,402,758,535;24,1,403,758,535;25,1,435,755,535;26,1,437,747,536;27,1,448,744,536;28,1,449,744,536;29,1,462,743,536;30,1,462,743,536;31,1,471,741,536;32,1,472,741,536;33,1,482,740,536;34,1,483,740,536;35,1,494,740,536;36,1,495,740,536;37,1,572,740,536;38,1,572,740,536;39,1,584,742,535;40,1,584,742,535;41,1,593,744,535;42,1,594,744,535;43,1,606,746,535;44,1,606,746,535;45,1,616,750,534;46,1,618,750,534;47,1,627,757,534;48,1,628,757,534;49,1,642,764,535;50,1,643,764,535;51,1,651,771,535;52,1,652,771,535;53,1,663,783,536;54,1,664,783,536;55,1,675,800,537;56,1,676,800,537;57,1,684,816,538;58,1,685,816,538;59,1,695,850,540;60,1,704,850,540;61,1,849,895,546;62,1,871,1120,587;63,1,874,1126,589;64,1,878,1128,590;65,1,887,1129,591;66,1,888,1129,591;67,1,1121,1133,593;68,1,1130,1139,593;69,1,1141,1140,593;70,1,1170,1140,593;71,1,1171,1140,593;72,1,1416,1139,593;73,1,1423,1138,592;74,1,1438,1137,592;75,1,1443,1136,592;76,1,1449,1136,591;77,1,1451,1136,591;78,1,1485,1136,591;79,1,1485,1137,590;80,1,1494,1137,588;81,1,1495,1137,588;82,1,1504,1138,585;83,1,1505,1138,585;84,1,1516,1140,583;85,1,1517,1140,583;86,1,1532,1141,581;87,1,1538,1141,581;88,1,1541,1142,579;89,1,1549,1144,577;90,1,1550,1144,577;91,1,1562,1145,576;92,1,1562,1145,576;93,1,1572,1146,575;94,1,1573,1146,575;95,1,1583,1147,574;96,1,1587,1147,574;97,1,1596,1148,574;98,1,1598,1148,574;99,1,1618,1148,573;256,3,5106,1244,954,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,%s/checkout/confirm-1,2,-94,-115,1,242493,32,0,0,0,242461,5106,0,1593857588656,12,17050,0,257,2841,1,0,5108,87744,0,76260A165DC066A281E308D22442E210~-1~YAAQNOx7XOg6hBVzAQAARcBQGQSyvSFbFGXl59iNajFhHhapCF6BkxAA0sqDaoD9MZ0sqZZZGU0QvNo4YzuehT+HCCZ+QcgR83ZMGQxqQpnXCIGFbPQ9lpbkkovEK8nocdwGx5GAqGaxWsVOHLXej4YT0gcTiqqlZg+6Z/Y6dVuzxBr7tkSnSODv52r6Sd9cr/U3w/VJTDmT2MpPwSWFHNx/PjOERknhjj1NY6yNNn9Df8Ih+lL8L7jIhNaMnur9afb0scBr7NhG0AVH/0qWz+O5+Zmxwi0s1ASNjAeh2jJHlr25uReBJ2l20pa5pUEB4UaqHwmCv4s4kYmORGswxW3u65E=~-1~-1~-1,32325,146,-242715172,26018161,PiZtE,81065,44-1,2,-94,-106,1,2-1,2,-94,-119,200,0,0,0,0,0,200,0,0,200,200,2200,1000,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,1844041464-1,2,-94,-118,175375-1,2,-94,-121,;3;6;0' %
                                           (session.headers['User-Agent'], site)
                        }
                        data_pay_fin = {
                            'checkoutId': checkout_id,
                            'eTag': etagini
                        }
                        session.headers.update({
                            "Referer": '%s/checkout/confirm' % site,
                            "Origin": site,
                            "Content-Type": 'text/plain;charset=UTF-8',
                            "Accept": "*/*",
                            "Host": site.strip('https://'),
                            "Authorization": "Bearer %s" % token
                        })
                        session.post(url_pay_bot, json=data_bot_pay, verify=False)
                        session.headers.update({
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "x-zalando-footer-mode": "desktop",
                            "x-zalando-checkout-app": "web",
                            "x-xsrf-token": cookies_2["frsx"],
                            "x-zalando-header-mode": "desktop"
                        })
                        reponse_checkout = session.post(url_pay_fin, json=data_pay_fin, verify=False)
                        stop_2 = timeit.default_timer()
                        if reponse_checkout.status_code == 200:
                            chronometre_2 = str(round(stop_2 - start_chrono, 5))
                            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                                  Style.RESET_ALL + "> Task %s - " % self.Task + Fore.GREEN + "Successfully checked "
                                                                                              "out !")
                        else:
                            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                                  Style.RESET_ALL + "> Task %s - " % self.Task + Fore.RED + "There is a problem with the checkout ! Check your details and try later !")
                            time.sleep(5)
                            main()

                    # Paiement par paypal
                    if self.Paiement == 'Paypal':
                        data_pay_3 = (
                            "payz_credit_card_pay_later_former_payment_method_id=-1&payz_credit_card_former_payment_method_id=-1&payz_selected_payment_method=PAYPAL&iframe_funding_source_id="
                        )
                        ua = session.headers['User-Agent']
                        session.headers.clear()
                        session.headers.update({
                            'Host': 'www.zalando.fr',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Accept-Language': 'fr-fr',
                            'Referer': 'https://www.zalando.fr/checkout/address',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'User-Agent': ua
                        })
                        urltestpay = 'https://www.zalando.fr/checkout/payment-complete'
                        session.get(urltestpay, verify=False)
                        session.headers.update({
                            "Referer": 'https://checkout.payment.zalando.com/selection',
                            "Origin": "https://checkout.payment.zalando.com",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Host": "checkout.payment.zalando.com"
                        })
                        session.post(url_pay_3, data=data_pay_3, verify=False)
                        url_pay_4 = "%s/checkout/payment-complete" % site
                        del session.headers["Content-Type"]
                        del session.headers["Origin"]
                        session.headers["Host"] = site.strip('https://')
                        b = session.get(url_pay_4, verify=False)
                        soupbis_3 = BeautifulSoup(b.content, "html.parser")
                        reponsefinale_3 = soupbis_3.find(attrs={"data-props": re.compile('eTag')})
                        reponsefinale1_3 = reponsefinale_3['data-props']
                        reponsefinale2_3 = json.loads(reponsefinale1_3)
                        checkout_id = reponsefinale2_3['model']['checkoutId']
                        etagini = reponsefinale2_3['model']['eTag']
                        url_pay_bot = '%s/resources/ef7c5d53c52028b315fc23b805e921' % site
                        url_pay_fin = '%s/api/checkout/buy-now' % site
                        data_bot_pay = {
                            'sensor_data': '7a74G7m23Vrp0o5c9179081.6-1,2,-94,-100,%s,uaend,11011,20030107,fr,Gecko,1,0,0,0,392213,6747499,1920,1080,1920,1080,1920,1017,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.11229682656,797028373749,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,-1,3960,0;-1,2,-94,-102,0,-1,0,0,-1,3960,0;-1,2,-94,-108,-1,2,-94,-110,0,1,866,1219,589;1,1,952,1330,303;2,1,956,1335,268;3,1,1052,1335,262;4,1,1053,1334,227;5,1,1223,1334,226;6,1,1232,1332,209;7,3,1457,1332,209,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,%s/checkout/confirm-1,2,-94,-115,1,21705,32,0,0,0,21673,1457,0,1594056747498,15,17052,0,8,2842,1,0,1458,8791,0,76260A165DC066A281E308D22442E210~-1~YAAQNex7XPmwUBBzAQAAL6wvJQQStigQokMVnZeVwO3MmTr9ShhhdNV9l0dDLJJncTeUUmbw1GxS3ewJgO07jimqFmuwVJLCKb+yJW1ozK9zuKyzyQ8n1t32g9OTRvVUauyicyddqYedyA/mGe0i4GjORlN34urlDCmDhGcVeOqX3n9bEJ7IbeFP4Ex8ublQhESaDOaEjbeK66uI99vMYtuREoZscMGcp3bDMxgOZQqnTJzzvBiNxsFutrC2KZXr+LcYRblAoMD85YVKZZnsgRcYT7OAHAHkGLXTn2HWI6DvnJ+Y/NHiqABiHh/beN3WtkNCCeHwHcowgTha20OefnKadT8=~-1~-1~-1,33150,7,-1229804841,26018161,PiZtE,91344,48-1,2,-94,-106,1,2-1,2,-94,-119,800,0,0,200,200,200,200,200,0,200,200,1600,1600,2200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,506063805-1,2,-94,-118,93065-1,2,-94,-121,;1;8;0' %
                                           (session.headers['User-Agent'], site)
                        }
                        data_pay_fin = {
                            'checkoutId': checkout_id,
                            'eTag': etagini
                        }
                        session.headers.update({
                            "Referer": '%s/checkout/confirm' % site,
                            "Origin": site,
                            "Content-Type": "text/plain;charset=UTF-8",
                            "Accept": "*/*",
                            "Host": site.strip('https://')
                        })
                        session.post(url_pay_bot, json=data_bot_pay, verify=False)
                        session.headers.update({
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "x-zalando-footer-mode": "desktop",
                            "x-zalando-checkout-app": "web",
                            "x-xsrf-token": cookies_2["frsx"],
                            "x-zalando-header-mode": "desktop"
                        })
                        reponse_checkout = session.post(url_pay_fin, json=data_pay_fin, verify=False)
                        stop_3 = timeit.default_timer()
                        if reponse_checkout.status_code == 200:
                            chronometre_3 = str(round(stop_3 - start_chrono, 5))
                            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                                  Style.RESET_ALL + "> Task %s - " % self.Task + Fore.GREEN + "Successfully checked "
                                                                                              "out !")
                        else:
                            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                                  Style.RESET_ALL + "> Task %s - " % self.Task + Fore.RED + "There is a problem with "
                                                                                            "the checkout ! Check your details and try later !")
                            time.sleep(5)
                            main()
                        json_reponse = json.loads(reponse_checkout.text)
                        url_paypal = str(json_reponse["url"])
            session.close()

            # Notification Discord WebHook
            if self.Mode == 'Quick':
                url_discord = self.List_Quick_Task[16].strip('\n').lstrip('"').rstrip('"')
                creditcard = self.List_Quick_Task[12].strip('\n').lstrip('"').rstrip('"')
            else:
                url_discord = profil[14].strip('\n').lstrip('"').rstrip('"')
                creditcard = profil[10].strip('\n').lstrip('"').rstrip('"')
            # Identifiants Discord Webhook
            webhook = DiscordWebhook(
                url=url_discord,
                username="Scred AIO",
                avatar_url='https://pbs.twimg.com/profile_images/1283768710138863617/D2yC8Qpg_400x400.jpg',
                verify=False
            )
            if self.Mode == 'Quick' or self.Paiement == 'CB_Auto':
                # Titre
                embed = DiscordEmbed(title='Successfully checked out !', color=1160473)
                # Pied de page
                embed.set_footer(text='SCRED AIO')
                embed.set_timestamp()
                # Photo du produit
                embed.set_thumbnail(
                    url=link_photo)
                embed.add_embed_field(name='Website', value=site.strip('https://'), inline=False)
                embed.add_embed_field(name='Product', value=name_product, inline=False)
                embed.add_embed_field(name='Size', value=self.taille_produit)
                embed.add_embed_field(name='Quantity', value=self.quantite)
                embed.add_embed_field(name='Mode', value='Auto Checkout', inline=False)
                embed.add_embed_field(name='Checkout Speed', value=chronometre_2, inline=False)
                embed.add_embed_field(name='Account',
                                      value='|| %s ||' % compte[0].strip('\n').lstrip('"').rstrip('"'),
                                      inline=False)
                embed.add_embed_field(name='Credit Card',
                                      value='|| %s ||' % creditcard,
                                      inline=False)
                webhook.add_embed(embed)
                webhook.execute()

            if self.Paiement == 'Paypal':
                # Titre
                embed = DiscordEmbed(title='Successfully checked out !', color=1160473)
                # Pied de page
                embed.set_footer(text='SCRED AIO')
                embed.set_timestamp()
                # Photo du produit
                embed.set_thumbnail(
                    url=link_photo)
                embed.add_embed_field(name='Website', value=site.strip('https://'), inline=False)
                embed.add_embed_field(name='Product', value=name_product, inline=False)
                embed.add_embed_field(name='Size', value=self.taille_produit)
                embed.add_embed_field(name='Quantity', value=self.quantite)
                embed.add_embed_field(name='Mode', value='Manual')
                embed.add_embed_field(name='Checkout Speed', value=chronometre_3)
                embed.add_embed_field(name='Checkout Link',
                                      value='|| %s ||' % url_paypal,
                                      inline=False)
                webhook.add_embed(embed)
                webhook.execute()

            if self.Paiement == 'CB':
                # Titre
                embed = DiscordEmbed(title='Successfully added to cart !', color=1160473)
                # Pied de page
                embed.set_footer(text='SCRED AIO')
                embed.set_timestamp()
                # Photo du produit
                embed.set_thumbnail(
                    url=link_photo)
                embed.add_embed_field(name='Website', value=site.strip('https://'), inline=False)
                embed.add_embed_field(name='Product', value=name_product, inline=False)
                embed.add_embed_field(name='Size', value=self.taille_produit)
                embed.add_embed_field(name='Quantity', value=self.quantite)
                embed.add_embed_field(name='Mode', value='Manual')
                embed.add_embed_field(name='Checkout Speed', value=chronometre_1, inline=False)
                embed.add_embed_field(name='Username',
                                      value='|| %s ||' % compte[0].strip('\n').lstrip('"').rstrip('"'))
                embed.add_embed_field(name='Password',
                                      value='|| %s ||' % compte[1].strip('\n').lstrip('"').rstrip('"'))
                embed.add_embed_field(name='Login Link',
                                      value='|| %s/welcomenoaccount/true ||' % site,
                                      inline=False)
                webhook.add_embed(embed)
                webhook.execute()

            # Insertion des tâches effectuées dans le fichier Task_History.csv
            if self.Paiement == 'Paypal':
                today = date.today()
                now = datetime.now()
                jour = today.strftime("%b-%d-%Y")
                heure = now.strftime("%H:%M:%S")
                mode_1 = 'Paypal'
                tasklist = [jour, heure, self.url_produit, self.taille_produit, self.quantite, mode_1, compte[0]]
                with open("Zalando/Success recap/Success_Recap.csv", "a") as f:
                    f.write(tasklist[0].strip('\n'))
                    f.write(",")
                    f.write(tasklist[1].strip('\n'))
                    f.write(",")
                    f.write(tasklist[2].strip('\n'))
                    f.write(",")
                    f.write(tasklist[3].strip('\n'))
                    f.write(",")
                    f.write(tasklist[4].strip('\n'))
                    f.write(",")
                    f.write(tasklist[5].strip('\n'))
                    f.write(",")
                    f.write(tasklist[6].strip('\n'))
                    f.write('\n')
                f.close()

            if self.Paiement == 'CB_Auto':
                today = date.today()
                now = datetime.now()
                Jour = today.strftime("%b-%d-%Y")
                heure = now.strftime("%H:%M:%S")
                mode_1 = 'Credit Card - %s' % creditcard
                tasklist = [Jour, heure, self.url_produit, self.taille_produit, self.quantite, mode_1, compte[0]]
                with open("Zalando/Success recap/Success_Recap.csv", "a") as f:
                    f.write(tasklist[0].strip('\n'))
                    f.write(",")
                    f.write(tasklist[1].strip('\n'))
                    f.write(",")
                    f.write(tasklist[2].strip('\n'))
                    f.write(",")
                    f.write(tasklist[3].strip('\n'))
                    f.write(",")
                    f.write(tasklist[4].strip('\n'))
                    f.write(",")
                    f.write(tasklist[5].strip('\n'))
                    f.write(",")
                    f.write(tasklist[6].strip('\n'))
                    f.write('\n')
                f.close()

            if self.Paiement == 'CB':
                today = date.today()
                now = datetime.now()
                jour = today.strftime("%b-%d-%Y")
                heure = now.strftime("%H:%M:%S")
                mode_1 = 'Manual Checkout'
                tasklist = [jour, heure, self.url_produit, self.taille_produit, self.quantite, mode_1, compte[0]]
                with open("Zalando/Success recap/Success_Recap.csv", "a") as f:
                    f.write(tasklist[0].strip('\n'))
                    f.write(",")
                    f.write(tasklist[1].strip('\n'))
                    f.write(",")
                    f.write(tasklist[2].strip('\n'))
                    f.write(",")
                    f.write(tasklist[3].strip('\n'))
                    f.write(",")
                    f.write(tasklist[4].strip('\n'))
                    f.write(",")
                    f.write(tasklist[5].strip('\n'))
                    f.write(",")
                    f.write(tasklist[6].strip('\n'))
                    f.write('\n')
                f.close()

        except:
            raise


def titre():
    print(Fore.RED + "  ___                     _     __     ______    ___ ")
    print(Fore.RED + "/ ___|  ___ ___  ___   __| |   /  \   |_    _| /  _  \ ")
    print(Fore.RED + "\___ \ / __|  _|/ _ \ / _' |  / /\ \    |  |  |  / \  |")
    print(Fore.RED + " ___) | (__| | |  __/| ( | | / /__\ \  _|  |_ |  \_/  |")
    print(Fore.RED + "|____/ \___|_|  \___| \_.__|/_/    \_\|______| \_____/")
    print("\n")


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
    horloge = Style.RESET_ALL + "[" + Fore.RED + heures + ":" + minutes + ":" + secondes + "." + milisecondes + Style.RESET_ALL + "]"
    return horloge


# ------------------------------------------------------------------------------------------------------------------------------------------------#

# Fonction latence
def latence(start):
    stop = timeit.default_timer()
    latence = Style.RESET_ALL + '[' + Fore.RED + str(round(stop - start, 4)) + Style.RESET_ALL + ']'
    return latence


# ----------------------------------------------------------------------------------Fonction licenses--------------------------------------------------------------#

# Informations du propriétaire à remplir 
RSAPubKey = "<RSAKeyValue><Modulus>zGKjhD1u4eZQg+U2oZgX8inZ1SLvb83jD+oKD20GplwpYcqquQZMAPokGXTs8FMD5X2sc6FtiNKg/wcapvkuyS9KRTauaoQib/B2SW7e9b4zkfpg3hJHW8zm9CZ3F2xbH5E8aXOlm0Knu9lOxjE+e7IogTQGk5RvyO4TO6QRO71bc9dW9h44KWdzku6lcF1VBHM646E6F10ziq7beGhmyLt/dbz88Yt9VP5CKBRH+/QDafbV+KD86WFTQ69p/j+k/h1QF2LYY2tVOhz9TL0iF9zpb8e4mR/vL1RGU3T3ztS21AwGwyCI2j1xc8KvWsUWnPgfDsIr4SRi6EH0d5joxQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyIyOTQ2NiIsInBGK1diMVN2TnhPd3ZZTnNxczNXd3MvZS8xT3hKK2RKZk9wbklBT1ciXQ=="


# -------------------------------------------------------------------------------------------------------------------------------------#

# Fonction de vérification les licences en ligne. (https://cryptolens.io/)
def VerificationLicense():
    with open("Data/License.txt", "r") as f:
        License = f.read()
        if License == "":
            print(Fore.RED + "Enter your License key in file : License.txt")
            time.sleep(10)
            exit()

    result = Key.activate(token=auth,
                          rsa_pub_key=RSAPubKey,
                          product_id=6868,
                          key=License,
                          machine_code=Helpers.GetMachineCode())

    if result[0] is None or not Helpers.IsOnRightMachine(result[0]):
        print("ERREUR: {0}".format(result[1]))
        print(
            Fore.RED + "Your license is invalid or you have an internet connection problem ! Check your details and try later !")
        time.sleep(10)
        exit()

    else:
        print(Fore.RED + "Your license is valid !")
        pass


# ------------------------------------------------------------------------------------------------------------------------------------------------#

# Récupérations des proxies
def proxy():
    with open('Zalando/Tasks/Proxy.txt', 'r') as f:
        liste_proxys = []
        for ligne in f:
            if ligne.strip('\n') != '':
                liste_proxys.append(ligne.strip('\n').split(":"))

        if not liste_proxys:
            print(Fore.RED + "You have not specified any proxies !")
            print(Fore.RED + "Enter the address of the proxy servers in the Proxy.txt file.")
            time.sleep(5)
            fonction_Zalando()

        return liste_proxys


# Création de la liste de compte "Liste_compte1"
def compte1():
    with open('Zalando/Accounts/Accounts_List_Paypal.csv', 'r') as f:
        Liste_compte1 = []
        for ligne in f:
            compte_list1 = ligne.split(",")
            Liste_compte1.append(compte_list1)
        Liste_compte1.pop(0)
    f.close()
    return Liste_compte1


# Création de la liste de compte "Liste_compte2"
def compte2():
    with open('Zalando/Accounts/Accounts_List_AutoCheckout.csv', 'r') as f:
        Liste_compte2 = []
        for ligne in f:
            compte_list2 = ligne.split(",")
            Liste_compte2.append(compte_list2)
        Liste_compte2.pop(0)
    f.close()
    return Liste_compte2


# Création de la liste de compte "Liste_compte3"
def compte3():
    with open('Zalando/Accounts/Accounts_List_CB.csv', 'r') as f:
        Liste_compte3 = []
        for ligne in f:
            compte_list3 = ligne.split(",")
            Liste_compte3.append(compte_list3)
        compte_list3.pop(0)
    f.close()
    return compte_list3


# Création de la liste de compte "Liste_comptegenerator"
def listecomptegenerator():
    with open('Zalando/Accounts/AccountGenerator.csv', 'r') as f:
        Liste_comptegenerator = []
        for ligne in f:
            comptegenerator_list = ligne.split(",")
            Liste_comptegenerator.append(comptegenerator_list)
        Liste_comptegenerator.pop(0)
    f.close()
    return Liste_comptegenerator


# Création de la liste de profiles "List_profile"
def profile():
    with open('Zalando/Profiles/Profiles.csv', 'r') as f:
        List_profile1 = []
        for ligne in f:
            profile_list = ligne.split(",")
            List_profile1.append(profile_list)
        List_profile1.pop(0)
    f.close()
    return List_profile1


# Création de la liste "List_Quick_Task"
def QuickTask():
    with open('Zalando/Tasks/Quick_Task.csv', 'r') as f:
        List_Quick_Task = []
        for ligne in f:
            List_Quick_Task2 = ligne.split(",")
            List_Quick_Task.append(List_Quick_Task2)
        List_Quick_Task.pop(0)
    f.close()
    return List_Quick_Task


# Création de la liste de tache "Liste_tache"
def tache():
    with open('Zalando/Tasks/Task.csv', 'r') as f:
        Liste_tache = []
        for ligne in f:
            liste_list = ligne.split(",")
            Liste_tache.append(liste_list)
        Liste_tache.pop(0)
    f.close()
    return Liste_tache


# Création de la liste "Liste_Success"
def Success():
    with open('Zalando/Success recap/Success_Recap.csv', 'r') as f:
        Liste_Success = []
        for ligne in f:
            liste_list = ligne.split(",")
            Liste_Success.append(liste_list)
        Liste_Success.pop(0)
    f.close()
    return Liste_Success


def VerificationProxys():
    list_proxy = proxy()
    for x in list_proxy:
        try:
            # Ouverture de la session
            with requests.Session() as session:
                # Réglage des paramètres de la session
                retries_2 = Retry(total=2, backoff_factor=0, status_forcelist=[429, 500, 502, 503, 504])
                session.mount("https://", TimeoutHTTPAdapter(max_retries=retries_2))
                session.headers.update(
                    {"User-Agent": generate_user_agent()}
                )
                # Réglage du proxy
                if len(x) == 4:
                    try:
                        session.proxies = {"https": "https://%s:%s@%s:%s/" % (x[2], x[3], x[0], x[1])}
                        # Connexion à la page d'accueil de Zalando
                        url_home = "https://www.zalando.fr"
                        session.get(url_home, verify=False, timeout=0.5)
                        # Test du proxy
                        print(Fore.GREEN + 'Proxy %s is OK !' % (x[0] + ":" + x[1] + ":" + x[2] + ":" + x[3]),
                              Style.RESET_ALL)
                    except:
                        session.proxies = {"http": "http://%s:%s@%s:%s/" % (x[2], x[3], x[0], x[1])}
                        # Connexion à la page d'accueil de Zalando
                        url_home = "https://www.zalando.fr"
                        session.get(url_home, verify=False)
                        # Test du proxy
                        print(Fore.GREEN + 'Proxy %s is OK !' % (x[0] + ":" + x[1] + ":" + x[2] + ":" + x[3]),
                              Style.RESET_ALL)
                else:
                    try:
                        session.proxies = {"https": "https://%s" % (x[0] + ":" + x[1])}
                        # Connexion à la page d'accueil de Zalando
                        url_home = "https://www.zalando.fr"
                        session.get(url_home, verify=False, timeout=0.5)
                        # Test du proxy
                        print(Fore.GREEN + 'Proxy %s is OK !' % (x[0] + ":" + x[1]), Style.RESET_ALL)
                    except:
                        session.proxies = {"http": "http://%s" % (x[0] + ":" + x[1])}
                        # Connexion à la page d'accueil de Zalando
                        url_home = "https://www.zalando.fr"
                        session.get(url_home, verify=False)
                        # Test du proxy
                        print(Fore.GREEN + 'Proxy %s is OK !' % (x[0] + ":" + x[1]), Style.RESET_ALL)

            session.close()
        # Gestion des exceptions
        except:
            if len(x) == 4:
                print(Fore.RED + "Proxy %s doesn't work !" % (x[0] + ":" + x[1] + ":" + x[2] + ":" + x[3]),
                      Style.RESET_ALL)
            else:
                print(Fore.RED + "Proxy %s doesn't work !" % (x[0] + ":" + x[1]), Style.RESET_ALL)


def DiscordStatutStart():
    client_id = "736398384226762763"
    RPC = Presence(client_id)
    try:
        RPC.connect()
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        RPC.update(start=timestamp, state="Version 0.0.3", details="Destroying Zalando", large_image="test",
                   small_image="start")
    except:
        pass


# Création des comptes à partir des informations saisies dans AccountGenerator.csv
def CreationComptes(Liste_comptegenerator, liste_proxys, liste):
    # Comptage du nombre de comptes présents dans la base de données
    nombrecompte = len(Liste_comptegenerator)

    # Création d'un compte pour chaque objet "Compte" présent dans la base de données
    for compte in range(0, nombrecompte):
        # Ouverture de la session
        with requests.Session() as session:
            # Réglage des paramètres de la session
            session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
            session.headers.update(
                {"User-Agent": generate_user_agent(os=("mac", "linux"))}
            )

            while True:
                # Réglage du proxy
                proxy = random.choice(liste_proxys)
                url_home = "https://www.zalando.fr"
                session.headers[
                    "Accept"
                ] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                session.headers['User-Agent'] = generate_user_agent()
                session.headers["Accept-Language"] = "fr-fr"
                session.headers["Accept-Encoding"] = "gzip, deflate, br"
                if len(proxy) == 4:
                    try:
                        session.proxies = {"https": "https://%s:%s@%s:%s/" % (proxy[2], proxy[3], proxy[0], proxy[1])}
                        # Connexion à la page d'accueil de Zalando
                        home = session.get(url_home, verify=False, timeout=0.5)
                    except:
                        session.proxies = {"http": "http://%s:%s@%s:%s/" % (proxy[2], proxy[3], proxy[0], proxy[1])}
                        # Connexion à la page d'accueil de Zalando
                        home = session.get(url_home, verify=False)
                else:
                    try:
                        session.proxies = {"https": "https://%s" % (proxy[0] + proxy[1])}
                        # Connexion à la page d'accueil de Zalando
                        home = session.get(url_home, verify=False)
                    except:
                        session.proxies = {"http": "http://%s" % (proxy[0] + proxy[1])}
                        # Connexion à la page d'accueil de Zalando
                        home = session.get(url_home, verify=False)

                if session.cookies != '<RequestsCookieJar[]>':
                    break

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
            # Choix au hasard du prénom
            listePrenom = ['Tim', 'Pierre', 'Jean', 'Tom',
                           'Jase', 'Nathan', 'Alexis',
                           'Olivier', 'Paola', 'Paolo', 'Lea',
                           'Dunvel', 'Arnaud', 'Lisa', 'Benjamin',
                           'Ines', 'Thomas', 'Romain', 'Lucile',
                           'Jules', 'Emilia', 'Emile', 'Julien',
                           'Rose', 'Juliette', 'Jasmine', 'Alexandre',
                           'Richard', 'Sophie', 'Laurent']
            random.shuffle(listePrenom)
            prenom = random.choice(listePrenom)
            # Choix au hasard du nom
            listeNom = ['Ricard', 'Dumas', 'Dufont', 'Danut',
                        'Aubris', 'Bailard', 'Dulemas', 'Bourssier',
                        'Rieta', 'Niel', 'Joels', 'Nueuto',
                        'mulier', 'Dupont', 'Dupond', 'Artoux',
                        'Balere', 'Zieta', 'Michel', 'Ricaux',
                        'Martin', 'Thomas', 'Bernard', 'Robert',
                        'Durand', 'Durant', 'Dubois', 'Moreau',
                        'Colin', 'Lucas', 'Noel', 'Duval']
            random.shuffle(listeNom)
            nom = random.choice(listeNom)
            # Data Inscription
            register = {
                "newCustomerData": {
                    "firstname": prenom,
                    "lastname": nom,
                    "email": Liste_comptegenerator[compte][0].strip('\n').lstrip('"').rstrip('"'),
                    "password": Liste_comptegenerator[compte][1].strip('\n').lstrip('"').rstrip('"'),
                    "fashion_preference": [],
                    "subscribe_to_news_letter": False,
                    "accepts_terms_and_conditions": True,
                    "date_of_birth": "",
                },
                "wnaMode": "shop",
            }
            session.get(url_get2, verify=False)
            session.headers["Origin"] = "https://www.zalando.fr"
            inscription = session.post(url_post2, json=register, verify=False)

            # Message de confirmation pour chaque compte créé
            if inscription.status_code == 201:
                print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                      Style.RESET_ALL + Fore.GREEN + "Account of %s was successfully created !" %
                      Liste_comptegenerator[compte][0].strip('\n').lstrip('"').rstrip('"'), )

            else:
                print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                      Style.RESET_ALL + Fore.RED + "There is a problem with the register ! Try later.")
                time.sleep(5)
                main()

        # Fermeture de la session
        session.close()

    # Insertion des comptes actualisés dans la base de données
    comptelist = []
    for b in range(0, len(Liste_comptegenerator)):
        comptelist.append(Liste_comptegenerator[b])
    with open("Zalando/%s" % liste, "a") as f:
        for compte_1 in comptelist:
            f.write(compte_1[0])
            f.write(",")
            f.write(compte_1[1])
        f.write('\n')
    f.close()

    # Rénitialisation du fichier AccountGenerator.csv
    comptelist2 = ['Email', 'Password']
    with open("Zalando/Accounts/AccountGenerator.csv", "w") as f:
        f.write(comptelist2[0])
        f.write(",")
        f.write(comptelist2[1])
    f.close()


# -----------------------------------------------------Ici toutes les fonction nécessaires pour zalando------------------------#
def fonction_Zalando():
    start = timeit.default_timer()  # J'ai besoin de cette ligne pour calculer la latence.
    init()
    # Proxys
    liste_proxys = proxy()
    if liste_proxys.count(['\n']) != 0:
        for x in range(0, liste_proxys.count(['\n'])):
            liste_proxys.remove(['\n'])
    random.shuffle(liste_proxys)
    # Accounts Generator
    Liste_comptegenerator = listecomptegenerator()
    if Liste_comptegenerator.count(['\n']) != 0:
        for x in range(0, Liste_comptegenerator.count(['\n'])):
            Liste_comptegenerator.remove(['\n'])
    # Accounts
    Liste_compte1 = compte1()
    if Liste_compte1.count(['\n']) != 0:
        for x in range(0, Liste_compte1.count(['\n'])):
            Liste_compte1.remove(['\n'])
    random.shuffle(Liste_compte1)
    Liste_compte2 = compte2()
    if Liste_compte2.count(['\n']) != 0:
        for x in range(0, Liste_compte2.count(['\n'])):
            Liste_compte2.remove(['\n'])
    random.shuffle(Liste_compte2)
    Liste_compte3 = []
    for x in Liste_compte1:
        Liste_compte3.append(x)
    for y in Liste_compte2:
        Liste_compte3.append(y)
    random.shuffle(Liste_compte3)
    # Profiles
    List_profile1 = profile()
    if List_profile1.count(['\n']) != 0:
        for x in range(0, List_profile1.count(['\n'])):
            List_profile1.remove(['\n'])
    # Tasks
    Liste_tache = tache()
    if Liste_tache.count(['\n']) != 0:
        for x in range(0, Liste_tache.count(['\n'])):
            Liste_tache.remove(['\n'])
    # Quick Tasks
    List_Quick_Task = QuickTask()
    if List_Quick_Task.count(['\n']) != 0:
        for x in range(0, List_Quick_Task.count(['\n'])):
            List_Quick_Task.remove(['\n'])
    # Check Database
    if Liste_compte1 == [] and Liste_compte2 == []:
        print(Fore.RED + "You have not specified any accounts !")
        print(Fore.RED + "You have to use the Account Generator.")
    if not List_profile1:
        print(Fore.RED + "You have not specified any profiles !")
        print(Fore.RED + "You have to complete the Profiles files.")

    while True:
        try:
            print("")
            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]", Style.RESET_ALL + "> 1. Quick Tasks")
            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]", Style.RESET_ALL + "> 2. Optimised Tasks")
            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]", Style.RESET_ALL + "> 3. Generated Accounts")
            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]", Style.RESET_ALL + "> 4. Proxy Check")
            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]", Style.RESET_ALL + "> 5. Main Menu")
            choix = int(input("\nChoice :"))
            if choix == 1:
                # Réglages Thread
                Paiement = 'CB_Auto'
                Mode = 'Quick'
                if len(List_Quick_Task) == 0:
                    print(Fore.RED + 'The file Quick_Task.csv is empty !')
                    time.sleep(3)
                    fonction_Zalando()
                if List_Quick_Task[0] == 1:
                    Liste_compte = Liste_compte1
                    message = 'Accounts_List_Paypal.csv'
                if List_Quick_Task[0] == 2:
                    Liste_compte = Liste_compte2
                    message = 'Accounts_List_AutoCheckout.csv'
                if List_Quick_Task[0] == 3:
                    Liste_compte = Liste_compte3
                List_profile = List_Quick_Task
                thread_list = []
                # Check Database
                if Liste_compte1 == [] and Liste_compte2 == []:
                    print(Fore.RED + "You have not specified any accounts !")
                    print(Fore.RED + "You have to use the Account Generator.")
                    time.sleep(3)
                    fonction_Zalando()
                if len(Liste_tache) == 0:
                    print(Fore.RED + 'The file Task.csv is empty !')
                    time.sleep(3)
                    fonction_Zalando()
                if len(List_Quick_Task) == 0:
                    print(Fore.RED + 'The file Quick_Task.csv is empty !')
                    time.sleep(3)
                    fonction_Zalando()
                if len(Liste_compte) < len(Liste_tache):
                    print(Fore.RED + 'You must have a greater number of accounts than the number of tasks !')
                    time.sleep(3)
                    fonction_Zalando()
                if len(Liste_compte) == 0:
                    print(Fore.RED + 'The file %s is empty !' % message)
                    time.sleep(3)
                    fonction_Zalando()
                # Start Thread
                for x in range(0, len(Liste_tache)):
                    url_produit = Liste_tache[x][0].lstrip('"').rstrip('"')
                    taille_produit = Liste_tache[x][1].lstrip('"').rstrip('"')
                    quantite = Liste_tache[x][2].lstrip('"').rstrip('"')
                    Task = x
                    thread = RechercheCommande(liste_proxys,
                                               List_profile,
                                               Liste_compte,
                                               url_produit,
                                               taille_produit,
                                               Paiement,
                                               Mode,
                                               Task,
                                               List_Quick_Task,
                                               quantite)
                    thread.start()
                    thread_list.append(thread)
                # Join Thread
                time.sleep(2)
                for t in thread_list:
                    t.join()
                main()

            if choix == 2:
                # Check Database
                if Liste_compte1 == [] and Liste_compte2 == []:
                    print(Fore.RED + "You have not specified any accounts !")
                    print(Fore.RED + "You have to use the Account Generator.")
                    time.sleep(3)
                    fonction_Zalando()
                if not List_profile1:
                    print(Fore.RED + "You have not specified any profiles !")
                    print(Fore.RED + "You have to complete the Profiles files.")
                    time.sleep(3)
                    fonction_Zalando()
                if len(Liste_tache) == 0:
                    print(Fore.RED + 'The file Task.csv is empty !')
                    time.sleep(3)
                    fonction_Zalando()
                # Choix du mode de paiement
                while True:
                    try:
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> 1. Credit Card Autocheckout")
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> 2. Credit Card Manual Checkout")
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> 3. Paypal Manual Checkout")
                        choix_2 = int(input("\nChoice :"))
                        if choix_2 == 1:
                            Paiement = 'CB_Auto'
                            break
                        if choix_2 == 2:
                            Paiement = 'CB'
                            break
                        if choix_2 == 3:
                            Paiement = 'Paypal'
                            break
                    except:
                        pass
                # Choix du profile
                while True:
                    try:
                        # Affichage des profiles
                        for u in range(0, len(List_profile1)):
                            print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                                  Style.RESET_ALL + "> %s. Profile%s" % (u + 1, u + 1))
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> %s. Select Multiple Profiles" % (len(List_profile1) + 1))
                        choix_3 = int(input("\nChoice :"))
                        # Choix
                        if choix_3 == len(List_profile1) + 1:
                            List_profilebis = []
                            for u in range(0, len(List_profile1)):
                                List_profilebis.append(List_profile1[u])
                            random.shuffle(List_profilebis)
                            List_profile = random.choice(List_profilebis)
                            break
                        if choix_3 < (len(List_profile1) + 1):
                            List_profile = List_profile1[choix_3 - 1]
                            break
                    except:
                        pass
                # Choix liste compte
                while True:
                    try:
                        # Affichage des propositions
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> 1. List 1")
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> 2. List 2")
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> 3. Select Multiple Lists")
                        choix_4 = int(input("\nChoice :"))
                        # Réglage du Thread
                        if choix_4 == 1:
                            Liste_compte = Liste_compte1
                            message = 'Accounts_List_Paypal.csv'
                        if choix_4 == 2:
                            Liste_compte = Liste_compte2
                            message = 'Accounts_List_AutoCheckout.csv'
                        thread_list = []
                        Mode = 'Normal'
                        # Check DB
                        if len(Liste_compte) < len(Liste_tache):
                            print(
                                Fore.RED + 'You must have a greater number of accounts than the number of tasks !')
                            time.sleep(5)
                            fonction_Zalando()
                        if len(Liste_compte) == 0:
                            print(Fore.RED + 'The file %s is empty !' % message)
                            time.sleep(5)
                            fonction_Zalando()
                        if choix_4 == 3:
                            Liste_compte = Liste_compte3
                            if len(Liste_compte) < len(Liste_tache):
                                print(
                                    Fore.RED + 'You must have a greater number of accounts than the number of tasks !')
                                time.sleep(5)
                                fonction_Zalando()
                        # Start Thread
                        for x in range(0, len(Liste_tache)):
                            url_produit = Liste_tache[x][0].lstrip('"').rstrip('"')
                            taille_produit = Liste_tache[x][1].lstrip('"').rstrip('"')
                            quantite = Liste_tache[x][2].lstrip('"').rstrip('"')
                            Task = x
                            thread = RechercheCommande(liste_proxys,
                                                       List_profile,
                                                       Liste_compte,
                                                       url_produit,
                                                       taille_produit,
                                                       Paiement,
                                                       Mode,
                                                       Task,
                                                       List_Quick_Task,
                                                       quantite)
                            thread.start()
                            thread_list.append(thread)
                        # Join Thread
                        time.sleep(2)
                        for t in thread_list:
                            t.join()
                        main()
                    except:
                        pass

            if choix == 3:
                if len(Liste_comptegenerator) == 0:
                    print(Fore.RED + 'The file AccountsGenerator.csv is empty !')
                    time.sleep(5)
                    fonction_Zalando()
                while True:
                    try:
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> 1. List 1")
                        print(horloge(), "[Scred AIO]", Fore.RED + "[Zalando]",
                              Style.RESET_ALL + "> 2. List 2")
                        choix_2 = int(input("\nChoice :"))
                        if choix_2 == 1:
                            liste = 'Accounts/Accounts_List_Paypal.csv'
                            CreationComptes(Liste_comptegenerator, liste_proxys, liste)
                            fonction_Zalando()
                        if choix_2 == 2:
                            liste = 'Accounts/Accounts_List_AutoCheckout.csv'
                            CreationComptes(Liste_comptegenerator, liste_proxys, liste)
                            fonction_Zalando()
                    except:
                        pass

            if choix == 4:
                VerificationProxys()

            if choix == 5:
                main()

        except:
            pass


# ----------------------------Initialisation du programme-------------------------------------------------------------#
def main():
    while True:
        titre()
        start = timeit.default_timer()  # J'ai besoin de cette ligne pour calculer la latence.
        while True:
            try:
                print(horloge(), "[Scred AIO]", latence(start), "> 1. Zalando")
                choix_depart = int(input("\nChoice :"))
                if choix_depart == 1:
                    fonction_Zalando()
            except:
                pass


# --------------------------------------------------------------------------------------------------------------------#

init()
print(Fore.YELLOW + "Data loading ...")
DiscordStatutStart()
print(Fore.GREEN + "Welcome ! Initializing Scred AIO - User data loaded !\n")
main()
