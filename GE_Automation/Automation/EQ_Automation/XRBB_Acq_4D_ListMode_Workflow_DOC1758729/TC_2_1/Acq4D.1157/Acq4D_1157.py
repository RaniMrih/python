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
CoincList=[]
ScanStartSINO=[]
TimeMarkList=[]
FrameStartSINO=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1157'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.1 Step 1157 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#--- find scan start time
def ScanStartTimeSINO():
   for line in open(TC_start + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   Scan Start Time =', line):
       StartSINO = line.replace(line[:21], '')
       ScanStartSINO.append(StartSINO)

#--- find Frame start time
def FrameStartTimeSINO():
   for line in open(TC_start + "/S2.1Sino.txt", "r"):
     line = line.rstrip()
     if re.search('   Frame Start Time =', line):
       StartSINO = line.replace(line[:22], '')
       FrameStartSINO.append(StartSINO)

#--- find Frame start time Coinc
def findCoincMsec():
   for line in open(TC_start + "/S2.1Sino.txt" , "r"):
      line = line.rstrip()
      if re.search('(Coinc msec)', line):
        Coinc = line.replace(line[:34], '')
        CoincList.append(Coinc)

#--- find First time mark
def findFirstTimeMark():
   for i in range(0,3):
      for line in open(TC_start + "/ListOut_f"+str(i)+".txt" , "r"):
         line = line.rstrip()
         if re.search('First Time Mark', line):
           line1=split_string(line)
           TimeMarkList.append(line1[3])


# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Scan Start Time : " +RESET)
ScanStartTimeSINO()
print ScanStartSINO[0]

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Frame Start Time : " +RESET)
FrameStartTimeSINO()
print FrameStartSINO[0]

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Scan Start Time - Frame Start Time = " +RESET)
#Time1= split_string(ScanStartSINO[0])
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
print diff

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The Acquisition Start Time of the first "+'\n'+"frame is 30 second after the scan start time?" +RESET)
if diff == 30:
  YesNo(True)
else:
  YesNo(False)

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Frame Start Time (Coinc msec) in msec"+'\n'+"for each frame:" +RESET)
findCoincMsec()
for i in range (0,3):
  print "Frame "+str(i+1)+": "+ str(CoincList[i])
# ------------------------------------ step 3 --------------------------------------------
# grep sinos  path
f = open( TC_start+"/LISTSPath2_1.txt" , "r")
for line in f:
  Listspath = line
print
print "Creating ListOut_f0.txt, ListOut_f1.txt' ListOut_f2.txt, please wait ..."
os.system("ssh ctuser@par ListDecode -s "+Listspath+"/LIST0000.BLF >ListOut_f0.txt")
os.system("ssh ctuser@par ListDecode -s "+Listspath+"/LIST0001.BLF >ListOut_f1.txt")
os.system("ssh ctuser@par ListDecode -s "+Listspath+"/LIST0002.BLF >ListOut_f2.txt")
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "3) 'First Time Mark' im msec for each"+'\n'+"frame:" +RESET)
findFirstTimeMark()
for i in range (0,3):
  print "Frame "+str(i+1)+": "+ str(TimeMarkList[i])

# ------------------------------------ step 4 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "4) The absolute difference in between the 'First Time'"+'\n'+"Time Mark' in the List file and the the 'Frame Start "+RESET)
print (BLUE + "Time (Coinc msec)' of the sinogram file, per Frame is:" +RESET)
results=[]
for i in range (0,3):
  diff=int(CoincList[i])-int(TimeMarkList[i])
  results.append(diff)
  print "Frame "+str(i+1)+": "+ str(diff)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "For Frame 1:" +RESET)
print (BLUE + "Is the difference between the 'First Time Mark' in"+'\n'+"List file and 'Frame Start Time (Coinc msec)' in  "+RESET)
print (BLUE + "sinogram file is 30,000 (+/- 5) msec?" +RESET)
if results[0] > 30005 or results[0]<29995:
  YesNo(False)
else:
  YesNo(True)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "For Frame 2 and 3:" +RESET)
print (BLUE + "Is the difference between the 'First Time Mark' in"+'\n'+"List file and 'Frame Start Time (Coinc msec)' in  "+RESET)
print (BLUE + "sinogram file is <= 5msec ?" +RESET)
if results[1] > 5 or results[1]<-5 or results[2] > 5 or results[2] < -5:
  YesNo(False)
else:
  YesNo(True)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1157")


os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1158/Acq4D_1158.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1158/Acq4D_1158.py")

