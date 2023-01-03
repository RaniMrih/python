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
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_11/Acq4D.1385'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_11/Acq4D.1228'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.11 Step 1385 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- find accepted triggers from Tell2.10
def findAcceptedTriggers ():
   for line in open(TC_start + "/Tell2.11.SINO0000", "r"):
      line = line.rstrip()
      if re.search('acceptedTriggers:', line):
        line1=split_string(line)
        print line1[1]
        SINOAcceptedTriggers.append(line1[1])

def findBinDwill():
   for i in SinoBinDwell:
     for line in open(TC_start + "/Tell2.11.SINO0000", "r"):
       line = line.rstrip()
       if re.search('   bin '+i+' dwell', line):
         print line.replace(line[:3],'')
         line1=split_string(line)
         BinsResult.append(line1[7])

#------------------------------------- step 1 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "1) Accepted Triggers: " + RESET)
findAcceptedTriggers ()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Accepted Triggers are 120 or 121 ?" + RESET)
if str(SINOAcceptedTriggers[0]) == 120 or str(SINOAcceptedTriggers[0]) == 121:
  YesNo(True)
else:
  YesNo(False)

#------------------------------------- step 2 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "2) Measured Dwell Times:" + RESET)
findBinDwill()

#----------- qustions ---------
print
j=0
for i in SinoBinDwell:
   time.sleep(1)
   print (BLUE + "Is the 15100 >= bin" +i+ " dwell >= 14900?" + RESET)
   if BinsResult[j] > 15100 or  BinsResult[j] < 14900 :
     YesNo(False)
   else :
     YesNo(True)
   j+=1

#-- determine if step Pass/Fail
Step_Result("Acq4D.1385")

print (GREEN + "                                                        ---- END of TC 2.11 Columbia ----" + RESET)

