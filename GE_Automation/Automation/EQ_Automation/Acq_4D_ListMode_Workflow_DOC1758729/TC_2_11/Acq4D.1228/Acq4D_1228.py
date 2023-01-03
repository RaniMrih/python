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
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_11/Acq4D.1228'
#TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_10/Acq4D.1223'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.11 Step 1228 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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
   with open(PWD + "/Tell2.11.SINO0000" , 'r') as f:
     for line in f.readlines():
       if 'Total coincidence events transmitted' in line:
         result = line
     return result

#---- grep Total coincidence Transmitted from Tell.2.9.SINO0000
def FindEventLoss():
   with open(PWD+ "/Tell2.11.SINO0000" , 'r') as f:
     for line in f.readlines():
       if 'Event Loss due to Sorter being bandwidth limit' in line:
         result = line
     return result


# ---------------------------------------------------------------------------------------
#use of raw_input() from user
SinosDirectory2_11 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.11 :" + RESET)
# while SinosDirectory2_11 is empty
while SinosDirectory2_11 == "":
  SinosDirectory2_11 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.11 again:" + RESET)

#like echo to file
f=open("SINOSPath2_11.txt", "w+")
f.write(SinosDirectory2_11)
f.close()

# ------------------------------------ step 2 (first) --------------------------------------------
#perform rdfTeller to sinos from TC2.11
print
print ("Creating Tell2.11 for SINOS, please wait...")
os.system("rdfTeller -r  '-h  efadS -S -v'  -f Tell2.11 "+ SinosDirectory2_11 +"/SINO*")
print ("Creating Tell2.11Geo for SINOS, please wait...")
os.system("rdfTeller -r  '-h  g -v'  -f Tell2.11Geo "+ SinosDirectory2_11 +"/SINO*")
print
os.system("cp /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215/Tell2.9* /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_11/Acq4D.1228")

#------------------------------------- step 1 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "1) Coinc Events transmitted to the Sorter:" + RESET)
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
Step_Result("Acq4D.1228")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_11/Acq4D.1385/Acq4D_1385.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_11/Acq4D.1385/Acq4D_1385.py")

