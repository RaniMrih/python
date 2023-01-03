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
Table_Live=[]
Table_Replay=[]
PWD = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1166'
TC_start_2_1='/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'
TC_start = '/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1165'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.2 Step 1166 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
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

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

#---- check if acqParams are identecal
def diffSysGeo():
   result1=[]
   result2=[]
   f1 = open(TC_start + "/LiveHdrs_2.1.tell", "r")
   f2 = open(TC_start + "/ReplayHdrs_2.2.tell", "r")
   for line1 in f1:
     if "sysGeo" in line1:
       result1.append(line1)
   for line2 in f2:
     if "sysGeo" in line2:
       result2.append(line2)
   if result1 != result2:
     return False
   else:
     return True

#-----------------------------------------------------------------------------------------

# grep sinos  path
f = open( TC_start_2_1+"/SINOSPath2_1.txt" , "r")
for line in f:
  SinosDirectory2_1 = line.strip('\n')

# grep sinos  path
f = open( TC_start +"/SINOSPath2_2.txt" , "r")
for line in f:
  SinosDirectory2_2 = line.strip('\n')

print "Creating LiveHdrs_2.1.tell file, please wait..."
os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SinosDirectory2_1+"/SINO* > LiveHdrs_2.1.tell")
time.sleep(1)
print "Creating ReplayHdrs_2.2.tell file, please wait..."
os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SinosDirectory2_2+"/SINO* > ReplayHdrs_2.2.tell")

os.system("grep 'Scan Description =\|Database Scan ID\|examData.scanIdDicom\|Scan ID\|examData.scanID|examData.scanDescription:' "+TC_start+"/LiveHdrs_2.1.tell > A.txt")
os.system("grep 'Scan Description =\|Database Scan ID\|examData.scanIdDicom\|Scan ID\|examData.scanID|examData.scanDescription:' "+TC_start+"/ReplayHdrs_2.2.tell > B.txt")

os.system("grep -v 'Scan Description =\|Database Scan ID\|examData.scanIdDicom\|Scan ID\|examData.scanID\|examData.scanDescription:' "+TC_start+"/LiveHdrs_2.1.tell | grep 'examData'>C.txt")
os.system("grep -v 'Scan Description =\|Database Scan ID\|examData.scanIdDicom\|Scan ID\|examData.scanID\|examData.scanDescription:' "+TC_start+"/ReplayHdrs_2.2.tell | grep 'examData'>D.txt")

# ------------------------------------ step 1 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "5. a) The RDF Exam/Scan Data should match for all"+'\n'+"the parameters other than following parameters ?" +RESET)
print (BLUE + "i) Scan Description"+'\n'+"ii) Database Scan ID and alias examData.scanIdDicom"+'\n'+"iii) Scan ID (RDF pathname seed in hex) and alias examData.scanID" +RESET)

os.system("diff "+TC_start+"/A.txt "+TC_start+"/B.txt > diff.txt")
os.system("diff "+TC_start+"/C.txt "+TC_start+"/D.txt > diff1.txt")

Diff=True
if os.stat(TC_start + "/diff.txt").st_size == 0:
  Diff = False
if os.stat(TC_start + "/diff1.txt").st_size > 0:
  Diff = False
YesNo(Diff)
os.system("rm -rf "+TC_start+"/A.txt")
os.system("rm -rf "+TC_start+"/B.txt")
os.system("rm -rf "+TC_start+"/C.txt")
os.system("rm -rf "+TC_start+"/D.txt")

#----------- qustion ---------
time.sleep(1)
print (BLUE + "All other not identified RDF Exam Information matchs ?" +RESET)
if os.stat(TC_start + "/diff1.txt").st_size == 0:
  YesNo(True)
else:
  YesNo(False)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "5. b) Acq Parameters Header Matchs for all "+'\n'+"parameters except :" +RESET)
print (BLUE + "i) Event Source"+'\n'+"ii) Event Simulation Data"+'\n'+"iii) Start Condition"+'\n'+"iv) Retro Scan flag" +RESET)

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "and possibly the 'Table Location' "+RESET)
# check table location
TableLocation=False
for line in open(TC_start + "/ReplayHdrs_2.2.tell", "r"):
  line = line.rstrip()
  if re.search('tableLocation', line):
    TableLocation=True
