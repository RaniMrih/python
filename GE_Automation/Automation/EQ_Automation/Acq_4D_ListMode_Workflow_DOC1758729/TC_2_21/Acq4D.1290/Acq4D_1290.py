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
Percent_Missing=[]
Loss_In_Aligned=[]
Max_List_Loss=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1290'
TC_start='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1287'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.21 Step 1290 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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
   for line in open(PWD + "/LT_Ml.ConcurListCopy_1284.txt", "r"):
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
   for line in open(PWD + "/LT_Ml.ConcurListCopy_1284.txt", "r"):
      line = line.rstrip()
      if re.search('Percent list loss in aligned section', line):
        line1=split_string(line)
        x=line1[6]
        #remove last char
        x=x[:-1]
        print str(x) + " %"
        Loss_In_Aligned.append(x)

#--- find list loss in aligned
def findMaxListLoss():
   for line in open(PWD + "/LT_Ml.ConcurListCopy_1284.txt", "r"):
      line = line.rstrip()
      if re.search('Maximum list loss rate:', line):
        line1=split_string(line)
        print line1[4]
        Max_List_Loss.append(line1[4])


def findMaxListLossPerSec():
   # the fake data result not exist in LT_ConcurListCopy.csv, used 80 for testing only
   i=0
   f = open( PWD + "/LT_ConcurListCopy_1284.csv", "r")
   result1 = ","+str(Max_List_Loss[0])
   for line in f:
     if i < 2:
       i+=1
       continue
     else:
       i+=1
       if result1 in line:
         line1=split_string1(line)
         return line1[5]

# ------------------------------------ step 1 --------------------------------------------
# grep list file path
f = open( TC_start + "/LISTSPath2_21_1.txt" , "r")
for line in f:
  path = line

print "Creating NewList_ConcurListCopy_1284.BLF, please wait..."
os.system("ln -sf " + path + "/LIST0000.BLF > NewList_ConcurListCopy_1284.BLF")
os.system("cp LIST0000.BLF " + PWD)
os.system("cp NewList_ConcurListCopy_1284.BLF " + PWD)
#----------------------------

print ("Creating LT_Ml.ConcurListCopy_1284.txt, LT_ConcurListCopy_1284.csv for ListFile, please wait...")
os.system("ListTool -Ml -f LT_ConcurListCopy_1284.csv LIST0000.BLF > LT_Ml.ConcurListCopy_1284.txt")
os.system("cp LT_ConcurListCopy_1284.csv " + PWD)
os.system("cp LT_Ml.ConcurListCopy_1284.txt " + PWD)

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
# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) the maxLossPercentPerSec to 0.1% "+'\n'+"precision is :" +RESET)
findMaxListLoss()
#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "is maxLossPercentPerSec is < 50.0%" +RESET)
result = findMaxListLossPerSec()
if float(result) < 50.0 :
  YesNo(True)
else:
  YesNo(False)
# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) Plot of LT_ConcurListCopy.csv Labeled"+'\n'+"with TEST Object ID and attached to test Results ?" +RESET)

print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE: LT_ConcurListCopy_1284.csv located at: ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1290' + RESET)
print
#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1290")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1291/Acq4D_1291.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1291/Acq4D_1291.py")

