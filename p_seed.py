from miller_rabin import miller_rabin_base_2
from Cryptodome.Random import random

f = open('p_key.txt', 'w')

while(True):
    temp = random.randint(2 ** 128, 2 ** 256)
    if miller_rabin_base_2(temp) == True:
        p = temp
        break

f.write(str(p))
f.close

f = open('p_key.txt', 'r')
print(f.read())