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
ScanStartLIST=[]
ScanStartSINO=[]
FrameStartSINO=[]
FrameStartLIST=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1217'
ListPath2_9 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215/LISTSPath2_9.txt'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.9 Step 1217 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ','
def split_string(line):
   list_string=line.split(',')
   return list_string

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string

#---- grep Total coincidence Transmitted from Tell.2.9.SINO0000
def FindTotalTransmitted():
   with open( "/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215/Tell2.9.SINO0000" , 'r') as f:
     for line in f.readlines():
       if 'Total coincidence events transmitted' in line:
         result = line
     return result

#---- grep Total coincidence Transmitted from Tell.2.9.SINO0000
def FindEventLoss():
   with open( "/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215/Tell2.9.SINO0000" , 'r') as f:
     for line in f.readlines():
       if 'Event Loss due to Sorter being bandwidth limit' in line:
         result = line
     return result

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
print (BLUE + "1) Coincidence Events transmitted to the Sorter:" + RESET)
result = FindTotalTransmitted()
# remove first 2 chars and 54 from the end
result = result[:-54]
result = result.replace(result[:2],'')
print result

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Event Loss due to Sorter being bandwidth limited:" + RESET)
result1 = FindEventLoss()
# remove first 2 chars and 54 from the end
result1 = result1[:-51]
result1 = result1.replace(result1[:10],'')
print result1

#------------------------------------- step 2 --------------------------------------------
#----------- qustions ---------
#   (Event Loss due to Sorter BW limited / (Total Coin events transmitted + Events Loss due to Sorter)) * 100.0
time.sleep(1)
print
print (BLUE + "2) Sorter Loss % :" + RESET)
sum = (float(result1) / (float(result) + float(result1))) * 100.0 
print str(sum) + " %"

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Sorter Loss % is less than 1% ?" + RESET)
if sum > 1.0:
  YesNo(False)
else:
  YesNo(True)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1217")
os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1218/Acq4D_1218.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1218/Acq4D_1218.py")

