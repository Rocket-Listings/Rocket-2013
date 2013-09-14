from math import radians, cos, sin, asin, sqrt
import json

def haversine(lat1, lng1, lat2, lng2):
  """
  Calculate the haversine (great circle) distance
  between two points on earth given by lat/lng in decimal degrees.
  """
  lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
  delta_lat = lat2 - lat1
  delta_lng = lng2 - lng1
  a = sin(delta_lat/2)**2 + cos(lat1) * cos(lat2) * sin(delta_lng/2)**2
  c = 2 * asin(sqrt(a))
  return 6367 * c

def closest_craigslist(lat, lng):
  file = open("rocket/templates/listings/partials/markets.json", "r")
  markets_array = dict(json.loads(file.read()))['markets']
  distance = 99999
  for market_dict in markets_array:
    calc_distance = haversine(lat, lng, market_dict['latitude'], market_dict['longitude'])
    if calc_distance < distance:
      distance = calc_distance
      closest_cl = market_dict
  return closest_cl