with open('../Data/AccountGenerator.csv', 'r') as f:
    Liste_comptegenerator = []
    for ligne in f:
        comptegenerator_list = ligne.split(";")
        Liste_comptegenerator.append(comptegenerator_list)
        Liste_comptegenerator.insert(5, "Id_Address")
f.close()

# Comptage du nombre de compte présents dans la base de données
nombrecompte = len(Liste_comptegenerator)
# Création d'un compte pour chaque objet "Compte" présent dans la base de données
for compte in range(1, nombrecompte):
    id_adresse = '123213'
    Liste_comptegenerator[compte].insert(5, id_adresse)
    liste_compte = []
    for b in range(0, len(Liste_comptegenerator)):
        liste_compte.append(Liste_comptegenerator[b])
    with open("../Data/Accounts.csv", "w") as f:
        for eleve in liste_compte:
            f.write(str(eleve[0]))
            f.write(";")
            f.write(eleve[1])
            f.write(";")
            f.write(eleve[2])
            f.write(";")
            f.write(eleve[3])
            f.write(";")
            f.write(eleve[4])
            f.write(";")
            f.write(eleve[5])
            f.write(";")
            f.write(eleve[6])
            f.write(";")
            f.write(eleve[7])
            f.write(";")
            f.write(eleve[8])
            f.write(";")
            f.write(eleve[9])
    f.close()