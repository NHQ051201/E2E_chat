import socket
import sys
import json
import threading
import random
import base64
from simplecrypt import encrypt, decrypt

from config import BASE, MODULUS, SERVER_ADDRESS, BUFSIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(SERVER_ADDRESS)

secret_key = random.randint(1, MODULUS)
print(secret_key)
public_key = pow(BASE, secret_key, MODULUS)
e2e_key = None


def calculate_e2ekey(pubkey):
    global e2e_key
    e2e_key = pow(pubkey, secret_key, MODULUS)


def send_message(text):
    sock.send(bytes(json.dumps({'type': 'message', 'text': text}), 'utf8'))


def handle_read():

    while True:
        data = sock.recv(BUFSIZE).decode('utf8')
        data = json.loads(data)

        if data.get('type') == 'init':
            pubkey = data.get('pubkey')
            calculate_e2ekey(pubkey)
            print('system\t>>\tReady! (e2e key={})'.format(e2e_key))

        if data.get('type') == 'system':
            print('system\t>>\t{}'.format(data['text']))

        if data.get('type') == 'message' and data.get('name') != sys.argv[1]:
            decoded = base64.b64decode(data['text'])
            text = decrypt(str(e2e_key), decoded)
            print('{}\t>>\t{}'.format(data['name'], text.decode('utf8')))


if __name__ == '__main__':
    print('\nsecret_key={}'.format(secret_key))
    print('public_key={}\n\n'.format(public_key))

    try:
        sock.send(
            bytes(json.dumps({'type': 'init', 'name': sys.argv[1], 'pubkey': public_key}), 'utf8'))
        thread = threading.Thread(target=handle_read).start()

        while True:
            msg = input()
            if msg == 'quit':
                send_message('quit')
                break
            else:
                chipertext = encrypt(str(e2e_key), msg)
                send_message(base64.b64encode(chipertext).decode('utf8'))
    finally:
        sock.close()
