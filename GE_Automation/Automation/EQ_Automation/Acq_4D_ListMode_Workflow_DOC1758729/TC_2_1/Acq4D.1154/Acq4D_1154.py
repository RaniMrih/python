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
SinosNum=[]
ListsNum=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'

print
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::::::: Running DMI TC_2.1 Step 1154 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.1 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- count files in directory
def CountFiles(File , Path):
   num=[]
   if File == "SINO00":
     for item in os.listdir(Path):
        if item.startswith(File):
          num.append(item)
          SinosNum.append(item)
     return len(num)
   elif File == "LIST00":
     for item in os.listdir(Path):
        if item.startswith(File):
          num.append(item)
          ListsNum.append(item)
     return len(num)

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                       ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                       ---- Step "+StepNum+" Passed ----" + RESET)
     print

#------------------------------------- step 1 -----------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_1 = line.strip('\n')
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_LIST.txt" , "r")
  for line in f:
    ListsDirectory2_1 = line.strip('\n')
  print "Enter Sinograms path directory from" + BLUE + " section 2.1 :" +RESET + SinosDirectory2_1
  print "Enter LIST path directory from" + BLUE + " section 2.1 :" +RESET + ListsDirectory2_1
else:
  #use of raw_input()
  SinosDirectory2_1 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.1 :" + RESET)
  # while SinosDirectory2_1 is empty
  while SinosDirectory2_1 == "":
    SinosDirectory2_1 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.1 again:" + RESET)
  ListsDirectory2_1 = raw_input("Enter Lists path directory from" + BLUE + " section 2.1 :" + RESET)
  # while ListsDirectory2_4 is empty
  while ListsDirectory2_1 == "":
    ListsDirectory2_1 = raw_input("Enter Lists path directory from" + BLUE + " section 2.1 again:" + RESET)

print
# like : echo $SinosDirectory2_4 > SINOSPath2_4.txt
f=open("SINOSPath2_1.txt", "w+")
f.write(SinosDirectory2_1)
f.close()
f=open("LISTSPath2_1.txt", "w+")
f.write(ListsDirectory2_1)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt")
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Scan Completed normally ?" +RESET)
print "[ ] Yes"
print "[ ] No"

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of Sinogram Files:" +RESET)
sumSinos = CountFiles("SINO00", SinosDirectory2_1 )
print sumSinos

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The name of Sinogram Files present :" +RESET)
for item in SinosNum:
  print str(item)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is there a 3 Sinogram Files, with filenames"+'\n'+"(SINO0000, SINO0001, SINO0002) ?" +RESET)
if int(sumSinos) == 3 and str(SinosNum[0])== "SINO0000" and str(SinosNum[1])== "SINO0001" and str(SinosNum[2])== "SINO0002":
  YesNo(True)
else:
  YesNo(False)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Number of List Files:" +RESET)
sumLists = CountFiles("LIST00", ListsDirectory2_1 )
print sumLists

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The name of the List Files found is :" +RESET)
for item in ListsNum:
  print str(item)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is there a 3 List Files, with filenames"+'\n'+"(LIST0000.BLF, LIST0001.BLF, LISTO0002.BLF) ?" +RESET)
if int(sumSinos) == 3 and str(ListsNum[0])== "LIST0000.BLF" and str(ListsNum[1])== "LIST0001.BLF" and str(ListsNum[2])== "LIST0002.BLF":
  YesNo(True)
else:
  YesNo(False)


#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1154")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1155/Acq4D_1155.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1155/Acq4D_1155.py")

