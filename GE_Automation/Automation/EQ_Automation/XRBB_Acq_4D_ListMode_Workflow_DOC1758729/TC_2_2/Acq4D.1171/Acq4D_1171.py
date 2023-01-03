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
MCPS_List=[]
CoinLoss_List=[]
ErrorLoss_List=[]
CPMLoss_List=[]
CPMLoss_Live_List=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1171'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1165'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.2 Step 1171 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ' '
def split_string(line):
   list_string=line.split(' ')
   return list_string

#---- split line to array according to  ':'
def split_string1(line):
   list_string=line.split(',')
   return list_string

#--- find MCPS from coinLoss_2_2.csv
def FindMCPS():
   i=0
   smaller=True
   for line in open( TC_start + "/coinLoss_2_2.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string1(line)
       MCPS_List.append(line1[2])
       CoinLoss_List.append(line1[3])
       ErrorLoss_List.append(line1[5])
       CPMLoss_List.append(line1[9].strip('\n'))
       i+=1

def Find_Live_CPM():
   i=0
   smaller=True
   for line in open( TC_start + "/coinLoss_2_1.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string1(line)
       CPMLoss_Live_List.append(line1[9].strip('\n'))
       i+=1


# ------------------------------------ step 1 --------------------------------------------
# grep sinos path live
f = open( TC_start_2_1 + "/SINOSPath2_1.txt" , "r")
for line in f:
  Sinospath2_1 = line

# grep sinos path Replay
f = open( TC_start + "/SINOSPath2_2.txt" , "r")
for line in f:
  Sinospath2_2 = line

print "Creating coinLoss_2_1.csv, coinLoss_2_2.csv, please wait..."
os.system("coinLossCk -v -c " + Sinospath2_1 + "/SINO*")
os.system("mv "+TC_start+"/coinLoss.csv coinLoss_2_1.csv")
os.system("cp "+TC_start+"/coinLoss_2_1.csv " +PWD)

os.system("coinLossCk -v -c " + Sinospath2_2 + "/SINO*")
os.system("mv "+TC_start+"/coinLoss.csv coinLoss_2_2.csv")
os.system("cp "+TC_start+"/coinLoss_2_2.csv " +PWD)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "a) Replay scan MCPS" +RESET)
FindMCPS()
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(MCPS_List[i])
print
#----------- qustion ---------
time.sleep(1)
print (BLUE + "b) Replay scan %SorterCoinLoss" +RESET)
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(CoinLoss_List[i])
print
#----------- qustion ---------
time.sleep(1)
print (BLUE + "c) Replay scan %LossError" +RESET)
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(ErrorLoss_List[i])
print
#----------- qustion ---------
time.sleep(1)
print (BLUE + "d) Replay scan CPM Loss" +RESET)
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(CPMLoss_List[i])
print
#----------- qustion ---------
time.sleep(1)
print (BLUE + "%SorterCoinLoss for Bed1, Bed2 & Bed3 is less "+'\n'+"than 1.0% ? " +RESET)
Within_1=True
for i in range (0,3):
  if float(CoinLoss_List[i]) > 1.0:
    Within_1 = False
YesNo(Within_1)
#----------- qustion ---------
time.sleep(1)
print (BLUE + "f) All frames have %LossError less than 1.0 % ?" +RESET)
Within_1=True
for i in range (0,3):
  if float(ErrorLoss_List[i]) > 1.0:
    Within_1 = False
YesNo(Within_1)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Live scan CPM Loss" +RESET)
Find_Live_CPM()
for i in range (0,3):
  print "Bed "+str(i+1)+" : "+ str(CPMLoss_Live_List[i])
print
#----------- qustion ---------
# %DiffCpmLoss = (abs(Live - Replay) / Live ) * 100.0
time.sleep(1)
print (BLUE + "%DiffCpmLoss" +RESET)
Within_1=True
for i in range (0,3):
  sum= float(CPMLoss_Live_List[i]) - float(CPMLoss_List[i])
  if sum < 0:
    sum*=-1
  sum = (sum / float(CPMLoss_Live_List[i])) * 100.0
  print "Bed "+str(i+1)+" : "+ str(sum)+ " %"
  if float(sum) > 1.0:
    Within_1=False

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The %DiffCpmLoss of live scan to replay is <= 0.1% ?" +RESET)
YesNo(Within_1)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1171")
os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1172/Acq4D_1172.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1172/Acq4D_1172.py")







