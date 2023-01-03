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
LiveTotal=[]
LiveDelays=[]
LiveDurationList=[]
ReplayTotal=[]
ReplayDelays=[]
ReplayDurationList=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1168'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1165'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.2 Step 1168 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  '='
def split_string3(line):
   list_string=line.split('=')
   return list_string


#--- find Total Prompts live Scan
def LiveTotalPrompts():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   totalPrompts     =', line):
       LivePrompts = split_string3(line)
       LiveTotal.append(LivePrompts[1])

#--- find Total Prompts Replay Scan
def ReplayTotalPrompts():
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   totalPrompts     =', line):
       ReplayPrompts = split_string3(line)
       ReplayTotal.append(ReplayPrompts[1])

#--- find Total Delays live Scan
def LiveTotalDelays():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('totalDelays', line):
       Live = split_string2(line)
       LiveDelays.append(Live[1])

#--- find Total Delays Replay Scan
def ReplayTotalDelays():
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
     line = line.rstrip()
     if re.search('totalDelays', line):
       Replay = split_string2(line)
       ReplayDelays.append(Replay[1])

#--- find Frame Duration Live Scan
def FrameDurationLive():
   for line in open(TC_start_2_1 + "/S2.1Sino.txt", "r"):
      line = line.rstrip()
      if re.search('Frame Duration', line):
        ReplayDuration = line.replace(line[:21], '')
        OnlyDuration2 = split_string(ReplayDuration)
        LiveDurationList.append(OnlyDuration2[1])

#--- find Frame Duration Replay Scan
def FrameDurationReplay():
   for line in open(TC_start + "/S2.2Sino.txt", "r"):
      line = line.rstrip()
      if re.search('Frame Duration', line):
        ReplayDuration = line.replace(line[:21], '')
        OnlyDuration2 = split_string(ReplayDuration)
        ReplayDurationList.append(OnlyDuration2[1])

# ------------------------------------ step 1 --------------------------------------------
# ------------------------------------ Bed 1  --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "1)"+'\n'+"::::: Bed 1 :::::"+'\n\n'+"totalPrompts for original (live) scan :" +RESET)
LiveTotalPrompts()
print LiveTotal[0].replace(LiveTotal[0][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "totalPrompts for replay (live) scan :" +RESET)
ReplayTotalPrompts()
print ReplayTotal[0].replace(LiveTotal[0][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Total Prompts Difference :" +RESET)
diff = int(LiveTotal[0]) - int(ReplayTotal[0])
if diff < 0:
  diff*=-1
print diff

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "totalDelays for original (live) scan:" +RESET)
LiveTotalDelays()
print LiveDelays[0].replace(LiveDelays[0][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "totalDelays for replay (live) scan:" +RESET)
ReplayTotalDelays()
print ReplayDelays[0].replace(ReplayDelays[0][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Total Delays Difference:" +RESET)
diff = int(LiveDelays[0]) - int(ReplayDelays[0])
if diff < 0:
  diff*=-1
print diff

# Prompt Rate = Total Prompts / Frame Duration  (in counts per millisecond)
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Prompt Rate for Original scan :" +RESET)
FrameDurationLive()
LiveRate= float(LiveTotal[0]) / float(LiveDurationList[0])
print str(LiveRate) + " cnts/ms"
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Prompt Rate for Replay scan:" +RESET)
FrameDurationReplay()
ReplayRate=  float(ReplayTotal[0]) / float(ReplayDurationList[0])
print str(ReplayRate) + " cnts/ms"

# ------------------------------------ Bed 2  --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "::::: Bed 2 :::::"+'\n\n'+"totalPrompts for original (live) scan :" +RESET)
LiveTotalPrompts()
print LiveTotal[1].replace(LiveTotal[1][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "totalPrompts for replay (live) scan :" +RESET)
ReplayTotalPrompts()
print ReplayTotal[1].replace(LiveTotal[1][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Total Prompts Difference :" +RESET)
diff = int(LiveTotal[1]) - int(ReplayTotal[1])
if diff < 0:
  diff*=-1
print diff

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "totalDelays for original (live) scan:" +RESET)
LiveTotalDelays()
print LiveDelays[1].replace(LiveDelays[1][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "totalDelays for replay (live) scan:" +RESET)
ReplayTotalDelays()
print ReplayDelays[1].replace(ReplayDelays[1][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Total Delays Difference:" +RESET)
diff = int(LiveDelays[1]) - int(ReplayDelays[1])
if diff < 0:
  diff*=-1
print diff

# Prompt Rate = Total Prompts / Frame Duration  (in counts per millisecond)
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Prompt Rate for Original scan :" +RESET)
FrameDurationLive()
LiveRate= float(LiveTotal[1]) / float(LiveDurationList[1])
print str(LiveRate) + " cnts/ms"
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Prompt Rate for Replay scan:" +RESET)
FrameDurationReplay()
ReplayRate=  float(ReplayTotal[1]) / float(ReplayDurationList[1])
print str(ReplayRate) + " cnts/ms"

# ------------------------------------ Bed 3  --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "::::: Bed 3 :::::"+'\n\n'+"totalPrompts for original (live) scan :" +RESET)
LiveTotalPrompts()
print LiveTotal[2].replace(LiveTotal[2][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "totalPrompts for replay (live) scan :" +RESET)
ReplayTotalPrompts()
print ReplayTotal[2].replace(LiveTotal[2][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Total Prompts Difference :" +RESET)
diff = int(LiveTotal[2]) - int(ReplayTotal[2])
if diff < 0:
  diff*=-1
print diff

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "totalDelays for original (live) scan:" +RESET)
LiveTotalDelays()
print LiveDelays[2].replace(LiveDelays[2][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "totalDelays for replay (live) scan:" +RESET)
ReplayTotalDelays()
print ReplayDelays[2].replace(ReplayDelays[2][:1],"")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Total Delays Difference:" +RESET)
diff = int(LiveDelays[2]) - int(ReplayDelays[2])
if diff < 0:
  diff*=-1
print diff

# Prompt Rate = Total Prompts / Frame Duration  (in counts per millisecond)
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Prompt Rate for Original scan :" +RESET)
FrameDurationLive()
LiveRate= float(LiveTotal[2]) / float(LiveDurationList[2])
print str(LiveRate) + " cnts/ms"
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Prompt Rate for Replay scan:" +RESET)
FrameDurationReplay()
ReplayRate=  float(ReplayTotal[2]) / float(ReplayDurationList[2])
print str(ReplayRate) + " cnts/ms"

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) ABS(Original - Replay Total Prompts) is  <= 0.05"+'\n'+"* (the greater of the original or the replay Prompts) :" +RESET)
Grater = int(LiveTotal[0])
if int(ReplayTotal[0]) > int(LiveTotal[0]) :
  Grater =  int(ReplayTotal[0])

sum = int(LiveTotal[0]) - int(ReplayTotal[0])
if sum < 0 :
  sum*=-1

if float(sum) > 0.05 * float(Grater):
  YesNo(False)
else:
  YesNo(True)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) ABS(Original - Replay Total Delays) is  <= 0.05"+'\n'+"* (the greater of the original or the replay Delays) :" +RESET)
Grater = int(LiveDelays[0])
if int(ReplayDelays[0]) > int(LiveDelays[0]) :
  Grater =  int(ReplayDelays[0])

sum = int(LiveDelays[0]) - int(ReplayDelays[0])
if sum < 0 :
  sum*=-1

if float(sum) > 0.05 * float(Grater):
  YesNo(False)
else:
  YesNo(True)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1168")
os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1171/Acq4D_1171.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1171/Acq4D_1171.py")





