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
CoincListReplay=[]
CoincListLive=[]
ScanStartSINO=[]
ReplayDurationList=[]
LiveDurationList=[]
FrameStartSINO=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1167'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1165'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.2 Step 1167 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                      ---- Step "+StepNum+" Failed ----" + RESET)
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

#--- find scan start time
def ScanStartTimeSINO():
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   Scan Start Time =', line):
       StartSINO = line.replace(line[:21], '')
       ScanStartSINO.append(StartSINO)

#--- find Frame start time
def FrameStartTimeSINO():
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   Frame Start Time =', line):
       StartSINO = line.replace(line[:22], '')
       FrameStartSINO.append(StartSINO)

#--- find Frame start time Coinc
def findCoincMsec():
   for line in open(TC_start + "/S2.2Sino.txt" , "r"):
      line = line.rstrip()
      if re.search('(Coinc msec)', line):
        Coinc = line.replace(line[:34], '')
        CoincListReplay.append(Coinc)

#--- find Frame start time Coinc
def findCoincMsecLive():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt" , "r"):
      line = line.rstrip()
      if re.search('(Coinc msec)', line):
        Coinc = line.replace(line[:34], '')
        CoincListLive.append(Coinc)

#--- find Frame Duration Replay Scan
def FrameDurationReplay():
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
      line = line.rstrip()
      if re.search('Frame Duration', line):
        ReplayDuration = line.replace(line[:21], '')
        OnlyDuration2 = split_string(ReplayDuration)
        ReplayDurationList.append(OnlyDuration2[1])


#--- find Frame Duration Live Scan
def FrameDurationLive():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
      line = line.rstrip()
      if re.search('Frame Duration', line):
        ReplayDuration = line.replace(line[:21], '')
        OnlyDuration2 = split_string(ReplayDuration)
        LiveDurationList.append(OnlyDuration2[1])


# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) S2.2Sino.txt replay Time-Of-Day (hh:mm:ss) for:"+'\n'+"Scan Start Time:" +RESET)
ScanStartTimeSINO()
print ScanStartSINO[0]

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Frame Start Time (For First Frame): " +RESET)
FrameStartTimeSINO()
print FrameStartSINO[0]

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The replay Frame Start Time of the first frame is"+'\n'+"30 seconds after the start of the scan ?" +RESET)
Time1=ScanStartSINO[0].replace(ScanStartSINO[0][:11],'')
Time1= split_string(Time1)
ScanSeconds = split_string2(Time1[0])

#Time2= split_string(FrameStartSINO[0])
Time2=FrameStartSINO[0].replace(FrameStartSINO[0][:11],'')
Time2= split_string(Time2)
FrameSeconds = split_string2(Time2[0])

diff = int(ScanSeconds[2]) - int(FrameSeconds[2])
if diff < 0:
  diff*= -1
if diff == 30:
  YesNo(True)
else:
  YesNo(False)


# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) The Frame Start Time (Coinc msec) timestamps "+'\n'+"for original and replay Frame for all beds " +RESET)
findCoincMsec()
findCoincMsecLive()

print
print (BLUE + "Original Scan :" +RESET)
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(CoincListLive[i])

time.sleep(1)
print
print (BLUE + "Replay Scan :" +RESET)
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(CoincListReplay[i])
print

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is the difference between original and replay "+'\n'+"Frame Start Time (Coinc msec) for all other beds  is <= 5ms ?" +RESET)
Within5=True
for i in range (0,3):
  diff=int(CoincListLive[i])-int(CoincListReplay[i])
  if diff > 5 or diff < -5:
    Within5=False
YesNo(Within5)

# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) The Frame Durations for original scan and  "+'\n'+"replay scan for all beds ?" +RESET)
print
FrameDurationLive()
FrameDurationReplay()
print (BLUE + "Original Scan :" +RESET)
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(LiveDurationList[i])
print

time.sleep(1)
print (BLUE + "Replay Scan :" +RESET)
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(ReplayDurationList[i])
print

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the difference between Frame Duration for"+'\n'+"original scan and replay scan is <= 5ms ?" +RESET)
Within5=True
for i in range (0,3):
  if int(LiveDurationList[i]) - int(ReplayDurationList[i]):
    Within5=False
YesNo(Within5)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1167")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1168/Acq4D_1168.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1168/Acq4D_1168.py")



















