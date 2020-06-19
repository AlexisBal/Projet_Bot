import requests
import timeit
from bs4 import BeautifulSoup
#from conf import *
from Generateurbien import *
import time

start = timeit.default_timer()
#url = URLGen()
url = "https://www.zalando.fr/nike-sportswear-air-force-1-07-an20-baskets-basses-whiteblack-ni112o0cl-a11.html"
print(url)
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

'''requette = requests.get(url, headers= header)
print(requette)

soup = BeautifulSoup(requette.text, 'lxml')'''

sensor_data = {"sensor_data":"7a74G7m23Vrp0o5c9175931.59-1,2,-94,-100,Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36,uaend,12147,20030107,fr-FR,Gecko,3,0,0,0,391854,8363491,1536,824,1536,864,1006,722,1536,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:1,bat:1,x11:0,x12:1,8315,0.18944723294,796299181745.5,loc:-1,2,-94,-101,do_en,dm_en,t_en-1,2,-94,-105,0,-1,0,0,1103,1103,0;1,-1,0,0,1466,1466,0;-1,2,-94,-102,0,-1,0,0,1103,1103,1;1,-1,0,0,1466,1466,1;-1,2,-94,-108,0,1,4499,17,0,4,-1;1,1,4685,undefined,0,0,-1;2,2,4688,undefined,0,0,-1;3,1,4689,69,0,4,-1;-1,2,-94,-110,0,1,142,-1,-1;1,1,142,-1,-1;2,1,149,70,3;3,1,157,75,7;4,1,165,80,11;5,1,173,84,15;6,1,181,90,21;7,1,190,96,26;8,1,197,104,31;9,1,205,110,36;10,1,213,117,42;11,1,221,123,46;12,1,229,128,50;13,1,237,134,54;14,1,246,140,57;15,1,253,145,59;16,1,261,152,63;17,1,269,160,66;18,1,277,168,70;19,1,285,179,74;20,1,293,191,78;21,1,301,207,84;22,1,309,221,90;23,1,317,236,98;24,1,325,248,106;25,1,333,262,114;26,1,341,271,122;27,1,349,280,130;28,1,357,288,138;29,1,365,296,146;30,1,373,303,154;31,1,381,310,164;32,1,390,316,173;33,1,398,321,181;34,1,434,340,210;35,1,437,344,218;36,1,445,349,226;37,1,453,355,234;38,1,461,361,242;39,1,469,367,248;40,1,477,372,254;41,1,486,376,260;42,1,493,380,266;43,1,523,390,278;44,1,525,393,282;45,1,533,396,286;46,1,542,400,289;47,1,549,402,292;48,1,557,405,294;49,1,565,408,297;50,1,573,411,300;51,1,581,415,303;52,1,590,420,306;53,1,598,425,310;54,1,606,432,313;55,1,613,440,316;56,1,621,450,321;57,1,629,459,324;58,1,638,468,328;59,1,645,476,331;60,1,653,484,334;61,1,661,491,337;62,1,669,494,338;63,1,677,496,338;64,1,685,499,340;65,1,694,500,340;66,1,701,501,341;67,1,710,502,342;68,1,717,504,342;69,1,729,506,343;70,1,733,508,344;71,1,741,512,345;72,1,749,516,346;73,1,757,520,347;74,1,765,523,349;75,1,773,525,350;76,1,781,528,351;77,1,790,532,353;78,1,798,536,354;79,1,806,542,356;80,1,813,547,357;81,1,821,551,358;82,1,829,556,358;83,1,837,559,359;84,1,845,562,360;85,1,853,564,360;86,1,870,565,360;87,1,910,567,360;88,1,918,569,360;89,1,925,573,360;90,1,933,582,360;91,1,941,591,358;92,1,949,598,358;93,1,957,607,358;94,1,965,614,358;95,1,973,620,358;96,1,981,626,358;97,1,990,631,358;98,1,997,636,358;99,1,1005,640,358;162,3,7263,764,359,-1;163,4,7325,764,359,-1;164,2,7326,764,359,-1;257,3,12454,703,342,-1;-1,2,-94,-117,-1,2,-94,-111,0,76,-1,-1,-1;-1,2,-94,-109,0,75,-1,-1,-1,-1,-1,-1,-1,-1,-1;-1,2,-94,-114,-1,2,-94,-103,2,4690;3,7261;2,8341;3,12453;-1,2,-94,-112,https://www.zalando.fr/login?target=/myaccount/-1,2,-94,-115,NaN,162803,32,76,75,0,NaN,12454,0,1592598363491,10,17037,4,258,2839,3,0,12455,109048,0,477A99D965D2622F881374ACD769C7B2~-1~YAAQfiMVAt87acFyAQAAIppCzgQGadKh8X78qtpKBik+w+93wmM/UF6eASy044H1fgLXULksXrmEuKiGQvMvZJKgaz1QptMcR7lsanpPhDcaLwkJvvwJ6B/J6Cute/5JZzn4tAVQ95MKURH3rKcmNjbZmkCtV1uU0jH8y+UFZA/h1hF/Fb+GH8I9FN079qwIzg9HVcgQkQaurwpX739i7ZpF07Px3bOmXZesRfZ6FlFz9D6NfPd1AV8DzbVECgPcaSudf2wHg+T4QkNkTvzvirC5zBgmueC9H7VNkcDJFWYdYPftL90oNd9GqDZR5/CmJQRM3h6D2crjYE0WQxuPi8RREac=~-1~-1~-1,32243,894,1404342648,30261693,NVVP,124,-1-1,2,-94,-106,1,3-1,2,-94,-119,5,7,7,6,14,15,10,6,8,4,4,1067,1182,205,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,11321144241322243122-1,2,-94,-70,1454252292;895908107;dis;,7,8;true;true;true;-120;true;24;24;true;false;-1-1,2,-94,-80,5534-1,2,-94,-116,125452512-1,2,-94,-118,185329-1,2,-94,-121,;5;7;0"}

securite = {
    "event":"event_tracking",
    "eventCategory":"checkout",
    "eventAction":"click",
    "eventLabel":"log in",
    "flowId":"ZvkoDZVfYey652AM",
    "host":"www.zalando.fr",
    "pathname":"/login",
    "referrer":"https://www.zalando.fr/cart/",
    "accept_language":"fr-FR",
    "timestamp":"2020-06-19T20:11:55.884Z"}

login_data =    {
    "username": "uzenetelenyelo@gmail.com", 
    "password": "Comptechaussures20", 
    "wnaMode" : "shop"}

with requests.session() as s:

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = "https://www.zalando.fr/login?target=/myaccount/"
    r= s.get(url, headers=header)
    soup = BeautifulSoup(r.content, 'lxml')
    
    r=s.post(url, data=sensor_data, headers=header)
    time.sleep(1)
    r= s.post(url, data=login_data, headers=header)
    print(r.content)




stop = timeit.default_timer()
print (stop - start)