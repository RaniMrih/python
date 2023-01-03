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
CoincList = []
DurationList =[]
EndTimeList=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_16_1/Acq4D.1318'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::: Running XRBB TC_2.16.1 Step 1318 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.16.1 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- count files in directory
def CountFiles(File , Path):
   num=[]
   for item in os.listdir(Path):
      if item.startswith(File):
        num.append(item)
   return len(num)

#---- count files in directory
def CountFiles1(File , Path):
   num=[]
   for item in os.listdir(Path):
      if item.startswith(File) and item.endswith('.BLF'):
        num.append(item)
   return len(num)

#--- find Frame start time Coinc
def findCoincMsec():
   for line in open(PWD + "/SSVP.PAC.Acq4D.1318_RecordedData" , "r"):
      line = line.rstrip()
      if re.search('(Coinc msec)', line):
        Coinc = line.replace(line[:54], '')
        CoincList.append(Coinc)

#---- find sino frame duration
def findFrameDuration():
   for line in open(PWD + "/SSVP.PAC.Acq4D.1318_RecordedData" , "r"):
      line = line.rstrip()
      if re.search('Frame Dur', line):
        line1=split_string(line)
        DurationList.append(line1[8])

#---- find End Time
def findEndTime():
   within_1sec = True
   for i in range (0,10):
     sum = int(CoincList[i]) + int(DurationList[i])
     EndTimeList.append(sum)
     time.sleep(0.1)
     print ("bed " + str(i) + ": " + str(sum))

#---- find if end time less than Coinc msec)
def findEndToFrameTime():
   diff = True
   for i in range (0,9):
      if EndTimeList[i] > CoincList[i+1]:
        diff = False
   YesNo(diff)


# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_16_1 = line.strip('\n')
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_LIST.txt" , "r")
  for line in f:
    ListsDirectory2_16_1 = line.strip('\n')
  print "Enter Sinogram path directory from" + BLUE + " section 2.16.1 :" +RESET + SinosDirectory2_16_1
  print "Enter LIST path directory from" + BLUE + " section 2.16.1 :" +RESET + ListsDirectory2_16_1

else:
  # ---------------------------------------------------------------------------------------
  #use of raw_input() from user from cmd
  SinosDirectory2_16_1 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.16.1 :" + RESET)
  # while SinosDirectory2_16_1 is empty
  while SinosDirectory2_16_1 == "":
    SinosDirectory2_16_1 = raw_input("Enter Sinogram path directory from" + BLUE + "  section 2.16.1 :" + RESET)
  # ---------------------------------------------------------------------------------------
  ListsDirectory2_16_1 = raw_input("Enter List path directory from" + BLUE + " section 2.16.1 :" + RESET)
  while ListsDirectory2_16_1 == "":
    ListsDirectory2_16_1 = raw_input("Enter List path directory from" + BLUE + " section 2.16.1 :" + RESET)

#like echo to file
f=open("SINOSPath2_16_1.txt", "w+")
f.write(SinosDirectory2_16_1)
f.close()

#like echo to file
f=open("LISTSPath2_16_1.txt", "w+")
f.write(ListsDirectory2_16_1)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt")
# ------------------------------------ step 4 (first) --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the Scan Completed Normally ?" +RESET)
print "[ ] Yes"
print "[ ] No"

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "4) Number of :" +RESET)
print (BLUE + "Number of Sinogram Files :" +RESET)
SumSinos=CountFiles("SINO000" , SinosDirectory2_16_1)
print SumSinos
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of LIST Files :" +RESET)
SumLists=CountFiles1("LIST000" , ListsDirectory2_16_1)
print SumLists
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Are there 10 Sinogram Files, with filenames "+'\n'+"(SINO0000, SINO0001..... SINO0009) ?" +RESET)
if SumSinos == 10 :
  YesNo(True)
else:
  YesNo(False)
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Are there 10 LIST Files, with filenames "+'\n'+"(LIST0000.BLF, LIST0001.BLF....... LIST0009.BLF) ?" +RESET)
if SumLists == 10 :
  YesNo(True)
else:
  YesNo(False)
# ------------------------------------ step 5 --------------------------------------------

print "Creating Tell2.16.1 for 10 Sinos, please wait..."
os.system("rdfTeller -r '-hf -S' -f Tell2.16.1 "+SinosDirectory2_16_1+"/SINO*")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "5) Is the 'recordedData' file labeled with  "+'\n'+"SSVP.PAC.Acq4D.1318 attached with this test case ?" +RESET)
os.system("egrep 'totalPrompts|   Segment ID\(SegGroup 1,Layout 5\) DS 0 Total Counts|   Segment ID\(SegGroup 1,Layout 5\) DS 1 Total Counts|Frame Start Time \(Coinc msec\)|Frame Duration' Tell2.16.1.SINO* > recordedData")
os.system("mv recordedData SSVP.PAC.Acq4D.1318_RecordedData")
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE: SSVP.PAC.Acq4D.1318_Recorded data located at: ~/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_16_1/Acq4D.1381' + RESET)
print

# ------------------------------------ step 6 --------------------------------------------
# --- EndTime = "Frame Start Time (Coinc msec)" + Frame Duration
#----------- qustion ---------
time.sleep(1)
print (BLUE + "End Time for beds :" +RESET)
findCoincMsec()
findFrameDuration()
findEndTime()

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the 'EndTime' for each bed is less than the  "+'\n'+"Frame Start Time (Coinc msec) of next bed ?" +RESET)
findEndToFrameTime()

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1318")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_16_1/Acq4D.1319/Acq4D_1319.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_16_1/Acq4D.1319/Acq4D_1319.py")


