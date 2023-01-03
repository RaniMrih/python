#!/usr/bin/env python
import os, sys
import time
import re
#VARIABLES
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'
Step_Pass=True
TotalPromptsReplay_List=[]
FrameDurationReplay_List=[]
Dwell_List=[]
SumSegment_List=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1420'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1448'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.3.1 Step 1420 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
time.sleep(1)
#------------------------------------- Functions -------------------------------------
def YesNo(YN):
   if YN == True:
     print (GREEN + "[X] Yes" + RESET)
     print ("[ ] No")
   else:
     print ("[ ] Yes")
     print (RED +"[X] No" + RESET)
     global Step_Pass
     Step_Pass=False
   print

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)

#---- split line to array according to  ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#---- split line to array according to  ':'
def split_string4(line):
   list_string=line.split('=')
   return list_string

#--- Multi params find function in Sino
def Find_In_Sino (File,Param):
   Arr=[]
   for line in open(TC_start + File, "r"):
      line = line.rstrip()
      if re.search( Param , line):
        Arr.append(line)
   return Arr
#--- Multi params find function in Sino Live
def Find_In_Sino_Live(File,Param):
   Arr=[]
   for line in open(TC_start_2_1 + File, "r"):
      line = line.rstrip()
      if re.search( Param , line):
        Arr.append(line)
#----------------- Dwells sum
def BinDwellSum():
   sum=0
   for line in open(TC_start + "/S2.3.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('dwell', line):
       Dwell=split_string4(line)
       Dwell_List.append(Dwell[1])
#-------------sum all bins segment for 30 SINOS
def SumSegment():
   sum1=0
   sum2=0
   sum3=0
   for i in range (30):
     if i < 10:
       for line in open(TC_start + "/Tell2.3.2.SINO000"+str(i), "r"):
         line = line.rstrip()
         if re.search('DS 0 Total Counts:', line):
           SumSegment_List.append(line)
     if i >10 and i <20:
       for line in open(TC_start + "/Tell2.3.2.SINO00"+str(i), "r"):
         line = line.rstrip()
         if re.search('DS 0 Total Counts:', line):
           SumSegment_List.append(line)
     if i > 19:
       for line in open(TC_start + "/Tell2.3.2.SINO00"+str(i), "r"):
         line = line.rstrip()
         if re.search('DS 0 Total Counts:', line):
           SumSegment_List.append(line)
# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Gated Replay Total Prompts: "+RESET)
TotalPromptsReplay = Find_In_Sino("/S2.3.2Sino.txt" , "statsData.totalPrompts:")
for i in range (3):
  result = split_string2(TotalPromptsReplay[i])
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(result[1].replace(" ", ""))
  TotalPromptsReplay_List.append(result[1].replace(" ", ""))
#----------- qustion ---------
# find Replay Duration
time.sleep(1)
print
print (BLUE + "Gated Replay 'Frame Duration' "+RESET)
FrameDurationReplay = Find_In_Sino("/S2.3.2Sino.txt" , "Frame Duration")
for i in range (3):
  result = split_string4(FrameDurationReplay[i])
  result1 = split_string(result[1])
  result1 = result1[1].replace(" ", "")
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(result1)
  FrameDurationReplay_List.append(result1)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Sum of Bin Dwell Times : "+RESET)
BinDwellSum()

sumBinDwell1=0
sumBinDwell2=0
sumBinDwell3=0
for i in range (30):
  if i < 10:
    sumBinDwell1+=int(Dwell_List[i])
  if i > 9 and i <20:
    sumBinDwell2+=int(Dwell_List[i])
  if i > 19:
    sumBinDwell3+=int(Dwell_List[i])


print BLUE+"Bed 1 : "+RESET+'\n'+ str(sumBinDwell1) + " ms"
print BLUE+"Bed 2 : "+RESET+'\n'+ str(sumBinDwell2) + " ms"
print BLUE+"Bed 3 : "+RESET+'\n'+ str(sumBinDwell3) + " ms"
# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
# grep sinos  path
f = open( TC_start +"/SINOSPath2_3_2_2.txt" , "r")
for line in f:
  SinosDirectory2_3_2 = line.strip('\n')
print
print "Creating Tell2.3.2.SINO0000 - SINO0029, Please Wait..."
os.system("rdfTeller -r '-h f -S' -f Tell2.3.2 "+SinosDirectory2_3_2+"/SINO*")
# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) Sum Segment 2 bin counts "+RESET)
SumSegment()
sumSegment1=0
sumSegment2=0
sumSegment3=0
for i in range (29):
  if i < 10:
    result=split_string2(SumSegment_List[i])
    sumSegment1 +=int(result[1])
  if i > 9 and i <20:
    result=split_string2(SumSegment_List[i])
    sumSegment2 +=int(result[1])
  if i > 19:
    result=split_string2(SumSegment_List[i])
    sumSegment3 +=int(result[1])

print BLUE+"Bed 1 : "+RESET+'\n'+ str(sumSegment1)
print BLUE+"Bed 2 : "+RESET+'\n'+ str(sumSegment2)
print BLUE+"Bed 3 : "+RESET+'\n'+ str(sumSegment3)
# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
Ratio1=[]
Ratio2=[]
print (BLUE + "3) Ratio of sum bin counts to total prompts: "+RESET)
#The sum bin counts to total prompts Ratios
result1 = float(sumSegment1) / float(TotalPromptsReplay_List[0])
result2 = float(sumSegment2) / float(TotalPromptsReplay_List[1])
result3 = float(sumSegment3) / float(TotalPromptsReplay_List[2])
Ratio1.append(result1)
Ratio1.append(result2)
Ratio1.append(result3)
print BLUE+"Bed 1 : "+RESET+'\n'+ str(result1) + " %"
print BLUE+"Bed 2 : "+RESET+'\n'+ str(result2) + " %"
print BLUE+"Bed 3 : "+RESET+'\n'+ str(result3) + " %"

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Ratio of sum bin dwell to frame duration: "+RESET)
#The sum bin dwell to frame duration Ratios

result1 = float(sumBinDwell1) / float(FrameDurationReplay_List[0])
result2 = float(sumBinDwell2) / float(FrameDurationReplay_List[1])
result3 = float(sumBinDwell3) / float(FrameDurationReplay_List[2])
Ratio2.append(result1)
Ratio2.append(result2)
Ratio2.append(result3)
print BLUE+"Bed 1 : "+RESET+'\n'+ str(result1) + " %"
print BLUE+"Bed 2 : "+RESET+'\n'+ str(result2) + " %"
print BLUE+"Bed 3 : "+RESET+'\n'+ str(result3) + " %"

#----------- qustion ---------
time.sleep(1)
print
within_1=True
print (BLUE + "% difference between ratios "+RESET)
for i in range (3):
  result = float(Ratio1[i]) - float(Ratio2[i])
  if float(result) < 1.0:
    result*=-1
  if float(result) > 1.0:
    within_1=False
  print BLUE+"Bed 1 : "+RESET+'\n'+ str(result) + " %"
# ------------------------------------ step 4 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "4) For all bed locations, the difference between"+'\n'+"the ratios is within 1% ?"+RESET)
YesNo(within_1)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1420")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1421/Acq4D_1421.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1421/Acq4D_1421.py")


