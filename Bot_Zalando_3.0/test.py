with open('../Data/AccountGenerator.csv', 'r') as f:
    Liste_comptegenerator = []
    for ligne in f:
        comptegenerator_list = ligne.split(";")
        Liste_comptegenerator.append(comptegenerator_list)

f.close()
Liste_comptegenerator[0].insert(5, "Id_Address")
print(Liste_comptegenerator)

# Comptage du nombre de compte présents dans la base de données
nombrecompte = len(Liste_comptegenerator)
# Création d'un compte pour chaque objet "Compte" présent dans la base de données
for compte in range(1, nombrecompte):
    id_adresse = '123213'
    Liste_comptegenerator[compte].insert(5, id_adresse)
    with open("../Data/Accounts.csv", "w") as f:
        for eleve in Liste_comptegenerator:
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
            f.write(";")
            f.write(eleve[10])
    f.close()