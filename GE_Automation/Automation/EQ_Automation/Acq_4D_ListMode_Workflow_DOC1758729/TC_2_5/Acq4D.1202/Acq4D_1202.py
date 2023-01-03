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
Block_MAX_Live_List =[]
Block_MAX_Replay_List =[]
TC_Start='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196'
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1202'
SinoPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/SINOSPath2_4.txt'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/LISTSPath2_4.txt'
Step_Pass=True

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.5 Step 1202 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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
   list_string=line.split(' ')
   return list_string

#---- find Block busy max from Live Sinos
def BlockBusyMax_Live():
   f=open("Block_Busy_Max_Live.txt", "w+")
   for i in range (0,16):
     if i < 10:
       for line in open("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1193/Tell2.4.SINO000" +str(i), "r"):
         line = line.rstrip()
         if re.search('Block Busy Max', line):
           Block_Max = line
           # like echo to file
           f.write("SINO000" +str(i) + "= " + Block_Max +'\n')
           tmp = split_string(Block_Max)
           Block_MAX_Live_List.append(tmp[7])
     else:
       for line in open("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1193/Tell2.4.SINO00" + str(i), "r"):
         line = line.rstrip()
         if re.search('Block Busy Max', line):
           Block_Max = line
           # like echo to file
           f.write("SINO00" +str(i) + "= " + Block_Max +'\n')
           tmp = split_string(Block_Max)
           Block_MAX_Live_List.append(tmp[7])
   f.close()

#---- find Block busy max from Replay Sinos
def BlockBusyMax_Replay():
   f=open("Block_Busy_Max_Replay.txt", "w+")
   for i in range (0,16):
     if i < 10:
       for line in open("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196/Tell2.5.SINO000" +str(i), "r"):
         line = line.rstrip()
         if re.search('Block Busy Max', line):
           Block_Max = line
           # like echo to file
           f.write("SINO000" +str(i) + "= " + Block_Max +'\n')
           tmp = split_string(Block_Max)
           Block_MAX_Replay_List.append(tmp[7])
     else:
       for line in open("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196/Tell2.5.SINO00" + str(i), "r"):
         line = line.rstrip()
         if re.search('Block Busy Max', line):
           Block_Max = line
           # like echo to file
           f.write("SINO00" +str(i) + "= " + Block_Max +'\n')
           tmp = split_string(Block_Max)
           Block_MAX_Replay_List.append(tmp[7])
   f.close()


def Check_Block_Max_Diff():
   within0_02=True
   for i in range (0,16):
     if float(Block_MAX_Live_List[i]) - float(Block_MAX_Replay_List[i]) > 0.02 * float(Block_MAX_Live_List[i]):
       within0_02 = False
   YesNo(within0_02)
# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "1) The Difference between 'Block Busy Max' for live "+'\n'+"and Replay scan is < = 0.002?" +RESET)

BlockBusyMax_Live()
BlockBusyMax_Replay()
Check_Block_Max_Diff()

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Results file labeled with test Object ID, printed and " +RESET)
print (BLUE + "attached ?" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE :Files Block_Busy_Max_Live/Replay.txt located at: ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1202' + RESET)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1202")
print (GREEN +"                                                      ---- END of TC 2.5 Columbia DMI ----" +RESET)

#--------------------- END of TC.2.5

