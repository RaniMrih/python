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
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1243'
SinosPath2_14 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1242/SINOSPath2_14.txt'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1242'


print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.14 Step 1243 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- grep Total coincidence Transmitted from Tell.2.9.SINO0000
def FindTotalTransmitted():
   with open(TC_start + "/Tell2.14.SINO0000" , 'r') as f:
     for line in f.readlines():
       if 'Total coincidence events transmitted' in line:
         result = line
     return result

#---- grep Total coincidence Transmitted from Tell.2.9.SINO0000
def FindEventLoss():
   with open( TC_start + "/Tell2.14.SINO0000" , 'r') as f:
     for line in f.readlines():
       if 'Event Loss due to Sorter being bandwidth limit' in line:
         result = line
     return result

# ------------------------------------ step 1 --------------------------------------------
# grep sinos  path
f = open( SinosPath2_14 , "r")
for line in f:
  path = line

#perform rdfTell to sinos from TC2.14
print
print ("Creating rdfTell -h df for SINO0000, please wait...")
os.system("rdfTell -h df "+ path +"/SINO0000 > Tell2.14.SINO0000")

#----------- qustions ---------
time.sleep(1)
print (BLUE + "1) Coincidence Events transmitted to Sorter:" + RESET)
result = FindTotalTransmitted()
# remove first 2 chars and 54 from the end
result = result[:-54]
result = result.replace(result[:2],'')
print result

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Event Loss due to Sorter BW limited:" + RESET)
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
Step_Result("Acq4D.1225")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1245/Acq4D_1245.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1245/Acq4D_1245.py")

