# Applied Cybersecurity & Binary Exploitation Suite

[![C](https://img.shields.io/badge/C-11-A8B9CC?style=flat&logo=c&logoColor=white)](https://en.cppreference.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![OpenSSL](https://img.shields.io/badge/OpenSSL-3.0-721412?style=flat&logo=openssl&logoColor=white)](https://www.openssl.org/)
[![Pwntools](https://img.shields.io/badge/Exploit-Pwntools-red?style=flat)](https://github.com/Gallopsled/pwntools)
[![Wireshark](https://img.shields.io/badge/Network-Wireshark-1679A7?style=flat&logo=wireshark&logoColor=white)](https://www.wireshark.org/)
[![Linux](https://img.shields.io/badge/Platform-Linux%20x86--64-FCC624?style=flat&logo=linux&logoColor=black)](https://kernel.org)

A comprehensive systems security engineering repository featuring low-level memory exploitation, applied cryptographic engineering in C, custom PKI/TLS pipelines, network packet injection, and web vulnerability remediation.

---

## 📌 Suite Overview & Technical Breakdown

```text
applied-cybersecurity-suite/
├── 01-binary-exploitation/   # Format string attacks, memory corruption, pwntools automation
├── 02-applied-cryptography/  # C OpenSSL EVP AES-128-CBC, RSA key encapsulation, custom TLS PKI
└── 03-network-security/      # Scapy/C raw socket packet injection & DOM XSS remediation

🧠 1: Binary Exploitation & Memory Safety
1. Multi-Round Format String Vulnerability Exploitation
Mechanism: Exploited uncontrolled format string vulnerabilities (printf(user_input)) on x86-64 Linux.
Automation: Built Python exploit routines using pwntools to dynamically parse runtime process outputs, track stack alignment offsets, and craft payload streams.
Targeted Memory Overwrite: Executed multi-stage byte-by-byte memory writes (%ln / %n) to overwrite targeted authentication state variables with specific hex values (0xdeadbeef).


🔐 2: Applied Cryptography & PKI Infrastructure1. 
2.1: Hybrid AES-128-CBC & RSA Key Encapsulation (C / OpenSSL)
Design: Engineered a hybrid cryptosystem in C combining high-speed symmetric data encryption with asymmetric key encapsulation.
Symmetric Engine: Utilized OpenSSL EVP APIs (EVP_EncryptInit_ex, EVP_EncryptUpdate, EVP_EncryptFinal_ex) with random 128-bit key and 16-byte Initialization Vector (IV) generation via RAND_bytes.
Asymmetric Key Exchange: Computed RSA modular exponentiation ($C = M^e \pmod n$, $M = C^d \pmod n$) using the OpenSSL BIGNUM interface for large prime mathematics ($p$, $q$, $n$, $\phi(n)$, $d$).

[Plaintext Payload] ──► AES-128-CBC (Random Key/IV) ──► [Encrypted Payload]
                               │
                      [AES Session Key]
                               │
                               ▼
                       RSA-2048 Public Key
                               │
                               ▼
                    [Encrypted Key Envelope]

2.2: Custom TLS 1.3 Client-Server Pipeline & PKI
Public Key Infrastructure (PKI): Established a private Certificate Authority (rootCA.crt), generated Certificate Signing Requests (CSRs), and issued server certificates with subjectAltName extensions.
Encrypted Sockets: Wrapped native TCP sockets with authenticated TLS contexts (ssl.CERT_REQUIRED, check_hostname=True) to enforce mutual transport confidentiality and server identity validation.

🌐 3: Network & Web Security
3.1: Forged Packet Injection & Source Spoofing
Python Scapy: Constructed and dispatched forged IPv4/ICMP Echo Request packets with spoofed source IP headers across multi-node virtual topologies.
C Raw Sockets: Replicated protocol spoofing in low-level C using raw network sockets (AF_INET, SOCK_RAW, IPPROTO_RAW) with IP_HDRINCL.
Internet Checksum Computation: Manually implemented the RFC 1071 ones-complement 16-bit checksum algorithm across arbitrary network headers.
Packet Inspection: Validated unidirectional spoofing and reply redirection using Wireshark display filters (ip.addr and icmp).

3.2: DOM-Based XSS Exploitation & Hardening
Vulnerability Analysis: Demonstrated reflected and stored Cross-Site Scripting (XSS) attack vectors abusing unsafe DOM manipulations (innerHTML).
Secure Remediation: Hardened front-end rendering engines by substituting unsafe sinks with secure node methods (textContent, createElement, createTextNode) to eliminate code-injection vectors.


🛠️ Tech Stack & Tooling:

Domain,Tools & Technologies
Exploitation & Reversing: "C, x86-64 Assembly, Pwntools, GDB, Ghidra, Angr"
Cryptography & PKI: "OpenSSL (EVP, BIGNUM), X.509, AES-128-CBC, RSA-2048, TLS"
Network & Web Security: "Scapy, C Raw Sockets, Wireshark, TCP/IP, JavaScript, DOM Security"

⚡ Reproduction & Build Instructions
1. Compile C Cryptography & Raw Socket Tools
# Install dependencies
sudo apt update && sudo apt install -y build-essential libssl-dev python3-pwntools

# Compile OpenSSL Hybrid Crypto Engine
gcc 02-applied-cryptography/hybrid_crypto.c -lcrypto -o hybrid_crypto
./hybrid_crypto

# Compile C Raw Socket Sender (Requires root/sudo for raw socket creation)
gcc 03-network-security/raw_socket_sender.c -o raw_sender
sudo ./raw_sender

2. Run Pwntools Exploit Harness
cd 01-binary-exploitation
python3 format_string_exploit.py

👤 Author
Ryan Chen – github.com/rchen4501
