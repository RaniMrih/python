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

PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1287'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.21 Step 1287 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.21 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#--- find SorterCoinLoss from coinLoss.csv
def CheckCoinLoss():
   i=0
   smaller=True
   for line in open( PWD + "/coinLoss_1284.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string1(line)
       i+=1
    #check if all SortercoinLoss < 1%
       if float(line1[3]) > 1.0:
         smaller=False
   YesNo(smaller)

#--- find ErrorLoss from coinLoss.csv
def FindErrorLoss():
   i=0
   smaller=True
   for line in open( PWD + "/coinLoss_1284.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string1(line)
       i+=1
    #check if all ErrorLoss < 1%
       if float(line1[5]) > 1.0:
         smaller=False
   YesNo(smaller)

# ---------------------------------------------------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos first path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_21_1 = line.strip('\n')
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_LIST.txt" , "r")
  for line in f:
    ListsDirectory2_21_1 = line.strip('\n')
 
 # grep sinos Second path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO1.txt" , "r")
  for line in f:
    SinosDirectory2_21_2 = line.strip('\n')
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_LIST1.txt" , "r")
  for line in f:
    ListsDirectory2_21_2 = line.strip('\n')

  print "Enter Sinogram path directory from" + BLUE + " section 2.21.1 Scan SSVP.PAC.Acq4D.1284:" +RESET + SinosDirectory2_21_1
  print "Enter Sinogram path directory from" + BLUE + " section 2.21.1 Scan SSVP.PAC.Acq4D.1285:" +RESET + SinosDirectory2_21_2
  print "Enter List path directory from" + BLUE + " section 2.21.1 Scan SSVP.PAC.Acq4D.1284:" +RESET + ListsDirectory2_21_1
  print "Enter List path directory from" + BLUE + " section 2.21.1 Scan SSVP.PAC.Acq4D.1285:" +RESET + ListsDirectory2_21_2

else:
  #use of raw_input() from user
  SinosDirectory2_21_1 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.21 Scan SSVP.PAC.Acq4D.1284 :" + RESET)
  # while SinosDirectory2_21_1 is empty
  while SinosDirectory2_21_1 == "":
    SinosDirectory2_21_1 = raw_input("Enter Sinogram path directory from" + BLUE + "  section 2.21 Scan SSVP.PAC.Acq4D.1284 :" + RESET)

  #use of raw_input() from user
  SinosDirectory2_21_2 = raw_input("Enter Sinogram path directory from" + BLUE + " section 2.21 Scan SSVP.PAC.Acq4D.1285 :" + RESET)
  # while SinosDirectory2_21_2 is empty
  while SinosDirectory2_21_2 == "":
    SinosDirectory2_21_2 = raw_input("Enter Sinogram path directory from" + BLUE + "  section 2.21 Scan SSVP.PAC.Acq4D.1285 :" + RESET)
  # ---------------------------------------------------------------------------------------
  ListsDirectory2_21_1 = raw_input("Enter Lists path directory from" + BLUE + " section 2.21 Scan SSVP.PAC.Acq4D.1284 :" + RESET)
  # while ListsDirectory2_21_1 is empty
  while ListsDirectory2_21_1 == "":
    ListsDirectory2_21_1 = raw_input("Enter Lists path directory from" + BLUE + " section 2.21 Scan SSVP.PAC.Acq4D.1284" + RESET)

  ListsDirectory2_21_2 = raw_input("Enter Lists path directory from" + BLUE + " section 2.21 Scan SSVP.PAC.Acq4D.1285 :" + RESET)
  # while ListsDirectory2_21_5 is empty
  while ListsDirectory2_21_2 == "":
    ListsDirectory2_21_2 = raw_input("Enter Lists path directory from" + BLUE + " section 2.21 Scan SSVP.PAC.Acq4D.1285" + RESET)


#like echo to file
f=open("SINOSPath2_21_1.txt", "w+")
f.write(SinosDirectory2_21_1)
f.close()

#like echo to file
f=open("SINOSPath2_21_2.txt", "w+")
f.write(SinosDirectory2_21_2)
f.close()

#like echo to file
f=open("LISTSPath2_21_1.txt", "w+")
f.write(ListsDirectory2_21_1)
f.close()

#like echo to file
f=open("LISTSPath2_21_2.txt", "w+")
f.write(ListsDirectory2_21_2)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO1.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST1.txt")

# ------------------------------------ step 1 --------------------------------------------
print
print "Creating coinLoss_1284.csv, please wait..."
os.system("coinLossCk -v -c " + SinosDirectory2_21_1 + "/SINO*")
os.system("mv coinLoss.csv coinLoss_1284.csv")

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "1) %SorterCoinLoss for each frame is less "+'\n'+"than 1.0 %?" +RESET)
CheckCoinLoss()

#----------- qustion ---------
time.sleep(1)
print (BLUE + "All frames have "+'\n'+"%LossError less than 1.0 %?" +RESET)
FindErrorLoss()

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "results file labeled with test Object ID,"+'\n'+" printed and attached" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE: coinLoss_1284.csv located at: ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1287' + RESET)
print
#-- determine if step Pass/Fail
Step_Result("Acq4D.1287")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1289/Acq4D_1289.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_21/Acq4D.1289/Acq4D_1289.py")

