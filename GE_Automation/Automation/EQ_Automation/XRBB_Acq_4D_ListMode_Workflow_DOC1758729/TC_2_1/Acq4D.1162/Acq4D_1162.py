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
SorterLossList=[]
LisTLossInAligned=[]
MaxListLoss=[]
ListFileMax1sec=[]
Sorter_Loss_csv=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1162'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.1 Step 1162 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to  ','
def split_string1(line):
   list_string=line.split(',')
   return list_string

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#--- find SorterCoinLoss from coinLoss.csv
def FindCoinLoss():
   i=0
   smaller=True
   for line in open( PWD + "/coinLoss.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string1(line)
       i+=1
       SorterLossList.append(line1[3])

#---- grep list loss in aligned from listfile
def List_Loss_aligned():
  for j in range (0,3):
    with open( TC_start + "/ListLoss"+str(j)+".txt" , 'r') as f:
      for line in f.readlines():
        if 'list loss in aligned' in line: 
          result=line.strip('\n')
          result = line.replace(line[:38], '')
          result= result[:-2]
          LisTLossInAligned.append(result)

#---- find max list loss 1 sec
def find_MaxListLoss():
  for j in range (0,3):
    with open( TC_start + "/ListLoss"+str(j)+".txt" , 'r') as f:
      for line in f.readlines():
        if 'Maximum list loss' in line:
          result=split_string(line)
          MaxListLoss.append(result[4].strip('\n'))

#--- find 1 sec inerval ( sorter coin loss in csvs)     
def find1Secinterval():
   i=0
   for j in range (0,3):
     f = open(TC_start + "/ListLoss"+str(j)+".csv", "r")
     result1 = ","+str(MaxListLoss[j])
     for line in f:
       if i < 2:
         i+=1
         continue
       else:
         i+=1
         if result1 in line:
           line1=split_string1(line)
           Sorter_Loss_csv.append(line1[5])

# ------------------------------------ step 1 --------------------------------------------
# grep sinos path
f = open( TC_start + "/SINOSPath2_1.txt" , "r")
for line in f:
  Sinospath = line

print
print "Creating coinLossCK.csv, please wait..."
os.system("coinLossCk -v -c " + Sinospath + "/SINO*")
os.system("cp /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154/coinLoss.csv " +PWD)


#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "1) Sinogram Sorter"+'\n'+"Coinc Loss (%)" +RESET)
FindCoinLoss()
Within_1 =True
for i in range (0,3):
  print "Frame "+str(i+1)+": "+ str(SorterLossList[i])
  if float(SorterLossList[i]) > 1.0:
    Within_1=False

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "For all bed location Sinogram  Files (SINO0000, "+'\n'+"SINO0001 & SINO0002),  the Sorter Coinc Loss % is  < 1.0 %?" +RESET)
YesNo(Within_1)

# ------------------------------------ step 2 --------------------------------------------
# grep list file path
f = open( TC_start + "/LISTSPath2_1.txt" , "r")
for line in f:
  Listspath = line

print "Creating ListLoss0-2.txt, please wait..."
for i in range (0,3):
  os.system("ListTool -Ml -Sl  -f ListLoss"+str(i)+".csv " + Listspath + "/LIST000"+str(i)+".BLF > ListLoss"+str(i)+".txt")
  os.system("cp ListLoss"+str(i)+".txt "+PWD)
  os.system("cp ListLoss"+str(i)+".csv "+PWD)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) List File overall aligned "+'\n'+"Coinc Loss (%)" +RESET)
List_Loss_aligned()
Within_1 =True
for i in range (0,3):
  print "LIST000 "+str(i+1)+".BLF : "+ str(LisTLossInAligned[i])+ " %"
  if float(LisTLossInAligned[i]) > 1.0:
    Within_1=False

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "For all bed location List Files (LIST0000, LIST0001 "+'\n'+"& LIST0002), the overall frame Coinc loss is < 1.0 %" +RESET)
YesNo(Within_1)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) List File Max 1 sec Coinc Loss" +RESET)
find_MaxListLoss()
Within_1 =True
for i in range (0,3):
  print "LIST000 "+str(i+1)+".BLF : "+ str(MaxListLoss[i])+ " %"
  if float(MaxListLoss[i]) > 1.0:
    Within_1=False
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "List File Max 1 sec Coinc Loss expressed as a "+'\n'+"percentage of the Prompt rate for same interval :" +RESET)
find1Secinterval()
Within_50=True
for i in range (0,3):
   print "LIST000"+str(i)+".BLF : "+str(Sorter_Loss_csv[i])
   if float(Sorter_Loss_csv[i]) > 50.0:
     Within_50=False

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "4) For all bed location List Files (LIST0000, "+'\n'+"LIST0001 & LIST0002), the Max List Coinc Loss at" +RESET)
print (BLUE + "any one sec interval is < 50.0 % ?" +RESET)
YesNo(Within_50)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "5) List Loss plots, printed, labeled and included in Test Results ?" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE: ListToolPlot.py Not found, perform manually."' + RESET)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1162")
print (GREEN +"                                                       ---- END of TC 2.1 for XRBB ----" +RESET)

