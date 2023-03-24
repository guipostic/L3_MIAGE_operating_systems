from interrupts import *

def handleWriteFinished():
    print("Fini d'écrire !")
    sem.release()

def handleReadFinished(cell):
    print("Lu donnée %s !" % cell)

sem = Semaphore(0) # On initialise le sémaphore à 0 pour que le tout premier appel d’acquire soit bloquant.

print(disk[0:10])

registerInterruptHandler(DISK_WRITE_FINISHED, handleWriteFinished) # fonction pour définir comment gérer l’interruption DISK_WRITE_FINISHED (ici, la fin de l'écriture)
registerInterruptHandler(DISK_READ_FINISHED, handleReadFinished) # pour l’interruption DISK_READ_FINISHED

writeCell(disk, 0, 32)

#print("Premier affichage:")
print(disk[0])
sem.acquire()

#sleep(2)
sleep(1) # The sleep() function suspends (waits) execution of the current thread for a given number of seconds. 

#print("Deuxième affichage:")
print(disk[0])

readCell(disk, 0)

# Note : delai de lecture également
#sleep(2)
#print(disk[0:10])

