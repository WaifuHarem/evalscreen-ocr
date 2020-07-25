import unittest

from ffr.ffr_core import FfrCore



class TestFFR(unittest.TestCase):

    def test_ffr(self):
        filename = 'unit_tests/data/ffr/test1.png'
        _, data = FfrCore(filename).process()

        print(data)