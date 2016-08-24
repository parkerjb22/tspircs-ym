class LZWCompressor:

    def __init__(self, inputFileName, compressedFileName, debug_mode = False):
        self.inputFileName = inputFileName
        self.compressedFileName = compressedFileName
        self.debug_mode = debug_mode


    def doSomething(self, inputString):

        count = 256
        charDict = {}
        output = []
        curr = inputString[0]

        for i in range (1, len(inputString)):
            next = inputString[i]
            test = curr + next
            if test not in charDict:
                charDict[test] = count
                self.outputChar(curr, charDict, output)
                curr = next
                count += 1
            else:
                curr += next

        self.outputChar(curr, charDict, output)
        return output

    def outputChar(self, curr, charDict, output):
        if curr not in charDict:
            if len(curr) > 1:
                raise Exception
            value = ord(curr)
        else:
            value = charDict[curr]
        output.append(value)