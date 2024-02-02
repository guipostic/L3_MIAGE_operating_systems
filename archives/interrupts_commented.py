import threading
from threading import Semaphore
from time import sleep
from random import uniform

disk = [0] * 1024

DISK_READ_FINISHED = 0
DISK_WRITE_FINISHED = 1
interruptTypes = [DISK_READ_FINISHED, DISK_WRITE_FINISHED]


class InterruptManager:
    handlers = {} # variable de classe (partagée par toutes les instances de la classe)
    # Dictionnaire, registre des types d'interruptions (clef) et leur associe un traitant (valeur)

    # self est utilisé pour représenter l'instance de la classe. C'est grâce à lui qu'on donc accéder aux attributs et aux méthodes de la classe.
    # n'est pas un mot réservé en Python. On pourrait utiliser "this".

    def __init__(self): # méthode exécutée à chaque instanciation d'un nouvel objet
        # XXX On enregistre tous les types d'interruptions possibles (clefs) avec None comme valeur associée
        for it in interruptTypes:
            self.handlers[it] = None # variable d'instance (valeur diffère d'un instance à l'autre)

    def registerHandler(self, interruptType, handler):
        self.handlers[interruptType] = handler


    # The syntax is to use the symbol * to take in a variable number of arguments; by convention, it is often used with the word args.
    # What *args allows you to do is take in more arguments than the number of formal arguments that you previously defined.
    # With *args, any number of extra arguments can be tacked on to your current formal parameters (including zero extra arguments).
    def invokeHandler(self, interruptType, *args):
        hndl = self.handlers[interruptType]
        if hndl:
            hndl(*args)
        else:
            # L’instruction raise permet de déclencher une exception spécifique.
            raise ValueError("No interrupt handler registered for\
            interrupt type %d." % interruptType)


mainInterruptManager = InterruptManager() # instanciation


def registerInterruptHandler(interruptType, handler): # XXX handler est une fonction (e.g. ici, affichage d'un message)
    """
    Un traitant d’interruption est un programme qui est appelé automatiquement lorsqu’une interruption survient. L’adresse de début du traitant est donnée par la table des vecteurs d’interruptions. Lorsque le traitant a effectué son travail, il exécute l’instruction spéciale IRET (pour Interrupt RETurn) qui permet de reprendre l’exécution à l’endroit où elle avait été interrompue.
    """
    mainInterruptManager.registerHandler(interruptType, handler)




def writeCell(disk, position, datum):
    threading.Thread(target=lambda: slowWriteCell(disk, position,
                                                  datum)).start()
# Les fonctions lambda sont définies par le mot-clé lambda et elles peuvent comporter n’importe quel nombre d’arguments mais une seule expression.
#     utilité = lorsque l’on veut utiliser une fonction qui prend comme argument une autre fonction.

# target : est l'objet appelable qui doit être invoqué par la méthode run(). La valeur par défaut est None, ce qui signifie que rien n'est appelé.
# start() : Lance l'activité du fil d'exécution. Elle ne doit être appelée qu'une fois par objet de fil. Elle fait en sorte que la méthode run() de l'objet soit invoquée dans un fil d'exécution.

def readCell(disk, position):
    threading.Thread(target=lambda: slowReadCell(disk,
                                                 position)).start()


def waitAWhile():
    sleep(uniform(0, 2))


def slowWriteCell(disk, position, datum):
    """
    Lance l’écriture de la donnée datum à la position sur le disk et renvoie le contrôle au fil d’exécution appelant.
    À la fin de l’écriture, le traitant de l’interruption DISK_WRITE_FINISHED sera appelé
    """
    waitAWhile()
    disk[position] = datum
    mainInterruptManager.invokeHandler(DISK_WRITE_FINISHED) # XXX Ne se termine pas par un return


def slowReadCell(disk, position):
    waitAWhile()
    mainInterruptManager.invokeHandler(DISK_READ_FINISHED,
                                       disk[position])

