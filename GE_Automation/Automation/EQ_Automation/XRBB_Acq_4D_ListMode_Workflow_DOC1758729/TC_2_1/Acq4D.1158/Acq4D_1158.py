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
Phys2List=[]
TimeMarkersList=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1158'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.1 Step 1158 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- find time markers
def findTimeMarks():
   for i in range(0,3):
      for line in open(TC_start + "/ListOut_f"+str(i)+".txt" , "r"):
         line = line.rstrip()
         if re.search('Time Markers:', line):
           line1=split_string(line)
           TimeMarkersList.append(line1[2])

#---- find Phys2
def findPhys2():
   for i in range(0,3):
      for line in open(TC_start + "/ListOut_f"+str(i)+".txt" , "r"):
         line = line.rstrip()
         if re.search('Phys2', line):
           line1=split_string(line)
           Phys2List.append(line1[11])

#---- Count TOF in TOF.txt file
def countTOF():
   TOFList=[]
   for line in open(TC_start + "/TOF.txt" , "r"):
     line = line.rstrip()
     if re.search('TOF', line):
       TOFList.append(line)  
   return TOFList

# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1a) The list file 'Time Markers' per list is:" +RESET)
findTimeMarks()
for i in range (0,3):
  print "LIST000"+str(i)+" : "+ str(TimeMarkersList[i])

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "'Time Markers' for the first (bed loc) list file is at"+'\n'+"least 129000 but less than 131000 ?" +RESET)
if int(TimeMarkersList[0]) > 131000 or int(TimeMarkersList[0]) < 129000:
  YesNo(False)
else:
  YesNo(True)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "'Time Markers' for the 2nd & 3rd (bed loc) list"+'\n'+"files is at least 99000 but less than 101000 ?" +RESET)
if int(TimeMarkersList[1]) > 101000 or int(TimeMarkersList[1]) < 99000 or int(TimeMarkersList[2]) > 101000 or int(TimeMarkersList[2]) < 99000:
  YesNo(False)
else:
  YesNo(True)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "1b) The list file 'Phys2' per list is:" +RESET)
findPhys2()
for i in range (0,3):
  print "LIST000"+str(i)+" : "+ str(Phys2List[i])

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Total 'Phys2 (Respiratory) Triggers' for the first "+'\n'+"(bed loc) list file are > 120 but less than 135 ?" +RESET)
if int(Phys2List[0]) > 135 or int(Phys2List[0]) < 120:
  YesNo(False)
else:
  YesNo(True)
 
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Total 'Phys2 (Respiratory) Triggers' for the 2nd & "+'\n'+"3rd (bed loc) list file are > 90 but less than 105 ?" +RESET)
if int(Phys2List[1]) > 105 or int(Phys2List[1]) < 90 or int(Phys2List[2]) > 105 or int(Phys2List[2]) < 90:
  YesNo(False)
else:
  YesNo(True)

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Is the evidence of TOF info per Prompt"+'\n'+"inspected, including TOF values that are changing?" +RESET)

# grep Lists  path
f = open( TC_start+"/LISTSPath2_1.txt" , "r")
for line in f:
  Listspath = line

os.system("ssh ctuser@par ListDecode "+Listspath+"/LIST0000.BLF | head -40 >TOF.txt")
os.system("ssh ctuser@par ListDecode "+Listspath+"/LIST0001.BLF | head -40 >>TOF.txt")
os.system("ssh ctuser@par ListDecode "+Listspath+"/LIST0002.BLF | head -40 >>TOF.txt")

NumTOF = countTOF()
if len(NumTOF)==117:
  YesNo(True)
else:
  YesNo(False)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1158")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1159/Acq4D_1159.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1159/Acq4D_1159.py")

