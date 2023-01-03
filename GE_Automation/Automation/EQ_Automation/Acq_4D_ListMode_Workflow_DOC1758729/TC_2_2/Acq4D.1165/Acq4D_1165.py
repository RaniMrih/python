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
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1165'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1165'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.2 Step 1165 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                      ---- Step "+StepNum+" Failed ----" + RESET)
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
    SinosDirectory2_2 = line.strip('\n')
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_LIST.txt" , "r")
  for line in f:
    ListsDirectory2_2 = line.strip('\n')
  print "Enter Sinograms path directory from" + BLUE + " section 2.2 :" +RESET + SinosDirectory2_2
  print "Enter LIST path directory from" + BLUE + " section 2.2 :" +RESET + ListsDirectory2_2
else:
  #use of raw_input()
  SinosDirectory2_2 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.2 :" + RESET)
  # while SinosDirectory2_2 is empty
  while SinosDirectory2_2 == "":
    SinosDirectory2_2 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.2 again:" + RESET)
  ListsDirectory2_2 = raw_input("Enter Lists path directory from" + BLUE + " section 2.2 :" + RESET)
  # while ListsDirectory2_2 is empty
  while ListsDirectory2_2 == "":
    ListsDirectory2_2 = raw_input("Enter Lists path directory from" + BLUE + " section 2.2 again:" + RESET)

print
# like : echo $SinosDirectory2_2 > SINOSPath2_4.txt
f=open("SINOSPath2_2.txt", "w+")
f.write(SinosDirectory2_2)
f.close()
f=open("LISTSPath2_2.txt", "w+")
f.write(ListsDirectory2_2)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt")

time.sleep(1)
print "Creating S2.2Sino.txt file ..."
os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SinosDirectory2_2+"/SINO* > S2.2Sino.txt")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the S2.2Sino.txt file produced ?" +RESET)
if os.path.exists(TC_start +'/S2.2Sino.txt'):
  YesNo(True)
else:
  YesNo(False)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1165")
os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1166/Acq4D_1166.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1166/Acq4D_1166.py")

