#!/usr/bin/env python

import sys
import os
import time

import pygame

FRAMERATE = 16000

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: synth.py <sounds dir> <input>"
        sys.exit(1)

    sounds_path = sys.argv[1]
    seq = sys.argv[2]

    diphs = [fst + sec for fst, sec in zip(seq, seq[1:])]

    pygame.mixer.init(frequency=FRAMERATE)

    for diph in diphs:
        sound_fname = "TMP_%s.wav" % diph
        sound_path = os.path.join(sounds_path, sound_fname)

        while pygame.mixer.get_busy():
            pass

        sound = pygame.mixer.Sound(sound_path)
        chan = sound.play()
        chan.set_volume(1)
