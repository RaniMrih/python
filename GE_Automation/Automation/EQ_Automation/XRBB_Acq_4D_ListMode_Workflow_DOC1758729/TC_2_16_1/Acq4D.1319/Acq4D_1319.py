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
Sorter_Coin_Loss=[]
Loss_In_Aligned=[]
Max_List_Loss=[]
Sorter_Loss_csv=[]
TC_start='/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_16_1/Acq4D.1318'
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_16_1/Acq4D.1319'

print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.16.1 Step 1389 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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
   for line in open( TC_start + "/coinLoss.csv", "r"):
     if i == 0:
       i+=1
       continue
     else:
    #go to def "split_string" to insert csv data to array
       line1=split_string1(line)
       i+=1
       Sorter_Coin_Loss.append(line1[3])

#---- print coin loss list for all sinos
def DisplayCoinLoss():
   for i in range (0,10):
     time.sleep(0.1)
     print "SINO000" + str(i) + " : "+ str(Sorter_Coin_Loss[i]) + " %" 

#---- grep List Loss in aligned from all 10 listloss.txt
def findListLossInAligned():
   for i in range (0,10):
     for line in open( TC_start + "/ListLoss"+str(i)+".txt", "r"):
      line = line.rstrip()
      if re.search('Percent list loss in aligned section', line):
        line1=split_string(line)
        x=line1[6]
        #remove last char
        x=x[:-1]
        time.sleep(0.1)
        print "LIST000"+str(i)+".BLF : "+str(x) + " %"
        Loss_In_Aligned.append(x)

#--- find max list loss in aligned
def findMaxListLoss():
   for i in range (0,10):
      for line in open( TC_start + "/ListLoss"+str(i)+".txt", "r"):
        line = line.rstrip()
        if re.search('Maximum list loss rate:', line):
          line1=split_string(line)
          time.sleep(0.1)
          print "LIST000"+str(i)+".BLF : "+str(line1[4])     
          Max_List_Loss.append(line1[4])

#--- find 1 sec inerval ( sorter coin loss in csvs)     
def find1Secinterval():
   for j in range (0,10):
     i=0
     f = open(TC_start + "/ListLoss"+str(j)+".csv", "r")
     result1 = ","+str(Max_List_Loss[j])
     for line in f:
       if i < 2:
         i+=1
         continue
       else:
         i+=1
         if result1 in line:
           line1=split_string1(line)
           Sorter_Loss_csv.append(line1[5])

   for i in range (0,10):
     time.sleep(0.1)
     print "LIST000"+str(i)+".BLF : "+Sorter_Loss_csv[i]

# ------------------------------------ step 1 --------------------------------------------
# grep sinos  path
f = open( TC_start +"/SINOSPath2_16_1.txt" , "r")
for line in f:
  SinosPath = line

print "Creating coinLoss_1319.csv, please wait..."
os.system("coinLossCk -v -c " + SinosPath + "/SINO*")

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "1) Sinogram Sorter"+'\n'+"Coinc Loss (%)" +RESET)
CheckCoinLoss()
DisplayCoinLoss()

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "For all bed locations Sinogram  Files (SINO0001,"+'\n'+"SINO0002,.... SINO0009),  the Sorter Coinc Loss"+'\n'"% is  < 1.0 %?" +RESET)
Within0_1= True
for item in Sorter_Coin_Loss:
   if float(item) > 0.1:
     Within0_1 = False
YesNo(Within0_1)

# ------------------------------------ step 2 --------------------------------------------
# grep sinos  path
f = open( TC_start +"/LISTSPath2_16_1.txt" , "r")
for line in f:
  ListsPath = line

#perform ListTool to 9 Listfile from TC2.16.1
print ("Creating ListLoss.txt for 10 ListFiles, please wait...")
for i in range (0,10):
   os.system("ListTool -Ml -Sl -f ListLoss"+str(i)+".csv " +ListsPath+ "/LIST000"+str(i)+".BLF > ListLoss"+str(i)+".txt")
#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "2) List File overall aligned"+'\n'+"Coinc Loss (%)" +RESET)
findListLossInAligned()

#----------- qustion --------
print
time.sleep(1)
print (BLUE + "For all bed locations List Files (LIST0001.BLF,"+'\n'+"LIST0002.BLF,....., LIST0009.BLF),  the overall frame"+'\n'"Coinc loss is < 1.0 %?" +RESET)
Within_1= True
for item in Loss_In_Aligned:
   if float(item) > 1.0:
     Within_1 = False
YesNo(Within_1)

# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) Maximum List File in one sec interval is:" +RESET)
findMaxListLoss()
# ------------------------------------ step 4 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "4) Is the Maximum List File in one sec interval"+'\n'+"expressed as a percentage of the Prompt rate for"+'\n'+"same interval:" +RESET)
find1Secinterval()

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "For all beds location List Files (LIST0001.BLF,"+'\n'+"LIST0002.BLF,.....LIST0009.BLF), the Max List Coinc"+'\n'+"Loss at any one sec interval is < 50.0 %?" +RESET)
Within_50= True
for item in Sorter_Loss_csv:
   if float(item) > 50.0:
     Within_50 = False
YesNo(Within_50)

# ------------------------------------ step 5 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "5) List Loss plots, printed, labeled and included in"+'\n'+"Test Results ?" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE: Use ListToolPlot.py to create a plot of the ListLoss.csv for each frame, and label as "SSVP.PAC.Acq4D.1319"' + RESET)
print
#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1319")
print (GREEN +"                                                        ---- END of TC 2.16.1 for XRBB ----" +RESET)






























