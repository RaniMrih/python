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
num =[]
sinosList = ["00","09","12","15"]
ScanStartLive=[]
ScanStartReplay=[]
FrameStartLive=[]
FrameStartReplay=[]
ScanCoincList=[]
LiveCoincList=[]
ReplayCoincList=[]
LiveDurationList=[]
ReplayDurationList=[]
TC_Start='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196'
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1197'
SinoPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/SINOSPath2_4.txt'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/LISTSPath2_4.txt'
Step_Pass=True

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.5 Step 1197 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#---- split line to array according to space ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string


#--- find scan start time live
def ScanStartTimeLive():
   for i in sinosList:
     for line in open(TC_Start + "/Tell2.4.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('   Scan Start Time =', line):
         ScanStart1 = line.replace(line[:21], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print ScanStart1
         OnlyTime1 = split_time(ScanStart1)
         OnlyTime1 = split_string(OnlyTime1[2])
         ScanStartLive.append(OnlyTime1[0])

#--- find scan start time Replay
def ScanStartTimeReplay():
   for i in sinosList:
     for line in open(TC_Start + "/Tell2.5.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('   Scan Start Time =', line):
         ScanStart2 = line.replace(line[:21], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print ScanStart2
         OnlyTime2 = split_time(ScanStart2)
         OnlyTime2 = split_string(OnlyTime2[2])
         ScanStartReplay.append(OnlyTime2[0])

#--- find Frame start time live
def FrameStartTimeLive():
   for i in sinosList:
     for line in open(TC_Start + "/Tell2.4.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('   Frame Start Time =', line):
         FrameStart1 = line.replace(line[:22], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print FrameStart1
         OnlyTime1 = split_time(FrameStart1)
         OnlyTime1 = split_string(OnlyTime1[2])
         FrameStartLive.append(OnlyTime1[0])

#--- find Frame start time Replay
def FrameStartTimeReplay():
   for i in sinosList:
     for line in open(TC_Start + "/Tell2.5.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('   Frame Start Time =', line):
         FrameStart2 = line.replace(line[:22], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print FrameStart2
         OnlyTime2 = split_time(FrameStart2)
         OnlyTime2 = split_string(OnlyTime2[2])
         FrameStartReplay.append(OnlyTime2[0])

#--- find if diff between Scan and Frame within 1 sec
def Diff_Scan_Frame():
   within_1sec = True
   for i in range (0,4):
     diffScanStart = int(ScanStartLive[i]) - int(ScanStartReplay[i])
     diffFrameStart = int(FrameStartLive[i]) - int(FrameStartReplay[i])
     if diffScanStart > 1 or diffScanStart < -1:
       within_1sec = False
     if diffFrameStart > 1 or diffFrameStart < -1:
       within_1sec = False
   YesNo(within_1sec)

#--- find Frame start time Coinc Live
def CoincTimeLive():
   for i in sinosList:
     for line in open(TC_Start + "/Tell2.4.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('(Coinc msec)', line):
         LiveCoinc = line.replace(line[:35], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print "Coinc msec= " + LiveCoinc
         LiveCoincList.append(LiveCoinc)

#--- find Frame start time Coinc Replay
def CoincTimeReplay():
   for i in sinosList:
     for line in open(TC_Start + "/Tell2.5.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('(Coinc msec)', line):
         ReplayCoinc = line.replace(line[:35], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print "Coinc msec= " + ReplayCoinc
         ReplayCoincList.append(ReplayCoinc)

#--- find if diff between Live and Replay Coinic within 5 msec
def Diff_Coinc_Time():
   within_5msec = True
   for i in range (0,4):
     diffConic = int(LiveCoincList[i]) - int(ReplayCoincList[i])
     if diffConic > 5 or diffConic < -5:
       within_5msec = False
   YesNo(within_5msec)

#--- find Frame DurationLive Scan
def FrameDurationLive():
   for i in sinosList:
     for line in open(TC_Start + "/Tell2.4.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('Frame Duration', line):
         LiveDuration = line.replace(line[:21], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print LiveDuration
         OnlyDuration1 = split_string(LiveDuration)
         LiveDurationList.append(OnlyDuration1[1])
  
#--- find Frame Duration Replay Scan
def FrameDurationReplay():
   for i in sinosList:
     for line in open(TC_Start + "/Tell2.5.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('Frame Duration', line):
         ReplayDuration = line.replace(line[:21], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print ReplayDuration
         OnlyDuration2 = split_string(ReplayDuration)
         ReplayDurationList.append(OnlyDuration2[1])
         
#--- diff durations
def Diff_Duration():
   within_5msec = True
   for i in range (0,4):
     diffDuration = int(LiveDurationList[i]) - int(ReplayDurationList[i])
     if diffDuration > 5 or diffDuration < -5:
       within_5msec = False
   YesNo(within_5msec)
   
#------------------------------------- step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "1) The 'Scan Start Time' for live scan" +RESET)
ScanStartTimeLive()
print 

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The 'Scan Start Time' for replay scan" +RESET)
ScanStartTimeReplay()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The 'Frame Start Time' for live scan" +RESET)
FrameStartTimeLive()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The 'Frame Start Time' for Replay scan" +RESET)
FrameStartTimeReplay()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is the 'Scan Start Time' and 'Frame Start Time' of"+'\n'+"the live and replay scan for the selected frames is" +RESET)
print (BLUE + "within 1 second?" +RESET)
Diff_Scan_Frame()

#------------------------------------- step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) The 'Frame Start Time (Coinc msec)' of live scan:" +RESET)
CoincTimeLive()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The 'Frame Start Time (Coinc msec)' of Replay scan:" +RESET)
CoincTimeReplay()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The 'Frame Start Time (Coinc msec)' for live scan"+'\n'+"and replay scan and replay scan is within 5 millisecond ?" +RESET)
Diff_Coinc_Time()

#------------------------------------- step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) The 'Frame Duration' (ms) of live Scan:" +RESET)
FrameDurationLive()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) The 'Frame Duration' (ms) of Replay Scan:" +RESET)
FrameDurationReplay()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is the difference between 'Frame Duration'"+'\n'+"(msec) for Live and Replay scan is <= 5 ?" +RESET)
Diff_Duration()

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1197")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1199/Acq4D_1199.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1199/Acq4D_1199.py")

