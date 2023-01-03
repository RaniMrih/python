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
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1155'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.1 Step 1155 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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
#---------------------------------------------------------------------------------------

# grep sinos  path
f = open( TC_start +"/SINOSPath2_1.txt" , "r")
for line in f:
  SinosDirectory = line.strip('\n')

# grep lists path
f = open( TC_start +"/LISTSPath2_1.txt" , "r")
for line in f:
  ListsDirectory = line.strip('\n')

time.sleep(1)
print "Creating S2.1Sino.txt file ..."
os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SinosDirectory+"/SINO* > S2.1Sino.txt")
print "Creating S2.1SinoHdrs.txt file ..."
os.system("rdfTeller -r '-h eag -Ha -v' "+SinosDirectory+"/SINO* > S2.1SinoHdrs.txt")
print "Creating S2.1ListHdrs.txt file ..."
os.system("rdfTeller -r '-h eag -Ha -v' "+ListsDirectory+"/LIST* > S2.1ListHdrs.txt")

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the S2.1Sino.txt, S2.1SinoHdrs.txt &"+'\n'+"S2.1ListHdrs.txt files were produced ?" +RESET)
if os.path.exists(TC_start +'/S2.1Sino.txt') and os.path.exists(TC_start +'/S2.1ListHdrs.txt'):
  YesNo(True)
else:
  YesNo(False)
  
#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1155")
os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1156/Acq4D_1156.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1156/Acq4D_1156.py")

