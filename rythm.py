from miditime.miditime import MIDITime
import random
from scapy.all import *
import argparse

#Array with notes to be played
midinotes = []
Notes = []

#arguementos
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True, help='.pcap file to filter')

#tratar de argumentos
args = vars(ap.parse_args())
ficheiro = args["file"]

tcp = []
udp = []
arp = []
dhcp = []
#carrega cap
pacotes = rdpcap(ficheiro)
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


# Conversor
def strcode(code):
	if (code==""):
		print("ERRO")
	while (len(code)):
		note = code[:7]
		code = code[8:]
		x = note_conv(note)
		Notes.append(x)

def note_conv(note):
	e = 0
	x = 0
	for i in range(0, len(note)):
		x = 2**e + x
		e += 1
	return x


def make_notes():
    strcode(tcp)
    strcode(udp)
    strcode(arp)
    strcode(dhcp)
    # for i in range(0, 50):
    #     rnd = random.randint(0, 127)
    #     Notes.append(rnd)

def set_note_array():
    j = 0
    #i = 0
    #midinotes.append([0, Notes[j], 127, 2]) #2 -> PROTOCOL
    j+=1
    #loop to go through all the available Notes
    for i in Notes:
        rnd  = random.randint(0,2)
        midinotes.append([j + rnd, i, 127, 1])
        j = j + 1 + rnd



#Rythm of the music
BPM = 250

#Inicialize song
song = MIDITime(BPM, 'teste.mid')
song.add_track(midinotes)


#main
#Output of the MIDI data to a file.mid
make_notes()
set_note_array()
song.save_midi()
