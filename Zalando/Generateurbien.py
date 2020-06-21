


def URLGen():
    
    base_url = 'https://www.zalando.fr/'

    #------------------------------------------------------------------Code produit-------------------------------------------------------------#
    
    #code_produit= input("Entrer le code du produit :")
    code_produit= 'Nike Sportswear'
    code_produit = code_produit.lower().replace(" ", "-")


    #--------------------------------------------------------------------Model--------------------------------------------------------------------#


    #model= str(input("entrer le model de la chaussure :"))
    model='AIR FORCE 1 ’07 AN20  - Baskets basses'
    model = model.lower().replace("’", "").replace("  ", " ").replace(" - ", "-").replace(" ", "-")

    #----------------------------------------------------------------Couleur-----------------------------------------------------------------#
    
    #couleur= input("Entrer la couleur du produit")
    couleur= 'white/black'
    couleur = couleur.lower().replace("/", "").replace(" ", "")

    #-------------------------------------------------------------------Reference--------------------------------------------------------#

    #reference= input("Entrer le code du produit :")
    reference= 'NI112O0CL-A11'
    reference = reference.lower().replace(" ", "")

    #---------------------------------------------------------------------------------------------------------------------------------#
    
    
    vrai_url = base_url + code_produit + '-' + model + "-" + couleur + "-" + reference + '.html'
    return vrai_url
