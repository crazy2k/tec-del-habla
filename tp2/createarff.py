#!/usr/bin/env python

import os
import sys

FREELING_CFG = "/usr/share/FreeLing/config/es.cfg"
TEMP_FNAME = "TEMPFILE"

TAG_SIZE = 8
VOWELS = ["a", "e", "i", "o", "u"]

def get_POS_tags(splt_sentence):

    def append_tag(l, item):
        if "+" in item:
            item = item.split("+")[0]
        l.append(item)

    sentence = " ".join(splt_sentence)
    os.system("echo %s | analyze --nortk --outf tagged -f %s > %s" %\
        (sentence, FREELING_CFG, TEMP_FNAME))

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
            append_tag(ret, tags[j])
        # si no, puede ser que FreeLing haya juntado la palabra con otras
        elif "_" in words[j]:
            # en ese caso, a todas les ponemos el mismo tag
            append_tag(ret, tags[j])
            for x in range(words[j].count("_")):
                append_tag(ret, tags[j])
                i += 1
            
            # chequeamos el caso patologico en el que se separo una contraccion
            # y se unio la primera parte a esta palabra
            if words[j].split("_")[-1].lower() in ["a", "de"] \
                and words[j + 1] == "el":
                j += 1
        # o puede que FreeLing haya partido la palabra en varias
        else:
            append_tag(ret, tags[j])

            # asumimos que si llegamos aca splt_sentence[i] es "al" o "del"
            j += 1

        j += 1
        i += 1

    assert (len(splt_sentence) == len(ret))

    return ret

def get_attributes(word_data):
    keys = word_data.keys()
    keys.sort()
    # juncture tiene que ir al final
    keys.remove("juncture")
    keys.append("juncture")

    # reemplazamos cada clave por su valor
    fields = [str(word_data[k]) for k in keys]

    return ",".join(fields)

def process_file(fname):
    ifile = open(fname)

    for line in ifile:
        # quitamos el primer item de la linea (no nos interesa)
        splt_lbl_sentence = line.split()[1:]

        # words_data es una lista de diccionarios; cada diccionario representa
        # a una palabra (y sus datos) de la oracion

        # tomamos las palabras y sus junturas de la linea de entrada
        words_data = [
            {"word": wj.split(":")[0], "juncture": wj.split(":")[1]} \
                for wj in splt_lbl_sentence]

        # limpiamos la entrada (quitamos la informacion de junturas)
        splt_sentence = [wj.split(":")[0] for wj in splt_lbl_sentence]

        # tomamos la informacion de POS tagging
        pos_tags = get_POS_tags(splt_sentence)
        for i, tag in enumerate(pos_tags):
            # llenamos los campos que faltan con cero hasta TAG_SIZE
            tag = tag.ljust(TAG_SIZE, "0")
            # cada atributo del tag es un atributo distinto en el ARFF
            for j, attr in enumerate(tag):
                key = "attr_%d" % j
                words_data[i][key] = attr

            if i + 1 < len(pos_tags):
                words_data[i]["next_is_verb"] = pos_tags[i + 1][0] == "V"
            else:
                words_data[i]["next_is_verb"] = False

        # conseguimos mas atributos
        for i, word in enumerate(splt_sentence):
            wd = words_data

            wd[i]["words_before"] = i
            wd[i]["words_before_perc"] = \
                wd[i]["words_before"]/float(len(splt_sentence))
            wd[i]["words_after"] = len(splt_sentence) - (i + 1)
            wd[i]["words_after_perc"] = \
                wd[i]["words_after"]/float(len(splt_sentence))
            wd[i]["first_word"] = i == 0
            wd[i]["last_word"] = i == (len(splt_sentence) - 1)
            wd[i]["ends_with"] = "V" if word[-1] in VOWELS else "C"
            wd[i]["length"] = len(word)

            if i + 1 < len(splt_sentence):    
                wd[i]["next_starts_with"] = \
                    "V" if splt_sentence[i + 1][0] in VOWELS else "C"
                wd[i]["next_length"] = len(splt_sentence[i + 1])
                wd[i]["next_word"] = splt_sentence[i + 1]
            else:
                wd[i]["next_starts_with"] = "N"
                wd[i]["next_length"] = 0
                wd[i]["next_word"] = "1r03r03032"

            sys.stdout.write("%s\n" % get_attributes(words_data[i]))
 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Uso: %s <archivo de entrada>\n" % sys.argv[0])
        sys.exit(1)

    input_fname = sys.argv[1]

    header = """
@RELATION juncture

@ATTRIBUTE attr_0           STRING
@ATTRIBUTE attr_1           STRING
@ATTRIBUTE attr_2           STRING
@ATTRIBUTE attr_3           STRING
@ATTRIBUTE attr_4           STRING
@ATTRIBUTE attr_5           STRING
@ATTRIBUTE attr_6           STRING
@ATTRIBUTE attr_7           STRING
@ATTRIBUTE endswith         STRING
@ATTRIBUTE firstword        STRING
@ATTRIBUTE lastword         STRING
@ATTRIBUTE length           NUMERIC
@ATTRIBUTE nextisverb       STRING
@ATTRIBUTE nextlength       NUMERIC
@ATTRIBUTE nextstartswith   STRING
@ATTRIBUTE nextword         STRING
@ATTRIBUTE word             STRING
@ATTRIBUTE wordsafter       NUMERIC
@ATTRIBUTE wordsafterperc   NUMERIC
@ATTRIBUTE wordsbefore      NUMERIC
@ATTRIBUTE wordsbeforeperc  NUMERIC

@ATTRIBUTE class        {0,1,2,3,4}

@DATA
"""
    sys.stdout.write(header)

    process_file(input_fname)
       
