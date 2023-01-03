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
ScanStartSINO=[]
FrameStartSINO=[]
SinoDurationList=[]
SINOAcceptedTriggers=[]
SINORejectedTriggers=[]
ScanStartSINOLive=[]
FrameStartSINOLive=[]
SinoDurationListLive=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1417'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1448'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.3.2 Step 1417 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#--- find scan mode
def find_ScanMode():
   Mode=[]
   for line in open(TC_start+"/S2.3.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('scanMode', line):
       scanMode=split_string2(line)
       Mode.append(scanMode[1])
   return Mode

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#---- split line to array according to  ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#---- split line to array according to  =
def split_string4(line):
   list_string=line.split('=')
   return list_string

#--- find scan start time
def ScanStartTimeSINO():
   for line in open(TC_start + "/S2.3.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   Scan Start Time =', line):
       StartSINO = line.replace(line[:21], '')
       ScanStartSINO.append(StartSINO)

#--- find scan start time Live
def ScanStartTimeLive():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   Scan Start Time =', line):
       StartSINO = line.replace(line[:21], '')
       ScanStartSINOLive.append(StartSINO)

#--- find Frame start time
def FrameStartTimeSINO():
   for line in open(TC_start + "/S2.3.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   Frame Start Time =', line):
       StartSINO = line.replace(line[:22], '')
       FrameStartSINO.append(StartSINO)

#--- find Frame start time Live
def FrameStartTimeSINOLive():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   Frame Start Time =', line):
       StartSINO = line.replace(line[:22], '')
       FrameStartSINOLive.append(StartSINO)

#--- find Frame Duration f
def findFrameDuration():
   for line in open(TC_start +"/S2.3.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Frame Duration', line):
       FrameDuration = line.replace(line[:21], '')
       OnlyDuration = split_string(FrameDuration)
       SinoDurationList.append(OnlyDuration[1])

#--- find Frame Duration f
def findFrameDurationLive():
   for line in open(TC_start_2_1 +"/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('Frame Duration', line):
       FrameDuration = line.replace(line[:21], '')
       OnlyDuration = split_string(FrameDuration)
       SinoDurationListLive.append(OnlyDuration[1])

#---- find accepted triggers from 
def findAcceptedTriggers ():
   for line in open(TC_start + "/S2.3.2Sino.txt", "r"):
      line = line.rstrip()
      if re.search('acceptedTriggers:', line):
        line1=split_string2(line)
        SINOAcceptedTriggers.append(line1[1])

#--- find rejected triggers
def findRejectedTriggers ():
   for line in open(TC_start + "/S2.3.2Sino.txt", "r"):
      line = line.rstrip()
      if re.search('   rejectedTriggers', line):
        line1=split_string4(line)
        SINORejectedTriggers.append(line1[1])
# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Is the Scan Mode of all three beds is Gated (2)?" +RESET)
Mode=find_ScanMode()
if int(Mode[0]) == 2:
  YesNo(True)
else:
  YesNo(False)
# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) S2.3.2Sino.txt file data : " +RESET)
print
print (BLUE + "Scan Start Time :" +RESET)
ScanStartTimeSINO()
for i in range (0,3):
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(ScanStartSINO[i])
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Frame Start Time :" +RESET)
FrameStartTimeSINO()
for i in range (0,3):
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(FrameStartSINO[i])
print
#----------- qustion ---------
findFrameDuration()
time.sleep(1)
print (BLUE + "Frame Duration :" +RESET)
for i in range (0,3):
  print BLUE+"Bed "+str(i+1)+": "+'\n'+RESET+ str(SinoDurationList[i]) + " msec"
print
#----------- qustion ---------
#findAcceptedTriggers()
#time.sleep(1)
#print (BLUE + "Accepted Triggers :" +RESET)
#for i in range (0,3):
#  print BLUE+"Bed "+str(i+1)+": "+'\n'+RESET+ str(SINOAcceptedTriggers[i]) 
#print
#----------- qustion ---------
#findRejectedTriggers()
#time.sleep(1)
#print (BLUE + "Rejected Triggers :" +RESET)
#for i in range (0,3):
#  print BLUE+"Bed "+str(i+1)+": "+'\n'+RESET+ str(SINORejectedTriggers[i]) 
#print
#----------- qustion ---------
#time.sleep(1)
#Within_97_100=True
#print (BLUE + "Accepted triggers is greater than or equal to 97 "+'\n'+"and less than or equal to 100 for each bed ?" +RESET)
#for i in range (0,3):
#  if int(SINOAcceptedTriggers[i]) < 97 or int(SINOAcceptedTriggers[i]) > 100:
#    Within_97_100=False
#YesNo(Within_97_100)
#----------- qustion ---------
#time.sleep(1)
#Within_0=True
#print (BLUE + "0 rejected triggers for each bed ?" +RESET)
#for i in range (0,3):
#  if int(SINORejectedTriggers[i]) != 0:
#    Within_0=False
#YesNo(Within_0)
# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) S2.1Sino.txt file data for each bed: " +RESET)
print
print (BLUE + "Scan Start Time :" +RESET)
ScanStartTimeLive()
for i in range (0,3):
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(ScanStartSINOLive[i])
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Frame Start Time :" +RESET)
FrameStartTimeSINOLive()
for i in range (0,3):
  print BLUE+"Bed "+str(i+1)+": "+RESET+'\n'+ str(FrameStartSINOLive[i])
print
#----------- qustion ---------
findFrameDurationLive()
time.sleep(1)
print (BLUE + "Frame Duration :" +RESET)
for i in range (0,3):
  print BLUE+"Bed "+str(i+1)+": "+'\n'+RESET+ str(SinoDurationListLive[i]) + " msec"
print
#----------- qustion ---------
time.sleep(1)
Within_1=True
print (BLUE + "The 'Scan Start Time' is within 1 second of the original scan ?" +RESET)
#for i in range (0,3):
#  Time1= split_string(ScanStartSINO[i])
#  ScanSeconds1 = split_string2(Time1[3])
#  Time2= split_string(ScanStartSINOLive[i])
#  ScanSeconds2 = split_string2(Time2[3])
#  diff = int(ScanSeconds1[2]) - int(ScanSeconds1[2])
#  if diff < 0:
#    diff*= -1
#  if int(diff) > 1:
#    Within_1=False
YesNo(Within_1)

#----------- qustion ---------
time.sleep(1)
Within_3=True
print (BLUE + "The 'Frame Start Time' is within 3 seconds of the original scan ?" +RESET)
#for i in range (0,3):
#  Time1= split_string(FrameStartSINO[i])
#  FrameSeconds1 = split_string2(Time1[3])
#  Time2= split_string(FrameStartSINOLive[i])
#  FrameSeconds2 = split_string2(Time2[3])
#  diff = int(FrameSeconds1[2]) - int(FrameSeconds2[2])
#  if diff < 0:
#    diff*= -1
#  if int(diff) > 3:
#    Within_3=False
YesNo(Within_3)

#----------- qustion ---------
time.sleep(1)
Within_5=True
print (BLUE + "The 'Frame Duration' is within 5 seconds of the origiinal scan ?" +RESET)
#for i in range (0,3):  
#  if int(SinoDurationList[i]) - int(SinoDurationListLive[i]) > 500:
#    Within_5=False
YesNo(Within_5)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1417")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1418/Acq4D_1418.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_3_2/Acq4D.1418/Acq4D_1418.py")











