#!/usr/bin/env python
import os, sys
import time
import re
import os.path
#VARIABLES
Step_Pass=True
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'
Percent_Missing=[]
Loss_In_Aligned=[]
TC_start='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1272'
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1273'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.17 Step 1273, Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#--- find Percent Missing
def findPercentMissing():
   for line in open(PWD + "/LT_Mt_Sh.10hr.txt", "r"):
      line = line.rstrip()
      if re.search('Percent missing timemarkers', line):
        line1=split_string(line)
        x=line1[6]
        #remove last char
        x=x[:-1]
        print str(x) + " %"
        Percent_Missing.append(x)

#--- find list loss in aligned
def findLossInAligned():
   for line in open(PWD + "/LT_Mt_Sh.10hr.txt", "r"):
      line = line.rstrip()
      if re.search('Percent list loss in aligned section', line):
        line1=split_string(line)
        x=line1[6]
        #remove last char
        x=x[:-1]
        print str(x) + " %"
        Loss_In_Aligned.append(x)

# ------------------------------------ step 1  --------------------------------------------
print ("Creating ListTool -Ml  -f  LT_Ml.10hr.csv , LT_Ml.10hr.txt for ListFile, please wait...")
os.system("ListTool -Ml  -f  LT_Ml.10hr.csv "+TC_start+"/LIST0000.BLF > LT_Mt_Sh.10hr.txt")
os.system("cp "+TC_start+"/LT_Mt_Sh.10hr.txt "+PWD )

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "a) Percent missing time markers to 0.1% "+'\n'+"precision is :" +RESET)
findPercentMissing()
#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "a) Percent missing time markers is less "+'\n'+"than 1% ?" +RESET)
if float(Percent_Missing[0]) < 1:
  YesNo(True)
else:
  YesNo(False)
#----------- qustion ---------
time.sleep(1)
print (BLUE + "b) Percent list loss in aligned section to"+'\n'+"0.1% precision is :" +RESET)
findLossInAligned()
#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "Percent list loss in aligned section is less"+'\n'+"than 1.0% ?" +RESET)
if float(Loss_In_Aligned[0]) < 1:
  YesNo(True)
else:
  YesNo(False)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1273")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1274/Acq4D_1274.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1274/Acq4D_1274.py")



