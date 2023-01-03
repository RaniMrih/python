#!/usr/bin/python
import os, sys
import time
import re

#VARIABLES
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/LISTSPath2_4.txt'
num = []
Step_Pass=True

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.4 Step 1190 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print
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

def split_string(line):
   list_string=line.split(',')
   return list_string

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
print (BLUE + "1) Number of List Files:" + RESET)

f = open( ListPath2_4 , "r")
for line in f:
  path = line

#coun files in directory
for item in os.listdir(path):
  if item.startswith('LIST'):
    num.append(item)

print len(num)
print
time.sleep(1)

print (BLUE + "The name of the list file with path:" + RESET)
for item in num:
  print (path + "/" + item + '\n')

time.sleep(1)
print (BLUE + "Is the name and path of the list file present in the"+'\n'+"directory matches with the associated " + RESET)
print (BLUE + "'where_is_list_frame' tag description field in"+'\n'+"Investigator's More Info tab?" + RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + "Note: Go to Investigator and check manually"+RESET+'\n')
#------------------------------------- step 2 --------------------------------------------
print (BLUE + "2) The 'list loss in aligned' for the list file is:" + RESET)
os.system("ListTool -Ml -Sl  -f ListLoss2.4.csv " + path + "/" + item + " > ListLoss2.4.txt")
os.system("cp ListLoss2.4.csv "+PWD)
os.system("cp ListLoss2.4.txt "+PWD)
#os.system("ssh ctuser@par ListTool -Ml -Sl  -f ListLoss2.4.csv " + path + "/" + item + ">" + PWD + "/" + "ListLoss2.4.txt")

with open(PWD + "/ListLoss2.4.txt", 'r') as f:
    for line in f.readlines():
      if 'list loss in aligned' in line:
        result = line.replace(line[:38], '')
        print result
        result = result[:-2]
        result = float(result)
time.sleep(1)
print
print (BLUE + "Is the  'list loss in aligned'  for the list file is less than"+'\n'+" 1.0 % ?" + RESET)
if result < 1:
  smaller = True
  YesNo(smaller)
else:
  smaller = False
  YesNo(smaller)
#------------------------------------- step 3 --------------------------------------------
print (BLUE + "3) Maximum  Coincidence Loss in any one second "+'\n'+"interval of from ListTool ouput:" + RESET)
with open(PWD +"/ListLoss2.4.txt", 'r') as f:
    for line in f.readlines():
      if 'Maximum list loss' in line:
        result = line.replace(line[:24], '')
print result
print ("Creating LT.csv")
time.sleep(0.5)
print ("Creating LT_Ml.txt")

#creating ListTool files LT.csv, LT_Ml.txt
os.system("ListTool -Ml -Sl  -f LT.csv " + path + "/" + item + " > LT_Ml.txt")
os.system("cp LT.csv "+PWD)
os.system("cp LT_Ml.txt "+PWD)

time.sleep(1)
print
print (BLUE + "Maximum  Coincidence Loss in any 1 second interval "+'\n'+"expressed as a percentage of the Prompt rate for" + RESET)
print (BLUE + "same interval:" + RESET)

f = open( PWD + "/LT.csv", "r")
result = ","+result
result=result.strip('\n')
for line in f:
  if result in line:
    line1=split_string(line)
    print line1[5]
print
#------------------------------------- step 4 --------------------------------------------
time.sleep(1)
print (BLUE + "4) The 'Maximum list loss' for any one second interval "+'\n'+"is less than 50% ?" + RESET)
i=0
percent50 = True
f = open(PWD + "/LT.csv", "r")
for line in f:
  if i < 2 :
    i+=1
    continue
  else:
    i+=1
    line1=split_string(line)
   # print line1[5]
    if float(line1[5]) > 50 or float(line1[5]) < -50:
      percent50 = False
YesNo(percent50)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1190")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1192/Acq4D_1192.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1192/Acq4D_1192.py")

