# Création de la liste de compte "Liste_compte2"
def compte2():
    with open('../Data/Accounts_List2.csv', 'r') as f:
        Liste_compte2 = []
        for ligne in f:
            compte_list2 = ligne.split(";")
            Liste_compte2.append(compte_list2)
    f.close()
    return Liste_compte2


def test(compte):
    test = compte[1][6] + " " + compte[1][7]
    print(test)

compte = compte2()
test(compte)