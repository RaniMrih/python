#!/usr/bin/env python
import os, sys
import time
import re
import os.path
#VARIABLES
Step_Pass=True
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'
IsCompressed =[]
Standard_dev=[]
Avg_Rate=[]
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1272'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::: Running XRBB TC_2.17 Step 1328 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.17 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- find Original list file Size
def find_Orig_List_Size():
   os.system("rdfTell -hl LIST0000.BLF | egrep sizeOfList > Tmp.txt")
   for line in open(PWD + "/Tmp.txt", "r"):
     line = line.rstrip()
     if re.search('listHdr.sizeOfList', line):
       line1=split_string(line)
       OriginSize=line1[12]
   return OriginSize

#---- find Compress list file Size
def find_Compress_List_Size():
   os.system("rdfTell -hl LIST0000.BLF | egrep sizeOfCompressedList > Tmp.txt")
   for line in open(PWD + "/Tmp.txt", "r"):
     line = line.rstrip()
     if re.search('listHdr.sizeOfCompressedList', line):
       line1=split_string(line)
       CompSize=line1[2]
   return CompSize

#---- find total duration
def find_Total_Duration():
   for line in open(PWD + "/LT_Mt_Sh.10hr.txt", "r"):
     line = line.rstrip()
     if re.search('Total duration', line):
       line1=split_string(line)
       TotalD=line1[2]
   return TotalD

#---- find Average Prompts per second
def find_Average_Prompts():
   for line in open(PWD + "/LT_Mt_Sh.10hr.txt", "r"):
     line = line.rstrip()
     if re.search('Average Prompts Per Second', line):
       line1=split_string(line)
       AvePrompts=line1[4]
   return AvePrompts

#---- find Standard Devaition in Statistics for prompts(C)
def find_StdV():
   for line in open(PWD + "/LT_Mt_Sh.10hr.txt", "r"):
     line = line.rstrip()
     if re.search('Standard Devaition:', line):
       line1=split_string(line)
       Standard_dev.append(line1[2])

#---- find Avg Rate in Randoms
def find_Avarage_rate():
   for line in open(PWD + "/LT_Mt_Sh.10hr.txt", "r"):
     line = line.rstrip()
     if re.search('Average Rate', line):
       line1=split_string(line)
       Avg_Rate.append(line1[2])
   
# ----------------------------------------------------------------------------------------

# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_LIST.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_LIST.txt" , "r")
  for line in f:
    ListsDirectory2_17 = line.strip('\n')
  print "Enter LIST path directory from" + BLUE + " section 2.17 :" +RESET + ListsDirectory2_17
  print

else:
  # ---------------------------------------------------------------------------------------
  ListsDirectory2_17 = raw_input("Enter List path directory from" + BLUE + " section 2.17 :" + RESET)
  while ListsDirectory2_17 == "":
    ListsDirectory2_17 = raw_input("Enter List path directory from" + BLUE + " section 2.17 :" + RESET)

#like echo to file
f=open("LISTSPath2_17.txt", "w+")
f.write(ListsDirectory2_17)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")
os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt")
# ------------------------------------ step 1 --------------------------------------------
print "Creating ln -sf "+ListsDirectory2_17+"/LIST0000.BLF > 10hr.BLF, please wait..."
time.sleep(1)
os.system("ln -sf " +ListsDirectory2_17 + "/LIST0000.BLF > 10hr.BLF")
os.system("rdfTell -hl LIST0000.BLF > Tmp.txt")
for line in open(PWD + "/Tmp.txt", "r"):
   line = line.rstrip()
   if re.search('listHdr.isListCompressed:', line):
     line1=split_string(line)
     IsCompressed.append(line1[6])

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "2) listHdr.isListCompressed: 1 ?" +RESET)
if int(IsCompressed[0]) == 1:
  YesNo(True)
else:
  YesNo(False)  
# ------------------------------------ step 3 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) size of the original LIST file (sizeOfList):" +RESET)
OriginalSize=find_Orig_List_Size()
print OriginalSize
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "size of the compressed LIST file "+'\n'+"(sizeOfCompressedList):" +RESET)
CompressSize=find_Compress_List_Size()
print CompressSize
os.system("rm -rf "+PWD+"/Tmp.txt")

#cant be zero accordin to instructions mark NA
if int(CompressSize) == 0 or int(OriginalSize) == 0:
  #----------- qustion ---------
  time.sleep(1)
  print
  print (BLUE + "The compressed list is at least 25%"+'\n'+"reduced ?" +RESET)
  print (RED+"NA -"+RESET+ "According to instruction")
else:
  #----------- qustion ---------
  time.sleep(1)
  print
  print (BLUE + "The compressed list is at least 25%"+'\n'+"reduced ?" +RESET)
  #percentReduced = 100 -((sizeOfCompressed / SizeOfList)*100.0)
  if 100 - ((float(CompressSize) / float(OriginalSize)) * 100.0) < 25.0:
    YesNo(True)
  else:
    YesNo(False)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "percentReduced to 0.1% percision :" +RESET)
print (RED +"NA -"+RESET+ "According to instruction")
print
# ------------------------------------ step 4 --------------------------------------------
print ("Creating LT_Mt_Sh.10.csv, LT_Mt_Sh.10hr.txt for ListFile, please wait...")
os.system("ListTool -Mt -Sh -f LT_Mt_Sh.10.csv "+PWD+"/LIST0000.BLF > LT_Mt_Sh.10hr.txt")

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "4)"+'\n'+"a)Total duration :" +RESET)
TotalDuration=find_Total_Duration()
print TotalDuration

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Total duration: 36001 secs +/-1 sec ?" +RESET)
if int(TotalDuration) > 36002 or int(TotalDuration) < 36000:
  YesNo(False)
else:
  YesNo(True)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "b) Average Prompts per second :" +RESET)
AvePrompts = find_Average_Prompts()
print AvePrompts

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "An 'Avg Prompts Per Sec' that is equal to the Test"+'\n'+"2.24.0-1 Recorded 'Prompt Rate At Pet Scan'"+'\n'+"Start' +/- 5% ?'" +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW+"NOTE : Compare with Prompt Count Rate at Pet Scan start at step 1271 "+ RESET)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Avg Prompts in KCPS :" +RESET)
KCPS = float(AvePrompts) / 1000.0
print KCPS

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "C) Standard Devaition :" +RESET)
find_StdV()
print Standard_dev[0]

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Standard Devaition Rate:" +RESET)
#StdV Rate = (standard devaition / Average Prompts per second)*100
Stdv_Rate = (float(Standard_dev[0]) / float(AvePrompts)) * 100
print Stdv_Rate


time.sleep(1)
print
print (BLUE + "Standard Devaition Rate is less than 10% ?" +RESET)

if float(Stdv_Rate) < 10.0:
  YesNo(True)
else:
  YesNo(False)
  
#----------- qustion ---------
time.sleep(1)
print (BLUE + "d) Average Rate for Randoms:" +RESET)
find_Avarage_rate()
print Avg_Rate[0]
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Standard Devaition for Randoms:" +RESET)
print Standard_dev[1]
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Standard Devaition Rate for Randoms: " +RESET)
#Standard Devaition Rate = (Standard Devaition / Average Rate) * 100
Stdv_Rate_Randoms = (float(Standard_dev[1]) / float(Avg_Rate[0])) * 100
print Stdv_Rate_Randoms

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Standard Devaition Rate for Randoms is less than 10% ?" +RESET)
if float(Stdv_Rate_Randoms) < 10.0:
  YesNo(True)
else:
  YesNo(False)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1272")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1273/Acq4D_1273.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1273/Acq4D_1273.py")










































