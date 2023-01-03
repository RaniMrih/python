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
Duration2_9=[]
Duration2_10=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_10/Acq4D.1223'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_10/Acq4D.1223'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::: Running XRBB TC_2.10 Step 1223 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC_2.10 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#--- find Frame Duration from Tell2.9
def FrameDuration2_9():
   for line in open(PWD + "/Tell2.9.SINO0000", "r"):
     line = line.rstrip()
     if re.search('Frame Duration', line):
       ReplayDuration = line.replace(line[:21], '')
       OnlyDuration = split_string(ReplayDuration)
       Duration2_9.append(OnlyDuration[1])

#--- find Frame Duration from Tell2.10
def FrameDuration2_10():
   for line in open(PWD + "/Tell2.10.SINO0000", "r"):
     line = line.rstrip()
     if re.search('Frame Duration', line):
       ReplayDuration = line.replace(line[:21], '')
       OnlyDuration = split_string(ReplayDuration)
       Duration2_10.append(OnlyDuration[1])

#---- check if acqParams are identecal except landmark
def diffAcqParams():
   result1 =""
   result2 =""
   f1 = open(PWD+"/Tell2.9.SINO0000" , "r")
   f2 = open(PWD+"/Tell2.10.SINO0000" , "r")
   for line1 in f1:
     if "acqParams" in line1:
       if "AcqLandmarkParams." in line1:
         continue
       else:
         result1=line1
   for line2 in f2:
     if "acqParams" in line2:
       if "AcqLandmarkParams." in line2:
         continue
       else:
         result2=line2
   if result1 != result2:
     return False
   else:
     return True

#---- check landmark identecal
def difflandmark():
   result1 =""
   result2 =""
   f1 = open(PWD+"/Tell2.9.SINO0000" , "r")
   f2 = open(PWD+"/Tell2.10.SINO0000" , "r")
   for line1 in f1:
     if "AcqLandmarkParams." in line1:
       result1=line1
   for line2 in f2:
     if "AcqLandmarkParams." in line2:
       result2=line2
   if result1 != result2:
     return False
   else:
     return True

#--- check system geometry
def checkSysGeo():
   result1=""
   result2=""
   f1 = open(PWD+"/Tell2.9Geo.SINO0000" , "r")
   f2 = open(PWD+"/Tell2.10Geo.SINO0000" , "r")
   for line1 in f1:
      if "sysGeo" in line1:
         result1=line1
   for line2 in f2:
      if "sysGeo" in line2:
         result2=line2
   if result1 != result2:
     return False
   else:
     return True

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

# ---------------------------------------------------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_10 = line.strip('\n')
  print "Enter Sinogram path directory from" + BLUE + " section 2.10 :" +RESET + SinosDirectory2_10
else:
  #use of raw_input() from user
  SinosDirectory2_10 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.10 :" + RESET)
  # while SinosDirectory2_10 is empty
  while SinosDirectory2_10 == "":
    SinosDirectory2_10 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.10 again:" + RESET)

#like echo to file
f=open("SINOSPath2_10.txt", "w+")
f.write(SinosDirectory2_10)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")

# ------------------------------------ step 2 (first) --------------------------------------------
#perform rdfTeller to sinos from TC2.10
print
print ("Creating Tell2.10 for SINOS, please wait...")
os.system("rdfTeller -r  '-h  efadS -S -v'  -f Tell2.10 "+ SinosDirectory2_10 +"/SINO*")
print ("Creating Tell2.10Geo for SINOS, please wait...")
os.system("rdfTeller -r  '-h  g -v'  -f Tell2.10Geo "+ SinosDirectory2_10 +"/SINO*")
print
os.system("cp /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_9/Acq4D.1215/Tell2.9* /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_10/Acq4D.1223")

#----------- qustions ---------
time.sleep(1)
print (BLUE + "2) Is the 'Frame Durations' matches in both scans?" + RESET)
FrameDuration2_9()
FrameDuration2_10()
if Duration2_9[0] == Duration2_10[0]:
  YesNo(True)
else :
  YesNo(False)

#----------- qustions ---------
time.sleep(1)
print (BLUE + "Are the 'Acquisition Parameters' matching for all the parameters ?" + RESET)
x= diffAcqParams()
YesNo(x)

#----------- qustions ---------
time.sleep(1)
print (BLUE + "Note: "+'\n'+"acqParams.RDFAcqLandmarkParams.landmarkDateTi"+'\n'+"me may or may not match." + RESET)
x= difflandmark()
YesNo(x)

#----------- qustions ---------
time.sleep(1)
print (BLUE + "Are the 'System Geometry Parameters' matches?   " + RESET)
x= checkSysGeo()
YesNo(x)

#-- determine if step Pass/Fail
Step_Result("Acq4D.1223")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_10/Acq4D.1384/Acq4D_1384.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_10/Acq4D.1384/Acq4D_1384.py")

