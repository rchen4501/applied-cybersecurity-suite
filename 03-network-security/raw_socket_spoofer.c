/**
 * @file raw_socket_spoofer.c
 * @author Ryan Chen
 * @brief Low-level IPv4 / ICMP Echo Request packet crafting and source IP spoofing using C raw sockets.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <unistd.h>

/// Computes the RFC 1071 Internet Checksum
unsigned short in_cksum(unsigned short *addr, int len) {
    int nleft = len;       
    int sum = 0;             
    unsigned short *w = addr;
    unsigned short answer = 0; 

    while (nleft > 1) {
        sum += *w++;
        nleft -= 2;
    }

    if (nleft == 1) {
        *(unsigned char *)(&answer) = *(unsigned char *)w;
        sum += answer;
    }

    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);
    answer = ~sum;
    return answer;
}

int main() {
    const char *src_ip = "192.168.234.1";
    const char *dst_ip = "192.168.234.130";

    // 1. Create a raw socket with IPPROTO_RAW
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sock < 0) {
        perror("Socket creation error");
        exit(1);
    }

    // 2. Enable IP_HDRINCL to instruct the kernel that we provide custom IP headers
    int enable = 1;
    if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &enable, sizeof(enable)) < 0) {
        perror("setsockopt IP_HDRINCL failed");
        exit(1);
    }

    // Buffer to hold our handcrafted IP and ICMP headers
    char packet_buf[4096];
    memset(packet_buf, 0, 4096);

    struct iphdr *ip = (struct iphdr *) packet_buf;
    struct icmphdr *icmp = (struct icmphdr *) (packet_buf + sizeof(struct iphdr));

    // 3. Populate IPv4 header fields manually
    ip->ihl = 5;
    ip->version = 4;
    ip->tos = 0;
    ip->tot_len = htons(sizeof(struct iphdr) + sizeof(struct icmphdr));
    ip->id = htons(45011);
    ip->frag_off = 0;
    ip->ttl = 255;
    ip->protocol = IPPROTO_ICMP;
    ip->check = 0;
    ip->saddr = inet_addr(src_ip);
    ip->daddr = inet_addr(dst_ip);

    // 4. Populate ICMP Echo Request header fields
    icmp->type = ICMP_ECHO;
    icmp->code = 0;
    icmp->un.echo.id = htons(4501);
    icmp->un.echo.sequence = htons(1);
    icmp->checksum = 0;

    // 5. Calculate ICMP checksum
    icmp->checksum = in_cksum((unsigned short *)icmp, sizeof(struct icmphdr));

    // 6. Define target address and dispatch raw packet
    struct sockaddr_in target_address;
    target_address.sin_family = AF_INET;
    target_address.sin_port = htons(0);
    target_address.sin_addr.s_addr = inet_addr(dst_ip);

    int packet_len = sizeof(struct iphdr) + sizeof(struct icmphdr);
    if (sendto(sock, packet_buf, packet_len, 0, (struct sockaddr *)&target_address, sizeof(target_address)) < 0) {
        perror("Packet Error");
    } else {
        printf("Packet successfully sent to %s with spoofed source %s\n", dst_ip, src_ip);
    }

    close(sock);
    return 0;
}
