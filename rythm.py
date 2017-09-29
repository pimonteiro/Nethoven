from miditime.miditime import MIDITime
import random
from scapy.all import *
import argparse

#Compare scales
c = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
csh = [1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121]
d = [2, 14, 26, 38, 50, 62, 74, 86, 98, 110, 122]
dsh = [3, 15, 27, 39, 51, 63, 75, 87, 99, 111, 123]
e = [4, 16, 28, 40, 52, 64, 76, 88, 100, 112, 123] 
f = [5, 17, 29, 41, 53, 65, 77, 89, 101, 113, 124]
fsh = [6, 18, 30, 42, 54, 66, 78, 90, 102, 114, 125] 
g = [7, 19, 31, 43, 55, 67, 79, 91, 103, 115]
gsh = [8, 20, 32, 44, 56, 68, 80, 92, 104, 116]
a = [9, 21, 33, 45, 57, 69, 81, 93, 105, 117]
ash = [10, 22, 34, 46, 58, 70, 82, 94, 106, 118]
b = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119]

do = [c, d, e, f, g, a, b]
dosh = [csh, dsh, f, fsh, gsh, ash, c]
re = [d, e, fsh, g, a, b, csh]
resh = [dsh, f, g, gsh, ash, c, d]
mi = [e, fsh, gsh, a, b, csh, dsh] 
fa = [f, g, a, ash, c, d, e]
fash = [fsh, gsh, ash, b, csh, dsh, f] 
sol = [g, a, b, c, d, e, fsh]
solsh = [gsh, ash, c, csh, dsh, f, g]
la = [a, b, csh, d, e, fsh, gsh]
lash = [ash, c, d, dsh, f, g, a]
si = [b, csh, dsh, e, fsh, gsh, ash]

escalas = [ do, dosh, re, mi, fa, fash, sol, solsh, la, lash, si]

#Array with notes to be played
midinotes = []
notes_tcp = []
notes_udp = []
notes_arp = []
notes_dhcp = []


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


def clean_list(lista):
    for i in range(len(lista)):
        codigo = lista[i][2:] 
        lista[i] = codigo

def clean_listas():
    clean_list(udp)
    clean_list(tcp)
    clean_list(arp)
    clean_list(dhcp)

# Conversor
def strcode(code, arrai, baixo):
    flag = 0
    if (code==""):
    #print("ERRO" + "codigo: " + code)
        arrai.append(random.randint(1, 127))
        return
    tamanho = int(len(code)/1000)
    while (tamanho>0):
        note = code[:7]
        code = code[8:]
        x = note_conv(note)
        for escala in escalas:
            for nota in escala:
                if(x in nota):
                    flag += 1
        # se tiver na escala
        if(flag != 0):
            if(baixo == 1 and x > 23):
                x = random.randint(0, 23) #notas de um baixo, segundo o senpai
                arrai.append(x)
                tamanho -= 7
            else:
                arrai.append(x)
                tamanho -= 7


def note_conv(note):
	e = 0
	x = 0
	if(len(note)==7):
		for i in range(0, 6):
		#x = 2**e + x
		#e += 1
			if(int(note[i])==1):
				x = 2**i + x
	return x


def make_notes():
    #strcode(f_tcp, notes_tcp, 1)
    #j = set_note_array(notes_tcp, 1, 0)

    #strcode(f_udp, notes_udp, j)
    #j = set_note_array(notes_udp, 1, 0)
    
    #strcode(f_arp, notes_arp, j)
    #j = set_note_array(notes_arp, 2, 0)
    
    strcode(f_dhcp, notes_dhcp, 1)
    j = set_note_array(notes_dhcp, 3, 0) #Bass
    # for i in range(0, 50):
    #     rnd = random.randint(0, 127)
    #     notes.append(rnd)

def set_note_array(arrai, PROTOCOL, j):
    #loop to go through all the available notes
    for i in arrai:
        rnd  = random.randint(0,2)
        midinotes.append([j + rnd, i, 127, PROTOCOL])
        j = j + 1 + rnd
    return j

#Rythm of the music
BPM = 250

#Inicialize song
song = MIDITime(BPM, 'teste.mid')
song.add_track(midinotes)

#main
#Output of the MIDI data to a file.mid
clean_listas()
f_udp = f_arp = f_dhcp = f_tcp = ""
for i in range(len(udp)):
    f_udp += udp[i]
for i in range(len(tcp)):
    f_tcp += tcp[i]
for i in range(len(dhcp)):
    f_dhcp += dhcp[i]
for i in range(len(arp)):
    f_arp += arp[i]

#print(len(f_udp)+len(f_tcp)+len(f_arp)+len(f_dhcp))
make_notes()
#print("NOTAS DHCP: \n")
#print(*notes_dhcp, sep='\n')
song.save_midi()