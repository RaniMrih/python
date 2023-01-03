#!/usr/bin/env python
import os, sys
import time
import re
import os.path
#VARIABLES
Step_Pass=True
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'
Total_Coincidence=[]
Total_Singles=[]
Total_CoinC=[]
Total_O_FOV=[]
TC_start='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1272'
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1275'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.17 Step 1275, Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to  ','
def split_string1(line):
   list_string=line.split(',')
   return list_string

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string


#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#---- find Total Coincedence from /TimeStampLatter.txt
def find_Total_coincidence():
   for line in open(PWD + "/rdfTell_hd10hr.txt", "r"):
      line = line.rstrip()
      if re.search('Total coincidence events lost in latter stages of CPM', line):
        line1=split_string2(line)
        Total_Coincidence.append(line1[0])

#---- find Total Singles from /TimeStampLatter.txt
def find_Total_Singles():
   for line in open(PWD + "/rdfTell_hd10hr.txt", "r"):
      line = line.rstrip()
      if re.search('Total singles events lost in coinc engine of CPM', line):
        line1=split_string2(line)
        Total_Singles.append(line1[0])

#---- find Total Coinc from /TimeStampLatter.txt
def find_Total_Coinc():
   for line in open(PWD + "/rdfTell_hd10hr.txt", "r"):
      line = line.rstrip()
      if re.search('Total coinc events FOV', line):
        line1=split_string2(line)
        Total_CoinC.append(line1[0])

def find_Total_Of_FOV():
   for line in open(PWD + "/rdfTell_hd10hr.txt", "r"):
      line = line.rstrip()
      if re.search('Total of in FOV coinc events made', line):
        line1=split_string2(line)
        Total_O_FOV.append(line1[0])

# ------------------------------------ step 1  --------------------------------------------
print ("Creating rdfTell_hd10hr.txt for ListFile, please wait...")
time.sleep(3)
os.system("rdfTell -hd "+TC_start+"/LIST0000.BLF > rdfTell_hd10hr.txt")
os.system("cp rdfTell_hd10hr.txt "+PWD)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "a) Evidence of non-zero counts for the identified"+'\n'+"Coincidence Processor Module (CPM) deadtime-related"+RESET)
print (BLUE + "counters in the Deadtime Samples associated with the"+'\n'+"List File ?"+RESET)

Non_Zero=True

find_Total_coincidence()
for i in Total_Coincidence:
  if i == 0:
    Non_Zero=False

find_Total_Singles()
for i in Total_Coincidence:
  if i == 0:
    Non_Zero=False

find_Total_Coinc()
for i in Total_CoinC:
  if i == 0:
    Non_Zero=False

find_Total_Of_FOV()
for i in Total_O_FOV:
  if i == 0:
    Non_Zero=False

YesNo(Non_Zero)


#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1275")
print (GREEN + "                                                      ---- END of TC 2.17 Columbia DMI ----" + RESET)

