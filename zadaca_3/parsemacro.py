def start_parse(self):
    j = 0
    for i in self._lines:
        if i[0].split("(")[0] == "$MV":
            pom = i[0].split("(")[1]
            D = pom.split(",")[0]
            pom1 = i[0].split(",")[1]
            S = pom1.split(")")[0]
            self.parse_MV(D,S,j)
        if i[0].split("(")[0] == "$SWP":
            pom = i[0].split("(")[1]
            D = pom.split(",")[0]
            pom1 = i[0].split(",")[1]
            S = pom1.split(")")[0]
            self.parse_SWP(D,S,j) 
        j += 1    
def posfix(self,pos,add):
    for i in range(pos+1,len(self._lines)):
                tup = self._lines[i]
                str = tup[0]
                pos1 = tup[1]
                pos2 = tup[2]
                newtup = (str,pos1+add,pos2+add)
                self._lines[i] = newtup

def parse_MV(self,DST, SRC,pos):
    if DST == "D":
        if SRC == "D":
            tup = ("D=D",pos,pos)
            self._lines[pos] = tup
        elif SRC == "M":
            tup = ("D=M",pos,pos)
            self._lines[pos] = tup
        elif SRC == "A":
            tup = ("D=A",pos,pos)
            self._lines[pos] = tup    
        elif SRC[0] == "@" and len(SRC)>1:
            tup = (SRC,pos,pos)
            self._lines[pos] = tup
            tup = ("D=M",pos+1,pos+1)
            self._lines.insert(pos+1,tup)
            self.posfix(pos+1,1)
        elif SRC.isdigit():
            tup = ("@"+SRC,pos,pos)
            self._lines[pos] = tup
            tup = ("D=A",pos+1,pos+1)
            self._lines.insert(pos+1,tup)
            self.posfix(pos+1,1)
    elif DST == "M":
        if SRC == "D":
            tup = ("M=D",pos,pos)
            self._lines[pos] = tup
        elif SRC == "M":
            tup = ("M=M",pos,pos)
            self._lines[pos] = tup
        elif SRC == "A":
            tup = ("M=A",pos,pos)
            self._lines[pos] = tup
    elif DST[0] == "@":
        if len(DST)>1:
            if SRC == "M":
                tup = ("D=M",pos,pos)
                self._lines[pos] = tup
                tup = (DST,pos+1,pos+1)
                self._lines.insert(pos+1,tup)
                tup = ("M=D",pos+2,pos+2)
                self._lines.insert(pos+2,tup)
                self.posfix(pos+2,2)
            elif SRC == "D":
                tup = (DST,pos,pos)
                self._lines[pos] = tup
                tup = ("M=D",pos+1,pos+1)
                self._lines.insert(pos+1,tup)
                self.posfix(pos+1,1)
            elif SRC == "A":
                tup = ("D=A",pos,pos)
                self._lines[pos] = tup
                tup = (DST,pos+1,pos+1)
                self._lines.insert(pos+1,tup)
                tup = ("M=D",pos+2,pos+2)
                self._lines.insert(pos+2,tup)
                self.posfix(pos+2,2)
            elif SRC[0]=="@" and len(SRC)>1:
                tup = (SRC,pos,pos)
                self._lines[pos] = tup
                tup = ("D=M",pos+1,pos+1)
                self._lines.insert(pos+1,tup)
                tup = (DST,pos+2,pos+2)
                self._lines.insert(pos+2,tup)
                tup = ("M=D",pos+3,pos+3)
                self._lines.insert(pos+3,tup)
                self.posfix(pos+3,3)
            elif SRC.isdigit():
                tup = ("@"+SRC,pos,pos)
                self._lines[pos] = tup
                tup = ("D=A",pos+1,pos+1)
                self._lines.insert(pos+1,tup)
                tup = (DST,pos+2,pos+2)
                self._lines.insert(pos+2,tup)
                tup = ("M=D",pos+3,pos+3)
                self._lines.insert(pos+3,tup)
                self.posfix(pos+3,3)
def parse_SWP(self,DST, SRC,pos):
    self.lines="$MV(D,"+DST+")"+self.lines
	self.lines="$MV("+DST+","+SRC +")"+self.lines
	self.lines="$MV("+SRC+",D)"+self.lines