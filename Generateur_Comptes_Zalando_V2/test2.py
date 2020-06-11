import requests

with requests.Session() as s:
    url_get = "https://www.zalando.fr/login/?view=register"
    cookies = dict(cookies_are='working')
    headers = {'user-agent': 'my-app/0.0.1'}
    s.get(url_get, headers=headers, cookies=cookies)
    url_post1 = "https://www.zalando.fr/api/reef/register/schema"
    s.get(url_post1, headers=headers, cookies=cookies)
    register = {
        "firstname": "alexis",
        "lastname": "balayre",
        "email": "alexis.balayre@isep.fr",
        "password": "Dubai007",
        "accepts_terms_and_conditions": True
    }
    url_post2 = "https://www.zalando.fr/api/reef/register"
    r = s.post(url_post2, data=register)
    print(r.status_code)
