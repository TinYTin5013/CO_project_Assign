from sys import stdin
opcodes = {"10000": "RRR", "10001": "RRR", "10010": "RI", "10011": "RR", "10100": "RM", "10101": "RM", "10110": "RRR",
           "10111": "RR", "11000": "RI", "11001": "RI", "11010": "RRR", "11011": "RRR", "11100": "RRR", "11101": "RR",
           "11110":"RR","11111":"M","01100":"M","01101":"M","01111":"M","01010":"H"}
registers = {"R0":"0"*16,"R1":"0"*16,"R2":"0"*16,"R3":"0"*16,"R4":"0"*16,"R5":"0"*16,"R6":"0"*16,"FLAGS":"0"*16}

def binaryToDec(s):
    n =0
    for i in range(len(s)-1,-1,-1):
        n = n + (2**(len(s)-i-1) if s[i] == "1" else 0)
    return n
def DecToBin(n,m=16):
    L = []
    while(n!=0):
        L.append(str(n%2))
        n =n//2
    L.reverse()
    return (("0"*(m-len(L))+"".join(L))[-m:])
def getReg(s):
    temp = registers.get("R"+str(binaryToDec(s)))
    if(temp!=None):
        return "R"+str(binaryToDec(s))
    else:
        return "FLAGS"
def printRegisters(prog):
    return (DecToBin(prog,8)+" "+registers["R0"]+" "+registers["R1"]+" "+registers["R2"]+" "+registers["R3"]+" "+registers["R4"]+" "+registers["R5"]+" "+registers["R6"]+" "+registers["FLAGS"])

#f = open("AssemblerOutput.txt","r")
instructions = []
for line in stdin:
    if line.strip()!="":
        instructions.append(line.strip())
#instructions = f.readlines()
#instructions = [i.strip() for i in instructions]
#f.close()
memory = [i.strip() for i in instructions]
memory = memory + ["0"*16 for i in range(len(instructions),256)]


pc = 0
file1=open("output.txt","w")
while(opcodes.get(instructions[pc][:5])!="H"):
    tpc = pc
    #print(pc)
    f=0
    #print(instructions[pc])
    tinst = instructions[pc][:5]
    #print("NEW INSTRUCTION, type = "+opcodes[tinst])
    if(opcodes.get(tinst)=="RRR"):
        r2 = getReg(instructions[pc][7:10])
        r3 = getReg(instructions[pc][10:13])
        r1 = getReg(instructions[pc][13:16])
        if(tinst=="10000"):
            s = binaryToDec(registers[r2])+binaryToDec(registers[r3])

            if(s>=2**16):
                registers["FLAGS"] = registers["FLAGS"][:-4]+"1"+registers["FLAGS"][-3:]
                #print("OVERFLOW ERROR Program counter address = "+str(pc))
                f=2
            registers[r1]= DecToBin(s)
            #print(r1 + "= " + r2 + " + " + r3 + " = " + registers[r1])
        elif (tinst == "10001"):
            s = binaryToDec(registers[r2]) - binaryToDec(registers[r3])
            if (s <0):
                registers["FLAGS"] = registers["FLAGS"][:-4] + "1" + registers["FLAGS"][-3:]
                #print("OVERFLOW ERROR\n Program counter address = " + str(pc))
                f=2
                s=0
            registers[r1] = DecToBin(s)
        elif(tinst =="10110"):
            s = binaryToDec(registers[r2]) * binaryToDec(registers[r3])
            if (s >= 2 ** 16):
                registers["FLAGS"] = registers["FLAGS"][:-4] + "1" + registers["FLAGS"][-3:]
                #print("OVERFLOW ERROR\n Program counter address = " + str(pc))
                f=2
            registers[r1] = DecToBin(s)
        elif (tinst == "11010"):
            s = binaryToDec(registers[r2]) ^ binaryToDec(registers[r3])
            registers[r1] = DecToBin(s)
        elif (tinst == "11011"):
            s = binaryToDec(registers[r2]) | binaryToDec(registers[r3])
            registers[r1] = DecToBin(s)
        elif (tinst == "11100"):
            s = binaryToDec(registers[r2]) & binaryToDec(registers[r3])
            registers[r1] = DecToBin(s)
    elif(opcodes.get(tinst)=="RR"):
        r1 = getReg(instructions[pc][10:13])
        r2 = getReg(instructions[pc][13:16])
        if(tinst=="10011"):
            registers[r2] =registers[r1]
        elif(tinst=="10111"):
            #try:
                n1 = binaryToDec(registers[r1])
                n2 = binaryToDec(registers[r2])
                registers["R0"] = DecToBin(n1 // n2)
                registers["R1"] = DecToBin(n1 % n2)
            #except:
                #print("ZERO Division error in register "+r2+" PC = "+str(pc))
        elif(tinst =="11101"):
            registers[r2] = "".join([chr(ord("0")+(ord("1")-ord(i))) for i in registers[r1]])
        elif(tinst == "11110"):
            f=1
            n1 = binaryToDec((registers[r1]))
            n2 = binaryToDec((registers[r2]))
            if(n1>n2):
                registers["FLAGS"] = registers["FLAGS"][:-3] + "010"
            elif(n1==n2):
                registers["FLAGS"] = registers["FLAGS"][:-3] + "001"
            elif(n1<n2):
                registers["FLAGS"] = registers["FLAGS"][:-3] + "100"
    elif(opcodes.get(tinst)=="RI"):
        r1 = getReg(instructions[pc][5:8])
        I = binaryToDec(instructions[pc][8:16])
        if(tinst=="10010"):
            registers[r1]= DecToBin(I)
            #print("Set "+r1 +" to "+registers[r1])
        elif(tinst=="11000"):
            registers[r1] = "0"*(min(16,I))+registers[r1][:-I]
        elif(tinst=="11001"):
            registers[r1] = registers[r1][I:]+"0"*min(16,I)
    elif(opcodes.get(tinst)=="RM"):
        r1 = getReg(instructions[pc][5:8])
        mem = instructions[pc][8:16]
        if(tinst=="10100"):
            registers[r1] = memory[binaryToDec(mem)]
            #print("Loaded "+ mem + "= "+ memory[binaryToDec(mem)] +" into "+r1)
        if(tinst=="10101"):
            memory[binaryToDec(mem)]=registers[r1]
            #print("Stored "+ r1+"= "+registers[r1]  +"into "+ mem + "= " + memory[binaryToDec(mem)])
    elif(opcodes.get(tinst)=="M"):
        mem = instructions[pc][8:16]
        if(tinst=="11111"):
            pc = binaryToDec(mem)-1
        elif(tinst=="01100"):
            if(registers["FLAGS"][-3]=="1"):
                pc = binaryToDec(mem)-1
        elif(tinst=="01111"):
            if (registers["FLAGS"][-1] == "1"):
                pc = binaryToDec(mem)-1
        elif(tinst=="01101"):
            if (registers["FLAGS"][-2] == "1"):
                pc = binaryToDec(mem)-1
    if (f == 0):
        registers["FLAGS"] = "0" * 16
    elif(f!=1):
        registers["FLAGS"] = registers["FLAGS"][:-4] + "1" + registers["FLAGS"][-3:]
    pc = pc + 1
    #file1.write(printRegisters(tpc)+"\n")
    print(printRegisters(tpc))
registers["FLAGS"]= "0"*16
#file1.write(printRegisters(pc)+"\n")
print(printRegisters(pc))
#file1.write("\n".join(memory)+"\n")
print("\n".join(memory))
#file1.close()
