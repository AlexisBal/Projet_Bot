import timeit
from colorama import Back, Fore, Style, deinit, init


start = timeit.default_timer()  # J'ai besoin de cette ligne pour calculer la latence.
 
 #Fonction latence
def latence(start):
    stop = timeit.default_timer()
    latence= str(stop-start)
    latence= latence[0] + latence[1] + latence[2] + latence[3] + latence[4] + latence[5]
    latence = Style.RESET_ALL + '[' + Fore.RED + latence + Style.RESET_ALL + ']'
    return latence


print(latence(start))