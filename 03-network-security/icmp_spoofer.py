#!/usr/bin/env python3
"""
ICMP Packet Forging & IP Spoofing via Scapy
Author: Ryan Chen
"""

from scapy.all import IP, ICMP, sr1

src_ip = "192.168.234.1"
dst_ip = "192.168.234.130"

# Craft ICMP Echo Request with forged source IP and custom payload
packet = IP(src=src_ip, dst=dst_ip) / ICMP() / b"CSCI4250-HW8"
reply = sr1(packet, timeout=2, verbose=False)

if reply:
    reply.show()
else:
    print("No reply received.")
