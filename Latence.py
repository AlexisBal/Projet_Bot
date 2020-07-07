import timeit
import time

start = timeit.default_timer()

def latence():

    print('chibre')
    time.sleep(1)
    stop = timeit.default_timer()
    print ('[' , stop - start , ']', sep="")

latence()
latence()