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
ScanStartLIST=[]
ScanStartSINO=[]
FrameStartSINO=[]
FrameStartLIST=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::: Running XRBB TC_2.9 Step 1215 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC_2.9 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to ':'
def split_time(line):
   list_string=line.split(':')
   return list_string

#---- count files in directory
def CountFiles(File , Path):
   num=[]
   for item in os.listdir(Path):
      if item.startswith(File):
        num.append(item)
   return len(num)

#--- find scan start time Tell2.9.SINO
def ScanStartTimeSINO():
   for line in open(PWD + "/Tell2.9.SINO0000", "r"):
     line = line.rstrip()
     if re.search('   Scan Start Time =', line):
       StartSINO = line.replace(line[:21], '')
       print StartSINO
       OnlyTime = split_string(StartSINO)
       ScanStartSINO.append(OnlyTime[3])

#--- find scan start time Tell2.9.List
def ScanStartTimeLIST():
   for line in open(PWD + "/Tell2.9.List", "r"):
     line = line.rstrip()
     if re.search('   Scan Start Time =', line):
       StartLIST = line.replace(line[:21], '')
       print StartLIST
       OnlyTime = split_string(StartLIST)
       ScanStartLIST.append(OnlyTime[3])

#--- find Frame start time Tell2.9.SINO
def FrameStartTimeSINO():
   for line in open(PWD + "/Tell2.9.SINO0000", "r"):
     line = line.rstrip()
     if re.search('   Frame Start Time =', line):
       StartSINO = line.replace(line[:22], '')
       print StartSINO
       OnlyTime = split_string(StartSINO)
       FrameStartSINO.append(OnlyTime[3])

#--- find Frame start time Tell2.9.SINO.List
def FrameStartTimeLIST():
   for line in open(PWD + "/Tell2.9.List", "r"):
     line = line.rstrip()
     if re.search('   Frame Start Time =', line):
       StartSINO = line.replace(line[:22], '')
       print StartSINO
       OnlyTime = split_string(StartSINO)
       FrameStartLIST.append(OnlyTime[3])

#---- check if other acqParams are identecal
def diffAcqParams():
   result1 =""
   result2 =""
   f1 = open(PWD+"/Tell2.9.SINO0000" , "r")
   f2 = open(PWD+"/Tell2.9.List" , "r")  
   for line1 in f1:
      if "acqParams" in line1:
         result1=line1
   for line2 in f2:
      if "acqParams" in line2:
         result2=line2
   if result1 != result2:
     return False

#--- check system geometry
def checkSysGeo():
   result1=""
   result2=""
   f1 = open(PWD+"/Tell2.9.SINO0000" , "r")
   f2 = open(PWD+"/Tell2.9.List" , "r")
   for line1 in f1:
      if "sysGeo" in line1:
         result1=line1
   for line2 in f2:
      if "sysGeo" in line2:
         result2=line2
   if result1 != result2:
     return False

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print



# ------------------------------------ step 1 --------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_9 = line.strip('\n')
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_LIST.txt" , "r")
  for line in f:
    ListsDirectory2_9 = line.strip('\n')
  print "Enter Sinograms path directory from" + BLUE + " section 9 :" +RESET + SinosDirectory2_9
  print "Enter LIST path directory from" + BLUE + " section 9 :" +RESET + ListsDirectory2_9

else:
  #use of raw_input() from user
  SinosDirectory2_9 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.9 :" + RESET)
  # while SinosDirectory2_9 is empty
  while SinosDirectory2_9 == "":
    SinosDirectory2_9 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.9 again:" + RESET)
  ListsDirectory2_9 = raw_input("Enter Lists path directory from" + BLUE + " section 2.9 :" + RESET)
  # while ListsDirectory2_9 is empty
  while ListsDirectory2_9 == "":
    ListsDirectory2_9 = raw_input("Enter Lists path directory from" + BLUE + " section 2.9 again:" + RESET)
 
#like echo to file
f=open("SINOSPath2_9.txt", "w+")
f.write(SinosDirectory2_9)
f.close()

#like echo to file
f=open("LISTSPath2_9.txt", "w+")
f.write(ListsDirectory2_9)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) a) Number of bins recorded in"+'\n'+"SSVP.PAC.Acq4D.1214" +RESET)
print (YELLOW + 'NOTE : Check manually previous step' + RESET)
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) b) Number of Sinogram files:" +RESET)
sum1 = CountFiles("SINO00", SinosDirectory2_9 )
print sum1
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of List Files:" +RESET)
sum2 = CountFiles("LIST", ListsDirectory2_9 )
print sum2
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the expected number of sinogram and list present" + '\n' + "in /petRDFS and /petLists dir?" +RESET)

if sum1 == 8 and sum2== 1:
  YesNo(True)
else:
  YesNo(False)
# ------------------------------------ step 2 --------------------------------------------
#perform rdfTeller to sinos from TC2.9
print ("Creating Tell2.9 for SINOS, please wait...")
os.system("rdfTeller -r  '-h  efadS -S -v'  -f Tell2.9 "+ SinosDirectory2_9 +"/SINO*")
print ("Creating Tell2.9Geo for SINOS, please wait...")
os.system("rdfTeller -r  '-h  g -v'  -f Tell2.9Geo "+ SinosDirectory2_9 +"/SINO*")
print

#perform rdfTeller to List from TC2.9
print ("Creating Tell2.9.List for ListFile, please wait...")
time.sleep(1)
os.system("rdfTell -h  efadS -v "+ ListsDirectory2_9 +"/* > Tell2.9.List")
print ("Creating Tell2.9Geo.List for ListFile, please wait...")
time.sleep(1)
os.system("rdfTell -h  g -v "+ ListsDirectory2_9 +"/* > Tell2.9Geo.List")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) The 'Scan Start Time' in Tell2.9.SINO0000" +RESET)
ScanStartTimeSINO()

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The 'Scan Start Time' in Tell2.9.List" +RESET)
ScanStartTimeLIST()

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the 'Scan Start Time' same in both the files?" +RESET)
if str(ScanStartSINO[0]) == str(ScanStartLIST[0]):
  YesNo(True)
else:
  YesNo(False)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The 'Frame Start Time' in Tell2.9.SINO0000" +RESET)
FrameStartTimeSINO()

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The 'Frame Start Time' in Tell2.9.List" +RESET)
FrameStartTimeLIST()

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the 'Frame Start Time' same in both the files?" +RESET)
if str(FrameStartSINO[0]) == str(FrameStartLIST[0]):
  YesNo(True)
else:
  YesNo(False)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Are RDF 'Acquisition Parameters' match in both the files?" +RESET)
x=True
x1 = diffAcqParams()
if x1 == False:
  x = False
YesNo(x)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Are all RDF 'System Geometry  Parameters' same in"+'\n'+"both the files?" +RESET)
x=True
x1 = checkSysGeo()
if x1 == False:
  x = False
YesNo(x)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1215")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1216/Acq4D_1216.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1216/Acq4D_1216.py")

