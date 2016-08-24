import os
import time

class Decompressor:

    def __init__(self, compressedFileName, outputFileName, debug_mode = False):
        self.compressedFileName = compressedFileName
        self.outputFileName = outputFileName
        self.debug_mode = debug_mode

    def run(self):
        start = time.time()
        newBytes, myMap = self.readCompressedFile()
        s = self.decompressFile(newBytes, myMap)
        self.writeBytesToFile(s)
        end = time.time()
        self.printResults(start, end)
        return myMap

    def printResults(self, start, end):
        decompressedSize = os.path.getsize(self.outputFileName)
        print ("Decompression complete.")
        print ("\tDuration: %.2fs" % (end - start))
        print ("\tFile size: %dB" % decompressedSize)

    def getHeaderSize(self, file):
        return int(file.read(1)[0])

    def digestHeader(self, file):
        binaryString = ''
        myMap = {}
        bytes = file.read(1)[0]

        bitNum, bytes, myMap = self.dive(file, bytes, 7, binaryString, myMap)
        return myMap

    def get_bit(self, byteVal,idx):
        return ((byteVal&(1<<idx))!=0)

    def dive(self, file, bytes, bitNum, str, myMap):
        c = self.get_bit(bytes, bitNum)

        if (c):
            chunk = file.read(1)
            if chunk:
                nextBytes = chunk[0]
            else:
                nextBytes = 0
            char = self.getMyByte(bytes, nextBytes, bitNum)
            myMap[str] = char
            bytes = nextBytes
        else:
            bitNum, bytes = self.advance(file, bitNum, bytes)
            bitNum, bytes, myMap = self.dive(file, bytes, bitNum, str + '0', myMap)
            bitNum, bytes = self.advance(file, bitNum, bytes)
            bitNum, bytes, myMap = self.dive(file, bytes, bitNum, str + '1', myMap)
        return bitNum, bytes, myMap

    def advance(self, file, bitNum, bytes):
        bitNum -= 1
        if (bitNum < 0):
            bytes = file.read(1)[0]
            bitNum = 7

        return bitNum, bytes


    def getMyByte(self, bytes, nextBytes, bitNum):
        top = (bytes << 8 - bitNum) % 256
        bottom = (nextBytes >> bitNum) % 256
        return top + bottom

    def readCompressedFile(self, chunkSize=8192):
        if self.debug_mode:
            print('readCompressedFile')
        result = []
        with open(self.compressedFileName, 'rb') as f:
            myMap = self.digestHeader(f)
            while 1:
                chunk = f.read(chunkSize)
                if chunk:
                    for byte in chunk:
                        result.append(byte)
                else:
                    break
        return result, myMap

    def decompressFile(self, newBytes, reverseMap):
        if self.debug_mode:
            print('decompressFile')
        binaryString = ''
        outPut = []
        numBytes = len(newBytes)
        for idx, byte in enumerate(newBytes):
            if (idx == numBytes - 2):
                bytesToRead = (newBytes[idx+1] & 7) + 6
                curr = "{0:08b}".format(byte)
                charIndex = 0
                for i in range(bytesToRead):
                    if (charIndex == 8):
                        curr = "{0:08b}".format(newBytes[idx + 1])
                        charIndex = 0
                    binaryString += curr[charIndex]
                    if binaryString in reverseMap:
                        outPut.append(reverseMap[binaryString])
                        binaryString = ''
                    charIndex += 1
                break

            curr = "{0:08b}".format(byte)
            for c in curr:
                binaryString += c
                if binaryString in reverseMap:
                    outPut.append(reverseMap[binaryString])
                    binaryString = ''
        return outPut

    def writeBytesToFile(self, myBytes):
        if self.debug_mode:
            print('writeBytesToFile')
        newFileByteArray  = bytes(myBytes)
        with open(self.outputFileName, 'wb') as f:
            f.write(newFileByteArray)

    def flipMap(self, myMap):
        if self.debug_mode:
            print('flipMap')
        result = {}
        for i, v in myMap.items():
            result[v] = i
        return result