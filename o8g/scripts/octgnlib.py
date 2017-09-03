from math import sqrt

def distance(position1, position2):
  return sqrt((position2[0] - position1[0])**2 + (position2[1] - position1[1])**2)

def closest(position, cards, f=lambda o: o.position):
  if not cards:
    return None
  return sorted(cards, key=lambda c: distance(position, f(c)))[0]
