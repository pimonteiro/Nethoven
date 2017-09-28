from miditime.miditime import MIDITime
import random
#Test - Notes that would be result of parsing the DATA string from the tcpdump
Notes = []

#Array with notes to be played
midinotes = []

def make_notes():
    for i in range(0, 50):
        rnd = random.randint(0, 127)
        Notes.append(rnd)

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

#Number of beats per second
BPS = BPM / 60

#Inicialize song
song = MIDITime(BPM, 'teste.mid')


song.add_track(midinotes)


#Output of the MIDI data to a file.mid
make_notes()
set_note_array()
song.save_midi()
