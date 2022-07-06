from sys import stdin

def switch(char):
  register={"R0":"000", "R1":"001", "R2": "010", "R3": "011", "R4":"100", "R5":"101", "R6":"110", "R7":"111", "FLAGS":"111"}
  return register.get(char)

def command(char):
  instruction = { 'add' : '00000' , 'sub' : '00001' , 'movI' : '00010' ,
            'mov' : '00011' , 'ld' : '00100' , 'st' : '00101' ,
            'mul' : '00110' , 'div' : '00111' , 'rs' : '01000' ,
            'ls' : '01001' , 'xor' : '01010' , 'or' : '01011' ,
            'and' : '01100' , 'not' : '01101' , 'cmp' : '01110' ,
            'jmp' : '01111' , 'jlt' : '10000' , 'jgt' : '10001' ,
            'je' : '10010' , 'hlt' : '10011' }
  return instruction.get(char)

def immediate(string):
  try:
    gabe=int(string)
    if(gabe>255 or gabe<0):
      return -2
    data=""
    count=0
    while(gabe>0):
      count+=1
      rem=(gabe%2)
      data=str(rem)+data
      gabe=gabe//2
    for i in range(count,8):
      data="0"+data
    return data
  except:
    return -1

def hlt_error(texter, countI):
  assert texter=="hlt", f"Error at line {countI}.Does not end with halt"
  return 0

def checkError(texter, lisreg, lisreg2, lisVar, lislabel,countI):
  if(texter[0]=="add" or texter[0]=="sub" or texter[0]=="xor" or texter[0]=="and" or texter[0]=="mul" or texter[0]=="or"):
    assert len(texter)==4, f"Error at line {countI}.Incorrect register declaration"
    assert texter[3]!="FLAGS" and texter[2]!="FLAGS" and texter[1]!="FLAGS", f"Error at line {countI}.Misuse of flag register"
    b=0
    if (texter[1] in lisreg) and (texter[2] in lisreg) and (texter[3] in lisreg):
      b=1
    assert b==1, f"Error at line {countI}.Incorret register declaration" 
  elif(texter[0]=="div" or texter[0]=="not" or texter[0]=="cmp"):
    assert len(texter)==3, f"Error at line {countI}.Incorrect register declaration"
    assert texter[1]!="FLAGS" and texter[2]!="FLAGS", f"Error at line {countI}.Misuse of flag register"
    b=0
    if (texter[1] in lisreg) and (texter[2] in lisreg):
      b=1
    assert b==1, f"Error at line {countI}.Incorrect register declaration"
  elif(texter[0]=="mov"):
    assert len(texter)==3, f"Error at line {countI}.Incorrect register declaration"
    if "$" in texter[2]:
      assert texter[1]!="FLAGS", f"Error at line {countI}.Misuse of flag register"
      b=0
      if (texter[1] in lisreg):
        b=1
      assert b==1, f"Error at line {countI}.Incorrect register declaration"
      c=immediate(texter[2][1:len(texter[2])])
      assert c!=-1, f"Error at line {countI}.Incorrect immediate declaration"
      assert c!=-2, f"Error at line {countI}.Immediate out of range"
    else:
      assert len(texter)==3, f"Error at line {countI}.Incorrect register declaration"
      assert texter[1]!="FLAGS", f"Error at line {countI}.Misuse of flag register"
      b=0
      if (texter[1] in lisreg) and (texter[2] in lisreg2):
        b=1
      assert b==1, f"Error at line {countI}.Incorrect register declaration"
  elif(texter[0]=="ls" or texter[0]=="rs"):
    assert len(texter)==3, f"Error at line {countI}.Incorrect register declaration"
    assert texter[1]!="FLAGS", f"Error at line {countI}.Misuse of flag register"
    b=0
    if (texter[1] in lisreg):
      b=1
    assert b==1, f"Error at line {countI}.Incorrect register declaration"
    c=immediate(texter[2][1:len(texter[2])])
    assert c!=-1, f"Error at line {countI}.Incorrect immediate declaration"
    assert c!=-2, f"Error at line {countI}.Immediate out of range"
  elif (texter[0]=="ld" or texter[0]=="st"):
    assert len(texter)==3, f"Error at line {countI}.Incorrect register declaration"
    assert texter[1]!="FLAGS", f"Error at line {countI}.Misuse of flag register"
    if(texter[1] in lisreg):
      b=1
    assert b==1, f"Error at line {countI}.Incorrect register declaration"
    c=0
    if(texter[2] in lisVar):
      c=1
    assert c==1, f"Error at line {countI}.Variable not within scope"
  elif (texter[0]=="jmp" or texter[0]=="je" or texter[0]=="jgt" or texter[0]=="jlt"):
    assert len(texter)==2, f"Error at line {countI}.Incorrect register declaration"
    c=0
    if(texter[1] in lislabel):
      c=1
    assert c==1, f"Error at line {countI}.Label not within scope"
  elif(texter[0]=="var"):
    b=0
    assert b==1, f"Error at line {countI}.Variable declared in the middle of the code"
  elif(texter[0][0:len(texter[0])-1] in lislabel):
    b=1
  elif(texter[0]=="hlt"):
    b=0
    assert b==1, f"Error at line {countI}.Hlt function in the middle of the code"
  else:
    b=0
    assert b==1, f"Error at line {countI}.Incorrect instruction declaration"

