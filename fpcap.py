from scapy.all import *
import argparse


tcp = []
udp = []
arp = []
dhcp = []
#carrega cap
pacotes = rdpcap(ficheiro)
print(pacotes[3].show())
for pacote in pacotes:
    #tem conteudo
    if(pacote.haslayer(Raw)):
        #conteudo
        test = pacote[Raw].load
        #conteudo em int
        test_int = int.from_bytes(test, byteorder='little')
        #conteudo binario
        load = bin(test_int)
        if(pacote.haslayer(UDP)):
            udp.append(load)
        if(pacote.haslayer(TCP)):
            tcp.append(load)
    if(pacote.haslayer(Padding)):
            test = pacote[Padding].load
            test_int = int.from_bytes(test, byteorder='little')
            load=bin(test_int)
            if(pacote.haslayer(ARP)):
                arp.append(load)
            if(pacote.haslayer(DHCP)):
                dhcp.append(load)

print(tcp)
print(udp)
print(arp)
print(dhcp)
