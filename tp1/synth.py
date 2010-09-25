#!/usr/bin/env python

import os
import sys

import pygame


FRAMERATE = 16000

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: %s <sounds dir> <input>" % sys.argv[0]
        sys.exit(1)

    sounds_path = sys.argv[1]
    seq = sys.argv[2]

    diphs = [fst + sec for fst, sec in zip(seq, seq[1:])]

    pygame.mixer.init(frequency=FRAMERATE)

    for diph in diphs:
        sound_fname = "TMP_%s.wav" % diph
        sound_path = os.path.join(sounds_path, sound_fname)

        sound = pygame.mixer.Sound(sound_path)
        chan = sound.play()
        chan.set_volume(1)

        while pygame.mixer.get_busy():
            pass

