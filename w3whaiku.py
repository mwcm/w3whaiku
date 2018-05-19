import random
import math
from os import environ

import what3words
from glom import glom

def main():
    key = environ['w3wkey']
    w3w = what3words.Geocoder(key)

    long_max = 180
    long_min = -180

    lat_max = 85.05112878
    lat_min = -85.05112878

    random_lat = random.uniform(lat_min, lat_max)
    random_long = random.uniform(long_min, long_max)

    res = w3w.reverse(lng=random_long, lat=random_lat)
    print(' '.join(glom(res, 'words').split('.')))

    raise SystemExit()


if __name__ == '__main__':
    main()
