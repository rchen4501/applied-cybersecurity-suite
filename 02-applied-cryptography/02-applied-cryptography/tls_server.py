#!/usr/bin/env python3
"""
Authenticated & Encrypted TLS Echo Server
Author: Ryan Chen
"""

import socket
import ssl

HOST = '0.0.0.0'
PORT = 8888
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

def start_tls_server():
    # 1. Create SSL Context for Server Authentication[cite: 3]
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)[cite: 3]
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)[cite: 3]

    # 2. Setup standard TCP socket
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    raw_socket.bind((HOST, PORT))
    raw_socket.listen(5)

    print(f"[*] TLS Server listening on {HOST}:{PORT}...")

    while True:
        client_sock, client_addr = raw_socket.accept()
        print(f"[+] Client connected from: {client_addr}")

        try:
            # 3. Perform TLS Handshake & wrap socket in secure stream[cite: 3]
            with context.wrap_socket(client_sock, server_side=True) as tls_conn:[cite: 3]
                print(f"[+] TLS handshake completed with cipher: {tls_conn.cipher()}")

                while True:
                    data = tls_conn.recv(1024)
                    if not data:
                        break
                    print(f"[*] Received: {data.decode('utf-8')}")
                    # Echo back over TLS tunnel
                    tls_conn.sendall(data)

        except ssl.SSLError as e:
            print(f"[-] TLS Handshake / Connection Error: {e}")
        finally:
            print(f"[-] Connection closed with {client_addr}")

if __name__ == '__main__':
    start_tls_server()
