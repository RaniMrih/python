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
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/PET_Data_Acquisition/TC_2_1/DACQ.1630'

print
time.sleep(1)
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::::::: Running DMI TC_2.1.1.2 Step 1630 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.1 press ctrl+c to stop :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

def Get_System_Config():
   sysConfig = os.popen('swhwinfo -pet')
   sysConfig= sysConfig.read().strip('\n')
   #--- bgo for OMNI
   if sysConfig == "8x8x2_bgo":
     sysConfig="BGO8x8_2_TUBEQAT"
   if sysConfig == "8x8x3_bgo":
     sysConfig="BGO8x8_3_TUBEQAT"
   if sysConfig == "8x8x4_bgo":
     sysConfig="BGO8x8_4_TUBEQAT"
   if sysConfig == "8x8x5_bgo":
     sysConfig="BGO8x8_5_TUBEQAT"
   #--- lyso for DMI
   if sysConfig == "16x9x3_lyso":
     sysConfig="LYSO4x9_3_SIPMGEN1"
   if sysConfig == "16x9x4_lyso":
     sysConfig="LYSO4x9_4_SIPMGEN1"
   if sysConfig == "16x9x5_lyso":
     sysConfig="LYSO4x9_5_SIPMGEN1"
   if sysConfig == "9x6x4_lyso":
     sysConfig="LYSO9x6_4_TUBEQAT"
   return sysConfig

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                       ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                       ---- Step "+StepNum+" Passed ----" + RESET)
     print


#------------------------------------- Step 1 -----------------------------------------
sysConfig = Get_System_Config()
print sysConfig

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Number of Scans requested:"+RESET)
ScanReq = os.popen("grep -c '<scanRequest' /usr/g/ctuser/acqAutoTest/protocols/ScanRunnerSequences/DataAcq_sequence."+sysConfig+".xml")
ScanReq = ScanReq.read().strip('\n')
print ScanReq

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of Scans requested is greater than 1 ?" +RESET)
if int(ScanReq) <= 1 :
  YesNo(False)
else:
   YesNo(True)
#------------------------------------- Step 2 -----------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Number of PASS :" +RESET)
ScanPassed = os.popen("grep -c 'Passed' /usr/g/ctuser/acqAutoTest/newResults/autoTestSummaryLog")
ScanPassed = ScanPassed.read().strip('\n')
print ScanPassed

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The number of PASS is equal to"+'\n'+"Number of Scans requested ?" +RESET)
if int(ScanReq) == int(ScanPassed):
  YesNo(True)
else:
  YesNo(False)
#------------------------------------- Step 3 -----------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) Number of FAILs :" +RESET)
ScanFailed = os.popen("grep -c 'Failed' /usr/g/ctuser/acqAutoTest/newResults/autoTestSummaryLog")
ScanFailed = ScanFailed.read().strip('\n')
print ScanFailed

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The number of FAIL is equal to zero ?" +RESET)
if int(ScanFailed) == 0:
  YesNo(True)
else:
  YesNo(False)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("DACQ.1630")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/PET_Data_Acquisition/TC_2_1/DACQ.1634/DACQ_1634.py")
os.system("/usr/g/ctuser/EQ_Automation/PET_Data_Acquisition/TC_2_1/DACQ.1634/DACQ_1634.py")
