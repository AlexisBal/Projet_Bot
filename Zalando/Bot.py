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


login_data =    {
    "username": "uzenetelnyelo@gmail.com", 
    "password": "Comptechaussures20", 
    }

with requests.session() as s:

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = "https://www.zalando.fr/login?target=/myaccount/"
    r= s.get(url, headers=header)
    soup = BeautifulSoup(r.content, 'lxml')

    
    headers2 = {
        'Host': 'www.zalando.fr',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'application/json',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.zalando.fr/login?target=/myaccount/',
        'x-zalando-client-id': 'de04a38f-81e9-410b-b652-fc8c71c1c72f',
        'x-zalando-render-page-uri': '/login?target=/myaccount/',
        'x-zalando-request-uri': '/login?target=/myaccount/',
        'x-zalando-redirect-target': 'http://www.zalando.fr/myaccount/',
        'x-flow-id': 'nF2fYSzGJAfAP3qh',
        'Content-Type': 'application/json',
        'x-xsrf-token': 'AAAAAIJVngpguH27Vc7evBur5ScwR2kngRAolGq-pSxzgkh1jaBSN1PmV4O8i7B3nz6tYjetgsnAV4j2YdNDhZcalCImAUVSEugUbzBQTxNmkeyEGaPbeC_DWzcDhY6YOJwYi3NyBQspnD0jYCqmrhA=',
        'Connection': 'keep-alive',
        'Cookie': 'Zalando-Client-Id=de04a38f-81e9-410b-b652-fc8c71c1c72f; _abck=B5CDF9F2189AC166430F432BC127478E~-1~YAAQ1Nt6XEReZZZyAQAADMHHzgTJl9MKYAuap3JTyV+76ehqwduVUUttQxQ5pHRqgDeYuURQUmRM8UpLRRy44iFCbJkEA9dDlsywO6spw0+WFCKX8eJaSrc7xvilcN0tKo1cKe/pGzfWcd0J/wMFUaapKG3WtLM1/QTMevStNa9ULMuW/tqj8jb1XjXsSc8c2hioP6etOX6zsx7vKFc6dUWQ43LUsRV11SlcLaoszuwTebTsbFkJ6keehe3p2ElxK88t+mK5iXkljngo0w1Cbj23RfAJZCzKtkR/NUBhtEiFidKcPDAACc6+0D5WuYqKycUMRxRGkLyek6tAZkp1LzqZrC8=~-1~-1~-1; _gcl_au=1.1.164078372.1591700050; sqt_cap=1591860562334; PESSIONID=28wnevkkugca7-z1t73r2n02noqo-z55oc6h; CUSTOMER=GzMrtc9tEOfuO8UpMu8cP5WV5RQJdOzjSKvmnroXpYoYU7SDo2TSBJ88AU6mxeXLVWZNv25eD3ToeBEgDcVETyzlBrPsa37M3MAF527BJR4TW9xOT4GoOobJgIAbc4C7R8bEOvhOCwPYZmhoKLojxvgVMmhzBe/Y9vD5UTRbhS7VR3aVXTmCh8H5bycaDJC/QHZ83iumz+sYU7SDo2TSBPgVMmhzBe/YMOf/HxQWG2E=; ncx=m; _ga=GA1.2.694087826.1592574834; JSESSIONID=97DB3EC4BB69C5D4FE11A002C2F2CAD7.jvm_http40_p0121; BIGipServerzalando_http=673267722.20480.0000; filter-position=; bm_sz=6ABB778F7590B1A2F46093CF1D495D44~YAAQJVNzaB5rxqtyAQAAAnYczgigdQagQqlI4VcqGCHbN3s75LZO7gjL+OAOWVWzeftX22gYwxtfYchpE1W0wRSDegSKCHpFhpFMGK2OXBrbV/Nvs0kkJkWClFU1TH95I4mVhLbWjTiIr5jU5pkf7Y146pHhNHsyGvRjW3vZSQcfAHnMx96uuGkJG68a7Jv/; frsx=AAAAAIJVngpguH27Vc7evBur5ScwR2kngRAolGq-pSxzgkh1jaBSN1PmV4O8i7B3nz6tYjetgsnAV4j2YdNDhZcalCImAUVSEugUbzBQTxNmkeyEGaPbeC_DWzcDhY6YOJwYi3NyBQspnD0jYCqmrhA=; ak_bmsc=09B4EA3B0AB9A9EE571489B5ED6E500C5C7ADBC404360000FC36ED5E26219222~pl5JPPU+d+bhxr0yBroma6AraDils/a6wAiwnwLVix7wQUTYldL8I0TTu+DxgigJ8vJv4m1Znx3yhq/3n27y6bloCvAW3syp0Qs2FOp3v/gRt4uE190k12f3QaBa/blTGrkSt3HhAXqDdC8QlqYpRDyvX3doIf4ZWZV4MBCx39rYUr7bpxYFyt1uxNsncG1vImo3aU6uq9jpSsIKdVku3P+K1TDjQppAm2ns/xCmIdodeSfjc6phWFjkTLxz9mfTZ3; zac=AAAAAImOJ_4GUSaF5x_BYw6LoOrVgFAiGCStyPjhb85sz47j-vrJYlnoz-nYOlu5djo7Wbelm2ALwANtj278aoWU4UJGN7M6OxywGPIziFnBSuU5FZr6uaoZGErLsUSrWY8DPhWHCz-HiwkspC09LaluLxlgPUkKeztM5d40p_sqrNeMdktLZVfAwJw-FrFcIYn_jpayi2kSJTJJIyhgvwzdYiSKIWniyXWBUGT3GLUlysjeuhxWeRW9aK7HnU0iHhPjTjVF7Bt9KE4-RS5FrPt9BSq5TwPuEvGNooSgws9NFfFcQOgBILkgZbYNvhvK9iGxXNwBqGG0qATbBVAVT8oBdTUfUk6Ht5Va_4BYhmJAXWgybl97QPae4EAhUZB5HAhWX8kt5zp1ycJjPMUQDM6oy1UXtFnj2Yo5vQQdbHHVV52HKAmTnNFK4YZLGJTy6iACFTSk1cFzUlAcAaAlz52Os-Y51gQCRV_sswYEPPD8ojGmuOhtyDt-JyWjFhYdWYIxAmeoBHi7zpk0w84dpdU5cpgGY8rgZy5W2qR9RInK4XLIQ-L6BJ8JEvpqVF8MEKxp8jznxjqYncTqCBsR2jkENISpfVB48nU9yyrpY3nElko-rStw47th8xueEvHhBXbE1IdRq_WDgnboZOl4lYM9ZSsVL3wwsAec9d0CI1rrX-rRVWgDV8Tud4KDUwXC4lkzCCUz1l1tFCMbOmN7lfELJy0BC3y88fREv72oll-5rkJ5No4pxn7GpRKoYKDds55Ok826JbJJ7ysA9SQdvTkALDyhnbi59zJz6mW1ifalQOemC0zp02OEOjnMved5eoT6jGyyHSY5qp3UBslWwyVzIv4DfJ90EaA-hMKKhzd2I3tQgWIhkW4nGYMtAsCEd1wcYx4_uA3t4Gpm-vzsonfUaI7h-VVBBof0X0OPx-5PHurgfUethziggJDcSYYfEsrgTHVbX8joTgSCiGs48YWqx7XO7Nzojo_AqVp5ItLNITqOHjRmOlG6QZV2F1-pFJ3wwJRxa-L9vIDxNptKlDFtCOoQ842anG8yaBnjNKEHKQpkEMAXiR3HuFxjsLBqu-h9WoE4hzevWFz_uu68Xsdm3v8JblWkLgECR4HF2Pw0Q64jmVo_F1MG5GYoJ41o5PPyGndt38MWng_U-72I94m76yRuuqzNWyWn9cAsek1uMmQ_s_gJV1-cwPqWzhPgcTADYCmznEWsxlp6w97w22OVRW4=; bm_mi=5DA5F49685210AADC7D28AD0E428D0A8~Y2fIOUI7tBLr7EnsqJpJXMl3/RfI/9Zee/6rsWN4Fjo0NBRalok6ok/7PVSJRMaI7qrG0btHOOsHaIKXdwK3NILG01+anB/9mMSPtZyIKyUp18q9V/sT4XeN5SJP+aXDnh9iKrWXMRcjVlVMGzvfzZO5vvP+bvPCDaQ14XRkZcKHlvNsItB4/fkcrq6GTp+tCF1XkCH/F5807lFjxztwP/wfKHTLm/wdhaTHBRZl6CWo/BRLjA0t0wWCmR69qS8pgSQxXYsYdD+KYSuluHIbz7WxnCpwKHYne+WcjgcHDPU=',
        'If-None-Match': 'W/"18d-nJvMn2d3brYtlyEJaBvaJarW5YA"',
        'TE': 'Trailers'
    }
    
    
        
    s.headers.update(headers2)
    s.get(url, verify=False)
    
    s.post(url, json=login_data, verify=False)
    
    url_checkout_2 = 'https://www.zalando.fr/checkout/address'
    a = s.get(url_checkout_2, verify=False)
    soup = BeautifulSoup(a.text, 'html.parser')
    print(soup)
    #print(soup.find('div').getText("data-props"))
    
    #print(r.content)






stop = timeit.default_timer()
print (stop - start)