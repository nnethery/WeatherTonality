import pysynth_b as voice2
import pysynth_e as voice1
import pysynth_s as voice3
import mixfiles as mix
from multiprocessing import Process

class GenerativePiece:

    def __init__(self, title, tempo):
        self.title = title
        self.tempo = tempo
        self.soprano = []
        self.bass = []
        self.alto = []

    def setSoprano(self, n, log):
        temp = fixCountour(n, log)
        for note in temp:
            self.soprano.append(str(self.midi2letter(note)) + str(self.midi2octave(note)))

    def setAlto(self, n):
        for note in n:
            self.alto.append(str(self.midi2letter(note)) + str(self.midi2octave(note)))

    def setBass(self, n):
        for note in n:
            self.bass.append(str(self.midi2letter(note)) + str(self.midi2octave(note)))

    def midi2letter(self, v):
        return {
            0:  'c',
            1:  'c#',
            2:  'd',
            3:  'd#',
            4:  'e',
            5:  'f',
            6:  'f#',
            7:  'g',
            8:  'g#',
            9:  'a',
            10: 'a#',
            11: 'b'
        }.get(v % 12)

    def midi2octave(self, v):
        if v <= 11:
            return -1
        if v <= 23 and v > 11:
            return 0
        if v <= 35 and v > 23:
            return 1
        if v <= 47 and v > 35:
            return 2
        if v <= 59 and v > 47:
            return 3
        if v <= 71 and v > 59:
            return 4
        if v <= 83 and v > 71:
            return 5
        if v <= 95 and v > 83:
            return 6
        if v <= 107 and v > 95:
            return 7
        if v <= 119 and v > 107:
            return 8
        else:
            return 9

    def createChannel(self, pitchList, filename, synth):
        song = []

        if (filename == "soprano"):
            beat = 4
        else:
            beat = 2

        for pitch in pitchList:
            temp = (pitch, beat)
            song.append(temp)

        if synth == 0:
            voice1.make_wav(song, fn=filename + ".wav", bpm=self.tempo)
        elif synth == 1:
            voice2.make_wav(song, fn=filename + ".wav", bpm=self.tempo)
        else:
            voice3.make_wav(song, fn=filename + ".wav", bpm=self.tempo)

    def createSong(self):
        p1 = Process(target=self.createChannel, args=(self.soprano,"soprano",1))
        p2 = Process(target=self.createChannel, args=(self.bass,"bass",0))
        p3 = Process(target=self.createChannel, args=(self.alto,"alto",2))

        m1 = Process(target=mix.mix_files, args=("bass.wav","alto.wav","left.wav"))

        p2.start()
        p3.start()
        p1.start()

        p2.join()
        p3.join()

        m1.start()

        p1.join()

        m1.join()

        mix.mix_files("left.wav","soprano.wav",self.title + "wav",chann = 2,phase=-0.1)

def fixCountour(n, log):
    fixed = []
    if log[0][0] != 0:
        fixed = fixed + n[:log[0][0]]

    for i in range(len(log)):
        if i == len(log)-1:
            fixed = fixed + tweakScaleDegree(n[log[i][0]:],log[i][1])
        else:
            left = log[i][0]
            right = log[i+1][0]
            fixed = fixed + tweakScaleDegree(n[left:right],log[i][1])
            #print(n[left:right])

    return fixed

def tweakScaleDegree(n,direction):
    transposition = n[0] % 12

    if direction == '+':
        for i in range(len(n)):
            degree = (n[i] - transposition) % 12
            if degree == 1:
                n[i] -= 1
            if degree == 3:
                n[i] += 1
            if degree == 6:
                n[i] += 1
            if degree == 8:
                n[i] -= 1
            if degree == 10:
                n[i] -= 1
    else:
        for i in range(len(n)):
            degree = (n[i] - transposition) % 12
            if degree == 1:
                n[i] += 1
            if degree == 4:
                n[i] -= 1
            if degree == 6:
                n[i] += 1
            if degree == 9:
                n[i] -= 1
            if degree == 11:
                n[i] -= 1

    return n
