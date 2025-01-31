from interrupts import * # ici, interrupts.py est nécessaire

buf = [0, 0, 0, 0] # le tampon
nEmpty = 4 # le nombre de cases vides
bufLock = Semaphore(1) # gestion d'accès concurrents au tampon

readPtr = 0 # pointeur de lecture
writePtr = 0 # pointeur d'écriture

writeLock = Semaphore(0) # gestion des écrivains
readLock = Semaphore(0) # gestion des lecteurs

writersWaiting = False # y a-t-il des écrivains en attente ?
readersWaiting = False # y a-t-il des lecteurs en attente ?

def writeBuffer(datum):
    # Indiquer que l'on utilise ces variables globales.
    global buf, nEmpty, readLock, writeLock, writePtr, readersWaiting, writersWaiting

    # Ne pas laisser plus d'un processus accéder au tampon.
    bufLock.acquire()

    if nEmpty == 0:
        # Plus de cases vides, on signale qu'on se met en attente ...
        writersWaiting = True
        # ... on relâche le tampon (pour d'éventuels lecteurs) ...
        bufLock.release()
        # ... et on attend.
        writeLock.acquire()

        # On rebloque le tampon pour pouvoir travailler dessus.
        bufLock.acquire()

    # Il y a des cases vides, écrire dedans ...
    buf[writePtr] = datum
    # ... décrémenter le nombre de cases vides ...
    nEmpty = nEmpty - 1
    # ... et avancer le pointeur d'écriture.
    writePtr = (writePtr + 1) % len(buf)

    # Réveiller les lecteurs en attente.
    if readersWaiting:
        readersWaiting = False
        readLock.release()

    # Laisser les autres accéder au tampon.
    bufLock.release()

def readBuffer():
    # Indiquer que l'on utilise ces variables globales.
    global buf, nEmpty, readLock, readPtr, writePtr, writeLock, writersWaiting, readersWaiting

    # Ne pas laisser plus d'un processus accéder au tampon.
    bufLock.acquire()

    datum = 0
    if nEmpty == len(buf):
        # Toutes les cases sont vides. On signale qu'on se met en
        # attente ...
        readersWaiting = True
        # ... on relâche le tampon (pour d'éventuels écrivains) ...
        bufLock.release()
        # ... et on attend.
        readLock.acquire()

        # On rebloque le tampon pour pouvoir travailler dessus.
        bufLock.acquire()

    # Lire la donnée ...
    datum = buf[readPtr]
    # ... incrémenter le nombre de cases vides ...
    nEmpty = nEmpty + 1
    # ... et avancer le pointeur d'écriture.
    readPtr = (readPtr + 1) % len(buf)

    # Réveiller les écrivains en attente.
    if writersWaiting:
        writersWaiting = False
        writeLock.release()

    # Laisser les autres accéder au tampon.
    bufLock.release()

    return datum


#  DEUX FONCTIONS IDEM Q5
# ==============================================================================

# Écrivez la fonction writeToDisk(data, nCells, pos) qui utilisera les primitives de la librairie
# interrupts et ceux de la section sur les tampons pour écrire nCells cases du tableau data à la
# position pos sur le disque.
# - L’écriture doit se faire de façon asynchrone : le fil d’exécution appelant ne doit pas attendre la fin de l’écriture.
# - La taille du tableau data peut dépasser la taille du tampon.


# NOTE:
# writeToDisk(data, nCells, pos):
#     data = une liste, par exemple [1,2,3,4,5,6,7,8,9,10]
#     nCells = le nombre d'éléments de la liste ci-dessus (en partant du premier) à écrire sur le disk ; donc valeur max = longueur de la liste
#     pos = position de la première écriture sur le disk de 1024 cases (défini dans interrupts.py)

# IL FAUDRA UTILISER writeCell(), définie dans interrupts.py
#     => fonction asynchrone/non-bloquante, qui démarre un nouveau thread
# EGALEMENT writeBuffer() et readBuffer(), définie ci-dessus

