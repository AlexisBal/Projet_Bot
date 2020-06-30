# Récupération de la liste du stock
stock = '38_0|39_0|40_1|41_1|42_1|43_1|44_1|45_1|46_1|47_1|48_1'

# Séparation des valeurs
liste_stock = stock.split('|')
liste_stock_bis = []

# Séparation des pointures et du stock
for x in liste_stock:
    y = x.split('_')
    liste_stock_bis.extend(y)

# Détermination de la position de la pointure et du stock
position_pointure = liste_stock_bis.index('40')
position_stock = position_pointure + 1

# Affichage du stock de la pointure concernée 
if liste_stock_bis[position_stock] == '1':
    print(True)
else:
    print(None)

