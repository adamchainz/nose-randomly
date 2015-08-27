import random
import unittest


class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.random_number = random.random()

    def test_random(self):
        self.assertEqual(self.random_number, 0.13436424411240122)


class TestsAgain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.random_number = random.random()

    def test_random_again(self):
        self.assertEqual(self.random_number, 0.13436424411240122)
