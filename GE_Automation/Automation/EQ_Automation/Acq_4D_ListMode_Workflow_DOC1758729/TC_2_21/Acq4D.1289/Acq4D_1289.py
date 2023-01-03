#!/usr/bin/env python
import os, sys
import time
import re

#VARIABLES
Step_Pass=True
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'

PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1289'
TC_start='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1287'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.21 Step 1289 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ','
def split_string1(line):
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

#--- find SorterCoinLoss from coinLoss.csv
def CheckCoinLoss():
   i=0
   smaller=True
   for line in open( TC_start + "/coinLoss_1285.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string1(line)
       i+=1
    #check if all SortercoinLoss < 1%
       if float(line1[3]) > 1.0:
         smaller=False
   YesNo(smaller)

#--- find ErrorLoss from coinLoss.csv
def FindErrorLoss():
   i=0
   smaller=True
   for line in open( TC_start + "/coinLoss_1285.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string1(line)
       i+=1
    #check if all ErrorLoss < 1%
       if float(line1[5]) > 1.0:
         smaller=False
   YesNo(smaller)


# ------------------------------------ step 1 --------------------------------------------
# grep list file path
f = open( TC_start + "/SINOSPath2_21_2.txt" , "r")
for line in f:
  path = line


print "Creating coinLoss_1285.csv, please wait..."
os.system("coinLossCk -v -c " + path + "/SINO*")
os.system("mv coinLoss.csv coinLoss_1285.csv")

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "1) %SorterCoinLoss for each frame is less "+'\n'+"than 1.0 %?" +RESET)
CheckCoinLoss()

#----------- qustion ---------
time.sleep(1)
print (BLUE + "All frames have "+'\n'+"%LossError less than 1.0 %?" +RESET)
FindErrorLoss()

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "results file labeled with test Object ID,"+'\n'+"printed and attached" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE: coinLoss_1285.csv located at: ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1287' + RESET)
print
#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1289")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1290/Acq4D_1290.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1290/Acq4D_1290.py")

