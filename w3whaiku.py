import random
import math
from os import environ

import what3words
from pyphen import Pyphen
from glom import glom


def setup():
    key = environ['w3wkey']
    w3w = what3words.Geocoder(key)
    dic = Pyphen(lang='en')
    return w3w, dic


def count_syllables(dictionary, word):
    count = 0
    hyphenated = dictionary.inserted(word)
    count = hyphenated.count('-') + 1
    return hyphenated, count


def main():

    long_max = 180
    long_min = -180

    lat_max = 85.05112878
    lat_min = -85.05112878

    w3w, dic = setup()

    random_lat = random.uniform(lat_min, lat_max)
    random_long = random.uniform(long_min, long_max)

    res = w3w.reverse(lng=random_long, lat=random_lat)

    words = glom(res, 'words').split('.')

    for word in words:
        count, hyphenated = count_syllables(dic, word)
        print(word, count, hyphenated)

    raise SystemExit()


if __name__ == '__main__':
    main()
