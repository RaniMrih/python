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
sinosList2_7 = ["00"]
LiveTotal=[]
ReplayTotal=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1211'
SinoPath2_7 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1209/SINOSPath2_7.txt'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/LISTSPath2_4.txt'
Step_Pass=True

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.7 Step 1211 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ','
def split_string(line):
   list_string=line.split(',')
   return list_string

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string

#--- find Total Prompts Replay Scan
def ReplayTotalPrompts():
   for i in sinosList2_7:
     for line in open("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1209/Tell2.7", "r"):
       line = line.rstrip()
       if re.search('   totalPrompts     =', line):
         ReplayPrompts = line.replace(line[:21], '')
         print "Total Prompts:"+ str(ReplayPrompts)
         ReplayTotal.append(ReplayPrompts)

#--- find Total Prompts in live Scan listfile
def ListFileTotalPrompts():
   for i in sinosList2_7:
     for line in open("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/ListLoss2.4.txt", "r"):
       line = line.rstrip()
       if re.search('Total Prompt', line):
         LivePrompts = line.replace(line[:14], '')
         print "Total Prompts:" + str(LivePrompts)
         LiveTotal.append(LivePrompts)

#--- find differences between Replay Scan and listfile
def DiffListReplay():
   within_1=True
   for i in range (0,1):
     sum = int(LiveTotal[i]) - int(ReplayTotal[i])
     if sum < 0:
       sum*=-1
     if sum > 0.01 * float(LiveTotal[i]):
       within_1 = False
   YesNo(within_1)

  
# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Replay to static Total Prompts :" +RESET)
ReplayTotalPrompts()

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) List File Total Prompts :" +RESET)
ListFileTotalPrompts()

# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "3) Difference :" +RESET)
sum = int(LiveTotal[0]) - int(ReplayTotal[0])
if sum < 0:
  sum*=-1

print sum
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The % Difference between the list file"+'\n'+"total prompts and the static replay total" +RESET)
print (BLUE + "prompts is less than 1% ?" +RESET)
DiffListReplay()

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1211")
print (GREEN +"                                                      ---- END of TC 2.7 Columbia DMI ----" +RESET)



#----------- END TC.2.7
