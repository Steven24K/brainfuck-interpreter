import sys, argparse, time, os

def createLogDir():
    dir_name = "debug_log"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    f = open(dir_name + "/log.txt", "w+")
    f.write("")

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
        self.last_output = "None"
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
        Program Counter: {}
        Last output: {}
        Loops: {}
        """
        return summary.format(str(type(self)), str(self.stack), str(self.pointer), str(self.pc), self.last_output ,str(self.loops))
    def evaluate(self, debug = False, timeout = None, log = False):
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
                self.last_output = str(chr(self.stack[self.pointer]))
            elif statement == ",":
                self.stack[self.pointer] = ord(sys.stdin.read(1))
            elif statement == "[" and self.stack[self.pointer] == 0:
                self.pc = self.loops[self.pc]
            elif statement == "]" and self.stack[self.pointer] > 0:
                self.pc = self.loops[self.pc]

            if debug: print(self)
            if timeout: time.sleep(timeout)
            if log: 
                log = open("debug_log/log.txt", "a")
                log.write(str(self))
            
            self.pc += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    debug = False
    log = False

    parser.add_argument("--program",default="examples/hello.bf", help = "The path to a branfuck file, the extension type does not matter. Only the body of the file is being ret.")
    parser.add_argument("--debug", help="Prints the memory stack in the console, at every iteration.")
    parser.add_argument("--timeout", default="0", help="Slows down the program by n secconds, works independently from the debugger. But it is usefull to use it with --debug")
    parser.add_argument("--log", help="Logs the current memory state to a txt file, in the current directory. If it allready exists the old log is being overwritten.")

    args = parser.parse_args()
    if args.program: brainfuck_file = args.program
    if args.debug: debug = args.debug
    if args.timeout: timeout = int(args.timeout)

    if args.log:
         log = args.log
         createLogDir()

    code = openCodefile(brainfuck_file)
    interpreter = Interpreter(code)
    interpreter.evaluate(debug, timeout, log)