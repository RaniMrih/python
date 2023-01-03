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
PWD = '/usr/g/ctuser/EQ_Automation/PET_Data_Acquisition/TC_2_1/DACQ.1634'
NewResults = '/usr/g/ctuser/acqAutoTest/newResults/'
print
time.sleep(1)
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::::::: Running DMI TC_2.1.1.3 Step 1634 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#------------------------------------- Step 1 -----------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1. Record values for the following :"+RESET+'\n')

Result = os.popen("grep -h radialModulesPerSystem  LT* | sort | uniq")
print Result.read().strip('\n')
time.sleep(0.1)

Result = os.popen("grep -h axialModulesPerSystem  LT*  | sort | uniq")
print Result.read().strip('\n')
time.sleep(0.1)

Result = os.popen("grep -h radialBlocksPerModule  LT* | sort | uniq")
print Result.read().strip('\n')
time.sleep(0.1)

Result = os.popen("grep -h --exclude='LT19*' axialBlocksPerModule   LT*  | sort | uniq")
print Result.read().strip('\n')
time.sleep(0.1)

Result = os.popen("grep -h radialCrystalsPerBlock  LT* | sort | uniq")
print Result.read().strip('\n')
time.sleep(0.1)

Result = os.popen("grep -h axialCrystalsPerBlock  LT*  | sort | uniq")
print Result.read().strip('\n')
