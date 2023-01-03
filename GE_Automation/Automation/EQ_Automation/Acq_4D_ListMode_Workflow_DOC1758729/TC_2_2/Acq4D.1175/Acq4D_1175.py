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
LiveBusyMax=[]
ReplayBusyMax=[]
LiveBusyMin=[]
ReplayBusyMin=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1175'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1165'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.2 Step 1175 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print
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
     print (RED + "                                                      ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#---- split line to array according to  ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string


#--- find Block Busy Max
def find_BlockBusyMax():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Block Busy Max', line):
       LiveBusyMax.append(line)
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Block Busy Max', line):
       ReplayBusyMax.append(line)

#--- find Block Busy Min
def find_BlockBusyMin():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Block Busy Min', line):
       LiveBusyMin.append(line)
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Block Busy Min', line):
       ReplayBusyMin.append(line)

# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Block Busy Max "+'\n' +RESET)
find_BlockBusyMax()
for i in range (0,3):
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  print LiveBusyMax[i].replace(LiveBusyMax[i][:29],"")
time.sleep(1)
print
for i in range (0,3):
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  print ReplayBusyMax[i].replace(ReplayBusyMax[i][:29],"")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is 'Block Busy Max' for each frame of Original &"+'\n'+"replay scan occurs in the same Module and Block ?" +RESET)
Same=True
for i in range (0,3):
  if str(LiveBusyMax[i]) != str(ReplayBusyMax[i]):
    Same=False
YesNo(Same)
#----------- qustion ---------
print (BLUE + "Original Scan :" +RESET)
print
Max_Live_List=[]
Max_Replay_List=[]

Within0_02=True
for i in range (0,3):
  time.sleep(1)
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  Max1 = LiveBusyMax[i][:-35]
  print Max1.replace(Max1[:3],"")
  Max1 = split_string2(Max1)
  Max_Live_List.append(Max1[1])

print
print (BLUE + "Replay Scan :" +RESET)
print
for i in range (0,3):
  time.sleep(1)
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  Max2 = ReplayBusyMax[i][:-35]
  print Max2.replace(Max2[:3],"")
  Max2 = split_string2(Max2)
  Max_Replay_List.append(Max2[1])
print

for i in range (0,3):
  print (BLUE + "% Difference Frame "+str(i+1)+" :" +RESET)
  diff = float(Max_Live_List[i])- float(Max_Replay_List[i])
  if diff < 0:
    diff*=-1
  if diff > 0.02:
    Within0_02=False
  print float(diff)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the Difference between each frame of Original"+'\n'+"and Replay scan for 'Block Busy Max' <=  0.002 ?" +RESET)
YesNo(Within0_02)

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Block Busy Min "+'\n' +RESET)
find_BlockBusyMin()
for i in range (0,3):
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  print LiveBusyMin[i].replace(LiveBusyMin[i][:29],"")
time.sleep(1)
print
for i in range (0,3):
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  print ReplayBusyMin[i].replace(ReplayBusyMin[i][:29],"")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is 'Block Busy Min' for each frame of Original &"+'\n'+"replay scan occurs in the same Module and Block ?" +RESET)
Same=True
for i in range (0,3):
  if str(LiveBusyMin[i]) != str(ReplayBusyMin[i]):
    Same=False
YesNo(Same)
#----------- qustion ---------
print (BLUE + "Original Scan :" +RESET)
print
Min_Live_List=[]
Min_Replay_List=[]

Within0_02=True
for i in range (0,3):
  time.sleep(1)
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  Min1 = LiveBusyMin[i][:-35]
  print Min1.replace(Min1[:3],"")
  Min1 = split_string2(Min1)
  Min_Live_List.append(Min1[1])

print
print (BLUE + "Replay Scan :" +RESET)
print
for i in range (0,3):
  time.sleep(1)
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  Min2 = ReplayBusyMin[i][:-35]
  print Min2.replace(Min2[:3],"")
  Min2 = split_string2(Min2)
  Min_Replay_List.append(Min2[1])
print

for i in range (0,3):
  print (BLUE + "% Difference Frame "+str(i+1)+" :" +RESET)
  diff = float(Min_Live_List[i])- float(Min_Replay_List[i])
  if diff < 0:
    diff*=-1
  if diff > 0.02 :
    Within0_02=False
  print float(diff)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the Difference between each frame of Original"+'\n'+"and Replay scan for 'Block Busy Min' <=  0.002 ?" +RESET)
YesNo(Within0_02)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1175")
print (GREEN +"                                                    ---- END of TC 2.2 Columbia DMI ----" +RESET)

#--------END TC2.2





