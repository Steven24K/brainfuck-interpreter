import sys

def fold(f, accumulator, seq):
    if len(seq) == 0:
        return accumulator
    else:
        return fold(f, f(accumulator, seq[0]), seq[1:])


class Interpreter: 
    def __init__(self, program):
        self.stack = [0,]
        self.pointer = 0
        self.program = ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], program))
        self.pc = 0
    def gotoEOF(self):
        self.pc = len(self.program) -1
    def __str__(self):
        summary = """
        ________BRAINFUCK Interpreter summary__________
        Type: {}
        Stack: {}
        Pointer: {}
        Program Counter {}
        """
        return summary.format(str(type(self)), str(self.stack), str(self.pointer), str(self.pc))
    def evaluate(self, debug = False):
        if self.pc < len(self.program):
            statement =  self.program[self.pc]
            if statement == ">":
                self.pointer+=1
                if self.pointer == len(self.stack): self.stack.append(0)
            elif statement == "<":
                self.pointer-=1
                if self.pointer < 0: 
                    sys.stdout.write("Stack out of range, pointer: " + str(self.pointer))
                    self.gotoEOF()
            elif statement == "+":
                self.stack[self.pointer]+=1
                if self.stack[self.pointer] > 255: self.stack[self.pointer] = 0
            elif statement == "-":
                self.stack[self.pointer]-=1
                if self.stack[self.pointer] < 0: self.stack[self.pointer] = 255
            elif statement == ".":
                sys.stdout.write(chr(self.stack[self.pointer]))
            elif statement == ",":
                self.stack[self.pointer] = ord(sys.stdin.read(1))
            elif statement == "[" and self.stack[self.pointer] == 0:
                self.pc = program[self.pc:].find("]")+1
            elif statement == "]" and self.stack[self.pointer] > 0:
                self.pc -= fold(lambda s,x: x+s, "", self.program[0:self.pc]).find("[")+1

            if debug: print(self)
            self.pc += 1
            self.evaluate(debug)


        

hello_world = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
test = ",[>+.<-]"
interpreter = Interpreter(hello_world)
interpreter.evaluate(debug=True)
#print(interpreter)