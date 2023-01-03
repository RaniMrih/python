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
SinoDurationList=[]
DeltaTimeList=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1159'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.1 Step 1159 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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
     print

#---- split line to array according to  ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#--- find Frame Duration from Tell2.9
def findFrameDuration():
   for line in open(TC_start +"/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Frame Duration', line):
       FrameDuration = line.replace(line[:21], '')
       OnlyDuration = split_string(FrameDuration)
       SinoDurationList.append(OnlyDuration[1])

#---- find Delta time
def findDeltaTime():
   for i in range(0,3):
      for line in open(TC_start + "/ListOut_f"+str(i)+".txt" , "r"):
         line = line.rstrip()
         if re.search(' Delta Time', line):
           line1=split_string2(line)
           DeltaTimeList.append(line1[3])
           

# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "'Frame Duration' of each sinogram file is :" +RESET)
findFrameDuration()
for i in range (0,3):
  print "Frame "+str(i+1)+": "+ str(SinoDurationList[i]) + " msec"

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Delta Time of each list file is :" +RESET)
findDeltaTime()
for i in range (0,3):
  print "Frame "+str(i+1)+": "+ str(DeltaTimeList[i]) + " msec"

#----------- qustion ---------
time.sleep(1)
print
diff=[]
print (BLUE + "Difference of 'Delta Time' in list file and 'Frame "+'\n'+"Duration in sinogram file is :" +RESET)
for i in range (0,3):
  result= int(DeltaTimeList[i]) - int(SinoDurationList[i])
  diff.append(result)
  print "Frame "+str(i+1)+": "+ str(result) + " ms"

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the difference of 'Delta Time' in list file and Frame "+'\n'+"Duration in sinogram file for frame 1 is 30 sceonds "+'\n'+"(+/- 5msec)?" +RESET)
if diff[0] > 30005 or diff[0] < 29995:
  YesNo(False)
else:
  YesNo(True)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is the 'Delta Time' in list file and 'Frame Duration' in "+'\n'+"sinogram file for frame 2 and frame 3 are same  (+/- 5 msec) ?" +RESET)
if int(diff[1]) - int(diff[2]) > 5 or int(diff[1]) - int(diff[2]) < -5:
  YesNo(False)
else:
  YesNo(True)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1159")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1160/Acq4D_1160.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1160/Acq4D_1160.py")

