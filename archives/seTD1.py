from interrupts import *


def handleWriteFinished():
    print("Fini d'écrire !")

def handleReadFinished(cell):
    print("Lu donnée %s !" % cell)


print(disk[0:10])

registerInterruptHandler(DISK_WRITE_FINISHED, handleWriteFinished) # fonction pour définir comment gérer l’interruption DISK_WRITE_FINISHED
registerInterruptHandler(DISK_READ_FINISHED, handleReadFinished) # pour l’interruption DISK_READ_FINISHED

writeCell(disk, 0, 32)

print("Premier affichage: ", end="")
print(disk[0])

#sleep(2)
sleep(1)

print("Deuxième affichage: ", end="")
print(disk[0])

readCell(disk, 0)


# Ci-dessous, les 3 situations possibles :
#
#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#Premier affichage: 0
#Fini d'écrire !
#Deuxième affichage: 32
#Lu donnée 32 !
#
#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#Premier affichage: 0
#Deuxième affichage: 0
#Lu donnée 0 !
#Fini d'écrire !
#
#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#Premier affichage: 0
#Deuxième affichage: 0
#Fini d'écrire !
#Lu donnée 32 !
#
