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
Block_MAX_Live_List =[]
Block_MAX_Replay_List =[]
sinosList2_4 = ["00","09","12","15"]
sinosList2_6 = ["00","45","60","90"]
ScanStartLive=[]
ScanStartReplay=[]
FrameStartLive=[]
FrameStartReplay=[]
LiveCoincList=[]
ReplayCoincList=[]
Step_Pass=True
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_6/Acq4D.1204'
SinoPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/SINOSPath2_4.txt'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/LISTSPath2_4.txt'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.6 Step 1204 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.6 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- count files in directory
def CountFiles(Tell,Path):
   num=[]
   for item in os.listdir(Path):
      if item.startswith(Tell):
        num.append(item)
   return len(num)

#--- find scan start time live
def ScanStartTimeLive():
   for i in sinosList2_4:
     for line in open(PWD + "/Tell2.4.SINO00" + i, "r"):
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
   for i in sinosList2_6:
     for line in open(PWD + "/Tell2.6.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('   Scan Start Time =', line):
         ScanStart2 = line.replace(line[:21], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print ScanStart2
         OnlyTime2 = split_time(ScanStart2)
         OnlyTime2 = split_string(OnlyTime2[2])
         ScanStartReplay.append(OnlyTime2[0])

#--- find if diff between Scan start Live/Replay within 1 sec
def Diff_Scan_Start():
   within_1sec = True
   for i in range (0,4):
     diffScanStart = int(ScanStartLive[i]) - int(ScanStartReplay[i])
     if diffScanStart > 1 or diffScanStart < -1:
       within_1sec = False
   YesNo(within_1sec)

#--- find Frame start time Coinc Live
def CoincTimeLive():
   for i in sinosList2_4:
     for line in open(PWD + "/Tell2.4.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('(Coinc msec)', line):
         LiveCoinc = line.replace(line[:35], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print "Coinc msec= " + LiveCoinc
         LiveCoincList.append(LiveCoinc)

#--- find Frame start time Coinc Replay
def CoincTimeReplay():
   for i in sinosList2_6:
     for line in open(PWD + "/Tell2.6.SINO00" + i, "r"):
       line = line.rstrip()
       if re.search('(Coinc msec)', line):
         ReplayCoinc = line.replace(line[:35], '')
         print (BLUE + "Frame "+i+" :" +RESET)
         print "Coinc msec= " + ReplayCoinc
         ReplayCoincList.append(ReplayCoinc)

#--- find if diff between Live and Replay Coinic within 5 msec
def Diff_Coinc_Time():
   within_10msec = True
   for i in range (0,4):
     diffConic = int(LiveCoincList[i]) - int(ReplayCoincList[i])
     if diffConic > 10 or diffConic < -10:
       within_10msec = False
   YesNo(within_10msec)

# ------------------------------------ step 1 --------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_6 = line.strip('\n')
  print "Enter Sinograms path directory from" + BLUE + " section 2.6 :" +RESET + SinosDirectory2_6

else:
  #use of raw_input() from user
  SinosDirectory2_6 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.6 :" + RESET)
  # while SinosDirectory2_6 is empty
  while SinosDirectory2_6 == "":
    SinosDirectory2_6 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.6 again:" + RESET)

#like echo to file
f=open("SINOSPath2_6.txt", "w+")
f.write(SinosDirectory2_6)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")

# grep sinos path from 1189 TC.2.4
f = open( SinoPath2_4 , "r")
for line in f:
  path = line

#perform rdfTeller to sinos from TC2.4  
print
print ("Creating Tell2.4 and for all SINOS form TC.2.4, please wait...")
os.system("rdfTeller -r  '-h  efadgS -S'  -f Tell2.4 "+ path +"/SINO*")
print

#perform rdfTeller to sinos from TC2.4  
print
print ("Creating Tell2.6 and for all SINOS form TC.2.6, please wait...")
os.system("rdfTeller -r  ' -h  efadgS -S'  -f Tell2.6  "+ SinosDirectory2_6 +"/SINO*")

#----------- qustion ---------
time.sleep(1)
print (BLUE + "1) Number of Tell2.4.SINO* text files:"+RESET)
sum = CountFiles("Tell2.4.SINO00", PWD )
print sum
print 

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Able to generate 16 Tell2.4.SINO* text files ?"+RESET)
if sum == 16:
  YesNo(True)
else:
  YesNo(False)

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Number of Replay sino files:"+RESET)
sum1 = CountFiles("SINO" ,SinosDirectory2_6 )
print sum1
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is there 100 SINO files in the scan directory ?"+RESET)
if sum1 == 100:
  YesNo(True)
else:
  YesNo(False)
# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) Number of Tell2.6.SINO* text files:"+RESET)
sum2 = CountFiles("Tell2.6.SINO00" ,PWD )
print sum2
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Able to generate a 100 Tell2.6.SINO* text files ?"+RESET)
if sum2  == 100:
  YesNo(True)
else:
  YesNo(False)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "4) Time-Of-Day (hh:mm:ss) of Section 2.4 Live Dyn Scan:"+RESET)
print (BLUE + "Scan Start Time:"+RESET)
ScanStartTimeLive()

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "Time-Of-Day (hh:mm:ss) of Section 2.6 Replay Dyn Scan:"+RESET)
print (BLUE + "Scan Start Time:"+RESET)
ScanStartTimeReplay()

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "'Scan Start Time' of the selected respective"+RESET)
print (BLUE + "frames are within 1 second?"+RESET)
Diff_Scan_Start()

#----------- qustion ---------
time.sleep(1)
print (BLUE + "'Frame Start Time (Coinc msec)' timestamp of" +'\n'+"Section 2.4 live Dyn scan" +RESET)
print (BLUE + "Frame Start Time (Coinc msec):"+RESET)
CoincTimeLive()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "'Frame Start Time (Coinc msec)' timestamp of" +'\n'+"Section 2.6 Replay Dyn scan" +RESET)
print (BLUE + "Frame Start Time (Coinc msec):"+RESET)
CoincTimeReplay()
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The 'Frame Start Time (Coinc msec)' "+'\n'+"timestamp of the respective frames are"+RESET)
print (BLUE + "within 10 millisecond?"+RESET)
Diff_Coinc_Time()

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1204")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_6/Acq4D.1206/Acq4D_1206.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_6/Acq4D.1206/Acq4D_1206.py")





