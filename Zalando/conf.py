dictionnaire = {

}

for i in range (0, 3):
    i = str(i)
    nom = "nom" + i
    print(nom)
    dictionnaire[nom] = 3

print(dictionnaire.keys())