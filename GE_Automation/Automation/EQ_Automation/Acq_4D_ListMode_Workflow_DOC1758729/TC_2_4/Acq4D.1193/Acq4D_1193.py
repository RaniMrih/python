#!/usr/bin/python
import os, sys
import time
import re

#VARIABLES
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1193'
SinoPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/SINOSPath2_4.txt'
ListPath2_4 = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1190/LISTSPath2_4.txt'
num = []
Step_Pass=True

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.4 Step 1193 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print
#------------------------------------- Functions -------------------------------------
#--- print Yes for true value
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

#---- split line to array according to ','
def split_string(line):
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

#------------------------------------- step 1 --------------------------------------------
# grep sinos path from 1189
f = open( SinoPath2_4 , "r")
for line in f:
  path = line

print ("Creating Tell2.4 and Tell2.4Geo for all SINOS, please wait..."+'\n')
os.system("rdfTeller -r  ' -h  efadS -v -Ha -S'  -f Tell2.4 "+ path +"/SINO*")
os.system("rdfTeller -r  ' -h  g -v -Ha -S'  -f Tell2.4Geo "+ path +"/SINO*")
os.system("cp ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/Tell2.4* " +PWD)

print (BLUE + "1) Summed values for Dynamic Frames: "+ RESET)
print (BLUE + "Frame Duration :"+ RESET)
os.system("grep 'frameDuration:' Tell2.4.SINO* > "+PWD+"/FD.txt")
sum=0
f = open(PWD+"/FD.txt", "r")
for line in f:
  num = line.replace(line[:41],'')
  num = num.rstrip('\n')
  sum+= int(num)
print str(sum) +" ms" 

print (BLUE + "Total Prompts :"+ RESET)
os.system("grep 'totalPrompts:' Tell2.4.SINO* >"+PWD+"/TP.txt")
sum1=0
f = open(PWD+"/TP.txt", "r")
for line in f:
  num = line.replace(line[:41],'')
  num = num.rstrip('\n')
  sum1+= int(num)

print sum1
print
#------------------------------------- step 2 --------------------------------------------
#--- find Delta Time in ListLoss2.4.txt
time.sleep(1)
print (BLUE + "2) Values from List File:"+ RESET)
print (BLUE + "List Duration (Delta Time):"+ RESET)
f = open("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/ListLoss2.4.txt","r")
for line in f:
  if "Delta" in line:
    line1=line.rstrip('\n')
    line1=line1.replace(line1[:12],'')
    print line1 +" ms"

#--- find Total prompts in LT_Ml.txt
print (BLUE + "Total Prompts"+ RESET)
f = open("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/ListLoss2.4.csv", "r")
for line in f:
  if "Total Prompt" in line:
    line2=line.replace(line[:30],'')
    print line2
#------------------------------------- step 3 --------------------------------------------
time.sleep(1)
print (BLUE + "3) The difference of output values from Dynamic "+'\n'+"frames and List File are:"+ RESET)
#DurationDiff=
print (BLUE + "Duration :"+ RESET)
result = int(sum) - int(line1)
print str(result) + " ms"
print (BLUE + "% Difference of Prompts is : "+ RESET)
result1 = int(sum1) -int(line2)
print str(result1) +" %"

#----------- qustions ---------
time.sleep(1)
print
print (BLUE + "Duration Difference within 10ms ?"+ RESET)
Within10=True
if int(result) > 10:
  Within10=False
YesNo(Within10)

time.sleep(1)
print (BLUE + "The Prompts agree within 1% ?"+ RESET)
Within1=True
OnePercent = float(line2) * 0.1
if int(result1) > int(OnePercent):
  Within1=False
YesNo(Within1)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1193")

print (GREEN +"                                                      ---- END of TC 2.4 Columbia DMI ----" +RESET)

#-----------------------------------------------END of TC2.4







