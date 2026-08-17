#!/usr/bin/env python3
"""
Authenticated TLS Echo Client with PKI Certificate Verification
Author: Ryan Chen
"""

import socket
import ssl
import time

TARGET_HOST = '127.0.0.1'
TARGET_PORT = 8888
CA_CERT_PATH = 'rootCA.crt'

def run_tls_client():
    # 1. Enforce strict TLS certificate verification against Root CA[cite: 3]
    context = ssl.create_default_context()[cite: 3]
    context.verify_mode = ssl.CERT_REQUIRED[cite: 3]
    context.check_hostname = False  # Set to True when hostname matches SubjectAltName[cite: 3]
    context.load_verify_locations(cafile=CA_CERT_PATH)[cite: 3]

    # 2. Establish TCP connection[cite: 10]
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)[cite: 10]
    print(f"[*] Connecting to {TARGET_HOST}:{TARGET_PORT}...")

    try:
        # 3. Perform TLS handshake and wrap the socket[cite: 3]
        with context.wrap_socket(raw_socket, server_hostname=TARGET_HOST) as tls_sock:[cite: 3]
            print(f"[+] TLS Connection Established! Cipher: {tls_sock.cipher()}")

            while True:
                text_message = input("Enter message (or 'quit'): ")[cite: 10]
                if text_message.lower() == 'quit':[cite: 10]
                    break

                tls_sock.sendall(text_message.encode('utf-8'))
                response = tls_sock.recv(1024)[cite: 10]
                print(f"[<] Server reply: {response.decode('utf-8')}")[cite: 10]
                time.sleep(0.2)[cite: 10]

    except ssl.SSLCertVerificationError as e:
        print(f"[-] Certificate Verification Failed: {e}")
    except Exception as e:
        print(f"[-] Connection Error: {e}")
    finally:
        raw_socket.close()[cite: 10]

if __name__ == '__main__':
    run_tls_client()
