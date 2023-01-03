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
SinosNum=[]
ListsNum=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1415'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1448'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.3.2 Step 1415 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- count files in directory
def CountFiles(File , Path):
   num=[]
   if File == "SINO00":
     for item in os.listdir(Path):
        if item.startswith(File):
          num.append(item)
          SinosNum.append(item)
     return len(num)
   elif File == "LIST00":
     for item in os.listdir(Path):
        if item.startswith(File):
          num.append(item)
          ListsNum.append(item)
     return len(num)


f = open( TC_start + "/SINOSPath2_3_2_2.txt" , "r")
for line in f:
  SinosDirectory2_3_2_2 = line.strip('\n')

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Scan Completed normally ?" +RESET)
print "[ ] Yes"
print "[ ] No"

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of Sinogram Files:" +RESET)
sumSinos = CountFiles("SINO00", SinosDirectory2_3_2_2 )
print sumSinos

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is there 30 Sinogram Files for this scan ?" +RESET)
if sumSinos == 30:
  YesNo(True)
else:
  YesNo(False)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1415")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1416/Acq4D_1416.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1416/Acq4D_1416.py")

