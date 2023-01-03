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
SINOBlockSingles=[]
SINOBlockBusy=[]
LISTAverageSingles=[]
LISTAverageBusy=[]

PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_20/Acq4D.1282'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::: Running XRBB TC_2.20 Step 1282 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.20 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#--- find block singles for module [5]
def findBlockSingles():
   for line in open("sino_segment_stats.txt", "r"):
      line = line.rstrip()
      if re.search('BS Module\[ 5]', line):
        line1=split_string(line)
        print line1[11]
        SINOBlockSingles.append(line1[11])

#--- find block Busy for module [5]
def findBlockBusy():
   for line in open("sino_segment_stats.txt", "r"):
      line = line.rstrip()
      if re.search('BBD Module\[ 5]', line):
        line1=split_string(line)
        print line1[17]
        SINOBlockBusy.append(line1[17])

#-- find Singles avarage from ListTool-Ms.txt
def findAvarageSingles():
   for line in open("ListTool-Ms.txt", "r"):
      line = line.rstrip()
      if re.search('Average:', line):
        line1=split_string(line)
        LISTAverageSingles.append(line1[1])

#-- find Busy avarage from ListTool-Mb.txt
def findAvarageBusy():
   for line in open("ListTool-Mb.txt", "r"):
      line = line.rstrip()
      if re.search('Average:', line):
        line1=split_string(line)
        LISTAverageBusy.append(line1[1])
# ---------------------------------------------------------------------------------------

#if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_20 = line.strip('\n')
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_LIST.txt" , "r")
  for line in f:
    ListsDirectory2_20 = line.strip('\n')
  print "Enter Sinogram path directory from" + BLUE + " section 2.20 :" +RESET + SinosDirectory2_20
  print "Enter LIST path directory from" + BLUE + " section 2.20 :" +RESET + ListsDirectory2_20

else:
  #use of raw_input() from user
  SinosDirectory2_20 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.20 :" + RESET)
  # while SinosDirectory2_20 is empty
  while SinosDirectory2_20 == "":
    SinosDirectory2_20 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.20 again:" + RESET)

  ListsDirectory2_20 = raw_input("Enter Lists path directory from" + BLUE + " section 2.20 :" + RESET)
  # while ListsDirectory2_20 is empty
  while ListsDirectory2_20 == "":
    ListsDirectory2_20 = raw_input("Enter Lists path directory from" + BLUE + " section 2.20 again:" + RESET)

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt")

# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Scan Completed normally ?" +RESET)
print "[ ] Yes"
print "[ ] No"

time.sleep(1)
print
print (BLUE + "List File Path:" +RESET)
print ListsDirectory2_20

time.sleep(1)
print
print (BLUE + "Sinogram File Path:" +RESET)
print SinosDirectory2_20

# ------------------------------------ step 2 --------------------------------------------
#perform rdfTell to sinos from TC2.14
time.sleep(1)
print
print ("Creating sino_segment_stats.txt for SINO0000, please wait...")
os.system("rdfTell -S "+ SinosDirectory2_20 +"/SINO0000 > sino_segment_stats.txt")

# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "3) Module :" +RESET)
print ("5")
print (BLUE + "Block :" +RESET)
print ("5")
# ------------------------------------ step 4 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "4) a) Singles value for selected module,"+'\n'+"block in sino RDF:" +RESET)
findBlockSingles()
time.sleep(1)
print
print (BLUE + "b) Block Busy value for selected module,"+'\n'+"block in sino RDF:" +RESET)
findBlockBusy()

# ------------------------------------ step 5 --------------------------------------------
#perform ListTool -Ms
time.sleep(1)
print
print ("Creating ListTool-Ms.txt for ListFile, please wait...")
os.system("ListTool -Ms -b5,5 "+ ListsDirectory2_20 +"/LIST* > ListTool-Ms.txt")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "5) a) Avarage Singles count from the List"+'\n'+"file :" +RESET)
findAvarageSingles()
print LISTAverageSingles[2]

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "5) b) Extrapolated Singles :" +RESET)
Extrapolated = int(LISTAverageSingles[2]) * 60
print Extrapolated

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The Extrapolated Singles is within 0.1%"+'\n'+"of singles value in the sinogram RDF?" +RESET)

High_Tolerance = float(SINOBlockSingles[0]) + float(SINOBlockSingles[0]) * 0.1
Low_Tolerance = float(SINOBlockSingles[0]) - float(SINOBlockSingles[0]) * 0.1
if float(Extrapolated) > float(High_Tolerance) or float(Extrapolated) < float(Low_Tolerance):
  YesNo(False)
else:
  YesNo(True)

# ------------------------------------ step 6 --------------------------------------------
#perform ListTool -Mb
time.sleep(1)
print ("Creating ListTool-Mb.txt for ListFile, please wait...")
os.system("ListTool -Mb -b5,5 "+ ListsDirectory2_20 +"/LIST* > ListTool-Mb.txt")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "6) a) Avarage Block Bust value from the List"+'\n'+"file :" +RESET)
findAvarageBusy()
print LISTAverageBusy[2]


#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "6) b) the List Tool Block Busy average is"+'\n'+"within 0.1% of the value in the sinogram RDF ?" +RESET)
if float(LISTAverageBusy[2])  < float(SINOBlockSingles[0]) * 0.1 :
  YesNo(True)
else:
  YesNo(False)

#-- END Step determine if step Pass/Fail
Step_Result("Acq4D.1282")
print (GREEN +"                                                        ---- END of TC 2.20 for XRBB ----" +RESET)
