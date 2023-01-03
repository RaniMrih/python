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
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1192'
SinoPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/SINOSPath2_4.txt'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/LISTSPath2_4.txt'
num = []
Step_Pass=True

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.4 Step 1192 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print
#------------------------------------- Functions -------------------------------------
#--- print Yes for true value 
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

#---- split line to array according to ','
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
print "Creating coinLoss.csv, please wait..."
print
print (BLUE + "1) %SorterCoinLoss for each frame is: "+'\n'+ RESET)

# grep sinos path from 1189
f = open( SinoPath2_4 , "r")
for line in f:
  path = line
os.system("coinLossCk -v -c " + path + "/SINO*")
os.system("cp ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/coinLoss.csv " +PWD)

#fetch from coinLoss.csv
print " Frame        %SorterCoinLoss  "
i=0
smaller=True
f = open( PWD + "/coinLoss.csv", "r")
for line in f:
  if i == 0:
    i+=1
    continue
  else:
#go to def "split_string" to insert csv data to array
    line1=split_string(line)
    i+=1
    time.sleep(0.1)
    print line1[0]+"    =    "+line1[3]
    #check if all ScoinLoss < 1%
    if float(line1[3]) > 1.0:
      smaller=False
print
time.sleep(1)
print (BLUE + "Is the %SorterCoinLoss for all the frames less"+'\n'+"than 1.0% ?" +RESET)
YesNo(smaller)
time.sleep(1)
print

#fetch LossError from coinLoss.csv
print (BLUE + "%LossError  for each frame is: "+'\n'+ RESET)
print " Frame             %ErrorLoss  "
i=0
smaller=True
f = open( PWD + "/coinLoss.csv", "r")
for line in f:
  if i == 0:
    i+=1
    continue
  else:
#go to def "split_string" to insert csv data to array
    line1=split_string(line)
    i+=1
    time.sleep(0.1)
    print line1[0]+"    =    "+line1[5]
    #check if all ScoinLoss < 1%
    if float(line1[5]) > 1.0:
      smaller=False
print
time.sleep(1)
print (BLUE + "Are all frames have "+'\n'+"%LossError less than 1.0 % ?" +RESET)
YesNo(smaller)

time.sleep(1)
print (BLUE + "Is the results file labeled with test Object ID, "+'\n'+"printed and attached ?" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE : coinLoss.csv  ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1192' + RESET)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1192")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1193/Acq4D_1193.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1193/Acq4D_1193.py")

