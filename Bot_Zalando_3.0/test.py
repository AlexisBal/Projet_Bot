import requests
import urllib3
import time
import datetime

urllib3.disable_warnings()

# Réglages Discord Webhook Paypal
timestamp = time.time()
timestamp = str(datetime.datetime.utcfromtimestamp(timestamp))
databot = {
    "username": "Scred AIO",
    "avatar_url": "https://pbs.twimg.com/profile_images/1283768710138863617/D2yC8Qpg_400x400.jpg",
    "embeds": [{
        "title": "Successfully checked out !",
        "description": None,
        "url": None,
        "timestamp": timestamp,
        "color": 1160473,
        "footer": {
            "text": "SCRED AIO",
            "icon_url": None,
            "proxy_icon_url": None
        },
        "image": None,
        "thumbnail": {
            "url": link_photo,
            "proxy_url": None,
            "height": None,
            "width": None
        },
        "video": None,
        "provider": None,
        "author": None,
        "fields": [{
            "name": "Website",
            "value": site.strip('https://'),
            "inline": False
        },
            {"name": "Product", "value": name_product, "inline": False},
            {"name": "Size", "value": self.taille_produit, "inline": True},
            {"name": "Quantity", "value": self.quantite, "inline": True},
            {"name": "Mode", "value": "Manual", "inline": True},
            {"name": "Checkout Speed", "value": chronometre_3, "inline": False},
            {"name": "Checkout Link",
             "value": '|| %s ||' % url_paypal,
             "inline": False
             }
        ]}
    ]}
headersdiscord = {
    'Host': 'discordapp.com',
    'User-Agent': 'python-requests/2.22.0',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json'
}
requests.post(url_discord, headers=headersdiscord, json=databot, verify=False)