# Rappels :
# ---------
# Une primitive de synchronisation est un terme informatique qui désigne une instruction simple qui permet la synchronisation de processus.
# Une primitive courante est l'exclusion mutuelle, ou verrou, qui permet à un processus d'être seul à effectuer la tâche ou à accéder la donnée protégée par ce verrou.
# Semaphore : one of the oldest synchronization primitives in the history of computer science, invented by the early Dutch computer scientist Edsger W. Dijkstra (he used the names P() and V() instead of acquire() and release()).



writeAt = 0 # la prochaine case à écrire sur le disque
toWrite = 0 # le nombre de cases qu'il reste à écrire XXX SUR LE DISK AUSSI (PAS LE BUFFER)


def writeToDisk(data, nCells, pos):
    global writeAt, toWrite

    if nCells == 0: # XXX Stop immédiat s'il n'y aucune donnée à écrire
        return

    writeAt = pos # on commence l'écriture à pos
    toWrite = nCells # on a nCells cases à écrire

    # On lance l'écriture dans un thread à part et on rend le contrôle au thread appelant << immédiatement >>.
    threading.Thread(target = startWrite(data, nCells)).start()

# Cette procédure lance l'écriture.
def startWrite(data, nCells):
    global toWrite, writeAt

    # On lance bientôt l'écriture de la première case.
    # On avance le pointeur d'écriture et décrémente le nombre de cases à écrire maintenant, pour éviter que writeOneMoreCell ne soit pas éxécutée avant que ces mises à jour ne soient faites.
    # XXX ???
    toWrite = toWrite - 1
    writeAt = writeAt + 1

    # Maintenant on lance l'écriture de la première case. XXX SUR LE DISK (PAS LE TAMPON)
    # NOTE: PREMIERE ECRITURE DISK : SEULE A NE PAS PASSER PAR LE TAMPON
    writeCell(disk, writeAt - 1, data[0]) # XXX <- FROM interrupts.py + (((NON BLOCANTE))) + INTERRUPTION TRAITEE PAR writeOneMoreCell()

    # Écrire la case suivante dans le tampon.
    for i in range(1, nCells): # NOTE: ON NE COMMENCE PAS A ZERO : LA PREMIERE VALEUR EST ECRITE SANS PASSER PAR LE TAMPON ; TOUTES LES AUTRES Y PASSENT (max = nCells)
        print("\nWriting %d to buffer." % data[i])
        writeBuffer(data[i])
        print(buf)


# Cette procédure est appellée à la fin de l'écriture d'une case sur le disque (à part pour la première case).
def writeOneMoreCell(): # NOTE: n'a pas d'argument
    global writeAt, toWrite

    #print("Wrote one more cell.  Still to write %d cells." % toWrite)
    print("INTERRUPT HANDLER OF writeCell(): writeOneMoreCell(). Still to write %d cells." % toWrite)
    print(disk[0:20])
    print("Number of BUFFER's empty cells = %d" % nEmpty)

    if toWrite > 0:
        # Il reste encore des cases à écrire. Récupérer la case suivante du tampon ...
        datum = readBuffer()

        # ... et lancer son écriture sur le disque.
        writeCell(disk, writeAt, datum) # NOTE: "récursion" : l'interruption de writeCell() appellera writeOneMoreCell()

        # Avancer le pointeur d'écriture sur le disque.
        writeAt = writeAt + 1

        # Il reste une case en moins à écrire.
        toWrite = toWrite - 1

# À la fin de l'écriture d'une case, appeler la procédure writeOneMoreCell.
registerInterruptHandler(DISK_WRITE_FINISHED, writeOneMoreCell) # NOTE: était définie au début de def startWrite() : pourquoi ???

writeToDisk([1,2,3,4,5,6,7,8,9,10], 10, 3)

print("\n  ==> Disk write going on asynchronously.\n") # NOTE: Executée quand la dernière valeur de la liste input (data) est écrite dans le tampon (cad, quand boucle dans startWrite() terminée)
# MAIS LES THREADS D'ECRITURE DU DISK DOIVENT ENCORE SE TERMINER (donc écriture asynchrone)
