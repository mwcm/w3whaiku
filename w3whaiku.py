import random
import math
from collections import namedtuple
from os import environ

import what3words
from pyphen import Pyphen
from glom import glom

Word  = namedtuple('Word', 'word syllables')
Line  = namedtuple('Line', 'words syllables')
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

def write_haiku(w3w, dic):

    # XXX: SMALLES NUMBER OF SYLLABLES IN AN ADDRESS SEEMS TO BE ABOUT 4
    while True:
        words = get_random_address(w3w, dic)
        total_s = 0
        for w in words:
            total_s += w.syllables

        return words, total_s



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
