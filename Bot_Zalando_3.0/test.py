import requests
import httpx
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from user_agent import generate_user_agent
import requests.auth
import urllib3
import pickle
import json
import json
import random
import time


def VerificationProxys():
    # Ouverture de la session
    # first load the home page
    home_page_link = 'https://www.zalando.fr'
    login_api_schema = "https://www.zalando.fr/api/reef/login/schema"
    login_api_post = "https://www.zalando.fr/api/reef/login"
    urlbot = 'https://www.zalando.fr/resources/08a9da6c9arn2028b315fc23b805e921'
    databot1 = {
        "sensor_data": "7a74G7m23Vrp0o5c9189171.6-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15,uaend,11011,20030107,fr,Gecko,1,0,0,0,393019,698443,1440,811,1440,900,1440,252,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.664537137332,798665349221.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,4703,undefined,0,0,2528,0;1,2,4752,undefined,0,0,2528,0;2,1,4766,undefined,0,0,2528,0;3,2,4784,undefined,0,0,2528,0;-1,2,-94,-110,0,1,332,730,42;1,1,529,769,104;2,1,534,562,48;3,1,548,552,40;4,1,695,548,37;5,1,1245,528,50;6,1,1588,572,209;7,1,1609,576,197;8,3,1621,576,197,1103;9,1,2544,576,197;10,4,2640,576,197,1103;11,1,3165,589,216;12,1,3437,589,217;13,1,3474,589,222;14,1,4795,595,244;15,1,5511,596,574;16,1,5526,779,514;17,1,5532,829,505;18,1,5537,829,505;19,1,5550,865,501;20,1,5555,885,500;21,1,5566,905,498;22,1,5571,922,496;23,1,5583,937,494;24,1,5588,952,492;25,1,5588,952,492;26,1,5596,956,491;27,1,5597,956,491;28,1,5604,966,490;29,1,5605,966,490;30,1,5612,974,489;31,1,5613,974,489;32,1,5621,979,488;33,1,5621,979,488;34,1,5628,985,488;35,1,5630,985,488;36,1,5636,988,488;37,1,5637,988,488;38,1,5645,990,488;39,1,5647,990,488;40,1,5652,992,487;41,1,5653,992,487;42,1,5662,992,487;43,1,5664,992,487;44,1,5669,993,487;45,1,5670,993,487;46,1,5683,993,487;47,1,5688,993,487;48,1,5694,993,487;49,1,5710,994,487;50,1,5713,994,487;51,1,5718,994,487;52,1,5729,994,488;53,1,5741,994,490;54,1,5743,994,491;55,1,5750,994,492;56,1,5752,994,492;57,1,5757,994,494;58,1,5758,994,494;59,1,5769,994,496;60,1,5774,994,498;61,1,5776,994,498;62,1,5782,994,501;63,1,5783,994,501;64,1,5790,993,503;65,1,5791,993,503;66,1,5798,992,506;67,1,5799,992,506;68,1,5806,990,508;69,1,5807,990,508;70,1,5814,988,511;71,1,5814,988,511;72,1,5822,985,512;73,1,5824,985,512;74,1,5830,984,514;75,1,5831,984,514;76,1,5839,982,516;77,1,5840,982,516;78,1,5846,981,517;79,1,5847,981,517;80,1,5854,978,519;81,1,5855,978,519;82,1,5863,978,519;83,1,5864,978,519;84,1,5871,976,520;85,1,5872,976,520;86,1,5879,975,521;87,1,5879,975,521;88,1,5887,975,521;89,1,5888,975,521;90,1,5895,974,522;91,1,5896,974,522;92,1,5904,974,522;93,1,5905,974,522;94,1,5911,974,522;95,1,5912,974,522;96,1,5919,973,523;97,1,5920,973,523;98,3,5957,973,523,1929;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,1600;2,3988;3,4765;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,NaN,650563,32,0,0,0,NaN,5957,0,1597330698443,25,17087,4,99,2847,3,0,5958,529879,0,8B67C98F047A1511B9B3DE521214EFD1~-1~YAAQPpHdWDrS3NxzAQAAMTdU6ATr+gk/dN/rsLG27CQnbySqmZIIHvAMCjrHm3AQ5gWKTvx55gKEVOZVSSuW+4eGyNBAudLuNTPfaEvMBii3oZ4jrTo56HDYwlzMQ9UMHMQMOe4FmQicODir61fhoob/TDxmFjVGlLg0WSlvjIyWypXfGB4Qs2AA1E0PS9iw1i4avLnppKkCbho2wV5/35DGzktt6H2052t0ZwqYfv4lG5DjFKC5UxoTOhzvjOMQwMsF3TWbHlhjKKoOHFOwwP6z8vTAgHbDYoXmEyi4k66OZR2COz4YV0oOswAEN23wFN8395KEz5LN13a7HXOAQVkZOSQ=~-1~-1~-1,32132,623,2080369960,26018161,PiZtE,57490,62-1,2,-94,-106,1,3-1,2,-94,-119,2200,7000,0,0,0,0,0,0,0,2000,200,800,3000,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,471446355-1,2,-94,-118,187387-1,2,-94,-121,;1;15;0"
    }
    databot2 = {
        "sensor_data": "7a74G7m23Vrp0o5c9189171.6-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15,uaend,11011,20030107,fr,Gecko,1,0,0,0,393019,698443,1440,811,1440,900,1440,252,1440,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,8919,0.382916112191,798665349221.5,loc:-1,2,-94,-101,do_dis,dm_dis,t_dis-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,4703,undefined,0,0,2528,0;1,2,4752,undefined,0,0,2528,0;2,1,4766,undefined,0,0,2528,0;3,2,4784,undefined,0,0,2528,0;-1,2,-94,-110,0,1,332,730,42;1,1,529,769,104;2,1,534,562,48;3,1,548,552,40;4,1,695,548,37;5,1,1245,528,50;6,1,1588,572,209;7,1,1609,576,197;8,3,1621,576,197,1103;9,1,2544,576,197;10,4,2640,576,197,1103;11,1,3165,589,216;12,1,3437,589,217;13,1,3474,589,222;14,1,4795,595,244;15,1,5511,596,574;16,1,5526,779,514;17,1,5532,829,505;18,1,5537,829,505;19,1,5550,865,501;20,1,5555,885,500;21,1,5566,905,498;22,1,5571,922,496;23,1,5583,937,494;24,1,5588,952,492;25,1,5588,952,492;26,1,5596,956,491;27,1,5597,956,491;28,1,5604,966,490;29,1,5605,966,490;30,1,5612,974,489;31,1,5613,974,489;32,1,5621,979,488;33,1,5621,979,488;34,1,5628,985,488;35,1,5630,985,488;36,1,5636,988,488;37,1,5637,988,488;38,1,5645,990,488;39,1,5647,990,488;40,1,5652,992,487;41,1,5653,992,487;42,1,5662,992,487;43,1,5664,992,487;44,1,5669,993,487;45,1,5670,993,487;46,1,5683,993,487;47,1,5688,993,487;48,1,5694,993,487;49,1,5710,994,487;50,1,5713,994,487;51,1,5718,994,487;52,1,5729,994,488;53,1,5741,994,490;54,1,5743,994,491;55,1,5750,994,492;56,1,5752,994,492;57,1,5757,994,494;58,1,5758,994,494;59,1,5769,994,496;60,1,5774,994,498;61,1,5776,994,498;62,1,5782,994,501;63,1,5783,994,501;64,1,5790,993,503;65,1,5791,993,503;66,1,5798,992,506;67,1,5799,992,506;68,1,5806,990,508;69,1,5807,990,508;70,1,5814,988,511;71,1,5814,988,511;72,1,5822,985,512;73,1,5824,985,512;74,1,5830,984,514;75,1,5831,984,514;76,1,5839,982,516;77,1,5840,982,516;78,1,5846,981,517;79,1,5847,981,517;80,1,5854,978,519;81,1,5855,978,519;82,1,5863,978,519;83,1,5864,978,519;84,1,5871,976,520;85,1,5872,976,520;86,1,5879,975,521;87,1,5879,975,521;88,1,5887,975,521;89,1,5888,975,521;90,1,5895,974,522;91,1,5896,974,522;92,1,5904,974,522;93,1,5905,974,522;94,1,5911,974,522;95,1,5912,974,522;96,1,5919,973,523;97,1,5920,973,523;98,3,5957,973,523,1929;99,4,6031,973,523,1929;100,2,6031,973,523,1929;101,1,6930,922,515;102,1,6935,910,527;103,1,6937,907,529;104,1,6938,904,530;170,3,9566,762,344,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,3,1600;2,3988;3,4765;-1,2,-94,-112,https://www.zalando.fr/login/?view=login-1,2,-94,-115,NaN,710565,32,0,0,0,NaN,9566,0,1597330698443,25,17087,4,171,2847,5,0,9568,579247,0,8B67C98F047A1511B9B3DE521214EFD1~-1~YAAQPpHdWD3S3NxzAQAAIkhU6ARAGTqT+gVNp6QJTxnJPQXIO7cw8DKRItdIZ+vqeYXsceiodNEDCsq2l/oZpqizEUUFzE5RG5JbA0+bw53ld9HRF3mICRl4ZCufz74YynC/yXNnMEYD8VQHqU5sMEgllLLePXKvrBbpkXf7XI0avqeAXwBxVOUd82dJdUdXoJP0T4qV03yrzbN90KNPPE8EogNzU87HLzkqqd/3D3kM3Z2qB9VQEKiAvSmrm0C5fipfrrUisz9rPhTCX0qEhawvSiu457l9QDCdddvLl9yxXJdMtaEYvEvVcGC0REWKlAesjDZfETskoaWZuoUGNtHZi5o=~-1~-1~-1,32749,623,2080369960,26018161,PiZtE,96793,48-1,2,-94,-106,1,4-1,2,-94,-119,2200,7000,0,0,0,0,0,0,0,2000,200,800,3000,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,1637755981;218306863;dis;;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,5266-1,2,-94,-116,471446355-1,2,-94,-118,195391-1,2,-94,-121,;2;15;0"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fr-fr',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.fr',
        'Host': 'www.zalando.fr',
        'DNT': '1',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1'
    }

    if __name__ == '__main__':
        with requests.Session() as s:
            s.headers.update(headers)

            s.trust_env = False
            s.proxies = {
                "http": "http://alex19132-country-FR:a6a17f-060e0d-374951-a1257e-2e7e9c@premium.residential.rotating.proxyrack.net:9000",
                "https": "http://alex19132-country-FR:a6a17f-060e0d-374951-a1257e-2e7e9c@premium.residential.rotating.proxyrack.net:9000"
            }



            r = s.get(home_page_link, verify=False)

            # fetch these cookies: frsx, Zalando-Client-Id
            cookie_dict = s.cookies.get_dict()
            # update the headers
            # remove this header for the xhr requests
            del s.headers['Upgrade-Insecure-Requests']
            # these 2 are taken from some response cookies
            s.headers['Referer'] = 'https://www.zalando.fr/'
            s.headers['x-xsrf-token'] = cookie_dict['frsx']
            s.headers['x-zalando-client-id'] = cookie_dict['Zalando-Client-Id']
            s.headers['Accept'] = '*/*'
            s.headers['Content-Type'] = 'text/plain;charset=UTF-8'
            s.post(urlbot, json=databot1, verify=False)
            s.post(urlbot, json=databot2, verify=False)
            del s.headers['Content-Type']

            # i didn't pay attention to where these came from
            # just saw them and manually added them
            s.headers['x-zalando-render-page-uri'] = '/'
            s.headers['x-zalando-request-uri'] = '/'
            # this is sent as a response header and is needed to
            # track future requests/responses
            s.headers['x-flow-id'] = r.headers['X-Flow-Id']
            # only accept json data from xhr requests
            s.headers['Accept'] = 'application/json'

            # when clicking the login button this request is sent
            # i didn't test without this request
            r = s.get(login_api_schema, verify=False)

            # add an origin header
            s.headers['Origin'] = 'https://www.zalando.fr'
            # finally log in, this should return a 201 response with a cookie
            login_data = {"username": "alexis.balayre@gmail.com", "password": "Dubai007", "wnaMode": "modal"}
            r = s.post(login_api_post, json=login_data, verify=False)
            print(r.status_code)
            print(r.headers)



urllib3.disable_warnings()
VerificationProxys()
