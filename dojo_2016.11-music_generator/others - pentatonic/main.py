#!/usr/bin/env python
import time
import sys
import random
from pygame import mixer

mixer.init()

# Bass
s12 = mixer.Sound('./sounds/12.wav')
s14 = mixer.Sound('./sounds/14.wav')
s16 = mixer.Sound('./sounds/16.wav')
s19 = mixer.Sound('./sounds/19.wav')
s21 = mixer.Sound('./sounds/21.wav')
s24 = mixer.Sound('./sounds/24.wav')

# Bass 2
s24 = mixer.Sound('./sounds/24.wav')
s26 = mixer.Sound('./sounds/26.wav')
s28 = mixer.Sound('./sounds/28.wav')
s31 = mixer.Sound('./sounds/31.wav')
s33 = mixer.Sound('./sounds/33.wav')
s36 = mixer.Sound('./sounds/36.wav')

# Melody
s36 = mixer.Sound('./sounds/36.wav')
s39 = mixer.Sound('./sounds/39.wav')
s41 = mixer.Sound('./sounds/41.wav')
s43 = mixer.Sound('./sounds/43.wav')
s45 = mixer.Sound('./sounds/45.wav')
s48 = mixer.Sound('./sounds/48.wav')

bass = [
    s12,
    s14,
    s16,
    s19,
    s21,
    s24
]

bass2 = [
    s24,
    s26,
    s28,
    s31,
    s33,
    s36
]

melody = [
    s36,
    s39,
    s41,
    s43,
    s45,
    s48
]

chordCounter = 0
chordCounterLimit = 3

while True:

    # bass chords
    chordCounter += 1
    if chordCounter >= chordCounterLimit:
        chordCounter = 0
        idx = random.randint(0, len(melody)-1)
        bass2[idx].play()

    # melody
    idx = random.randint(0, len(melody)-1)
    melody[idx].play()
    time.sleep(0.25)
