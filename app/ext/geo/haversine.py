# -*- coding: utf-8 -*-
"""
  A pure Python implementation of Haversine formula
  Based on Bartek Górny implementation and others
  Author: Jorge Brunal Perez <diniremix@gmail.com>

  How to use:

  from haversine import calculate_distance

  origin = [4.6565, -74.564654]
  destiny = [4.6748, -74.05485]

  result_in_kms = calculate_distance(origin, destiny, 'kms')
  print "result in kms", result_in_kms

  Otherwise
  result_in_mts = calculate_distance(origin, destiny)
  print "result in mts", result_in_mts

"""

import math


def calculate_distance(lat, lon, type_measure='mts'):
    r = 6371
    rad = (math.pi / 180)
    lat1 = lat[0]
    lat2 = lon[0]

    lon1 = lat[1]
    lon2 = lon[1]

    dlat = ((lat2 - lat1) * rad)
    dlon = ((lon2 - lon1) * rad)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1 * rad) * math.cos(lat2 * rad) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.asin(math.sqrt(a))
    d = r * c

    resp = 0
    if type_measure is 'kms':
        resp = round(d, 2)
    if type_measure is 'mts':
        resp = round((d * 1000), 2)
    return resp
