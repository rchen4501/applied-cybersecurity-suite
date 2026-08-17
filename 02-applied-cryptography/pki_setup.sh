#!/bin/bash
# Generate Root CA and Server X.509 Certificates using OpenSSL[cite: 3]

echo "1. Generating Root CA private key and self-signed certificate..."[cite: 3]
openssl req -x509 -newkey rsa:2048 -nodes -keyout rootCA.key -out rootCA.crt -days 365 \
  -subj "/C=US/ST=Georgia/L=Athens/O=SecurityLab/CN=CustomRootCA"

echo "2. Generating Server private key and CSR..."[cite: 3]
openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr \
  -subj "/C=US/ST=Georgia/L=Athens/O=SecurityLab/CN=127.0.0.1"

echo "3. Creating Subject Alternative Name (SAN) extension..."[cite: 3]
echo "subjectAltName=IP:127.0.0.1,IP:192.168.234.129" > server_ext.cnf[cite: 3]

echo "4. Signing Server certificate with Root CA..."[cite: 3]
openssl x509 -req -in server.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial \
  -out server.crt -days 365 -extfile server_ext.cnf[cite: 3]

echo "[+] PKI setup complete: rootCA.crt, server.crt, server.key created."[cite: 3]
