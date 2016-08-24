import sys


class BfReader:
    def __init__(self):
        # simulate the cells with a list
        self.tape = [0] * (3 * 10 ** 4)

        # the data pointer
        self.ptr = 0

        # primitives which can directly be handled
        self.handle_directly = {".": self.dot, ",": self.comma, "<": self.lt, ">": self.gt, "+": self.plus,
                                "-": self.minus}

        self.inputMsg = input('Word ---> ')

    def lt(self):
        """ performs a < """
        if self.ptr <= 0:
            raise (ValueError, "Segmentation fault!")
        self.ptr -= 1

    def gt(self):
        """" performs a > """
        if self.ptr >= 3 * 10 ** 4 - 1:
            raise (ValueError, "Segmentation fault!")
        self.ptr += 1

    def plus(self):
        """ performs a + """
        self.tape[self.ptr] = (self.tape[self.ptr] + 1) % 256

    def minus(self):
        """ perfoms a - """
        self.tape[self.ptr] = (self.tape[self.ptr] - 1) % 256

    def dot(self):
        """ performs a . """
        #sys.stdout.write(chr(self.tape[self.ptr]))
        print (str(self.tape[self.ptr]))

    def comma(self):
        """ performs a , """
        if (len(self.inputMsg) == 0):
            c = 0
        else :
            #c = ord(sys.stdin.read(1))
            c = ord(self.inputMsg[0])
            self.inputMsg = self.inputMsg[1:]
            #print (self.inputMsg)

        if c != 26:
            self.tape[self.ptr] = c

    def parse(self, code):
        """ maps the "["s to the corresponding "]"s """
        # stack to contain the indices of the opening brackets
        opening = []
        # dict which maps the indices of the opening brackets
        # to the closing brackets
        loop = {}
        for i, c in enumerate(code):
            if c == "[":
                opening.append(i)
            elif c == "]":
                try:
                    begin = opening.pop()
                    loop[begin] = i
                except IndexError:
                    raise (ValueError, "Supplied string isn't balanced, too many ]s!")
        # if the stack isn't empty, the string cannot be balanced
        if opening != []:
            raise (ValueError, "Supplied string isn't balanced, too many [s")
        else:
            return loop

    def eval_bf(self, code):
        """ evaluates bf code """
        global ptr
        # get the scopes of the "[", "]"s
        loop = self.parse(code)
        # initialize the program counter
        pc = 0
        # a stack to store the pc for loops
        stack = []
        while pc < len(code):
            instruction = code[pc]
            # handle the primitives directly
            if instruction in self.handle_directly:
                self.handle_directly[instruction]()
            elif instruction == "[":
                # if loop condition is fullfiled
                # enter loop block
                if self.tape[self.ptr] > 0:
                    stack.append(pc)
                else:  # else go to the end of the block
                    pc = loop[pc]
            elif instruction == "]":
                # jump back where you came from!
                pc = stack.pop() - 1
            pc += 1
