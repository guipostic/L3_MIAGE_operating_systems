
# NOTE: "Assurez-vous que votre code marchera bien quand plusieurs processus tenteront d’accéder au tampon en même temps."
# Rappel : un seul et même sémaphore peut être partagé par des milliers de threads

#from interrupts import *
from threading import * # NOTE: suffisant
from time import *

buf = [0, 0, 0, 0] # le tampon
nEmpty = 4 # le nombre de cases vides
bufLock = Semaphore(1) # gestion d'accès concurrents au tampon

readPtr = 0 # pointeur de lecture NOTE: i.e. indice dans la liste
writePtr = 0 # pointeur d'écriture

writeLock = Semaphore(0) # gestion des écrivains XXX le tout premier appel d’acquire soit bloquant
readLock = Semaphore(0) # gestion des lecteurs

writersWaiting = False # y a-t-il des écrivains en attente ?
readersWaiting = False # y a-t-il des lecteurs en attente ?







# NOTE:
# Le système effectue des opérations de lecture et d'écriture dans le tampon.
# Pour cela, il doit d'abord vérifier l'état de remplissage de la mémoire (variable nEmpty):
# - si plein :
#     - suspendre les opérations d'écriture,
#     - jusqu'à ce qu'un fil de lecture vienne vider une case mémoire
# - si vide :
#     - suspendre les opérations de lecture,
#     - jusqu'à ce qu'un fil d'écriture vienne remplir une case mémoire
#
# Les threads de lecture et d'écriture ("lecteurs" et "écrivains") vont être ainsi bloqués/débloqués,
# grâce à leurs sémaphores respectifs (variables readLock, writeLock).
# Ces sémaphores sont partagés :
# - un écrivain peut
#     - se bloquer lui-même
#     - débloquer un lecteur en attente (variable readersWaiting)
# - et réciproquement pour les lecteurs.
# Pour le tampon, un troisième sémaphore sera partagé par les lecteurs et écrivains, qui pourront chacun le bloquer et débloquer.






def writeBuffer(datum): # NOTE: Un argument + pas de return
    # Indiquer que l'on utilise ces variables globales.
    # NOTE: global est une instruction Python qui l’informe que la variable a qui est utilisée à l’intérieur de la fonction est la même que celle qui est définie à l’extérieur de la fonction (dans l’environnement global).
    global buf, nEmpty, readLock, writeLock, writePtr, readersWaiting, writersWaiting

    # Ne pas laisser plus d'un processus accéder au tampon. XXX


    if nEmpty == 0: # NOTE Mémoire tampon pleine -> interdire (temporairement) l'écriture
        # Plus de cases vides, on signale qu'on se met en attente ... # NOTE: ce signal sera utilisé par les threads de lecture
        # ... on relâche le tampon (pour d'éventuels lecteurs) ...
        # ... et on attend.

        # On rebloque le tampon pour pouvoir travailler dessus.


    # Il y a des cases vides, écrire dedans ...
    # ... décrémenter le nombre de cases vides ...


    # ... et avancer le pointeur d'écriture.


    # Réveiller les lecteurs en attente. # NOTE: des lecteurs pouvaient être en attente si aucune case n'était écrite ; ce n'est plus le cas désormais
    if readersWaiting:

    # Laisser les autres THREADS accéder au tampon.



def readBuffer(): # NOTE: Pas d'argument + un return
    # Indiquer que l'on utilise ces variables globales.
    global buf, nEmpty, readLock, readPtr, writeLock, writersWaiting, readersWaiting # NOTE writePtr inutile

    # Ne pas laisser plus d'un processus accéder au tampon.

    datum = 0


    if nEmpty == len(buf): # NOTE: Mémoire tampon vide -> interdire (temporairement) la lecture
        # Toutes les cases sont vides. On signale qu'on se met en attente ... # NOTE: ce signal sera utilisé par les threads d'écriture
        # ... on relâche le tampon (pour d'éventuels écrivains) ...
        # ... et on attend.

        # On rebloque le tampon pour pouvoir travailler dessus.


    # Lire la donnée ...
    # ... incrémenter le nombre de cases vides ...


    # ... et avancer le pointeur d'écriture.


    # Réveiller les écrivains en attente.
    if writersWaiting:

    # Laisser les autres accéder au tampon.

    return datum



# "Pour tester notre réalisation, on effectuera les opérations de base et on affichera le contenu du tampon ainsi que les positions des pointeurs."
print("Test: Basic operations")

writeBuffer(1)
print(buf) # [1, 0, 0, 0]

writeBuffer('lol')
print(buf) # [1, 'lol', 0, 0]

print("r = %d, w = %d" % (readPtr, writePtr)) # r = 0, w = 2
print(readBuffer()) # 1

print("r = %d, w = %d" % (readPtr, writePtr)) # r = 1, w = 2
print(readBuffer()) # 'lol'







# "Pour tester le réveil des lecteurs par les écrivains, on utilisera un fil d’exécution (un thread en anglais) à part."

print("\nTest: Writers wake up readers.")

def writeLater():
    sleep(1)
    writeBuffer(3)

Thread(target = writeLater).start()

print("r = %d, w = %d" % (readPtr, writePtr)) # r = 2, w = 2
print(readBuffer()) # 3



# "On fera pareil pour tester le réveil des écrivains par les lecteurs."

print("\nTest: Readers wake up writers.")

writeBuffer(4)
writeBuffer(5)
writeBuffer(6)
writeBuffer(7)

print("Finished writing")
print(buf) # [5, 6, 7, 4]

print("r = %d, w = %d" % (readPtr, writePtr)) # r = 3, w = 3

def readLater():
    sleep(1)
    print("Reading...")
    print(readBuffer()) # 4

Thread(target = readLater).start()

writeBuffer(8)
print(buf) # [5, 6, 7, 8]
