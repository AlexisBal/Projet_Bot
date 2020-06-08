import requests


url_post = "https://www.zalando.fr/api/reef/register"
url_get = "https://www.zalando.fr/login/?view=register"
register_data = {
    'firstname': "Alexis",
    'lastname': "Balayre",
    'email': "alexis.balayre@isep.fr",
    'password': "Dubai007",
}
s = requests.session()
s.get("https://www.zalando.fr/login/?view=register", verify=True)


#register_request = client.post(url_post, data=register_data)

