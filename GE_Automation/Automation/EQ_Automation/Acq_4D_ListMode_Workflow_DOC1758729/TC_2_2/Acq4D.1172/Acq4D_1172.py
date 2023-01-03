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
LiveSingles=[]
ReplaySingles=[]
LiveSinglesMin=[]
ReplaySinglesMin=[]
LiveSinglesTotal=[]
ReplaySinglesTotal=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1172'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1165'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.2 Step 1172 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  '  '
def split_string4(line):
   list_string=line.split('  ')
   return list_string

#--- find Singles Block Max live and Replay Scan
def find_SinglesBlockMax():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Singles Block Max Counts', line):
       LiveSingles.append(line)
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Singles Block Max Counts', line):
       ReplaySingles.append(line)

#--- find Singles Block Min live and Replay Scan
def find_SinglesBlockMin():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Singles Block Min Counts', line):
       LiveSinglesMin.append(line)
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Singles Block Min Counts', line):
       ReplaySinglesMin.append(line)

#--- find Singles Total live and Replay Scan
def find_SinglesTotal():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Singles Total Counts', line):
       LiveSinglesTotal.append(line)
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Singles Total Counts', line):
       ReplaySinglesTotal.append(line)


# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "1) Module and Block for Singles with Max Counts"+'\n' +RESET)
find_SinglesBlockMax()
for i in range (0,3):
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  print LiveSingles[i].replace(LiveSingles[i][:39],"")
time.sleep(1)
print
for i in range (0,3):
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  print ReplaySingles[i].replace(ReplaySingles[i][:39],"")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Singles with Max Counts for each frame of "+'\n'+"Original & Replay occurs in the same Module and Block ?" +RESET)
Same=True
for i in range (0,3):
  if str(LiveSingles[i]) != str(ReplaySingles[i]):
    Same=False
YesNo(Same)
#----------- qustion ---------
print (BLUE + "Block Singles with Max Counts :" +RESET)
Within0_01=True
for i in range (0,3):
  time.sleep(1)
  print
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  Max1 = LiveSingles[i][:-35]
  print Max1.replace(Max1[:3],"")
  Max1 = split_string2(Max1)
  Max1= Max1[1]
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  Max2 = ReplaySingles[i][:-35]
  print Max2.replace(Max2[:3],"")
  Max2 = split_string2(Max2)
  Max2= Max2[1]
  print (BLUE + "% Difference Frame "+str(i+1)+" :" +RESET)
  diff = int(Max1)- int(Max2)
  if diff < 0:
    diff*=-1
  if diff > 0.01 :
     Within0_01=False
  print diff

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the % Difference between the Singles with Max "+'\n'+"Counts for each frame of Original and Replay scan <= 0.01% ?" +RESET)
YesNo(Within0_01)

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Module and Block for Singles with Min Counts"+'\n' +RESET)
find_SinglesBlockMin()
for i in range (0,3):
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  print LiveSinglesMin[i].replace(LiveSinglesMin[i][:39],"")
time.sleep(1)
print
for i in range (0,3):
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  print ReplaySinglesMin[i].replace(ReplaySinglesMin[i][:39],"")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Singles with Min Counts for each frame of "+'\n'+"Original & Replay occurs in the same Module and Block ?" +RESET)
Same=True
for i in range (0,3):
  if str(LiveSinglesMin[i]) != str(ReplaySinglesMin[i]):
    Same=False
YesNo(Same)
#----------- qustion ---------
print (BLUE + "Block Singles with Min Counts :" +RESET)
Within0_01=True
for i in range (0,3):
  time.sleep(1)
  print
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  Max1 = LiveSinglesMin[i][:-35]
  print Max1.replace(Max1[:3],"")
  Max1 = split_string2(Max1)
  Max1= Max1[1]
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  Max2 = ReplaySinglesMin[i][:-35]
  print Max2.replace(Max2[:3],"")
  Max2 = split_string2(Max2)
  Max2= Max2[1]
  print (BLUE + "% Difference Frame "+str(i+1)+" :" +RESET)
  diff = int(Max1)- int(Max2)
  if diff < 0:
    diff*=-1
  if diff > 0.01 :
     Within0_01=False
  print diff

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the % Difference between the Singles with Min "+'\n'+"Counts for each frame of Original and Replay scan <= 0.01% ?" +RESET)
YesNo(Within0_01)
# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) Singles Total Counts" +RESET)
find_SinglesTotal()
Within0_01=True
for i in range (0,3):
  time.sleep(1)
  print
  print (BLUE + "Original Scan Frame "+str(i+1)+" :" +RESET)
  Max1 = LiveSinglesTotal[i]
  print Max1.replace(Max1[:3],"")
  Max1 = split_string2(Max1)
  Max1= Max1[1]
  print (BLUE + "Replay Scan Frame "+str(i+1)+" :" +RESET)
  Max2 = ReplaySinglesTotal[i]
  print Max2.replace(Max2[:3],"")
  Max2 = split_string2(Max2)
  Max2= Max2[1]
  print (BLUE + "% Difference Frame "+str(i+1)+" :" +RESET)
  diff = int(Max1)- int(Max2)
  if diff < 0:
    diff*=-1
  if diff > 0.01 :
     Within0_01=False
  print diff

  #----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the % Difference between the Singles with Total "+'\n'+"Counts for each frame of Original and Replay scan <= 0.01% ?" +RESET)
YesNo(Within0_01)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1172")
os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1175/Acq4D_1175.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1175/Acq4D_1175.py")



















