import unittest
from lzwcompressor import LZWCompressor

class MyTest(unittest.TestCase):

    def test_doSomething(self):

        input = "thisisthe"
        actual = LZWCompressor(None, None).doSomething(input)
        expected = [116, 104, 105, 115, 258, 256, 101]
        self.assertEqual(expected, actual)