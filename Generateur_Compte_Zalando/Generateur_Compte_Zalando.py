import rpa as r
import json
from password_generator import PasswordGenerator


# Définition de la classe "Compte"
class Compte:
    def __init__(self, **compte_attributes):
        for attr_name, attr_value in compte_attributes.items():
            setattr(self, attr_name, attr_value)


# Saisie des informations personnelles et du nombre de comptes souhaité
def SaisieInformations():
    liste_comptes = []
    prenom = input("Entrer votre prenom :")
    nom = input("Entrer votre nom :")
    nombrecompte = int(
        input(
            "Entrer le nombre de comptes souhaité (1 adresse mail valide par compte) :"
        )
    )
    for i in range(0, nombrecompte):
        i = {
            "prenom": prenom,
            "nom": nom,
            "email": input("Entrer une adresse mail valide :"),
            "motdepasse": "",
        }
        pwo = PasswordGenerator()
        i["motdepasse"] = pwo.generate()
        liste_comptes.append(i)
    with open("Generateur_Compte_Zalando/Comptes.json", "w") as f:
        json.dump(liste_comptes, f, indent=4)
    f.close()


# Création des objets "Compte" et de la liste d'objet "compte_objet_list"
def creation_objet_compte():
    acces_fichier = open("Generateur_Compte_Zalando/Comptes.json", "r")
    compte_objet_list = []
    for compte_attributes in json.load(acces_fichier):
        compte_objet = Compte(**compte_attributes)
        compte_objet_list.append(compte_objet)
    acces_fichier.close()
    return compte_objet_list


# Création des comptes à partir des attributs de chaque objet "Compte"
def CreationComptes(compte_objet_list):
    nombrecompte = len(compte_objet_list)
    for x in range(0, nombrecompte):
        r.init()
        r.url("https://www.zalando.fr/login/?view=register")
        r.type(
            '//*[@name="register.firstname"]', compte_objet_list[x].prenom, "[enter]"
        )
        r.type('//*[@name="register.lastname"]', compte_objet_list[x].nom, "[enter]")
        r.type('//*[@name="register.email"]', compte_objet_list[x].email, "[enter]")
        r.type(
            '//*[@name="register.password"]', compte_objet_list[x].motdepasse, "[enter]"
        )
        r.click(
            '//*[@class="T7EZ2Y XQCmZ9 gM8atJ VcCaWc O82Ha7 UnzkRv P6b3OO febL1w X3ffeU _53iU3L KyqyyN VMeYkv"]'
        )
        r.close()
        print("Le compte de ", compte_objet_list[x].email, "a bien été créé !")


SaisieInformations()
compte = creation_objet_compte()
CreationComptes(compte)
