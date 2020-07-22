import random

Liste_compte = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Choix au hasard d'un compte
random.shuffle(Liste_compte)
for Task in range(1, 5):
    print(Task)
    print(Liste_compte[Task])

