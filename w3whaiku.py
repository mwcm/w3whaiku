import math
import json
import random
from os import environ
from time import sleep
from collections import namedtuple

import what3words
from glom import glom
from pyphen import Pyphen

Word  = namedtuple('Word', 'syllables string')
Line  = namedtuple('Line', 'map type words syllables string')
Haiku = namedtuple('Haiku', 'maps lines syllables string')

LONG_MAX = 180
LONG_MIN = -180

LAT_MAX = 85.05112878
LAT_MIN = -85.05112878

MAX_SYLLABLES = 18
MIN_SYLLABLES = 17

api_hits = 0


def setup():
    key = environ['w3wkey']
    w3w = what3words.Geocoder(key)
    dic = Pyphen(lang='en')
    return w3w, dic


def count_syllables(dictionary, word):
    hyphenated = dictionary.inserted(word)
    # add one for first syllable
    count      = hyphenated.count('-') + 1
    return count, hyphenated


def get_random_address(w3w, dic):
    global api_hits

    counted_words = []
    random_lat    = random.uniform(LAT_MIN, LAT_MAX)
    random_long   = random.uniform(LONG_MIN, LONG_MAX)
    res           = w3w.reverse(lng=random_long, lat=random_lat)

    if glom(res, 'status.status') == 200:
        api_hits += 1
        # print('getting random address')
        print('api hit: {}' .format(api_hits))
        print('map: {}'     .format(glom(res, 'map')))
        print('response: {}'.format(res))

    else:
        raise SystemExit('failure response from api {}'.format(res))

    random_words = glom(res, 'words').split('.')
    address_map  = glom(res, 'map')

    total_syllables = 0
    for w in random_words:
        syllable_count, hyphenated = count_syllables(dic, w)
        temp = Word(string=w, syllables=syllable_count)
        counted_words.append(temp)
        total_syllables += syllable_count

    return counted_words, total_syllables, address_map


def get_line(w3w, dic):
    # set (t)ype to 1 by default, this type represents either outer line
    t = 1

    # get a random address from w3w
    three_words, counted_syllables, m = get_random_address(w3w, dic)

    # form string representation
    line_string = ' '.join([three_words[0].string,
                            three_words[1].string,
                            three_words[2].string])

    # if we count more than 1/3 total syllables in a line we know this is our
    # middle line, since the middle line of a haiku must be the longest
    if counted_syllables >  MAX_SYLLABLES / 3:
        t = 2

    line = Line(map=m,
                type=t,
                words=three_words,
                syllables=counted_syllables,
                string=line_string)
    return line


def get_line_of_type(w3w, dic, requested_type):
    if requested_type not in [1,2]:
        raise SystemError('invalid type')
    while True:
        line = get_line(w3w, dic)
        if line.type == requested_type:
            return line
        else:
            sleep(1)
            pass


def write_haiku(w3w, dic):
    while True:
        line_one   = get_line_of_type(w3w, dic, 1)
        line_two   = get_line_of_type(w3w, dic, 2)
        line_three = get_line_of_type(w3w, dic, 1)


        haiku_syllables = line_one.syllables + \
                          line_two.syllables + \
                          line_three.syllables

        if MAX_SYLLABLES >= haiku_syllables >= MIN_SYLLABLES:

            haiku_lines = [line_one, line_two, line_three]
            haiku_maps  = [line_one.map, line_two.map, line_three.map]
            haiku_str   = '\n'.join([line_one.string, line_two.string, line_three.string])

            haiku = Haiku(maps=haiku_maps,
                          lines=haiku_lines,
                          syllables=haiku_syllables,
                          string=haiku_str)
            return haiku
        pass


def main():
    w3w, dic = setup()
    haiku = write_haiku(w3w, dic)
    print(json.dumps(haiku._asdict()))
    print('\n')
    print(haiku.string)
    print('\n')
    print('\n'.join(haiku.maps))
    raise SystemExit()


if __name__ == '__main__':
    main()
