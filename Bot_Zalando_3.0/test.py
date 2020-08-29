import requests
import httpx
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from user_agent import generate_user_agent
import requests.auth
import urllib3
from requests.auth import HTTPBasicAuth
import pickle
import json
import json
import random
import time


def VerificationProxys():
    # Ouverture de la session
    # first load the home page
    url_test_Ip = 'https://httpbin.org/ip'
    home_page_link = 'https://www.zalando.fr/'
    login_page = 'https://www.zalando.fr/myaccount/'
    login_api_schema = "https://www.zalando.fr/api/reef/login/schema"
    login_api_post = "https://www.zalando.fr/api/reef/login"
    urlbot = 'https://www.zalando.fr/resources/21fc8621fcrn205b4cb8c19079dd8bfe'
    databot1 = {
        "sensor_data": "7a74G7m23Vrp0o5c9189491.62-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15,uaend,11011,20030107,fr,Gecko,1,0,0,0,393047,4427649,1920,1080,1920,1080,1920,432,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.453452179226,798722213824.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1005,-1,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1005,-1,0;0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-108,-1,2,-94,-110,0,1,328,1336,24;1,1,1849,1336,25;2,1,2251,1327,79;3,1,2333,1394,50;4,1,2555,1329,73;5,1,2566,1310,82;6,1,2605,1332,72;7,1,2707,1336,70;8,1,2713,1339,68;9,1,2907,1339,71;10,1,3164,1337,112;11,1,3191,1342,147;12,1,3232,1342,151;13,1,3268,1338,162;14,1,3283,1336,164;15,1,3289,1335,166;16,1,3296,1335,166;17,1,3427,1335,166;18,1,3429,1334,165;19,1,3433,1333,164;20,1,3443,1332,162;21,1,3498,1332,161;22,1,3705,1331,160;23,1,3719,1331,159;24,1,3724,1331,158;25,1,3724,1331,158;26,1,4018,1331,157;27,1,4075,1333,142;28,1,4165,1334,139;29,1,4655,1336,136;30,1,4820,1340,120;31,3,4846,1340,120,-1;32,4,5025,1340,120,-1;33,2,5026,1340,120,-1;34,1,6046,1234,186;35,1,6124,1210,196;36,1,6155,1200,196;37,1,6177,1200,196;38,1,6396,1199,196;39,1,6512,1070,216;40,1,6525,1048,226;41,1,6830,1048,226;42,1,6869,1291,116;43,1,6899,1206,116;44,1,6910,1203,116;45,1,6911,1203,116;46,1,6920,1199,116;47,1,6920,1199,116;48,1,6929,1195,116;49,1,6930,1195,116;50,1,6943,1192,116;51,1,6944,1192,116;52,1,6952,1185,116;53,1,6953,1185,116;54,1,6963,1176,116;55,1,6964,1176,116;56,1,6976,1166,116;57,1,6977,1166,116;58,1,6986,1159,116;59,1,6987,1159,116;60,1,6997,1148,115;61,1,7002,1148,115;62,1,7010,1135,115;63,1,7010,1135,115;64,1,7032,1109,113;65,1,7032,1109,113;66,1,7043,1100,112;67,1,7075,1096,111;68,1,7079,1082,107;69,1,7113,1074,105;70,1,7116,1047,99;71,1,7121,1037,97;72,1,7124,1037,97;73,1,7133,1032,96;74,1,7134,1032,96;75,1,7146,1028,94;76,1,7148,1028,94;77,1,7156,1025,93;78,1,7157,1025,93;79,1,7168,1024,93;80,1,7169,1024,93;81,1,7180,1024,93;82,1,7181,1024,93;83,1,7734,1020,92;84,1,7736,1020,92;85,1,7742,1009,90;86,1,7743,1009,90;87,1,7750,1000,88;88,1,7751,1000,88;89,1,7765,990,87;90,1,7766,990,87;91,1,7776,983,85;92,1,7777,983,85;93,1,7786,977,85;94,1,7786,977,85;95,1,7798,969,84;96,1,7843,959,83;97,1,7862,956,83;98,1,7930,956,83;99,1,7935,950,76;100,1,7946,940,65;101,1,7948,940,65;102,1,7972,907,35;110,3,8360,898,32,1103;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,4811;-1,2,-94,-112,https://www.zalando.fr/-1,2,-94,-115,1,756472,32,0,0,0,756440,8360,0,1597444427649,37,17089,0,111,2848,3,0,8361,617999,0,714D1852BCE26E3A820E71C365942E32~-1~YAAQO5HdWJXQxuVzAQAAuKcb7wTA7JvlDTzlmqob5nGlACkeqKUOgodrwGlFHti1ImPerhBzDQEVdExzRwjExi2IDckJTc/tG9lyNzoUc8CAoIJKMErjW4UGh37s4vCgeKx+SQsBlrCN43c02bORWtTF9QkRjpBH9AZFHFvfe3sgqDjgpsrpXYGLrSVAr5T+2krS7KxbcSSVYG6nqnJuuHlPuRdzGdR2wKCzhU/DJiariNMKwCJwdsePinE9Y1rLApjC07TKZto/CGiaKqOMG3mG4gZYxupY3MT+wYggN8CDftArxMbD7BRSAgpIe0FtPWNbSHFbSz+shFwX7ORqdvCZ/L0=~-1~-1~-1,33091,849,974130393,26018161,PiZtE,29433,46-1,2,-94,-106,1,4-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,200,3200,3800,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,66414831-1,2,-94,-118,184786-1,2,-94,-121,;2;4;0"
    }
    databot2 = {
        "sensor_data": "7a74G7m23Vrp0o5c9189491.62-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15,uaend,11011,20030107,fr,Gecko,1,0,0,0,393047,4427649,1920,1080,1920,1080,1920,432,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.634607788317,798722213824.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,0,0,0,-1,113,0;0,-1,0,0,1005,-1,0;-1,2,-94,-102,0,0,0,0,-1,113,0;0,-1,0,0,1005,-1,0;0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,10830,undefined,0,0,1103,0;1,2,10835,undefined,0,0,1103,0;2,1,10885,undefined,0,0,1103,0;3,2,10888,undefined,0,0,1103,0;-1,2,-94,-110,0,1,328,1336,24;1,1,1849,1336,25;2,1,2251,1327,79;3,1,2333,1394,50;4,1,2555,1329,73;5,1,2566,1310,82;6,1,2605,1332,72;7,1,2707,1336,70;8,1,2713,1339,68;9,1,2907,1339,71;10,1,3164,1337,112;11,1,3191,1342,147;12,1,3232,1342,151;13,1,3268,1338,162;14,1,3283,1336,164;15,1,3289,1335,166;16,1,3296,1335,166;17,1,3427,1335,166;18,1,3429,1334,165;19,1,3433,1333,164;20,1,3443,1332,162;21,1,3498,1332,161;22,1,3705,1331,160;23,1,3719,1331,159;24,1,3724,1331,158;25,1,3724,1331,158;26,1,4018,1331,157;27,1,4075,1333,142;28,1,4165,1334,139;29,1,4655,1336,136;30,1,4820,1340,120;31,3,4846,1340,120,-1;32,4,5025,1340,120,-1;33,2,5026,1340,120,-1;34,1,6046,1234,186;35,1,6124,1210,196;36,1,6155,1200,196;37,1,6177,1200,196;38,1,6396,1199,196;39,1,6512,1070,216;40,1,6525,1048,226;41,1,6830,1048,226;42,1,6869,1291,116;43,1,6899,1206,116;44,1,6910,1203,116;45,1,6911,1203,116;46,1,6920,1199,116;47,1,6920,1199,116;48,1,6929,1195,116;49,1,6930,1195,116;50,1,6943,1192,116;51,1,6944,1192,116;52,1,6952,1185,116;53,1,6953,1185,116;54,1,6963,1176,116;55,1,6964,1176,116;56,1,6976,1166,116;57,1,6977,1166,116;58,1,6986,1159,116;59,1,6987,1159,116;60,1,6997,1148,115;61,1,7002,1148,115;62,1,7010,1135,115;63,1,7010,1135,115;64,1,7032,1109,113;65,1,7032,1109,113;66,1,7043,1100,112;67,1,7075,1096,111;68,1,7079,1082,107;69,1,7113,1074,105;70,1,7116,1047,99;71,1,7121,1037,97;72,1,7124,1037,97;73,1,7133,1032,96;74,1,7134,1032,96;75,1,7146,1028,94;76,1,7148,1028,94;77,1,7156,1025,93;78,1,7157,1025,93;79,1,7168,1024,93;80,1,7169,1024,93;81,1,7180,1024,93;82,1,7181,1024,93;83,1,7734,1020,92;84,1,7736,1020,92;85,1,7742,1009,90;86,1,7743,1009,90;87,1,7750,1000,88;88,1,7751,1000,88;89,1,7765,990,87;90,1,7766,990,87;91,1,7776,983,85;92,1,7777,983,85;93,1,7786,977,85;94,1,7786,977,85;95,1,7798,969,84;96,1,7843,959,83;97,1,7862,956,83;98,1,7930,956,83;99,1,7935,950,76;100,1,7946,940,65;101,1,7948,940,65;102,1,7972,907,35;110,3,8360,898,32,1103;111,4,8672,898,32,1103;112,2,8673,898,32,1103;250,3,11727,982,162,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,4811;2,9635;3,10873;-1,2,-94,-112,https:/www.zalando.fr/-1,2,-94,-115,NaN,789030,32,0,0,0,NaN,11727,0,1597444427649,37,17089,4,251,2848,5,0,11728,690509,0,714D1852BCE26E3A820E71C365942E32~-1~YAAQO5HdWMnQxuVzAQAAqa8b7wTtT9VVXzXKA+gaSbdK7rw4bx4vkwtJ5FB55SQ/0R/09ymcg6n75re562Q4l6G/KHCtiTJq5zacJJq16Yeh0+4Muf7eoPfoSv6ZBlUL5VXNI23rEno6B4bj+duPO6QlBLmay3lXfEK6Wz//JIEXIdZW4filUALB3XZwYiyOp8ecc7W0VTffEjPUAWDqbVyn3G2SLg/jPGnQY2FPdVvG2fRJ+FJJU7FROuWGZORdB4NuaUrkzqGg5Nln7K9hXgHlG7Nzgj73Ju+fozZJ4MY+QoMBocynFS35BT8xLIlSG9oM+ArYLfoaucd5ZmLGMPsHPUQ=~-1~-1~-1,31835,849,974130393,26018161,PiZtE,17650,80-1,2,-94,-106,1,5-1,2,-94,-119,0,0,0,0,0,0,0,0,0,0,0,600,600,400,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,66414831-1,2,-94,-118,195847-1,2,-94,-121,;1;4;0"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fr-fr',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'www.zalando.fr',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.fr'
    }
    proxies = {
        'http': 'http://alex19132-country-FR-city-Paris:a6a17f-060e0d-374951-a1257e-2e7e9c@premium.residential.rotating.proxyrack.net:9000',
        'https': 'https://alex19132-country-FR-city-Paris:a6a17f-060e0d-374951-a1257e-2e7e9c@premium.residential.rotating.proxyrack.net:9000'
    }
    with requests.Session() as s:
        # s.proxies = proxies
        s.trust_env = False
        s.headers.update(headers)
        r = s.get(home_page_link, verify=False)
        s.get(login_page, verify=False)
        # these 2 are taken from some response cookies
        s.headers['Referer'] = 'https://www.zalando.fr/login?target=/myaccount/'
        s.headers['Accept'] = '*/*'
        s.headers['Origin'] = 'https://www.zalando.fr'
        s.headers['Content-Type'] = 'text/plain;charset=UTF-8'
        test1 = s.post(urlbot, json=databot1, verify=False)
        test2 = s.post(urlbot, json=databot2, verify=False)
        print(test1)
        print(test2)
        del s.headers['Origin']

        s.headers['x-xsrf-token'] = s.cookies['frsx']
        s.headers['x-zalando-client-id'] = s.cookies['Zalando-Client-Id']
        s.headers['x-zalando-render-page-uri'] = '/login?target=/myaccount/'
        s.headers['Referer'] = 'https://www.zalando.fr/login?target=/myaccount/'
        s.headers['x-zalando-request-uri'] = '/login?target=/myaccount/'
        s.headers['x-zalando-redirect-target'] = 'http://www.zalando.fr/myaccount/'
        s.headers['x-flow-id'] = r.headers['X-Flow-Id']
        s.headers['Accept'] = 'application/json'
        s.headers['Content-Type'] = 'application/json'
        s.get(login_api_schema)
        s.headers['Origin'] = 'https://www.zalando.fr'
        login_data = {"username": "nameb86952@icanav.net", "password": "Dubai007", "wnaMode": "shop"}
        r = s.post(login_api_post, json=login_data, verify=False)
        print(r)
        s.headers.clear()
        s.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'
        }
        print(s.get(url_test_Ip, verify=False).json())


urllib3.disable_warnings()
VerificationProxys()
