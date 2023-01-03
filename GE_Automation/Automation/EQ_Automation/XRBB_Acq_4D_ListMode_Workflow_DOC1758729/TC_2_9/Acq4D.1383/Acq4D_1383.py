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
SinoBinDwell=["0","2","4","6"]
SINOAcceptedTriggers=[]
BinsResult=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1383'
ListPath2_9 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215/LISTSPath2_9.txt'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.9 Step 1383 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string

def findAcceptedTriggers ():
   for line in open(TC_start + "/Tell2.9.SINO0000", "r"):
      line = line.rstrip()
      if re.search('acceptedTriggers:', line):
        line1=split_string(line)
        print line1[1]
        SINOAcceptedTriggers.append(line1[1])

def findBinDwill():
   for i in SinoBinDwell:
     for line in open(TC_start + "/Tell2.9.SINO0000", "r"):
       line = line.rstrip()
       if re.search('   bin '+i+' dwell', line):
         print line.replace(line[:3],'')
         line1=split_string(line)
         BinsResult.append(line1[7])

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#------------------------------------- step 1 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "1) Accepted Triggers: " + RESET)
findAcceptedTriggers ()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Accepted Triggers are 120 or 121 ?" + RESET)
if int(SINOAcceptedTriggers[0]) == 120 or int(SINOAcceptedTriggers[0]) == 121:
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
   if int(BinsResult[j]) > 15100 or  int(BinsResult[j] < 14900) :
     YesNo(False)
   else : 
     YesNo(True) 
   j+=1
  

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1383")

print (GREEN +"                                                        ---- END of TC 2.9 for XRBB ----" +RESET)

#----------- END TC.2.9
