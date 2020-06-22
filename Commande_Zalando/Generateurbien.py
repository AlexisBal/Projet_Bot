import time
import requests
from bs4 import BeautifulSoup


def URLGen():
    
    base_url = 'https://www.zalando.fr/'

    #------------------------------------------------------------------Code produit-------------------------------------------------------------#
    
    code_produit= input("Entrer le code du produit :")
    #code_produit= 'Selected Homme'
    code_produit = code_produit.lower().replace(" ", "-")


    #--------------------------------------------------------------------Model--------------------------------------------------------------------#


    model= str(input("Entrer le model du produit :"))
    #model='SLHMELROSE - T-shirt imprimé'
    model = model.lower().replace("’", "").replace("  ", " ").replace(" - ", "-").replace(" ", "-").replace("é", "e")

    #----------------------------------------------------------------Couleur-----------------------------------------------------------------#
    
    couleur= input("Entrer la couleur du produit :")
    #couleur= 'sky captain'
    couleur = couleur.lower().replace(" ", "-").replace("/", "")

    #-------------------------------------------------------------------Reference--------------------------------------------------------#

    reference= input("Entrer le code du produit :")
    #reference= 'NI112O0CL-A11'
    reference = reference.lower().replace(" ", "")

    #---------------------------------------------------------------------------------------------------------------------------------#
    
    
    vrai_url_1 = base_url + code_produit + '-' + model + "-" + couleur + "-" + reference + '.html'
    vrai_url_2 = base_url + code_produit + '-' + model + "-" + reference + '.html'

    URLs = [vrai_url_1, vrai_url_2]

    return URLs

lien_produit=(URLGen())
print(lien_produit[0], lien_produit[1])


def scanner(lien):
    
    while True :
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        requette = requests.get(lien, headers= header)
        if requette.status_code == 200 :
            break

    return True 

#resultat = scanner(lien_produit)

#print(resultat)
