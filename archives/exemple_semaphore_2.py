from threading import *
import time
# NOTE: autre façon d'importer tous les modules : from time import *
# => on utilisera alors sleep() au lieu de time.sleep()

obj = Semaphore(1)
obj2 = Semaphore(2)
#print(obj._value)

def some_function(name):
    obj.acquire()

    print(name, "has started...")
    time.sleep(3)
    print(name, "is done!")

    obj.release()

def other_function(name):
    obj2.acquire()

    print(name, "has started...")
    time.sleep(3)
    print(name, "is done!")

    obj2.release()

# Creating multiple threads
t1 = Thread(target = some_function , args = ('Fil-1',))
t2 = Thread(target = some_function , args = ('Thread-2',))
t3 = Thread(target = some_function , args = ('Thread-3',))

t4 = Thread(target = other_function , args = ('Thread-4',))
t5 = Thread(target = other_function , args = ('Thread-5',))


print("Calling the threads")
t1.start()
t2.start()
t3.start()

t4.start()
t5.start()
