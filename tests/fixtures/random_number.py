import random
import unittest


class Tests(unittest.TestCase):

    def test_random(self):
        self.assertEqual(random.random(), 0.13436424411240122)
