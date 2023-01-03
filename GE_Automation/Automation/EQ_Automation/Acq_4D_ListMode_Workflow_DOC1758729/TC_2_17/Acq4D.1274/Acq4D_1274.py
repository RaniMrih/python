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
TimeStamp_Inc=[]
TimeStamp_Latter=[]
TimeStamp_First=[]
TimeStamp_Last=[]
Avg_Rate=[]
TC_start='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1272'
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1274'
print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.17 Step 1274, Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#--- check if step pass or fail according to yes/no
def Step_Result(StepNum):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)

#---- find valid Singles samples
def find_Valid_Singles():
   for line in open(PWD + "/rdfTell_hs_LIST0000.txt", "r"):
      line = line.rstrip()
      if re.search('    Number of valid Singles samples in the RDF:', line):
        line1=split_string2(line)
   return line1[1]

#---- find valid units Integration Deadtime samples
def find_valid_Unit_Integration():
   for line in open(PWD + "/rdfTell_hd_LIST0000.txt", "r"):
      line = line.rstrip()
      if re.search('valid Unit Integration Deadtime', line):
        line1=split_string2(line)
   return line1[0]

#---- find valid Unit Mux Deadtime samples
def find_Unit_Mux_units():
   for line in open(PWD + "/rdfTell_hd_LIST0000.txt", "r"):
      line = line.rstrip()
      if re.search('valid Unit Mux Deadtime samples', line):
        line1=split_string2(line)
   return line1[0]

#---- find valid Deadtime Events samples
def find_DeadTime_Events():
   for line in open(PWD + "/rdfTell_hd_LIST0000.txt", "r"):
      line = line.rstrip()
      if re.search('valid Deadtime Events samples', line):
        line1=split_string2(line)
   return line1[0]

#---- find valid Deadtime samples Records
def find_DeadTime_Samples_Records():
   for line in open(PWD + "/rdfTell_hd_LIST0000.txt", "r"):
      line = line.rstrip()
      if re.search('valid Deadtime Samples Records', line):
        line1=split_string2(line)
   return line1[0]

#---- find timestampe increaces by 1000ms
def find_TimeStamp_Increace():
   for line in open(PWD + "/TimeStampInitial.txt", "r"):
      line = line.rstrip()
      if re.search('Length of sample in milliseconds', line):
        line1=split_string2(line)
        TimeStamp_Inc.append(line1[0])

#---- find timestampe increaces by 1000ms for later data
def find_TimeStamp_Latter():
   for line in open(PWD + "/TimeStampLatter.txt", "r"):
      line = line.rstrip()
      if re.search('Length of sample in milliseconds', line):
        line1=split_string2(line)
        TimeStamp_Latter.append(line1[0])


#---- find First timestampe
def find_First_TimeStamp():
   for line in open(PWD + "/TimeStampInitial.txt", "r"):
      line = line.rstrip()
      if re.search('Start of sample in millisecond', line):
        line1=split_string2(line)
        TimeStamp_First.append(line1[0])

#---- find last timestampe from /TimeStampLatter.txt
def find_Last_TimeStamp():
   for line in open(PWD + "/TimeStampLatter.txt", "r"):
      line = line.rstrip()
      if re.search('Start of sample in millisecond', line):
        line1=split_string2(line)
        TimeStamp_Last.append(line1[0])

# ------------------------------------ step 1  --------------------------------------------
print ("Creating rdfTell -hS 10hr.BLF,rdfTell -hd 10hr.BLF for ListFile, please wait...")
os.system("rdfTell -hS "+TC_start+"/LIST0000.BLF > rdfTell_hs_LIST0000.txt")
os.system("rdfTell -hd "+TC_start+"/LIST0000.BLF > rdfTell_hd_LIST0000.txt")
os.system("cp rdfTell_hs_LIST0000.txt " +PWD)
os.system("cp rdfTell_hd_LIST0000.txt " +PWD)
#----------- qustion ---------
print
time.sleep(3)
print (BLUE + "1) Number of valid Singles samples :" +RESET)
Vsingles=find_Valid_Singles()
print Vsingles

