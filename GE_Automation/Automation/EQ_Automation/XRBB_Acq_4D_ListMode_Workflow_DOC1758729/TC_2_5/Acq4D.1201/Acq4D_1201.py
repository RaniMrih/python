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
SinglesLive_List =[]
SinglesReplay_List =[]
TC_Start='/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196'
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1201'
SinoPath2_4 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/SINOSPath2_4.txt'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/LISTSPath2_4.txt'
Step_Pass=True

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.5 Step 1201 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#---- split line to array according to space ' '
def split_string(line):
   list_string=line.split(',')
   return list_string

#--- find 'Singles total counts' from all Live sinos, write to file and append to array
def SinglesTotalCounts_Live():
   f=open("Singles_Counts_Live.txt", "w+")
   for i in range (0,16):
     if i < 10:
       for line in open("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1193/Tell2.4.SINO000" +str(i), "r"):
         line = line.rstrip()
         if re.search('Singles Total Counts', line):
           Singles = line.replace(line[:3], '')  
           # like echo to file
           f.write("SINO000" +str(i) + "= " + Singles +'\n')
           SinglesLive_List.append(line.replace(line[:24], ''))
     else:
       for line in open("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1193/Tell2.4.SINO00" + str(i), "r"):
         line = line.rstrip()
         if re.search('Singles Total Counts', line):
           Singles = line.replace(line[:3], '')
           # like echo to file
           f.write("SINO00" +str(i) + "= " + Singles +'\n')
           SinglesLive_List.append(line.replace(line[:24], ''))
   f.close()

#--- find 'Singles total counts' from all Replay sinos, write to file and append to array

def SinglesTotalCounts_Replay():
   f=open("Singles_Counts_Replay.txt", "w+")
   for i in range (0,16):
     if i < 10:
       for line in open("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196/Tell2.5.SINO000" +str(i), "r"):
         line = line.rstrip()
         if re.search('Singles Total Counts', line):
           Singles = line.replace(line[:3], '')
           # like echo to file
           f.write("SINO000" +str(i) + "= " + Singles +'\n')
           SinglesReplay_List.append(line.replace(line[:24], ''))
     else:
       for line in open("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196/Tell2.5.SINO00" + str(i), "r"):
         line = line.rstrip()
         if re.search('Singles Total Counts', line):
           Singles = line.replace(line[:3], '')
           # like echo to file
           f.write("SINO00" +str(i) + "= " + Singles +'\n')
           SinglesReplay_List.append(line.replace(line[:24], ''))
   f.close()

def CheckSinglesDiff():
   within0_2=True
   for i in range (0,16):
     if int(SinglesLive_List[i]) - int(SinglesReplay_List[i]) > 0.2 * float(SinglesLive_List[i]):
       within0_2 = False
   YesNo(within0_2)
# ------------------------------------ step 1 --------------------------------------------                 
#----------- qustion ---------
time.sleep(1)
print (BLUE + "All Frames Have 'Singles Total Counts'"+'\n'+"%diff between original and replay scan is" +RESET)
print (BLUE + "<= 0.2% ?" +RESET)

SinglesTotalCounts_Live()
SinglesTotalCounts_Replay()
CheckSinglesDiff()

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Results file labeled with test Object ID, printed and" +RESET)
print (BLUE + "attached ?" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE :Files Singles_Counts_Live/Replay.txt located  at : ~/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1201' + RESET)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1201")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1202/Acq4D_1202.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1202/Acq4D_1202.py")



