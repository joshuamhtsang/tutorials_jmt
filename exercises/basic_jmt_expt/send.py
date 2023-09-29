#!/usr/bin/env python3
import random
import socket
import sys

from scapy.all import (
    IP, 
    TCP, 
    Ether, 
    get_if_hwaddr, 
    get_if_list, 
    sendp,
    Packet,
    IntField,
    bind_layers
    )

TYPE_MYDORAEMON = 0x1212


class MyDoraemon(Packet):
    name = "MyDoraemon"
    fields_desc = [
        IntField("dorayaki", 0) # Start with 0 dorayaki
    ]

bind_layers(Ether, MyDoraemon, type=TYPE_MYDORAEMON)

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def main():

    if len(sys.argv)<3:
        print('pass 2 arguments: <destination> "<message>"')
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    print("sending on interface %s to %s" % (iface, str(addr)))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IP(dst=addr) / TCP(dport=1234, sport=random.randint(49152,65535)) / MyDoraemon(dorayaki=5) / sys.argv[2]
    pkt.show2()
    pkt.show()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
