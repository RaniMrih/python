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
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1421'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1448'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.3.2 Step 1421 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
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
   return Arr
#----------- qustion ---------
time.sleep(1)
print
Original = Find_In_Sino_Live("/S2.1Sino.txt" ,"Singles Total Counts" )
Replay = Find_In_Sino("/S2.3.2Sino.txt" ,"Singles Total Counts" )

Live_List=[]
Replay_List=[]
Within_4=True

print (BLUE + "Singles Total Counts"+RESET)
print
for i in range (3):
  time.sleep(1)
  print (BLUE + "Original Scan Frame "+str(i+1)+" :"+RESET)
  Total = split_string2(Original[i])
  print Total[1].replace(" ","")
  Live_List.append(Total[1])
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :"+RESET)
  Total = split_string2(Original[i])
  print Total[1].replace(" ","")
  Replay_List.append(Total[1])
  print (BLUE + "% Difference Frame "+str(i+1)+" :"+RESET)
  diff = (float(Live_List[i]) - float(Replay_List[i])) / float(Live_List[i])
  print str(diff)+ " %"
  if float(diff) > 4.0:
    Within_4=False
  print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is the % Difference between Singles Total Counts for"+'\n'+"each frame of Original and Replay scan <= 4% ?" +RESET)
YesNo(Within_4)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1421")
os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1422/Acq4D_1422.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1422/Acq4D_1422.py")


