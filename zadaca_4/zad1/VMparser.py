class Parser:

    def __init__(self):
        self._labels=[]
        self._lab = 0
        self._olines = []
        self._flag = True

    def parseFile(self, filename):
        try:
            self._file = open(filename + ".vm", "r")
        except:
            Parser._error("File", -1, "Cannot open source file.")
            return

        self._ilines = []
        self._name = filename
        self._func = ""

        try:
            self._readFile()
        except:
            Parser._error("File", -1, "Cannot read source file.")
            return

        for (line, n) in self._ilines:
            a = line.split("//")
            a = a[0]
            a = a.split()
            if a[0] == "label":
                if len(a)>2:
                    self._flag = False
                    Parser._error("Parser", n, "Undefined label.")
                    return ""
                self._labels.append(a[1])
        
        if not self._parseLines():
            return

    def writeFile(self, filename):
        try:
            self._file = open(filename + ".asm", "w")
        except:
            Parser._error("File", -1, "Cannot open destination file.")
            return

        try:
            self._writeFile()
        except:
            Parser._error("File", -1, "Cannot write to destination file.")
            return

    def _parseLines(self):
        lines = []
        for (line, n) in self._ilines:
            l = self._parseLine(line, n)
            if not self._flag:
                return False
            if len(l) > 0:
                lines.append(l)
        self._olines = self._olines + lines
        return True

    def _parseLine(self, line, n):
        l = line.split("//"); l = l[0]
        if len(l) == 0: return ""
        l = l.split()
        if len(l) == 0: return ""
        if len(l[0]) == 0: return ""

        if l[0] == "push":
            if len(l) == 3:
                return "// " + " ".join(l) + "\n" + self._push(l[1], l[2], n)
            else:
                self._flag = False
                Parser._error("Parser", n, "Undefined push.")
                return ""

        elif l[0] == "pop":
            if len(l) == 3:
                return "// " + " ".join(l) + "\n" + self._pop(l[1], l[2], n)
            else:
                self._flag = False
                Parser._error("Parser", n, "Undefined pop.")
                return ""

        elif len(l) > 1 or l[0] == "return":
            if l[0] == "goto" and len(l) == 2:
                return "// " + " ".join(l) + "\n" + self._goto(l[1], n)
            elif l[0] == "if-goto" and len(l) == 2:
                return "// " + " ".join(l) + "\n" + self._ifgoto(l[1], n)
            elif l[0] == "label" and len(l) == 2:
                return "// " + " ".join(l) + "\n" + self._label(l[1], n)
            elif l[0] == "function" and len(l) == 3:
                return "// " + " ".join(l) + "\n" + self._function(l[1], l[2], n)
            elif l[0] == "return" and len(l) == 1:
                return "// " + " ".join(l) + "\n" + self._return(n)
            elif l[0] == "call" and len(l) == 3:
                return "// " + " ".join(l) + "\n" + self._call(l[1], l[2], n)
            else:
                self._flag = False
                Parser._error("Parser", n, "Undefined control command.")
                return ""

        elif len(l) == 1:
            return "// " + " ".join(l) + "\n" + self._comm(l[0], n)

        return ""

    def _goto(self, lab, n):
        if lab not in self._labels:
            self._flag = False
            Parser._error("Parser", n, "Undefined label.")
            return ""
        return "@" + self._func + "$" + lab + "\n0;JMP"

    def _ifgoto(self, lab, n):
        if lab not in self._labels:
            self._flag = False
            Parser._error("Parser", n, "Undefined label.")
            return ""
        return "@" + self._func + "$" + lab + "\n0;JMP"

        return "@SP\nAM=M-1\nD=M+1\n@" + self._func + "$" + lab + "\nD;JEQ"

    def _label(self, lab, n):
        return "(" + self._func + "$" + str(lab) + ")"

    def _function(self, name, nvar, n):
        self._func = self._name + "." + name
        t = "(" + self._name + "." + name + ")" # function label
        for i in range(1, 1 + int(nvar)):       # push n locals
            t += "\n@SP\nM=M+1\nA=M-1\nM=0"
        return t

    def _return(self, n):
        t = "@LCL\nD=M\n@R15\nM=D\n" \
          + "@5\nD=A\n@R15\nA=M-D\nD=M\n@R14\nM=D\n" \
          + "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n" \
          + "@ARG\nD=M+1\n@SP\nM=D\n" \
          + "@R15\nAM=M-1\nD=M\n@THAT\nM=D\n" \
          + "@R15\nAM=M-1\nD=M\n@THIS\nM=D\n" \
          + "@R15\nAM=M-1\nD=M\n@ARG\nM=D\n" \
          + "@R15\nAM=M-1\nD=M\n@LCL\nM=D\n" \
          + "@R14\nA=M\n0;JMP"
        return t

    def _call(self, name, narg, n):
        h = name + "$ret." + str(self._lab) # return label name
        self._lab += 1
        t = "@" + h + "\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n" \
          + "@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n" \
          + "@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n" \
          + "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n" \
          + "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n" \
          + "@" + str(int(narg) + 5) + "\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n" \
          + "@SP\nD=M\n@LCL\nM=D\n" \
          + "@" + name + "\n0;JMP\n" \
          + "(" + h + ")"
        return t

    def _push(self, src, loc, n):
        try:
            if int(loc)<0:
                self._flag = False
                Parser._error("Push", n, "Undefined loc \"" + loc + "\".")
                return ""
        except:
            self._flag = False
            Parser._error("Push", n, "Undefined loc \"" + loc + "\".")
            return ""
        
        if src == "constant":
            l = "@" + str(loc) + "\nD=A\n"
        elif src == "local":
            l = "@" + str(loc) + "\nD=A\n@LCL\nA=D+M\nD=M\n"
        elif src == "argument":
            l = "@" + str(loc) + "\nD=A\n@ARG\nA=D+M\nD=M\n"
        elif src == "this":
            l = "@" + str(loc) + "\nD=A\n@THIS\nA=D+M\nD=M\n"
        elif src == "that":
            l = "@" + str(loc) + "\nD=A\n@THAT\nA=D+M\nD=M\n"
        elif src == "static":
            l = "@" + self._name + "." + str(loc) + "\nD=M\n"
        elif src == "temp":
            l = "@" + str(5 + int(loc)) + "\nD=M\n"
        elif src == "pointer":
            l = "@" + str(3 + int(loc)) + "\nD=M\n"
        else:
            self._flag = False
            Parser._error("Push", n, "Undefined source \"" + src + "\".")
            return ""
        return l + "@SP\nM=M+1\nA=M-1\nM=D"

    def _pop(self, dst, loc, n):
        try:
            if int(loc)<0:
                self._flag = False
                Parser._error("Pop", n, "Undefined loc \"" + loc + "\".")
                return ""
        except:
            self._flag = False
            Parser._error("Pop", n, "Undefined loc \"" + loc + "\".")
            return ""
        
        if dst == "local":
            l = "@" + str(loc) + "\nD=A\n@LCL\nD=M+D\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
        elif dst == "argument":
            l = "@" + str(loc) + "\nD=A\n@ARG\nD=M+D\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
        elif dst == "this":
            l = "@" + str(loc) + "\nD=A\n@THIS\nD=M+D\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
        elif dst == "that":
            l = "@" + str(loc) + "\nD=A\n@THAT\nD=M+D\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"
        elif dst == "static":
            l = "@SP\nAM=M-1\nD=M\n@" + self._name + "." + str(loc) + "\nM=D"
        elif dst == "temp":
            l = "@SP\nAM=M-1\nD=M\n@" + str(5 + int(loc)) + "\nM=D"
        elif dst == "pointer":
            l = "@SP\nAM=M-1\nD=M\n@" + str(3 + int(loc)) + "\nM=D"
        else:
            self._flag = False
            Parser._error("Pop", n, "Undefined destination.")
            return ""
        return l

    def _comm(self, comm, n):
        if comm == "add":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D"
        elif comm == "sub":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D"
        elif comm == "neg":
            l = "@SP\nA=M-1\nM=-M"
        elif comm == "eq":
            l1 = "LAB" + str(self._lab)
            l2 = "LAB" + str(self._lab + 1)
            self._lab += 2
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n" + \
                "@" + str(l1) + "\nD;JEQ\n" + "@" + str(l2) + "\nD=0;JMP\n" + \
                "(" + str(l1) + ")\nD=-1\n" + "(" + str(l2) + ")\n@SP\nA=M-1\nM=D"
        elif comm == "gt":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n" + \
                "@" + str(l1) + "\nD;JGT\n" + "@" + str(l2) + "\nD=0;JMP\n" + \
                "(" + str(l1) + ")\nD=-1\n" + "(" + str(l2) + ")\n@SP\nA=M-1\nM=D"
        elif comm == "lt":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n" + \
                "@" + str(l1) + "\nD;JLT\n" + "@" + str(l2) + "\nD=0;JMP\n" + \
                "(" + str(l1) + ")\nD=-1\n" + "(" + str(l2) + ")\n@SP\nA=M-1\nM=D"
        elif comm == "and":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D"
        elif comm == "or":
            l = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D"
        elif comm == "not":
            l = "@SP\nA=M-1\nM=!M"
        elif comm == "ep":
            l = "($EP$)\n@$EP$\n0;JMP"
        elif comm == "sp":
            l = "@256\nD=A\n@SP\nM=D"
        else:
            self._flag = False
            Parser._error("Comm", n, "Undefined command.")
            return ""
        return l

    def _readFile(self):
        n = 0
        for line in self._file:
            if len(line) > 0:
                self._ilines.append((line, n))
            n += 1

    def _writeFile(self):
        for line in self._olines:
            self._file.write(line + "\n")

    @staticmethod
    def _error(src, line, msg):
        if len(src) > 0 and line > -1:
            print("[" + src + ", " + str(line + 1) + "] " + msg)
        elif len(src) > 0:
            print("[" + src + "] " + msg)
        else:
            print(msg)

def main():
    P = Parser()
    P.parseFile("test")
    #P.parseFile("sum")
    #P.writeFile("test")

if __name__ == '__main__':
    main()
