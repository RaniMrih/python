#!/usr/bin/env python
import os, sys
import time
import re

#VARIABLES
Step_Pass=True
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'
SinoBinDwell=["0","2","4","6"]
SINOAcceptedTriggers=[]
BinsResult=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1242'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.14 Step 1242 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC_2.14 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to  ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#---- count files in directory
def CountFiles(File , Path):
   num=[]
   for item in os.listdir(Path):
      if item.startswith(File):
        num.append(item)
   return len(num)

# ---------------------------------------------------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_14 = line.strip('\n')
  print "Enter Sinograms path directory from" + BLUE + " section 2.14 :" +RESET + SinosDirectory2_14

else:
  #use of raw_input() from user
  SinosDirectory2_14 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.14 :" + RESET)
  # while SinosDirectory2_14 is empty
  while SinosDirectory2_14 == "":
    SinosDirectory2_14 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.14 again:" + RESET)

#like echo to file
f=open("SINOSPath2_14.txt", "w+")
f.write(SinosDirectory2_14)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Scan Completed normally ?" +RESET)
print "[ ] Yes"
print "[ ] No"

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) Number of Sinogram RDFs:" +RESET)
sum1 = CountFiles("SINO00", SinosDirectory2_14 )
print sum1

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Was 10 Sinograms Files created ?" +RESET)
if sum1 == 10:
  YesNo(True)
else:
  YesNo(False)

#-- determine if step Pass/Fail
Step_Result("Acq4D.1242")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1243/Acq4D_1243.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1243/Acq4D_1243.py")








































