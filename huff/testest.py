import unittest
from compressor import Compressor
from decompressor import Decompressor
import io

class MyTest(unittest.TestCase):

    def getHeader(self, chars, payloadFormat):
        binaryChars = []
        for char in chars:
            binaryChars.append(("{0:08b}".format(int.from_bytes(char.encode(), 'big'))))

        payload = payloadFormat.format(binaryChars)
        pad = 8 - (len(payload) % 8)
        return payload + '0'*pad

    def getIOBuff(self, inputString):
        bytes = []
        while len(inputString) >= 8:
            intVal = int(inputString[:8], 2)
            bytes.append(intVal)
            inputString = inputString[8:]

        return io.BytesIO(bytearray(bytes))

    def test_generateHeader(self):
        myMap = {
            ord('r') : '01',
            ord('e') : '00',
            ord('j') : '11',
            ord('l') : '10',
        }
        chars = ['e', 'r', 'l', 'j']
        payloadFormat = '001{0[0]}1{0[1]}01{0[2]}1{0[3]}'

        expected = self.getHeader(chars, payloadFormat)
        actual = Compressor(None, None).generateHeader(myMap)
        self.assertEqual(expected, actual)


    def test_generateHeader2(self):
        myMap = {
            ord(' ') : '010',
            ord('r') : '000',
            ord('b') : '111',
            ord('e') : '10',
            ord('o') : '011',
            ord('!') : '1101',
            ord('p') : '001',
            ord('x') : '1100',
        }
        chars = ['r', 'p', ' ', 'o', 'e', 'x', '!', 'b']
        payloadFormat = '0001{0[0]}1{0[1]}01{0[2]}1{0[3]}01{0[4]}001{0[5]}1{0[6]}1{0[7]}'

        expected = self.getHeader(chars, payloadFormat)
        actual = Compressor(None, None).generateHeader(myMap)
        self.assertEqual(expected, actual)

    def test_generateHeader3(self):
        myMap = {
            ord('b') : '100',
            ord('p') : '01',
            ord('e') : '00',
            ord('o') : '101',
            ord('r') : '1110',
            ord('x') : '1111',
            ord('!') : '1101',
            ord(' ') : '1100'
        }
        chars = ['e', 'p', 'b', 'o', ' ', '!', 'r', 'x']
        payloadFormat = '001{0[0]}1{0[1]}001{0[2]}1{0[3]}001{0[4]}1{0[5]}01{0[6]}1{0[7]}'

        expected = self.getHeader(chars, payloadFormat)
        actual = Compressor(None, None).generateHeader(myMap)
        self.assertEqual(expected, actual)

    def test_getMyByte(self):

        bytes = 2
        nextBytes = 26
        bitNum = 4
        expected = 33
        actual = Decompressor(None, None).getMyByte(bytes, nextBytes, bitNum)
        self.assertEqual(expected, actual)

    def test_getMyByte2(self):
        bytes = 107
        nextBytes = 46
        bitNum = 3
        expected = 101
        actual = Decompressor(None, None).getMyByte(bytes, nextBytes, bitNum)
        self.assertEqual(expected, actual)


    def test_digestHeader(self):
        header = '00101100101101110000001011000101011011110010010000010010000101011100101011110000'
        expected = {
            98 : '100',
            112 : '01',
            101 : '00',
            111 : '101',
            114 : '1110',
            120 : '1111',
            33 : '1101',
            32 : '1100'
        }

        expected = Decompressor(None, None).flipMap(expected)
        self.assertEquals(len(header) % 8, 0)
        f = self.getIOBuff(header)

        actual = Decompressor(None, None).digestHeader(f)
        self.assertEqual(expected, actual)

    def test_digestHeader2(self):
        header = '010110010110111000000000'
        expected = {
            112 : '1',
            101 : '0',
        }

        expected = Decompressor(None, None).flipMap(expected)
        self.assertEquals(len(header) % 8, 0)
        f = self.getIOBuff(header)

        actual = Decompressor(None, None).digestHeader(f)
        self.assertEqual(expected, actual)

    def test_digestHeader3(self):
        header = '01011001010101100010101110000000'
        expected = {
            112 : '11',
            98 : '10',
            101 : '0',
        }

        expected = Decompressor(None, None).flipMap(expected)
        self.assertEquals(len(header) % 8, 0)
        f = self.getIOBuff(header)

        actual = Decompressor(None, None).digestHeader(f)
        self.assertEqual(expected, actual)



    def test_decompressFile1(self):
        reverseMap = {
            '101' : ord('b'),
            '100' : ord('o'),
            '11'  : ord('x'),
            '00'  : ord('z'),
            '01'  : 3,
        }
        newBytes = [178, 92, 2] # boobxzF
        expected = [98, 111, 111, 98, 120, 122]

        actual = Decompressor(None, None).decompressFile(newBytes, reverseMap)
        self.assertEqual(expected, actual)

    def test_processFile1(self):
        lastByte = '11'
        expected = [196]
        actual = Compressor(None, None).processEOF(lastByte, [])
        self.assertEqual(expected, actual)


    def test_processFile2(self):
        lastByte = '11001'
        expected = [207]
        actual = Compressor(None, None).processEOF(lastByte, [])
        self.assertEqual(expected, actual)

    def test_processFile3(self):
        lastByte = '10000001'
        expected = [129, 2]
        actual = Compressor(None, None).processEOF(lastByte, [])
        self.assertEqual(expected, actual)

    def test_processFile4(self):
        lastByte = '1000001'
        expected = [130, 1]
        actual = Compressor(None, None).processEOF(lastByte, [])
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()