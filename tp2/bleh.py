#!/usr/bin/env python

import os
import sys

INPUT_FNAME = "tp2-textos.txt"

FREELING_CFG = "/usr/share/FreeLing/config/es.cfg"
TEMP_FNAME = "TEMP"
TAG_SIZE = 8

def get_POS_tags(splt_sentence):
    sentence = " ".join(splt_sentence)
    os.system("echo %s | analyze --nortk --outf tagged -f %s > %s" %\
        (sentence, FREELING_CFG, TEMP_FNAME))

    def get_word_tag(line):
        word, _, tag, _ = line.split()
        return word, tag

    # tomamos las palabras y tags de la salida de FreeLing
    words = [line.split()[0] for line in open(TEMP_FNAME) \
        if line.strip() != ""]
    tags = [line.split()[2] for line in open(TEMP_FNAME) \
        if line.strip() != ""]

    ret = []
    i = 0
    j = 0
    while j < len(words) and i < len(splt_sentence):
        # si la palabra taggeada y la que queremos taggear coinciden...
        if splt_sentence[i] == words[j]:
            ret.append(tags[j])
        # si no, puede ser que FreeLing haya juntado la palabra con otras
        elif "_" in words[j]:
            # en ese caso, a todas les ponemos el mismo tag
            ret.append(tags[j])
            for x in range(words[j].count("_")):
                ret.append(tags[j])
                i += 1
            
            if words[j].split("_")[-1].lower() in ["a", "de"] \
                and words[j + 1] == "el":
                j += 1
        # o puede que FreeLing haya partido la palabra en varias
        else:
            ret.append(tags[j])
            # asumimos que si llegamos aca splt_sentence[i] es "al" o "del"
            if splt_sentence[i].lower() not in ["al", "del"]:
                sys.stdout.write("WHAT! " + str(splt_sentence) + "\n")
                sys.stdout.write("WHAT! " + str(words) + "\n")
                sys.stdout.write(splt_sentence[i] + " " + words[j] + "\n")
                sys.stdout.write(str(i) + " " + str(j) + "\n")
                return

            j += 1


            while False:
                if i + 1 < len(splt_sentence):
                    if splt_sentence[i + 1] == "al":
                        j = words[j:].index("a") + j
                        ret.append(tags[j])
                    if splt_sentence[i + 1] == "del":
                        j = words[j:].index("de") + j
                        ret.append(tags[j])
                    break

                j += 1
                if j >= len(words) or i + 1 >= len(splt_sentence) \
                    or splt_sentence[i + 1] == words[j + 1] \
                    or "_" in words[j + 1]:
                    break

        j += 1
        i += 1

    print splt_sentence
    print ret
    assert (len(splt_sentence) == len(ret))

    return ret

def get_attributes(word_data):
    wd = word_data
    fmt = "%s,%s\n"
    return ""
    return fmt % (wd["words_before"], wd["words_after"])

def process_file(fname):
    ifile = open(fname)

    for line in ifile:
        # quitamos el primer item de la linea (no nos interesa)
        splt_lbl_sentence = line.split()[1:]

        # words_data es una lista de diccionarios; cada diccionario representa
        # a una palabra (y sus datos) de la oracion

        # tomamos las palabras y sus junturas de la linea de entrada
        words_data = [
            {"word": wj.split(":")[0], "joint": wj.split(":")[1]} \
                for wj in splt_lbl_sentence]

        # limpiamos la entrada (quitamos la informacion de junturas)
        splt_sentence = [wj.split(":")[0] for wj in splt_lbl_sentence]

        # tomamos la informacion de POS tagging
        for i, tag in enumerate(get_POS_tags(splt_sentence)):
            # llenamos los campos que faltan con cero hasta TAG_SIZE
            tag = tag.ljust(TAG_SIZE, "0")
            # cada atributo del tag es un atributo distinto en el ARFF
            for j, attr in enumerate(tag):
                key = "attr_%d" % j
                words_data[i][key] = attr

        # conseguimos mas atributos
        for i, word in enumerate(splt_sentence):
            words_data[i]["words_before"] = i
            words_data[i]["words_after"] = len(splt_sentence) - (i + 1)

            sys.stdout.write(get_attributes(words_data[i]))
 

if __name__ == "__main__":
    header = """
@RELATION joint

@ATTRIBUTE wordsbefore  NUMERIC
@ATTRIBUTE wordsafter   NUMERIC
@ATTRIBUTE class        (0,1,2,3,4)
"""
    sys.stdout.write(header)

    process_file(INPUT_FNAME)
       