def printData(texter, lislabel, lisVar, lislabelpos, lisVarpos, i,countInstr):
  data=""
  if(texter[i+0]=="add" or texter[i+0]=="sub" or texter[i+0]=="xor" or texter[i+0]=="and" or texter[i+0]=="mul" or texter[i+0]=="or"):
    data+=str(command(texter[i+0]))+"00"+str(switch(texter[i+1]))+str(switch(texter[i+2]))+str(switch(texter[i+3]))
  elif(texter[i+0]=="div" or texter[i+0]=="not" or texter[i+0]=="cmp"):
    data+=str(command(texter[i+0]))+"00000"+str(switch(texter[i+1]))+str(switch(texter[i+2]))
  elif(texter[i+0]=="ls" or texter[i+0]=="rs"):
    data+=str(command(texter[i+0]))+str(switch(texter[i+1]))+str(immediate(texter[i+2][1:]))
  elif(texter[i+0]=="mov"):
    if("$" in texter[i+2]):
      data+=str(command("movI"))+str(switch(texter[i+1]))+str(immediate(texter[i+2][1:]))
    else:
      data+=str(command(texter[i+0]))+"00000"+str(switch(texter[i+1]))+str(switch(texter[i+2]))
  elif (texter[i+0]=="ld" or texter[i+0]=="st"):
    data+=str(command(texter[i+0]))+str(switch(texter[i+1]))
    tim=0
    for j in range(0,len(lisVar)):
      if lisVar[j]==texter[i+2]:
        tim=lisVarpos[j]+countInstr
    data+=str(immediate(tim))
  elif(texter[i+0]=="jmp" or texter[i+0]=="jgt" or texter[i+0]=="jlt" or texter[i+0]=="je"):
    data+=str(command(texter[i+0]))+"000"
    tim=0
    for j in range(0, len(lislabel)):
      if(lislabel[j]==texter[i+1]):
        tim=lislabelpos[j]
    data+=str(immediate(tim))
  elif(texter[i+0]=="hlt"):
    return (str(command(texter[i+0]))+"00000000000")
  return data

def checkVar(texter):
  if(texter=="var"):
    return 1
  return 0

def checkLabel(texter):
  if ":"==texter[-1]:
    return(len(texter))
  return -1

#f=open("testCaseAss.txt", "r")
texter=stdin.readlines()
t2 = []
for i in texter:
  if(i.strip()!=""):
    t2.append(i)
texter=t2
lisreg=["R0", "R1", "R2", "R3", "R4", "R5", "R6"]
lisreg2=["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]
liscomm=[]
lisVar=[]
lisVarpos=[]
lislabel=[]
lislabelpos=[]
countVar=0
for i in texter:
  j=i.strip()
  liscomm.append([k for k in j.split()])
indexLabel=0
indexVar=0
countInstr=0
countI=0
for i in range(len(liscomm)):
  if(len(liscomm[i])==0):
    countI+=1
    indexVar+=1
    continue
  if(liscomm[i][0][0]!="v"):
    break
  countI+=1
  b=checkVar(liscomm[i][0])
  assert b==1, f"Error at line {countI}.Variable not declared properly"
  assert (len(liscomm[i]))==2, f"Error at line {countI}.Variable not declared properly"
  lisVar.append(liscomm[i][1])
  lisVarpos.append(i-indexVar)
  countVar+=1
for i in range(countVar+indexVar, len(liscomm)):
  if(len(liscomm[i])==0):
    indexLabel+=1
    continue
  countInstr+=1
  b=checkLabel(liscomm[i][0])
  if (b==-1):
    continue
  else:
    lislabel.append(liscomm[i][0][0:b-1])
    lislabelpos.append(i-indexLabel-countVar-indexVar)
for i in range(countVar+indexVar, len(liscomm)):
  countI+=1
  if(len(liscomm[i])==0):
    continue
  if(i==(len(liscomm)-1)):
    a=hlt_error(liscomm[i][-1], countI)
    break
  if liscomm[i][0][-1]==":":
    checkError(liscomm[i][1:], lisreg, lisreg2, lisVar, lislabel,countI)
  else:
    checkError(liscomm[i], lisreg, lisreg2, lisVar, lislabel,countI)
# for i in lislabel:
#   print(i)
for i in range(countVar+indexVar, len(liscomm)):
  if(len(liscomm[i])==0):
    continue
  else:
    #print(liscomm[i])
    if liscomm[i][0][-1]==":":
      print(printData(liscomm[i],  lislabel, lisVar, lislabelpos,lisVarpos, 1,countInstr))
    else:
      print(printData(liscomm[i], lislabel, lisVar, lislabelpos,lisVarpos, 0,countInstr))
#f.close()