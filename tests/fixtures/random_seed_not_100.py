import random
import unittest


class Tests(unittest.TestCase):
    def test_not_reseeded_to_100(self):
        numbers = [random.random() for i in range(100)]

        # Now reseed with 100 to find what the first 100 numbers *would* be
        random.seed(100)
        numbers_seed_100 = [random.random() for i in range(100)]

        self.assertNotEqual(numbers, numbers_seed_100)
