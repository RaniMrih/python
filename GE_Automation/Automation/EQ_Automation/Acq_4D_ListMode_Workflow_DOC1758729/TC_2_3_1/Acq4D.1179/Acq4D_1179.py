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
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1179'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.3.1 Step 1179 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.3.1 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

# ------------------------------------ step 1 --------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_3_1 = line.strip('\n')
  print "Enter 30 Sinograms path directory from" + BLUE + " section 2.3.1 :" +RESET + SinosDirectory2_3_1
else:
  #use of raw_input()
  SinosDirectory2_3_1 = raw_input("Enter 30 Sinograms path directory from" + BLUE + " section 2.3.1 :" + RESET)
  # while SinosDirectory2_3_1 is empty
  while SinosDirectory2_3_1 == "":
    SinosDirectory2_3_1 = raw_input("Enter 30 Sinograms path directory from" + BLUE + " section 2.3.1 again:" + RESET)

# like : echo $SinosDirectory2_3_1 > SINOSPath2_3_1.txt
f=open("SINOSPath2_3_1.txt", "w+")
f.write(SinosDirectory2_3_1)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt")

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
sumSinos = CountFiles("SINO00", SinosDirectory2_3_1 )
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
Step_Result("Acq4D.1179")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1180/Acq4D_1180.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1180/Acq4D_1180.py")


