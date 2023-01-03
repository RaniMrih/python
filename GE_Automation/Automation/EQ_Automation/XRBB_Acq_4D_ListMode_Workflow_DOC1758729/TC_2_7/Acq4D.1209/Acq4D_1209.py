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
sinosList2_4 = ["00","09","12","15"]
sinosList2_6 = ["00","45","60","90"]
sinosList2_7 = ["00"]
ScanStartLive=[]
ScanStartReplay=[]
FrameStartLive=[]
FrameStartReplay=[]
ReplayDurationList=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1209'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::: Running XRBB TC_2.4 Step 1209 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.7 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to  ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string

#--- find scan start time Replay
def ScanStartTimeReplay():
   for i in sinosList2_7:
     for line in open(PWD + "/Tell2.7", "r"):
       line = line.rstrip()
       if re.search('   Scan Start Time =', line):
         ScanStart2 = line.replace(line[:21], '')
         print ScanStart2
         OnlyTime2 = split_time(ScanStart2)
         OnlyTime2 = split_string(OnlyTime2[2])
         ScanStartReplay.append(OnlyTime2[0])

#--- find Frame start time Replay
def FrameStartTimeReplay():
   for i in sinosList2_7:
     for line in open(PWD + "/Tell2.7", "r"):
       line = line.rstrip()
       if re.search('   Frame Start Time =', line):
         FrameStart2 = line.replace(line[:22], '')
         print FrameStart2
         OnlyTime2 = split_time(FrameStart2)
         OnlyTime2 = split_string(OnlyTime2[2])
         FrameStartReplay.append(OnlyTime2[0])

#--- find Frame Duration Replay Scan
def FrameDurationReplay():
   for i in sinosList2_7:
     for line in open(PWD + "/Tell2.7", "r"):
       line = line.rstrip()
       if re.search('Frame Duration', line):
         ReplayDuration = line.replace(line[:21], '')
         print ReplayDuration
         OnlyDuration2 = split_string(ReplayDuration)
         ReplayDurationList.append(OnlyDuration2[1])

#--- find if diff between Scan and Frame within 1 sec
def Diff_Scan_Frame():
   within_1sec = True
   for i in range (0,1):
     diffScan = int(ScanStartReplay[i]) - int(FrameStartReplay[i])
     if diffScan > 1 or diffScan < -1:
       within_1sec = False
   YesNo(within_1sec)

def Duration_Within10k():
   within_10k = True
   for i in range (0,1):
     if int(ReplayDurationList[i]) > 100000:
       within_10k = False
   YesNo(within_10k)

# ------------------------------------ step 1 --------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_7 = line.strip('\n')
  print "Enter Sinogram path directory from" + BLUE + " section 2.7 :" +RESET + SinosDirectory2_7

else:
  #use of raw_input() from user
  SinosDirectory2_7 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.7 :" + RESET)
  # while SinosDirectory2_6 is empty
  while SinosDirectory2_7 == "":
    SinosDirectory2_7 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.7 again:" + RESET)

#like echo to file
f=open("SINOSPath2_7.txt", "w+")
f.write(SinosDirectory2_7)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")

#perform rdfTeller to sinos from TC2.4  
print
print ("Creating Tell2.7 for SINO, please wait...")
os.system("rdfTell -h efadgS -v -S "+ SinosDirectory2_7 +"/SINO* > Tell2.7")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Scan Start Time :" +RESET)
ScanStartTimeReplay()
print (BLUE + "Frame Start Time :" +RESET)
FrameStartTimeReplay()
print (BLUE + "Frame Duration:" +RESET)
FrameDurationReplay()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is the 'Scan Start Time' and 'Frame Start" +'\n'+"Time' is within 1 second ?" +RESET)
Diff_Scan_Frame()

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is the 'Frame Duaration' is within 100000" +'\n'+"+/-10 milliseconds ?" +RESET)
Duration_Within10k()

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1209")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1210/Acq4D_1210.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_7/Acq4D.1210/Acq4D_1210.py")
