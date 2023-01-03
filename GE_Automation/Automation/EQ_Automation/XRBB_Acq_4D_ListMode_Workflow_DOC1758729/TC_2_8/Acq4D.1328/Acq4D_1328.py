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
Singles_Block_Max=[]
Step_Pass=True

PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_8/Acq4D.1328'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::: Running XRBB TC_2.8 Step 1328 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.8 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#--- find Singles Block
def findSinglesBlock():
   for line in open(PWD + "/Tell2.8", "r"):
     line = line.rstrip()
     if re.search('Singles Block Max', line):
       Singles_Block_Max.append(line)

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

# ------------------------------------ step 3 (first) --------------------------------------------
# ---------------------------------------------------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_8 = line.strip('\n')
  print "Enter Sinograms path directory from" + BLUE + " section 2.8 :" +RESET + SinosDirectory2_8

else:
  #use of raw_input() from user
  SinosDirectory2_8 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.8 :" + RESET)
  # while SinosDirectory2_8 is empty
  while SinosDirectory2_8 == "":
    SinosDirectory2_8 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.8 again:" + RESET)

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")

#perform rdfTeller to sino8 from TC2.8  
print
print ("Creating rdfTeller for sinos 2.8, please wait...")
os.system("rdfTeller -r  '-S' "+ SinosDirectory2_8 +"/SINO*  > Tell2.8")
findSinglesBlock()

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Scan Completed normally ?" +RESET)
print "[ ] Yes"
print "[ ] No"

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "3) For Singles data the 'Module' number for "+'\n'+"1st data is:" +RESET)
ModuleNum1 = Singles_Block_Max[0].replace(Singles_Block_Max[0][:39],'')
print ModuleNum1

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "For Singles data the 'Block' number for "+'\n'+"1st data is:" +RESET)
BlockNum1 = Singles_Block_Max[0].replace(Singles_Block_Max[0][:39],'')
print BlockNum1

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "For Singles data the 'Module' number for "+'\n'+"5th data is:" +RESET)
ModuleNum2 = Singles_Block_Max[4].replace(Singles_Block_Max[0][:39],'')
print ModuleNum2

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "For Singles data the 'Block' number for "+'\n'+"5th data is:" +RESET)
BlockNum2 = Singles_Block_Max[4].replace(Singles_Block_Max[0][:39],'')
print BlockNum2

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the 'Module' and 'Block' number for 1st and  "+'\n'+"5th data are same ?" +RESET)
if str(ModuleNum1) == str(BlockNum1) and str(ModuleNum2) == str(BlockNum2):
  YesNo(True)
else:
  YesNo(False)

time.sleep(1)
Step_Result("Acq4D.1328")
print (GREEN +"                                                        ---- END of TC 2.8 for XRBB ----" +RESET)

