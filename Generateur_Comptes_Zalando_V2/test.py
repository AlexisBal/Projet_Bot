import requests
import certifi


url_post = "https://www.zalando.fr/api/reef/register"
register_data = {
    'firstname': "Alexis",
    'lastname': "Balayre",
    'email': "alexis.balayre@isep.fr",
    'password': "Dubai007",
}
r = requests.post("https://www.zalando.fr/api/reef/register", data=register_data)


#register_request = client.post(url_post, data=register_data)

