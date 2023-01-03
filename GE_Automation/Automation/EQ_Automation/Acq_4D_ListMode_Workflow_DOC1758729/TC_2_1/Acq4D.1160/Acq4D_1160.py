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
TimeMarkList=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1160'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.1 Step 1160 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to  ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#--- find First time mark
def findFirstTimeMark():
   for i in range(0,3):
      for line in open(TC_start + "/ListOut_f"+str(i)+".txt" , "r"):
         line = line.rstrip()
         if re.search('First Time Mark', line):
           TimeMarkList.append(line)

# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Frame 0 Last Time Mark:" +RESET)
findFirstTimeMark()
splited = split_string(TimeMarkList[0])
Frame0Last = splited[7]
print str(Frame0Last) + " ms"

print (BLUE + "1) Frame 1 First Time Mark:" +RESET)
splited = split_string(TimeMarkList[1])
Frame1First = splited[3]
print str(Frame1First) + " ms"

print (BLUE + "Frame 1 Last Time Mark:" +RESET)
splited = split_string(TimeMarkList[1])
Frame1Last = splited[7]
print str(Frame1Last) + " ms"

print (BLUE + "Frame 2 First Time Mark:" +RESET)
splited = split_string(TimeMarkList[2])
Frame2First = splited[3]
print str(Frame2First) + " ms"

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) f0_f1_gap is :" +RESET)
result = int(Frame1First) - int(Frame0Last)
print result
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "f1_f2_gap is :" +RESET)
result1 = int(Frame2First) - int(Frame1Last)
print result1

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the f0_f1_gap greater than 1 second but less than"+'\n'+"five seconds ?" +RESET)
if result > 5000 or result < 1000 :
  YesNo(False)
else:
  YesNo(True)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is the f2_f1_gap greater than 1 second but less than"+'\n'+"five seconds ?" +RESET)
if result1 > 5000 or result1 < 1000 :
  YesNo(False)
else:
  YesNo(True)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1160")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1162/Acq4D_1162.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1162/Acq4D_1162.py")





 



