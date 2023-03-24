# NOTE: "Assurez-vous que votre code marchera bien quand plusieurs processus tenteront d’accéder au tampon en même temps."
# Rappel : un seul et même sémaphore peut être partagé par des milliers de threads

#from interrupts import *
from threading import * # XXX is sufficient
from time import *

buf = [0, 0, 0, 0] # le tampon
nEmpty = 4 # le nombre de cases vides
bufLock = Semaphore(1) # gestion d'accès concurrents au tampon  XXX <- THIS

readPtr = 0 # pointeur de lecture XXX a.k.a. indice dans la liste
writePtr = 0 # pointeur d'écriture

writeLock = Semaphore(0) # gestion des écrivains XXX le tout premier appel d’acquire soit bloquant
readLock = Semaphore(0) # gestion des lecteurs

writersWaiting = False # y a-t-il des écrivains en attente ?
readersWaiting = False # y a-t-il des lecteurs en attente ?



def writeBuffer(datum): # XXX Un argument + pas de return
