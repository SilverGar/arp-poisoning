#! /usr/bin/env python3

import os
import socket
from scapy.all import *

def select_interface():
    list_interfaces = []
    cont = 1
    for inter in socket.if_nameindex():
        list_interfaces.append(inter[1])
        print(cont, " ", inter[1])
        cont+=1

    num = int(input("Enter the interface number: "))
    return list_interfaces[num-1]

def scan_targets():
    print(socket.AF_INET)

    

interface = select_interface()

print("1. Enter targets manually")
print("2. Scan hosts on the network")
option = int(input())

if option == 1:
    target_1 = input("Target 1 IP: ")
    target_2 = input("Target 2 IP: ")
elif option == 2:
    scan_targets()

print(interface) 