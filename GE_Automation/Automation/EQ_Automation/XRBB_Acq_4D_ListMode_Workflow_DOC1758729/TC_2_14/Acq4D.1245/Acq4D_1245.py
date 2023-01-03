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
SinoBinDwell=["0","2","4","6"]
SINOAcceptedTriggers=[]
SINORejectedTriggers=[]
SINOBinningMode=[]
SINOBinDuration=[]
SINODwellList=[]

PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1245'
SinosPath2_14 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1242/SINOSPath2_14.txt'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_14/Acq4D.1242'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.14 Step 1245 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ':'
def split_string1(line):
   list_string=line.split(':')
   return list_string

#---- split line to array according to  '.'
def split_string2(line):
   list_string=line.split('.')
   return list_string

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#--- find accepted triggers
def findAcceptedTriggers ():
   for line in open(TC_start + "/Tell2.14.SINO0000", "r"):
      line = line.rstrip()
      if re.search('   acceptedTriggers', line):
        line1=split_string(line)
        print line1[5]
        SINOAcceptedTriggers.append(line1[5])

#--- find rejected triggers
def findRejectedTriggers ():
   for line in open(TC_start + "/Tell2.14.SINO0000", "r"):
      line = line.rstrip()
      if re.search('   rejectedTriggers', line):
        line1=split_string(line)
        print line1[5]
        SINORejectedTriggers.append(line1[5])

#--- find rejected triggers
def findBinningMode():
   for line in open(TC_start + "/Tell2.14.SINO0000-fa", "r"):
      line = line.rstrip()
      if re.search('binningMode', line):
        line1=split_string1(line)
        x = line1[1]
        x= x.replace(x[:1],'')
        print x
        SINOBinningMode.append(line1[1])

def findBinDuration():
   for line in open(TC_start + "/Tell2.14.SINO0000-fa", "r"):
      line = line.rstrip()
      if re.search('binDurations', line):
        x= line
        x= x.replace(x[:30],'')
        print x
        line1=split_string1(line)
        SINOBinDuration.append(line1[1])

#--- find max/min bin dwell
def findBinDwell():
   for line in open(TC_start + "/Tell2.14.SINO0000", "r"):
      line = line.rstrip()
      if re.search('dwell', line):
        line1=split_string(line)
        SINODwellList.append(int(line1[7]))

#------------------------------------- step 1 --------------------------------------------
#perform rdfTell to sinos from TC2.14
print
# grep sinos  path
f = open( SinosPath2_14 , "r")
for line in f:
  path = line

print ("Creating rdfTell -h fa for SINO0000, please wait...")
os.system("rdfTell -h fa "+ path +"/SINO0000 > Tell2.14.SINO0000-fa")
#----------- qustions ---------
time.sleep(1)
print (BLUE + "1)"+'\n'+"a) Number of accepted triggers (acceptedTriggers):"+ RESET)
findAcceptedTriggers()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "b) Number of rejected triggers (rejectedTriggers):"+ RESET)
findRejectedTriggers()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "c) acqParams binning mode (binningMode):"+ RESET)
findBinningMode()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Is accepted triggers, rejected triggers and binning"+'\n'+"mode are as expected ?"+ RESET)
AsExpected = True

if int(SINOAcceptedTriggers[0]) > 80 or int(SINOAcceptedTriggers[0])<78:
  AsExpected = False

elif int(SINORejectedTriggers[0]) != 0 :
  AsExpected = False

elif int(SINOBinningMode[0]) != 5:
  AsExpected = False

YesNo(AsExpected)

#----------- qustions ---------
time.sleep(1)
print (BLUE + "d)"+ RESET)
findBinDuration()

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "All bins have duration of 10.0 ?"+ RESET)
Duration_10 = True
for i in SINOBinDuration:
   if float(i) != 10:
     Duration_10=False
YesNo(Duration_10)

#------------------------------------- step 2 --------------------------------------------
#----------- qustions ---------
time.sleep(1)
print (BLUE + "2) Max bin dwell time:"+ RESET)
findBinDwell() 
MaxDwell = max(SINODwellList)
print str(MaxDwell) + " ms"
print

#----------- qustions ---------
time.sleep(1)
print (BLUE + "Min bin dwell time:"+ RESET)
MinDwell = min(SINODwellList)
print str(MinDwell) + " ms"
print

#----------- qustions ---------
time.sleep(1)
print (BLUE + "Max - Min dwell time:"+ RESET)
diffDwell = MaxDwell - MinDwell
print str(diffDwell) + " ms"
print

#----------- qustions ---------
time.sleep(1)
print (BLUE + "Max bin dwell - Min bin dwell < = (2*Number of "+'\n'+"accepted triggers)?"+ RESET)
if diffDwell <= int(SINOAcceptedTriggers[0]) * 2:
  YesNo(True)
else:
  YesNo(False)

#-- determine if step Pass/Fail
Step_Result("Acq4D.1245")

print (GREEN +"                                                        ---- END of TC 2.14 for XRBB ----" +RESET)



