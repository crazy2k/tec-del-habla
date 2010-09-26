#!/usr/bin/env python
# coding: utf8

"""
Sintetizador concatenativo de dífonos
=====================================

Este programa se encarga de sintetizar palabras de un lenguaje acotado.

Valiéndose de un inventario de sonidos correspondientes a dífonos de un
lenguaje, este programa genera, a partir de una secuencia de fonemas
(expresada como una cadena de caracteres), un archivo de sonido con el habla
sintetizada. Opcionalmente, si se cuenta con la biblioteca pygame instalada,
permite reproducir el archivo generado.

La secuencia de fonemas de entrada debe estar expresada como una cadena de
caracteres. Cada caracter corresponderá a un fono del lenguaje.

Los archivos del inventario deben estar en formato WAV y sus nombres deben
corresponderse con dífonos del lenguaje; por ejemplo, el archivo
correspondiente al dífono "pa" (por los fonos "p" y "a") debe llamarse
"pa.wav". El archivo generado también tendrá el formato WAV.

Para información sobre el uso del programa, ejecutarlo con el argumento "-h" o
"--help" (sin las comillas).

"""

from optparse import OptionParser
import os
import sys

import pygame

if __name__ == "__main__":
    #
    # Manejo de opciones
    #
    usage = "Uso: %prog [opciones] <directorio de inventario> <secuencia> "\
        "<archivo de salida>"
    optparser = OptionParser(usage)
    optparser.add_option("-p", "--play", action="store_true",
        dest = "play_option", default = False,
        help = "reproducir el archivo generado (requiere pygame)")

    (options, args) = optparser.parse_args()

    if len(args) != 3:
        optparser.error("número incorrecto de argumentos")

    sounds_path = args[0]
    seq = args[1]
    outfile = args[2]

    seq = "-" + seq + "-"

    diphs = [fst + sec for fst, sec in zip(seq, seq[1:])]

    pygame.mixer.init(frequency=FRAMERATE)

    for diph in diphs:
        sound_fname = "%s.wav" % diph
        sound_path = os.path.join(sounds_path, sound_fname)

        sound = pygame.mixer.Sound(sound_path)
        chan = sound.play()
        chan.set_volume(1)

        while pygame.mixer.get_busy():
            pass