#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "Number of valid Singles samples in the RDF: 36001 +/-1 ?" +RESET)
if int(Vsingles) > 36002 or int(Vsingles) < 36000:
  YesNo(False)
else:
  YesNo(True)

# ------------------------------------ step 2  --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print (BLUE + "2) Number of valid Unit Integration Deadtime samples:" +RESET)
V_U_Integration = find_valid_Unit_Integration()
print V_U_Integration
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of valid Unit Mux Deadtime samples :" +RESET)
V_U_Mux = find_Unit_Mux_units()
print V_U_Mux
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of valid Deadtime Events samples :" +RESET)
V_DeadTime_Events = find_DeadTime_Events()
print V_DeadTime_Events

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of valid Deadtime Samples Records :" +RESET)
V_DeadTime_Samples_Records = find_DeadTime_Samples_Records()
print V_DeadTime_Samples_Records

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Number of valid Unit Integration Deadtime samples are 36001 +/-1 ?"+RESET)
if int(V_U_Integration) > 36002 or int(V_U_Integration) < 36000:
  YesNo(False)
else:
  YesNo(True)
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Number of valid Unit Mux Deadtime samples are 36001 +/-1 ?"+RESET)
if int(V_U_Mux) > 36002 or int(V_U_Mux) < 36000:
  YesNo(False)
else:
  YesNo(True)
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Number of valid Unit Deadtime Events samples are 36001 +/-1 ?"+RESET)
if int(V_DeadTime_Events) > 36002 or int(V_DeadTime_Events) < 36000:
  YesNo(False)
else:
  YesNo(True)
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Number of valid Deadtime samples Records are 36001 +/-1 ?"+RESET)
if int(V_DeadTime_Samples_Records) > 36002 or int(V_DeadTime_Samples_Records) < 36000:
  YesNo(False)
else:
  YesNo(True)
# ------------------------------------ step 3  --------------------------------------------
os.system('rdfTell -hd '+TC_start+'/LIST0000.BLF | egrep "\[ | Start | Len" | head -30 > TimeStampInitial.txt')
os.system("cp TimeStampInitial.txt "+PWD)
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) The timestamps of each Sample in initial set of"+'\n'+"Samples increases by 1000 milliseconds from one"+RESET)
print (BLUE + "sample to the next?"+RESET)
find_TimeStamp_Increace()
Within_1K_Ms=True
for i in TimeStamp_Inc:
   if int(i) != 1000:
     Within_1K_Ms=False
YesNo(Within_1K_Ms)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "first Sample timestamp :"+RESET)
find_First_TimeStamp()
print TimeStamp_First[0]

# ------------------------------------ step 4  --------------------------------------------
os.system('rdfTell -hd '+TC_start+'/LIST0000.BLF | egrep "\[ | Start | Len" | tail -30 > TimeStampLatter.txt')
os.system("cp TimeStampLatter.txt "+PWD)
#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "4)The timestamps of each Sample in latter set of "+'\n'+"Samples increases by 1000 milliseconds from one "+RESET)
print (BLUE + "sample to the next?"+RESET)
find_TimeStamp_Latter()
Within_1K_Ms=True
for i in TimeStamp_Latter:
   if int(i) != 1000:
     Within_1K_Ms=False
YesNo(Within_1K_Ms)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "last Sample timestamp :"+RESET)
find_Last_TimeStamp()
Last= TimeStamp_Last[len(TimeStamp_Last)-1]
print Last
#----------- qustion ---------
print
time.sleep(1)
print (BLUE + "5) The last Sample timestamp minus the first Sample "'\n'+"shall equal 36001000 +/- 1000 milliseconds? "+RESET)
sum=int(Last) - int(TimeStamp_First[0])
if int(sum) > 36002000 or int(sum) < 36000000:
  YesNo(False)
else:
  YesNo(True)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1274")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1275/Acq4D_1275.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_17/Acq4D.1275/Acq4D_1275.py")





