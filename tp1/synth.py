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
import time
import wave


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

    #
    # Procesamiento de la entrada
    #

    # construimos los dífonos
    seq = "-" + seq + "-"
    diphs = [fst + sec for fst, sec in zip(seq, seq[1:])]

    # obtenemos los datos de cada archivo
    params = None
    data = []
    for diph in diphs:
        sound_fname = "%s.wav" % diph
        sound_path = os.path.join(sounds_path, sound_fname)

        w = wave.open(sound_path, "rb")

        if not params:
            params = w.getparams()

        frames = w.readframes(w.getnframes())
        data.append(frames)

        w.close()

    # creamos el archivo de salida
    output = wave.open(outfile, "wb")
    output.setparams(params)
    for frames in data:
        output.writeframes(frames)
    output.close()

    # reproducimos el archivo creado si se pide
    if options.play_option:
        import pygame

        pygame.mixer.init(frequency=params[2])
        sound = pygame.mixer.Sound(outfile)
        chan = sound.play()
        chan.set_volume(1)

        while pygame.mixer.get_busy():
            time.sleep(1)

