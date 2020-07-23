import timeit
import time
from colorama import Back, Fore, Style, deinit, init


start_chrono = timeit.default_timer()  # J'ai besoin de cette ligne pour calculer la latence.
 
#Mesurer le temps d'execution du code
def chronometre(start_chrono):
    stop = timeit.default_timer()
    latence = Style.RESET_ALL + '[' + Fore.RED + str(round(stop-start_chrono,4)) + Style.RESET_ALL + ']'
    return latence

time.sleep(1.1)
print(chronometre(start_chrono))