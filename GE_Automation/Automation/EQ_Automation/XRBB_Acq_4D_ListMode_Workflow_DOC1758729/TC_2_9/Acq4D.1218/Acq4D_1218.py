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
LISTDuration=[]
SINODuration=[]
LISTPrompts=[]
SINOPrompts=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1218'
ListPath2_9 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215/LISTSPath2_9.txt'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.9 Step 1218 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string

#---- find list aligned duration
def ListAlignedDuration():
   for line in open(TC_start +"/ListLoss2.9.txt", "r"):
      line = line.rstrip()
      if re.search('Aligned duration', line):
        line1 = split_string(line)
        result = float(line1[2]) * 1000.0
        print str(result) + " ms"
        LISTDuration.append(result)

#---- find list Prompts
def ListAlignedPrompts():
   for line in open(TC_start + "/ListLoss2.9.txt", "r"):
      line = line.rstrip()
      if re.search('Aligned List Prompt Tot', line):
        line1=split_string(line)
        print line1[10]
        LISTPrompts.append(line1[10])

#---- find sino frame duration
def SinoDuration():
   for line in open(TC_start + "/Tell2.9.SINO0000", "r"):
      line = line.rstrip()
      if re.search('Frame Dur', line):
        line1=split_string(line)
        print str(line1[8]) + " ms"
        SINODuration.append(line1[8])

#---- find sino Prompts
def SinoPrompts():
   for line in open(TC_start + "/Tell2.9.SINO0000", "r"):
      line = line.rstrip()
      if re.search('Prompts:', line):
        line1=split_string(line)
        print line1[1]
        SINOPrompts.append(line1[1])

#---- find diff between sino and list durations
def DiffDurations():
   sum = float(LISTDuration[0])- float(SINODuration[0])
   if sum > 31100 or sum < 28900:
     YesNo(False)
   else:
     YesNo(True)
#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print





#------------------------------------- step 1 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "1)"+'\n'+"a) List File Duration :" + RESET)
ListAlignedDuration()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "b) List File Prompts :" + RESET)
ListAlignedPrompts()

#------------------------------------- step 2 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "2)"+'\n'+"a) Sinogram Frame Duration:" + RESET)
SinoDuration()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Sinogram Total Prompts ::" + RESET)
SinoPrompts()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "The List File Duration is longer than the sinogram "+'\n'+"frame duration by the amount of the prescan delay " + RESET)
print (BLUE + "(30s) , +/- 1100 ms?" + RESET)
DiffDurations()
#------------------------------------- step 3 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "3) Expected Prompts by scaling Prompts from List :" + RESET)
# (Sino Frame Duration / List Duration) * List File Prompts
ExpectedPrompts = (float(SINODuration[0]) / float(LISTDuration[0])) * float(LISTPrompts[0])
print ExpectedPrompts

#------------------------------------- step 4 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "4) % Prompts Difference: " + RESET)
# ( abs(Expected Prompts - Sino Frame Prompts) / Expected Prompts ) * 100.0
DiffPrompts = ((ExpectedPrompts - float(SINOPrompts[0])) / ExpectedPrompts ) * 100.0
if DiffPrompts < 0:
  DiffPrompts*=-1
print DiffPrompts

#------------------------------------- step 4 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Is the %Prompts Difference is <= 1.0 % ? " + RESET)
if float(DiffPrompts) > 1.0:
  YesNo(False)
else: 
  YesNo(True)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1218")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1383/Acq4D_1383.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1383/Acq4D_1383.py")























