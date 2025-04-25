# Client script for AES encrypted communication with the server
# Developed by HexSec Team

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import socket

def encrypt(message):
    """
    Encrypts a message using AES EAX mode.
    Returns the nonce, tag, and ciphertext combined.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return cipher.nonce + tag + ciphertext

def decrypt(ciphertext):
    """
    Decrypts a received ciphertext using AES EAX mode.
    Verifies the integrity with the authentication tag.
    """
    nonce = ciphertext[:16]
    tag = ciphertext[16:32]
    ciphertext = ciphertext[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode('utf-8')

# Server connection settings
host = '192.168.1.2'  # Server IP Address
port = 7777           # Server Port
s = socket.socket()

# Connect to the server
s.connect((host, port))

# Receive the AES key from the server
key = s.recv(32)
print(f"[+] AES Key received from server: {key}")

# Start chatting
while True:
    responses = s.recv(1024)
    print(f"Server: {decrypt(responses)}")
    message = input("Client: ")
    s.send(encrypt(message))
