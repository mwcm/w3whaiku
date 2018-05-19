import random
import math
from collections import namedtuple
from os import environ

import what3words
from pyphen import Pyphen
from glom import glom

Word  = namedtuple('Word', 'word syllables')
Line  = namedtuple('Line', 'words syllables number')
Haiku = namedtuple('Haiku', 'lines syllables')

LONG_MAX = 180
LONG_MIN = -180

LAT_MAX = 85.05112878
LAT_MIN = -85.05112878


def setup():
    key = environ['w3wkey']
    w3w = what3words.Geocoder(key)
    dic = Pyphen(lang='en')
    return w3w, dic


def count_syllables(dictionary, word):
    count = 0
    hyphenated = dictionary.inserted(word)
    count = hyphenated.count('-') + 1
    return count, hyphenated


def get_random_address(w3w, dic):
    counted_words = []
    random_lat = random.uniform(LAT_MIN, LAT_MAX)
    random_long = random.uniform(LONG_MIN, LONG_MAX)
    res = w3w.reverse(lng=random_long, lat=random_lat)
    random_words = glom(res, 'words').split('.')

    for w in random_words:
        count, hyphenated = count_syllables(dic, w)
        temp = Word(word=w, syllables=count)
        counted_words.append(temp)

    return counted_words


def get_line(w3w, dic):

    three_words = get_random_address(w3w, dic)

    if three_words.syllables > 6:
        # must be line #2 (18 is max syllables; 18/3 = 6; middle line must have
        # most syllables)
        line = Line(words=three_words, syllables=three_words.syllables, number=2)
    else:
        # can be used as 1 or 3
        line = Line(words=three_words, syllables=three_words.syllables, number=13)

    return line


def write_haiku(w3w, dic):
    # XXX: SMALLEST NUMBER OF SYLLABLES IN AN ADDRESS SEEMS TO BE ABOUT 4

    # TODO: organize into EITHER 3 or 4 rows (start with 3)
    # TODO: 17 - 18 syllables
    # TODO: middle line MUST contain more syllables than other two
    # TODO: MAINTAIN WORD ORDER FROM ADDRESSES

    haiku = Haiku()
    all_words = []
    while  19 > syllables:
        if 18 >= syllables >= 17:
            return haiku

        words = get_random_address(w3w, dic)



        for w in words:
            line_s += w.syllables


            all_words.append(words)
        pass

    write_haiku(w3w, dic)


def main():

    w3w, dic = setup()
    words, total = write_haiku(w3w, dic)
    for word in words:
        print(word)

    print(total)
    # words = get_random_address(w3w, dic)
    # for line in haiku.lines:
        # print(line)

    # for word in words:
        # print(word)

    raise SystemExit()


if __name__ == '__main__':
    main()
