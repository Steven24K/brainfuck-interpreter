import sys, argparse, time

def fold(f, accumulator, seq):
    if len(seq) == 0:
        return accumulator
    else:
        return fold(f, f(accumulator, seq[0]), seq[1:])


def openCodefile(file):
    code = open(file)
    code = code.readlines()
    result = ""
    for line in code:
        result += line
    return "".join(filter(lambda x: x in [".", ",", "[", "]", "<", ">", "+", "-",], result))

class Interpreter: 
    def __init__(self, program):
        self.stack = [0,]
        self.pointer = 0
        self.program = program
        self.pc = 0
        self.loops = self.checkLoops()
    def checkLoops(self):
        tmp = []
        loops = {}
        index = 0
        while index < len(self.program):
            if self.program[index] == "[": tmp.append(index)
            if self.program[index] == "]": 
                start = tmp.pop()
                loops[start] = index
                loops[index] = start
            index = index + 1
        return loops
    def __str__(self):
        summary = """
        __________________________BRAINFUCK Interpreter summary__________________________
        Type: {}
        Stack: {}
        Pointer: {}
        Program Counter {}
        Loops: {}
        """
        return summary.format(str(type(self)), str(self.stack), str(self.pointer), str(self.pc), str(self.loops))
    def evaluate(self, debug = False, timeout = None):
        while self.pc < len(self.program):
            statement =  self.program[self.pc]
            if statement == ">":
                self.pointer+=1
                if self.pointer == len(self.stack): self.stack.append(0)
            elif statement == "<":
                self.pointer-=1
                if self.pointer < 0: 
                    sys.stdout.write("Stack out of range, pointer: " + str(self.pointer))
                    sys.exit()
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
                self.pc = self.loops[self.pc]
            elif statement == "]" and self.stack[self.pointer] > 0:
                self.pc = self.loops[self.pc]

            if debug: print(self)
            if timeout: time.sleep(timeout)
            
            self.pc += 1


if __name__ == "__main__":
    brainfuck_file = "examples/hello.bf"
    debug = False
    timeout = None

    parser = argparse.ArgumentParser()

    parser.add_argument("--program")
    parser.add_argument("--debug")
    parser.add_argument("--timeout")

    args = parser.parse_args()
    if args.program:brainfuck_file = args.program
    if args.debug: debug = args.debug
    if args.timeout: timeout = int(args.timeout)

    code = openCodefile(brainfuck_file)
    interpreter = Interpreter(code)
    interpreter.evaluate(debug, timeout)