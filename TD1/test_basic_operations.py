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

