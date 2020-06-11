import requests
import json


url_post = "https://www.zalando.fr/api/reef/register"
url_get = "https://www.zalando.fr/login/?view=register"
payload = {
    "firstname": "Alexis",
    "lastname": "Balayre",
    "email": "alexis.balayre@isep.fr",
    "password": "Dubai007",
    "fashion_preference": [],
    "subscribe_to_news_letter": "false",
    "accepts_terms_and_conditions": "true",
    "date_of_birth": "", 
    "wnaMode": "shop"
}

try:
    response = requests.get(url_get)
    response.raise_for_status()
except requests.exceptions.HTTPError as errh:
    print("An Http Error occurred:", repr(errh))
except requests.exceptions.ConnectionError as errc:
    print("An Error Connecting to the API occurred:", repr(errc))
except requests.exceptions.Timeout as errt:
    print("A Timeout Error occurred:", repr(errt))
except requests.exceptions.RequestException as err:
    print("An Unknown Error occurred", repr(err))


#r = requests.post("https://www.zalando.fr/login/?view=register", data=payload)




