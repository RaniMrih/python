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
num =[]
sinosList = ["00","09","12","15"]
ScanStartLive=[]
ScanStartReplay=[]
FrameStartLive=[]
FrameStartReplay=[]
ScanCoincList=[]
LiveCoincList=[]
ReplayCoincList=[]
LiveDurationList=[]
ReplayDurationList=[]
TC_Start='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196'
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1199'
Step_Pass=True

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.5 Step 1199 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to space ' '
def split_string(line):
   list_string=line.split(',')
   return list_string

#--- find SorterCoinLoss from coinLoss.csv
def FindCoinLoss():
   i=0
   smaller=True
   for line in open( PWD + "/coinLoss.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string(line)
       i+=1
    #check if all SortercoinLoss < 1%
       if float(line1[3]) > 1.0:
         smaller=False
   YesNo(smaller)

#--- find ErrorLoss from coinLoss.csv
def FindErrorLoss():
   i=0
   smaller=True
   for line in open( PWD + "/coinLoss.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string(line)
       i+=1
    #check if all SortercoinLoss < 1%
       if float(line1[5]) > 1.0:
         smaller=False
   YesNo(smaller)

#------------------------------------- step 1 --------------------------------------------
# grep sinos path from step 1196
print "Creating coinLossCK.csv, please wait..."
for line in open(TC_Start +"/SINOSPath2_5.txt","r"):
  path = line
os.system("coinLossCk -v -c " + path + "/SINO*")
os.system("cp ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196/coinLoss.csv " +PWD)

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "1) %SorterCoinLoss for each frame is less than 1.0 %?" +RESET)
FindCoinLoss()

#----------- qustion ---------
time.sleep(1)
print (BLUE + "All frames have %LossError less than 1.0 % ?" +RESET)
FindErrorLoss()

#------------------------------------- step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "results file labeled with test Object ID, printed and attached" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE : coinLoss.csv  ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1199' + RESET)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1197")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1201/Acq4D_1201.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1201/Acq4D_1201.py")

