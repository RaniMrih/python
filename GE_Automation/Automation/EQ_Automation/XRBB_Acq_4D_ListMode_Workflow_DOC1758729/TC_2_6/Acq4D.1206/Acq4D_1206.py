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
Block_MAX_Live_List =[]
Block_MAX_Replay_List =[]
sinosList2_4 = ["00","09","12","15"]
sinosList2_6 = ["00","45","60","90"]
ScanStartLive=[]
ScanStartReplay=[]
FrameStartLive=[]
FrameStartReplay=[]
LiveCoincList=[]
ReplayCoincList=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_6/Acq4D.1206'
SinoPath2_4 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/SINOSPath2_4.txt'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/LISTSPath2_4.txt'
SinoPath2_6 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_6/Acq4D.1204/SINOSPath2_6.txt'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.6 Step 1206 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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
    #check if all SortercoinLoss < 50%
       if float(line1[3]) > 50.0:
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
    #check if all ErrorLoss < 2%
       if float(line1[5]) > 2.0:
         smaller=False
   YesNo(smaller)

# ------------------------------------ step 1 --------------------------------------------
# grep sinos path from 1204 TC.2.6
f = open( SinoPath2_6 , "r")
for line in f:
  path = line

print "Creating coinLossCK.csv, please wait..."
os.system("coinLossCk -v -c " + path + "/SINO*")
os.system("cp ~/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_6/Acq4D.1204/coinLoss.csv " +PWD)

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "1) %SorterCoinLoss for each frame is less "+'\n'+"than 50.0 %?" +RESET)
FindCoinLoss()

#----------- qustion ---------
time.sleep(1)
print (BLUE + "All frames have %LossError less than "+'\n'+"2.0 %?" +RESET)
FindErrorLoss()

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "results file labeled with test Object ID,"+'\n'+" printed and attached" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE: coinLoss.csv located at: ~/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_6/Acq4D.1206' + RESET)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1206")
print (GREEN +"                                                        ---- END of TC 2.6 for XRBB ----" +RESET)

#---- End of TC.2.6















