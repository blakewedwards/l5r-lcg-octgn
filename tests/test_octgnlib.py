import os
import sys
import unittest
sys.path.append(os.path.join('..', 'o8g', 'scripts'))
from octgnlib import distance, closest

class TestOctgnLib(unittest.TestCase):
  def test_distance(self):
    self.assertEqual(distance([0, 0], [0, 0]), 0)
    self.assertEqual(distance([0, 0], [2, 0]), 2)
    self.assertEqual(distance([0, -2], [0, 0]), 2)

  def test_closest(self):
    self.assertEqual(closest([0, 0], [], lambda o: o), None)
    self.assertEqual(closest([0, 0], [[0, 0]], lambda o: o), [0, 0])
    self.assertEqual(closest([0, 0], [[1, 1], [2, 2]], lambda o: o), [1, 1])
    self.assertEqual(closest([0, 0], [[1, 1], [-1, -1]], lambda o: o), [1, 1]) # Two points equally close returns first found

if __name__ == '__main__':
  unittest.main()
