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
    # Création d'une liste "liste_compte" vide
    liste_comptes = []

    # Saisie des informations
    prenom = input("Entrer votre prenom :")
    nom = input("Entrer votre nom :")
    cp = input("Entrer votre code postal :")
    ville = input("Entrer votre ville (sans accents):")
    adresse = input("Entrer votre adresse (sans accents) :")
    nombrecompte = int(
        input(
            "Entrer le nombre de comptes souhaité (1 adresse mail valide par compte) :"
        )
    )
    for i in range(0, nombrecompte):
        email = input("Entrer une adresse mail valide :")
        i = {
            "prenom": prenom,
            "nom": nom,
            "email": email,
            "motdepasse": "",
            "pays": "France",
            "codepostal": cp,
            "ville": ville,
            "adresse": adresse,
        }
        # Génération d'un mot de passe aléatoire et sécurisé
        pwo = PasswordGenerator()
        i["motdepasse"] = pwo.generate()
        # Insertion des comptes dans la liste "liste_compte"
        liste_comptes.append(i)

    # Insertion des comptes dans la base de données "Comptes.json"
    with open("Generateur_Compte_Zalando/Comptes.json", "w") as f:
        json.dump(liste_comptes, f, indent=4)
    f.close()

    # Message de confimation
    print("Vos informations ont bien été sauvegardées !")


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
    # Comptage du nombre de compte présents dans la base de données
    nombrecompte = len(compte_objet_list)
    # Création d'un compte pour chaque objet "Compte" présent dans la base de données
    for x in range(0, nombrecompte):
        # Initialisation de la requête et ouverture du navigateur
        r.init()
        # Connexion à la page d'inscription de Zalando
        r.url("https://www.zalando.fr/login/?view=register")
        # Saisie des informations
        r.type(
            '//*[@name="register.firstname"]', compte_objet_list[x].prenom, "[enter]"
        )
        r.type('//*[@name="register.lastname"]', compte_objet_list[x].nom, "[enter]")
        r.type('//*[@name="register.email"]', compte_objet_list[x].email, "[enter]")
        r.type(
            '//*[@name="register.password"]', compte_objet_list[x].motdepasse, "[enter]"
        )
        # Validation des informations et inscription
        r.click(
            '//*[@class="T7EZ2Y XQCmZ9 gM8atJ VcCaWc O82Ha7 UnzkRv P6b3OO febL1w X3ffeU _53iU3L KyqyyN VMeYkv"]'
        )
        # Fermeture du navigateur
        r.close()
        # Message de confimation pour chaque compte créé
        print("Le compte de ", compte_objet_list[x].email, "a bien été créé !")


SaisieInformations()
comptes = creation_objet_compte()
CreationComptes(comptes)
