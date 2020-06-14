import urllib3
import json

http = urllib3.PoolManager(maxsize=10, block=True)

url_get = "https://www.zalando.fr/login/?view=register"
a = http.request(
    'GET',
    url_get,
    headers={
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": ""
    }
)
print(a.status)

x_flow_id = a.getheader('X-Zalando-Child-Request-Id')
Set_Cookie = a.getheader('Set-Cookie').rsplit('; ')
x_xsrf_token = Set_Cookie[0].lstrip('frsx=')
x_zalando_client_id = Set_Cookie[4].lstrip('Secure, Zalando-Client-Id=')


e = http.request(
    'GET',
    'https://www.zalando.fr/resources/a6c5863f92201d42d0a3ba96882c7b',
    headers={
        'Host': 'www.zalando.fr',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://www.zalando.fr/login/?view=register',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1'
    }
)
print(e.status)

f = http.request(
    'GET',
    'https://www.zalando.fr/api/rr/pr/sajax?flowId=ju36xvKEqGdtc9vr&try=1',
    headers={
        'Host': 'www.zalando.fr',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.zalando.fr/login/?view=register',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1'
    }
)
print(f.status)

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
url_post1 = "https://www.zalando.fr/resources/a6c5863f921840dbe8f36578d86f32"
b = http.request(
    'POST',
    url_post1,
    body=json.dumps(sensor_data).encode('utf-8'),
    headers={
        'Host': 'www.zalando.fr',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }
)
print(b.status)

url_get2 = "https://www.zalando.fr/api/reef/register/schema"
c = http.request(
    'GET',
    url_get2,
    headers={
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1',
        'Host': 'www.zalando.fr',
        'Origin': 'https://www.zalando.fr',
        'Referer': 'https://www.zalando.fr/login/?view=register',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'x-flow-id': x_flow_id,
        'x-xsrf-token': x_xsrf_token,
        'x-zalando-client-id': x_zalando_client_id,
        'x-zalando-render-page-uri': '/login/?view=register',
        'x-zalando-request-uri': '/login/?view=register'
    }
)
print(c.status)

register = {
    "newCustomerData": {
        "accepts_terms_and_conditions": "true",
        "date_of_birth": "",
        "email": "benjamain.balayre@isep.fr",
        "fashion_preference": [],
        "firstname": "alexis",
        "lastname": "balayre",
        "password": "Dubai007",
        "subscribe_to_news_letter": False
    },
    "wnaMode": "shop"
}

url_post2 = "https://www.zalando.fr/api/reef/register"
d = http.request(
    'POST',
    url_post2,
    body=json.dumps(register).encode('utf-8'),
    headers={
        'Host': 'www.zalando.fr',
        'Connection': 'keep-alive',
        'Content-Length': '241',
        'x-xsrf-token': x_xsrf_token,
        'x-zalando-render-page-uri': '/login/?view=register',
        'x-zalando-client-id': x_zalando_client_id,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-zalando-request-uri': '/login/?view=register',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'x-flow-id': x_flow_id,
        'Origin': 'https://www.zalando.fr',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.zalando.fr/login/?view=register',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1'
    }
)
print(d.status)
