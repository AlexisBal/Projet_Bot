import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


with requests.Session() as session:
    headers = {
        "User-Agent": generate_user_agent()
    }
    url = 'https://temp-mail.org/fr/'
    requete = requests.get(url, headers=headers)
    soup_2 = BeautifulSoup(requete.content, "html.parser")
    print(soup_2)