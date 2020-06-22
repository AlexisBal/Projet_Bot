<<<<<<< Updated upstream
#Fichier de configuration





card_cvv = userinfo["card_cvv"]
card_exp_month = userinfo["card_exp_month"]
card_exp_year = userinfo["card_exp_year"]
card_number = userinfo["card_number"]
card_type = userinfo["card_type"]
email = userinfo["email"]
first_name = userinfo["first_name"]
last_name = userinfo["last_name"]
phone_number = userinfo["phone_number"]
shipping_address_1 = userinfo["shipping_address_1"]
shipping_address_2 = userinfo["shipping_address_2"]
shipping_apt_suite = userinfo["shipping_apt_suite"]
shipping_city = userinfo["shipping_city"]
shipping_state = userinfo["shipping_state"]
shipping_state_abbrv = userinfo["shipping_state_abbrv"]
shipping_zip = userinfo["shipping_zip"]
shipping_country = userinfo["shipping_country"]
shipping_country_abbrv = userinfo["shipping_country_abbrv"]
billing_address_1 = userinfo["billing_address_1"]
billing_address_2 = userinfo["billing_address_2"]
billing_apt_suite = userinfo["billing_apt_suite"]
billing_city = userinfo["billing_city"]
billing_state = userinfo["billing_state"]
billing_state_abbrv = userinfo["billing_state_abbrv"]
billing_zip = userinfo["billing_zip"]
billing_country = userinfo["billing_country"]
billing_country_abbrv = userinfo["billing_country_abbrv"]
=======
import requests 
import time

def URLGen():
    
    base_url = 'https://www.zalando.fr/'

    #------------------------------------------------------------------Code produit-------------------------------------------------------------#
    
    #code_produit = input("Entrer le code du produit ('Selected Homme'):")
    code_produit = 'Selected Homme'
    code_produit = code_produit.lower().replace(" ", "-")


    #--------------------------------------------------------------------Model--------------------------------------------------------------------#


    #model= str(input("Entrer le model du produit :"))
    model ='SLHMELROSE - T-shirt imprimé'
    model = model.lower().replace("’", "").replace("  ", " ").replace(" - ", "-").replace(" ", "-").replace("é", "e")

    #----------------------------------------------------------------Couleur-----------------------------------------------------------------#
    
    #couleur = input("Entrer la couleur du produit :")
    couleur = 'sky captain'
    couleur = couleur.lower().replace(" ", "-").replace("/", "")

    #-------------------------------------------------------------------Reference--------------------------------------------------------#

    #reference = input("Entrer le code du produit :")
    reference = 'SE622O0LW-K11'
    reference = reference.lower().replace(" ", "")

    #-------------------------------------------------------------------------------------------------------------------------------#
    
    
    vrai_url_1 = base_url + code_produit + '-' + model + "-" + couleur + "-" + reference + '.html'
    vrai_url_2 = base_url + code_produit + '-' + model + "-" + reference + '.html'
    time.sleep(0.2)

    URLs = [vrai_url_1, vrai_url_2]

    return URLs

liens= URLGen()
print(liens)


def scanner(lien):
    
    while True :
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        requette_1 = requests.get(lien[0], headers=header, verify=False)
        requette_2 = requests.get(lien[1], headers=header, verify=False)
        time.sleep(3)

        if requette_2.status_code == 200 :
            url_produit = lien[0]
            break

        if requette_1.status_code == 200  :
            url_produit = lien[0]
            break

    

    return  url_produit


liens= URLGen()
scanner(liens)
>>>>>>> Stashed changes
