import timeit
import time #Pour tester


#C'est la fonction chronometre qu'il te fallait. La librairie est deja importée dans le code principal puisque 
#c'est la même que pour la fonction latence.
#Tu places le strat_chrono au début du code que tu veux chronometrer
#Et en appelant la fonction "chronometre" ca stop et ca t'affiche le temps d'executiion.
#Si t'as besoin d'une valeur plus précise que 4 chiffres apres la virgule, faut que tu modifie le "4" en ce 
#que tu veux dans le code suivant : "round(stop-start_chrono,4)""

start_chrono = timeit.default_timer() #Lancement du chronomètre
 
#Chronometre
def chronometre(start_chrono):
    stop = timeit.default_timer()
    chronometre =str(round(stop-start_chrono,4))
    return chronometre


time.sleep(0.1) #Teste

print(chronometre(start_chrono))