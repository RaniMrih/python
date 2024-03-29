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
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1180'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1179'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.3.1 Step 1180 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

# grep sinos  path
f = open( TC_start +"/SINOSPath2_3_1.txt" , "r")
for line in f:
  SinosDirectory2_3_1 = line.strip('\n')

print "Creating S2.3.1Sino.txt file, Please wait... "
os.system("rdfTeller -r '-h efadgS -v -S' "+SinosDirectory2_3_1+"/SINO0000* > S2.3.1Sino.txt")
os.system("rdfTeller -r '-h efadgS -v -S' "+SinosDirectory2_3_1+"/SINO0010* >> S2.3.1Sino.txt")
os.system("rdfTeller -r '-h efadgS -v -S' "+SinosDirectory2_3_1+"/SINO0020* >> S2.3.1Sino.txt")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the S2.3.1Sino.txt file produced ?" +RESET)
if os.path.exists(TC_start +'/S2.3.1Sino.txt'):
  YesNo(True)
else:
  YesNo(False)
  
#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1180")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1181/Acq4D_1181.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1181/Acq4D_1181.py")

