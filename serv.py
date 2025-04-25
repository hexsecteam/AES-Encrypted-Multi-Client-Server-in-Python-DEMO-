# Server script for AES encrypted communication with a client
# Developed by HexSec Team

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import socket

# Generate a secure random 256-bit AES key (32 bytes)
key = get_random_bytes(32)
print(f"Generated AES Key (for testing only): {key}")

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
host = "192.168.1.2"  # Server IP Address (change if needed)
port = 7777           # Port to listen on
s = socket.socket()

def bind_socket():
    """Bind the server socket to the specified IP and port."""
    s.bind((host, port))
    s.listen(5)
    print(f"[+] Server is listening on {host}:{port}")

def socket_accept():
    """Accept a client connection and exchange the AES key."""
    conn, address = s.accept()
    conn.sendall(key)  # Send AES key to client (in a trusted LAN environment)
    print(f"[+] Connection established with {address[0]}:{address[1]}")
    send_commands(conn)
    conn.close()

def send_commands(conn):
    """Send and receive encrypted messages with the connected client."""
    while True:
        message = input("Server: ")
        conn.send(encrypt(message))
        client_response = conn.recv(1024)
        print(f"Client: {decrypt(client_response)}")

def main():
    """Main function to start the server."""
    bind_socket()
    socket_accept()

if __name__ == "__main__":
    main()
