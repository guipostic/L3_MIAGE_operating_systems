import threading
from threading import Semaphore
from time import sleep
from random import uniform

disk = [0] * 1024

DISK_READ_FINISHED = 0
DISK_WRITE_FINISHED = 1

interruptTypes = [DISK_READ_FINISHED, DISK_WRITE_FINISHED]


class InterruptManager:
    handlers = {}

    def __init__(self):
        for it in interruptTypes:
            self.handlers[it] = None

    def registerHandler(self, interruptType, handler):
        self.handlers[interruptType] = handler

    def invokeHandler(self, interruptType, *args):
        hndl = self.handlers[interruptType]
        if hndl:
            hndl(*args)
        else:
            raise ValueError("No interrupt handler registered for\
            interrupt type %d." % interruptType)


mainInterruptManager = InterruptManager()


def registerInterruptHandler(interruptType, handler):
    mainInterruptManager.registerHandler(interruptType, handler)


def writeCell(disk, position, datum):
    threading.Thread(target=lambda: slowWriteCell(disk, position,
                                                  datum)).start()


def readCell(disk, position):
    threading.Thread(target=lambda: slowReadCell(disk,
                                                 position)).start()


def waitAWhile():
    sleep(uniform(0, 2))


def slowWriteCell(disk, position, datum):
    waitAWhile()
    disk[position] = datum
    mainInterruptManager.invokeHandler(DISK_WRITE_FINISHED)


def slowReadCell(disk, position):
    waitAWhile()
    mainInterruptManager.invokeHandler(DISK_READ_FINISHED,
                                       disk[position])


def makeEmptyBuffer(size):
    return [0] * size


def sendToPrinter(datum):
    print("Sending '%s' to printer.")
