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
TotaCoincidence_List=[]
EventLoss_List=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1182'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1179'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.3.1 Step 1182 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#--- Multi params find function in Sino
def Find_In_Sino (File,Param):
   Arr=[]
   for line in open(TC_start + File, "r"):
      line = line.rstrip()
      if re.search( Param , line):
        Arr.append(line)
   return Arr
# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Total coincidence events transmitted to the Sorter :" +RESET)
TotaCoincidence = Find_In_Sino("/S2.3.1Sino.txt" , "Total coincidence events transmitted")
for i in range (3):
  result = split_string2(TotaCoincidence[i])
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(result[0].replace(" ", ""))
  TotaCoincidence_List.append(result[0].replace(" ", ""))
# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) Event Loss due to Sorter being bandwidth limited :" +RESET)
EventLoss = Find_In_Sino("/S2.3.1Sino.txt" , "Event Loss due to Sorter being bandwidth limited")
for i in range (3):
  result = split_string2(EventLoss[i])
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(result[0].replace(" ", ""))
  EventLoss_List.append(result[0].replace(" ", ""))
# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "3) Sorter Loss % " +RESET)
#(Event Loss due to Sorter BW limited / (Total Coin events transmitted + Events Loss due to Sorter BW limited)) * 100.0
Within_1=True
for i in range(3):
  SorterLoss = (int(EventLoss_List[i]) / (int(TotaCoincidence_List[i]) + int(EventLoss_List[i]))) * 100
  if int(SorterLoss) > 1:
    Within_1=False
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(SorterLoss)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Sorter Loss % is less than 1% for all beds ? " +RESET)
YesNo(Within_1)
#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1182")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1183/Acq4D_1183.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_1/Acq4D.1183/Acq4D_1183.py")

