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
ScanStartLIST=[]
ScanStartSINO=[]
FrameStartSINO=[]
FrameStartLIST=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1216'
ListPath2_9 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215/LISTSPath2_9.txt'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.9 Step 1216 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ','
def split_string(line):
   list_string=line.split(',')
   return list_string

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string

#---- grep list loss in aligned from listfile
def List_Loss_aligned():
   with open( PWD + "/ListLoss2.9.txt" , 'r') as f:
     for line in f.readlines():
       if 'list loss in aligned' in line:
         result = line.replace(line[:38], '')
     return result

def Maximum_List_Loss():
   with open(PWD +"/ListLoss2.9.txt", 'r') as f:
     for line in f.readlines():
       if 'Maximum list loss' in line:
         result = line.replace(line[:24], '')
     return result

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#------------------------------------- step 1 --------------------------------------------
# grep list file path
f = open( ListPath2_9 , "r")
for line in f:
  path = line

#perform ListTool to Listfile from TC2.9
print ("Creating ListLoss2.9.txt for ListFile, please wait...")
os.system("ListTool -Ml -Sl  -f ListLoss2.9.csv " + path + "/LIST0000.BLF > ListLoss2.9.txt")
os.system("cp ListLoss2.9.txt "+PWD)
os.system("cp ListLoss2.9.csv "+PWD)
#----------- qustions ---------
time.sleep(1)
print (BLUE + "1)" + RESET)
print (BLUE + "a) Overall  Coincidence Loss for the list file:" + RESET)
result = List_Loss_aligned()
print result

#----------- qustions ---------
time.sleep(1)
print (BLUE + "b) Maximum  Coincidence Loss in any 1 second"+'\n'+"interval of the listfile:" + RESET)
result1 = Maximum_List_Loss()
print result1

#----------- qustions ---------
time.sleep(1)
print (BLUE + "c) Maximum  Coincidence Loss in any 1 second"+'\n'+"interval expressed as a percentage of the Prompt " + RESET)
print (BLUE + "rate for same interval:" + RESET)

f = open( PWD + "/ListLoss2.9.csv", "r")
result1 = ","+result1
result1=result1.strip('\n')
for line in f:
  if result1 in line:
    line1=split_string(line)
    print line1[5]

#----------- qustions ---------
time.sleep(1)
print 
print (BLUE + "Is the overall sorter coincidence losses for the list file"+'\n'+"does not exceed  1%?" + RESET)
result = List_Loss_aligned()
#remove last char '%'
result2 = result[:-2] 
if float(result2) < 1.0:
  YesNo(True)
else:
  YesNo(False)

#------------------------------------- step 2 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "2) The Maximum coincidence losses for any one "+'\n'+"second interval in the list file does not exceed 50% ?" + RESET)
f = open( PWD + "/ListLoss2.9.csv", "r")
result1 = ","+result1
result1=result1.strip('\n')
for line in f:
  if result1 in line:
    line1=split_string(line)
if float(line1[5]) < 50.0 :
  YesNo(True)
else:
  YesNo(False)  
#------------------------------------- step 3 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "3) Is the results plot labeled with test Object ID,"+'\n'+"printed and attached ?" + RESET)
print (YELLOW + 'NOTE: ListLoss.csv located at ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1216' + RESET)
print 

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1216")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1217/Acq4D_1217.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1217/Acq4D_1217.py")

