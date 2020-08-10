import requests
import random
import string
from random import randint

def generateur_mail():

    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    word = get_random_string(6)

    nombre = randint(1111, 9999)
    doamine = ["@icanav.net", "@in4mail.net", "@intsv.net", "@kleogb.com", "@mail2paste.com", "@mailvk.net", "@ofmailer.net"]
    terminaison = randint(0, 6)

    email = word + str(nombre) + str(doamine[terminaison])
    print(email)


    cookies = {
        '__cfduid':"daefa9e0678aece69232c4a1fed3854d91596924607",
        'adonis-session':"60776c3d80e359efd93daadd541f6561yC7dvWqt4tQRQhoudmFPACvdMLbHDAPrE4aiOz1af11QQL18utdbZYSaFc1fSiCnEDco/XL7km8BhooeWBIsrpnPL2OrGJeMYog1oBr7VX1CZD5KtjyVVZ5stQsndSqG",
        'adonis-session-values':"8170ffee8bd8274aaf71e84160a14c92BM/XqnPpZQShBOHMtA5o4UHb5exgRO2TQMLKGOAgxeK6ifwmSn1aUVjwUQg0DqtePHPJBbWXvfx0SNAuiDQNfdtPNx/HewGIuExCtpGblvnJYbfv1oLy+m7M1nAqkzFBpf6yMnEH7W1QBfOhFFtkizHNo0DOwIKZl2/0kiDoQGo=",
        'email':email,
        'lang':"3868851761e9e5dac5b04923f0473297ZDkdtR7JqVfhl51kBg4jYpCYDqj+7uB8Lkb+1DR3ojUOFgJQ2RIw3eeDy1vKI1JPCHJZmuEB46SpPppXmR7uZQ==",
        'paddlejs_campaign_referrer':"www.google.com",
        'paddlejs_checkout_variant':"{\"inTest\":true,\"controlGroup\":false,\"isForced\":false,\"variant\":\"multipage-radio-payment\"}",
        'XSRF-TOKEN':"c0d4f4ee25c31e4c32762677398ac68aRCOK7QAjCRFE5NHaQhFR8zNQJj7oSqktsEnRg5rnc1lg2IStDHdXP/KAXeizGHi4L7KtNJEd03/5dsdJdzJP8dzWDyqdNcriFU7Wo7h/lHSYuTiCGP6aUmFotl0p4Yog"
    }

    r = requests.get('https://temp-mail.org/fr/', cookies=cookies)
    print(r)

    
generateur_mail()