from miditime.miditime import MIDITime
from datetime import datetime
from scapy.all import *
import argparse

random.seed(datetime.now())


# arguementos
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True, help='.pcap file to filter')
ap.add_argument('-s', '--scale', required=False, help='Scale of the notes between 0-11', type=int, default=0)

# tratar de argumentos
args = vars(ap.parse_args())
ficheiro = args["file"]
escala = args["scale"]


# Protocols Position on Music
p_tcp = 2
p_udp = 3
p_arp = 4

# Compare scales
c = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
csh = [13, 25, 37, 49, 61, 73, 85, 97, 109, 121]
d = [14, 26, 38, 50, 62, 74, 86, 98, 110, 122]
dsh = [15, 27, 39, 51, 63, 75, 87, 99, 111, 123]
e = [16, 28, 40, 52, 64, 76, 88, 100, 112, 124]
f = [17, 29, 41, 53, 65, 77, 89, 101, 113, 125]
fsh = [18, 30, 42, 54, 66, 78, 90, 102, 114, 126]
g = [19, 31, 43, 55, 67, 79, 91, 103, 115, 127]
gsh = [20, 32, 44, 56, 68, 80, 92, 104, 116]
a = [21, 33, 45, 57, 69, 81, 93, 105, 117]
ash = [22, 34, 46, 58, 70, 82, 94, 106, 118]
b = [23, 35, 47, 59, 71, 83, 95, 107, 119]

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

escalas = [do, dosh, re, resh, mi, fa, fash, sol, solsh, la, lash, si]

# Array with notes to be played
midinotes = []
notes_tcp = []
notes_udp = []
notes_arp = []


tcp = []
udp = []
arp = []

# carrega cap
pacotes = rdpcap(ficheiro)
for pacote in pacotes:
    # tem conteudo
    if pacote.haslayer(Raw):
        # conteudo
        test = pacote[Raw].load
        # conteudo em int
        test_int = int.from_bytes(test, byteorder='little')
        # conteudo binario
        load = bin(test_int)
        if pacote.haslayer(UDP):
            udp.append(load)
        if pacote.haslayer(TCP):
            tcp.append(load)
    if pacote.haslayer(Padding):
        test = pacote[Padding].load
        test_int = int.from_bytes(test, byteorder='little')
        load = bin(test_int)
        if pacote.haslayer(ARP):
            arp.append(load)


def clean_list(lista):
    for i in range(len(lista)):
        codigo = lista[i][2:]
        lista[i] = codigo


def clean_listas():
    clean_list(udp)
    clean_list(tcp)
    clean_list(arp)


def pertence_a_escala(x):
    for nota in escalas[escala]: # 0 = escala VARIAVEL
        if x in nota:
            return 1
    return 0


# Conversor
def strcode(code, arrai, position):
    flag = 0
    if code == "":
        if position == p_arp:
            arrai.append(random.randint(12, 35))
        # print("ERRO" + "codigo: " + code)
        if position == p_udp:
            arrai.append(random.randint(12, 127))
        if position == p_tcp:
            arrai.append(random.randint(60, 84))
        else:
            print("ERRO " + code)
        return
    tamanho = int(len(code) / 10)
    while tamanho > 0:
        #print("FODA-SE")
        y = random.randint(1, 8)
        note = code[:y]
        code = code[(y+1):]
        x = note_conv(note, y)
        for nota in escalas[escala]:
            if x in nota:
                flag += 1
        # se tiver na escala
        if flag != 0:
            while True:
                #print("Nao saio daqui")
                if (position == p_arp and (x < 12 or x > 35)) or not pertence_a_escala(x):
                    x = random.randint(12, 35)  # notas de um baixo, segundo o senpai
                if position == p_tcp and (x < 60 or x > 84):
                    tamanho -= y
                    break
                if position == p_udp:
                    arrai.append(x)
                    tamanho -= y
                    break
                if pertence_a_escala(x):
                    arrai.append(x)
                    tamanho -= y
                    break


def note_conv(note, y):
    x = 0
    if len(note) == y:
        for i in range(0, y-1):
            if int(note[i]) == 1:
                x = 2 ** i + x
    return x


def make_notes():
    strcode(f_tcp, notes_tcp, p_tcp)
    set_note_array(notes_tcp, 1)


    strcode(f_udp, notes_udp, p_udp)
    set_note_array(notes_udp, 1)


    strcode(f_arp, notes_arp, p_arp)
    set_note_array(notes_arp, 2)


def set_note_array(arrai, PROTOCOL):
    j = 0
    # loop to go through all the available notes
    for i in arrai:
        rnd = random.randint(0, 2)
        midinotes.append([j + rnd, i, 127, PROTOCOL])
        j = j + 1 + rnd


# Rythm of the music
BPM = 300

# Inicialize song
song = MIDITime(BPM, 'teste.mid')
song.add_track(midinotes)

# main
# Output of the MIDI data to a file.mid
clean_listas()
f_udp = f_arp = f_dhcp = f_tcp = ""
for i in range(len(udp)):
    f_udp += udp[i]
for i in range(len(tcp)):
    f_tcp += tcp[i]
for i in range(len(arp)):
    f_arp += arp[i]

# print(len(f_udp)+len(f_tcp)+len(f_arp)+len(f_dhcp))
make_notes()
# print("NOTAS DHCP: \n")
# print(*notes_dhcp, sep='\n')
song.save_midi()
