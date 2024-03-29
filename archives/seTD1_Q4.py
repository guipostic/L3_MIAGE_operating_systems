from interrupts import *

def handleWriteFinished():
    print("Fini d'écrire !")
    sem.release()
    #print("Counter = %s" % sem._value)

def handleReadFinished(cell):
    print("Lu donnée %s !" % cell)

sem = Semaphore(0) # On initialise le sémaphore à 0 pour que le tout premier appel d’acquire soit bloquant.

print(disk[0:10])

registerInterruptHandler(DISK_WRITE_FINISHED, handleWriteFinished) # fonction pour définir comment gérer l’interruption DISK_WRITE_FINISHED (ici, la fin de l'écriture)
registerInterruptHandler(DISK_READ_FINISHED, handleReadFinished) # pour l’interruption DISK_READ_FINISHED

sem.acquire()
writeCell(disk, 0, 32)

print("Premier affichage: ", end="")
print(disk[0])

sleep(1)
#sleep(2) # The sleep() function suspends (waits) execution of the current thread for a given number of seconds. 

print("Deuxième affichage: ", end="")
print(disk[0])

readCell(disk, 0)

# Note : delai de lecture également
#sleep(2)
#print(disk[0:10])

