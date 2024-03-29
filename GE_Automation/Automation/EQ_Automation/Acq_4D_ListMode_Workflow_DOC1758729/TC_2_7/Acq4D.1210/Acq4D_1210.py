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
sinosList2_4 = ["00","09","12","15"]
sinosList2_6 = ["00","45","60","90"]
sinosList2_7 = ["00"]
ScanStartLive=[]
ScanStartReplay=[]
FrameStartLive=[]
FrameStartReplay=[]
ReplayDurationList=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1210'
SinoPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/SINOSPath2_4.txt'
SinoPath2_6 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_6/Acq4D.1204/SINOSPath2_6.txt'
SinoPath2_7 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1209/SINOSPath2_7.txt'
Step_Pass=True

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.7 Step 1210 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ','
def split_string(line):
   list_string=line.split(',')
   return list_string

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string

#--- find SorterCoinLoss from coinLoss.csv
def CheckCoinLoss():
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
       print line1[3]


# ------------------------------------ step 1 --------------------------------------------
# grep sinos path from 1209 TC.2.7
f = open( SinoPath2_7 , "r")
for line in f:
  path = line

print "Creating coinLossCK.csv, please wait..."
os.system("coinLossCk -v -c " + path + "/SINO*")
os.system("cp ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1209/coinLoss.csv " +PWD)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "%SorterCoinLoss value : " +RESET)
FindCoinLoss()

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "1) %SorterCoinLoss for each frame is less "+'\n'+"than 1.0 %?" +RESET)
CheckCoinLoss()

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1210")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1211/Acq4D_1211.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1211/Acq4D_1211.py")

