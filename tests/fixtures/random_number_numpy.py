import unittest

import numpy as np


class Tests(unittest.TestCase):

    def test_random(self):
        self.assertEqual(np.random.rand(), 0.417022004702574)