YesNo(TableLocation)

os.system("grep -v 'eventSource\|eventSimulationData\|startCondition\|retroScan' "+TC_start+"/LiveHdrs_2.1.tell > A.txt")
os.system("grep -v 'eventSource\|eventSimulationData\|startCondition\|retroScan' "+TC_start+"/ReplayHdrs_2.2.tell > B.txt")
os.system("grep -v 'eventSource\|eventSimulationData\|startCondition\|retroScan' "+TC_start+"/LiveHdrs_2.1.tell | grep 'acqParams' > C.txt")
os.system("grep -v 'eventSource\|eventSimulationData\|startCondition\|retroScan' "+TC_start+"/ReplayHdrs_2.2.tell | grep 'acqParams' > D.txt")

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Acq Parameters Table Location matches within +/- 0.5mm "+RESET)
for line in open(TC_start + "/LiveHdrs_2.1.tell", "r"):
  line = line.rstrip()
  if re.search('tableLocation', line):
    result=split_string2(line)
    Table_Live.append(result[1])


for line in open(TC_start + "/ReplayHdrs_2.2.tell", "r"):
  line = line.rstrip()
  if re.search('tableLocation', line):
    result=split_string2(line)
    Table_Replay.append(result[1])

diff = float(Table_Live[0]) - float(Table_Replay[0])
if diff > 0.5 or diff < -0.5:
  YesNo(False)
else:
  YesNo(True) 

#----------- qustion ---------
time.sleep(1)
print (BLUE + "c) The RDF System Geometry Headers matches for "+'\n'+"all the parameters ? " +RESET)
SysGeo= diffSysGeo()
YesNo(SysGeo)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "5. d) The Detector Module Signature Data 'Serial"+'\n'+"Numbers' and 'Block Valid Flags' Match ?   " +RESET)

os.system("grep 'Module\[' "+TC_start + "/LiveHdrs_2.1.tell > A.txt")
os.system("grep 'Module\[' "+TC_start + "/ReplayHdrs_2.2.tell > B.txt")
os.system("diff A.txt B.txt > C.txt")
if os.stat("C.txt").st_size > 0:
  ModulesDiff = False
else:
  ModulesDiff = True
YesNo(ModulesDiff)

os.system("rm -rf "+TC_start+"/A.txt")
os.system("rm -rf "+TC_start+"/B.txt")
os.system("rm -rf "+TC_start+"/C.txt")
os.system("rm -rf "+TC_start+"/D.txt")

#----------- qustion ---------
time.sleep(1)
print (BLUE + "6) The SSVP.1166.objE.txt file is  printed, labeled"+'\n'+"with 'SSVP.PAC.Acq4D.1166', initialed, dated  " +RESET)
print (BLUE + "and included as part of Test Results." +RESET)

os.system("egrep 'Detector Mod|RingDiam|scanMode' "+TC_start+"/LiveHdrs_2.1.tell > SSVP.1166.objE.txt")
os.system("egrep 'Detector Mod|RingDiam|scanMode' "+TC_start+"/ReplayHdrs_2.2.tell >> SSVP.1166.objE.txt")
os.system("diff "+TC_start +"/LiveHdrs_2.1.tell "+TC_start+"/ReplayHdrs_2.2.tell >> SSVP.1166.objE.txt")

if os.stat(TC_start+"/SSVP.1166.objE.txt").st_size > 0:
  os.system("cp "+TC_start+"/SSVP.1166.objE.txt "+PWD)
  YesNo(True)
  print (YELLOW + 'NOTE: SSVP.1166.objE.txt located at: ~/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1166' + RESET)
else:
  YesNo(False)

#-- determine if step Pass/Fail
time.sleep(1)
print
Step_Result("Acq4D.1166")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1167/Acq4D_1167.py")
os.system("/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729/TC_2_2/Acq4D.1167/Acq4D_1167.py")


