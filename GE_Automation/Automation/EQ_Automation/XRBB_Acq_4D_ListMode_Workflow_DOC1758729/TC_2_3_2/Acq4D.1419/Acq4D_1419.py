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
TotalPromptsReplay_List=[]
TotalPromptsLive_List=[]
FrameDurationReplay_List=[]
FrameDurationLive_List=[]
Extrapolated_List=[]
Dwell_List=[]
SINOAcceptedTriggers=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1419'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1448'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.3.2 Step 1419 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

def Find_In_Sino_Live(File,Param):
   Arr=[]
   for line in open(TC_start_2_1 + File, "r"):
      line = line.rstrip()
      if re.search( Param , line):
        Arr.append(line)
   return Arr

#----------------- Dwells sum
def BinDwellSum():
   sum=0
   for line in open(TC_start + "/S2.3.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('dwell', line):
       Dwell=split_string4(line)
       Dwell_List.append(Dwell[1])

#---- find accepted triggers 
def findAcceptedTriggers ():
   for line in open(TC_start + "/S2.3.2Sino.txt", "r"):
      line = line.rstrip()
      if re.search('acceptedTriggers:', line):
        line1=split_string2(line)
        SINOAcceptedTriggers.append(line1[1])

# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Gated Replay :" +RESET)
print (BLUE + "a) Total Prompts (totalPrompts): "+RESET)
TotalPromptsReplay = Find_In_Sino("/S2.3.2Sino.txt" , "statsData.totalPrompts:")
for i in range (3):
  result = split_string2(TotalPromptsReplay[i])
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(result[1].replace(" ", ""))
  TotalPromptsReplay_List.append(result[1].replace(" ", ""))

#----------- qustion ---------
TotalPromptsLive = Find_In_Sino_Live("/S2.1Sino.txt" , "statsData.totalPrompts:")
for i in range (3):
  result = split_string2(TotalPromptsLive[i])
  TotalPromptsLive_List.append(result[1].replace(" ", ""))

#----------- qustion ---------
# find Replay Duration
time.sleep(1)
print
print (BLUE + "b) Gated Replay 'Frame Duration' "+RESET)
FrameDurationReplay = Find_In_Sino("/S2.3.2Sino.txt" , "Frame Duration")
for i in range (3):
  result = split_string4(FrameDurationReplay[i])
  result1 = split_string(result[1])
  result1 = result1[1].replace(" ", "")
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(result1)
  FrameDurationReplay_List.append(result1)

# find Live Duration
FrameDurationLive = Find_In_Sino_Live("/S2.1Sino.txt" , "Frame Duration")
for i in range (3):
  result = split_string4(FrameDurationLive[i])
  result1 = split_string(result[1])
  result1 = result1[1].replace(" ", "")
  FrameDurationLive_List.append(result1)

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
# Extrapolated Prompts = (Replay Duration / Original Duration) * Original Prompts.
time.sleep(1)
print
print (BLUE + "2) Gated Extrapolated Prompts "+RESET)
for i in range (0,3):
  Extrapolated= (float(FrameDurationReplay_List[i]) / float(FrameDurationLive_List[i])) * float(TotalPromptsLive_List[i])
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(Extrapolated)
  Extrapolated_List.append(Extrapolated)

# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
#Prompts Percent Difference = (ABS( Extrapolated Prompts - actual Replay Prompts ) / Extrapolated Prompts) * 100.0
time.sleep(1)
print
print (BLUE + "3) Actual vs extrapolated Prompts Percent Difference :"+RESET)
for i in range (0,3):
   sum= (float(Extrapolated_List[i]) - float(TotalPromptsReplay_List[i])) / float(Extrapolated_List[i])
   if sum < 0:
     sum*=-1
   sum*=100
   print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(sum) + " %"

#----------- qustion ---------
# Extrapolated Prompts = (Replay Duration / Original Duration) * Original Prompts.
time.sleep(1)
print
print (BLUE + "For all bed locations, the Total Prompts in the "+'\n'+"Replay are within 0.5% of the of the Extrapolated Prompts ?"+RESET)
Within0_5=True
for i in range (0,3):
  sum = float(Extrapolated_List[i]) + (0.5 * float(Extrapolated_List[i]))
  if float(TotalPromptsReplay_List[i]) > sum:
    Within0_5=False
YesNo(Within0_5)
# ------------------------------------ step 4 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "4) Sum of Bin Dwell Times : "+RESET)
BinDwellSum()
List1=[]
List2=[]
List3=[]
sum1=0
sum2=0
sum3=0
for i in range (30):
  if i < 10:
    sum1 +=int(Dwell_List[i])
    List1.append(Dwell_List[i])
  if i > 9 and i <20:
    sum2 +=int(Dwell_List[i])
    List2.append(Dwell_List[i])
  if i > 19:
    sum3+=int(Dwell_List[i])
    List3.append(Dwell_List[i])

print BLUE+"Bed 1 : "+RESET+'\n'+ str(sum1) + " ms"
print BLUE+"Bed 2 : "+RESET+'\n'+ str(sum2) + " ms"
print BLUE+"Bed 3 : "+RESET+'\n'+ str(sum3) + " ms"

# ------------------------------------ step 5 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "5) Bin Dwell: "+RESET)
MaxDwell1 = max(List1)
MinDwell1 = min(List1)
diff1 = int(MaxDwell1)-int(MinDwell1)
MaxDwell2 = max(List2)
MinDwell2 = min(List2)
diff2 = int(MaxDwell2)-int(MinDwell2)
MaxDwell3 = max(List3)
MinDwell3 = min(List3)
diff3 = int(MaxDwell3)-int(MinDwell3)

print "        Max   |  Min  |  Diff  "
print "----------------------------------"
print "Bed 1: "+str(MaxDwell1)+"    "+str(MinDwell1)+"     "+str(diff1)
print "Bed 2: "+str(MaxDwell2)+"    "+str(MinDwell2)+"     "+str(diff2)
print "Bed 3: "+str(MaxDwell3)+"    "+str(MinDwell3)+"     "+str(diff3)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "For all bed locations, the sum of the bin dwell time should "+RESET)
print (BLUE + "be within 1500ms of the Gated Replay Frame duration ? "+RESET)
if int(sum1) > int(FrameDurationReplay_List[0]) + 1500 or int(sum2) > int(FrameDurationReplay_List[1]) + 1500 or int(sum3) > int(FrameDurationReplay_List[2]) + 1500:
  YesNo(False)
else:
  YesNo(True)
  #----------- qustion ---------
time.sleep(1)
print (BLUE + "For all bed locations, the Max bin dwell - Min bin"+RESET)
print (BLUE + "dwell < = (2*Numberof accepted triggers) ?"+RESET)
findAcceptedTriggers()
if int(diff1) > 2 * int(SINOAcceptedTriggers[0]) or int(diff2) > 2 * int(SINOAcceptedTriggers[1]) or int(diff3) > 2 * int(SINOAcceptedTriggers[2]):
  YesNo(False)
else:
  YesNo(True)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1419")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1420/Acq4D_1420.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1420/Acq4D_1420.py")


