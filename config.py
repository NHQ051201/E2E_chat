g_key = open('g_key.txt', 'r') 
p_key = open('p_key.txt', 'r')

BASE = int(g_key.read())
MODULUS = int(p_key.read())
print('Base =', BASE)
print('Modules =', MODULUS)
SERVER_ADDRESS = ('localhost', 8000)
BUFSIZE = 1024