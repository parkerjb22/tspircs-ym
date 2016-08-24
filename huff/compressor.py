from queue import PriorityQueue
import time
import os

class Compressor:

    def __init__(self, inputFileName, compressedFileName, debug_mode = False):
        self.inputFileName = inputFileName
        self.compressedFileName = compressedFileName
        self.debug_mode = debug_mode

    def run(self):
        start = time.time()
        nodes = self.buildWeightedQueue()
        root = self.buildNodeTree(nodes)
        myMap = self.mapTree(root, {})
        myBytes = self.processFile(myMap)
        self.writeBytesToFile(myBytes)
        end = time.time()
        self.printResults(start, end)

    def printResults(self, start, end):
        originalSize = os.path.getsize(self.inputFileName)
        compressedSize = os.path.getsize(self.compressedFileName)
        print ("Compression complete.")
        print ("\tDuration: %.2fs" % (end - start))
        print ("\tOriginal size: %dB" % originalSize)
        print ("\tCompressed size: %dB" % compressedSize)
        print ('\tCompression Rate: %.2f%%' % (compressedSize/originalSize * 100))

    def buildWeightedQueue(self, chunkSize=8192):
        if self.debug_mode:
            print('buildWeightedQueue')
        myMap = {}
        with open(self.inputFileName, 'rb') as f:
            while 1:
                chunk = f.read(chunkSize)
                if not chunk:
                    break
                for byte in chunk:
                    if byte in myMap:
                        myMap[byte] += 1
                    else:
                        myMap[byte] = 1

        nodes = PriorityQueue()
        for i, v in myMap.items():
            nodes.put(Node(i, v))
        return nodes

    def buildNodeTree(self, nodes):
        if self.debug_mode:
            print('buildNodeTree')
        while nodes.qsize() > 1:
            leftChild = nodes.get()
            rightChild = nodes.get()
            weight = leftChild.weight + rightChild.weight
            newNode = Node(None, weight, leftChild, rightChild)
            nodes.put(newNode)
        return nodes.get()

    def mapTree(self, root, myMap, code = ''):
        if self.debug_mode:
            print('mapTree')
        if root.value is not None:
            myMap[root.value] = code
        else :
            self.mapTree(root.leftChild, myMap, code+'0')
            self.mapTree(root.rightChild, myMap, code+'1')
        return myMap

    def generateHeader(self, myMap):
        flippedMap = self.flipMap(myMap)
        payload = self.generateHeaderPayLoad(flippedMap)
        pad = 8 - (len(payload) % 8)
        header = payload + '0'*pad
        return header

    def generateHeaderPayLoad(self, myMap, binaryString = ''):
        if self.debug_mode:
            print('mapTree')
        if binaryString in myMap:
            value = ("{0:08b}".format(myMap[binaryString]))
            return '1' + value
        else:
            return '0' + self.generateHeaderPayLoad(myMap, binaryString + '0') + self.generateHeaderPayLoad(myMap, binaryString + '1')

    def processFile(self, myMap, chunkSize=8192):
        if self.debug_mode:
            print('processFile')

        newResult = []
        binaryString = self.generateHeader(myMap)
        with open(self.inputFileName, 'rb') as f:
            while 1:
                chunk = f.read(chunkSize)
                if not chunk:
                    break
                for byte in chunk:
                    if byte not in myMap:
                        raise Exception
                    binaryString += myMap[byte]
                    while (len(binaryString)> 8):
                        intVal = int(binaryString[:8], 2)
                        newResult.append(intVal)
                        binaryString = binaryString[8:]

        return self.processEOF(binaryString, newResult)

    def processEOF(self, binaryString, newResult):
        if (len(binaryString) > 6):
            size  = len(binaryString) - 6
            intVal = int(binaryString.ljust(8, '0'), 2)
            newResult.append(intVal)
            binaryString = ''.ljust(5, '0')
        else:
            size  = len(binaryString) + 2

        intVal = int(binaryString.ljust(8, '0'), 2) | size
        newResult.append(intVal)

        return newResult

    def writeBytesToFile(self, myBytes):
        if self.debug_mode:
            print('writeBytesToFile')
        newFileByteArray  = bytes(myBytes)
        with open(self.compressedFileName, 'wb') as f:
            f.write(newFileByteArray)

    def flipMap(self, myMap):
        if self.debug_mode:
            print('flipMap')
        result = {}
        for i, v in myMap.items():
            result[v] = i
        return result

class Node:
    def __init__(self, value, weight, leftChild = None, rightChild = None):
        self.value = value
        self.weight = weight
        self.leftChild = leftChild
        self.rightChild = rightChild

    def __lt__(self, other):
        if (self.weight < other.weight):
            return True
        elif (self.value is not None and other.value is not None):
            return self.value < other.value
        return False