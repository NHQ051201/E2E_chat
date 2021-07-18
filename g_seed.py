from Cryptodome.Random import random
from miller_rabin import miller_rabin_base_2

f = open('g_key.txt', 'w')
a = open('p_key.txt', 'r')
b = int(a.read())

while(True):
    temp = random.randint(2 ** 128, 2 ** 256)
    if miller_rabin_base_2(temp) == True and temp < b:
        g = temp
        break
    
f.write(str(g))
f.close()

f = open('g_key.txt', 'r')
print(f.read())