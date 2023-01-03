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
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1156'
TC_start = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1154'

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::::::: Running TC_2.1 Step 1156 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )

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

#---- split line to array according to  ':'
def split_string2(line):
   list_string=line.split(':')
   return list_string

def find_Operator_Id(File):
   for line in open(TC_start + File, "r"):
     line = line.rstrip()
     if re.search('Operator', line):
       name=line.replace(line[:9],'')
   return name

def find_Patient_Id(File):
   for line in open(TC_start + File, "r"):
     line = line.rstrip()
     if re.search('patientID', line):
       name=line.replace(line[:9],'')
   return name

### if searching for Scan ID the step will fail 
def find_Scan_Id(File):
   for line in open(TC_start + File, "r"):
     line = line.rstrip()
     if re.search('Database Scan ID', line):
       name=line.replace(line[:9],'')
   return name

#---- check if examData are identecal
def diffexamData():
   Same = True
   f1 = os.popen("grep -v 'examData.patientID\|examData.scanIdDicom\|examData.Operator\|examData.scanID'  " + TC_start + "/S2.1SinoHdrs.txt | grep examData")
   f1 = f1.read()
   f2 = os.popen("grep -v 'examData.patientID\|examData.scanIdDicom\|examData.Operator\|examData.scanID'  " + TC_start + "/S2.1ListHdrs.txt | grep examData")
   f2 = f2.read()
   if f1 != f2:
     Same=False
   return Same

#---- check if acqParams are identecal
def diffAcqParams():
   result1=[]
   result2=[]
   f1 = open(TC_start + "/S2.1SinoHdrs.txt", "r")
   f2 = open(TC_start + "/S2.1ListHdrs.txt", "r")
   for line1 in f1:
     if "acqParams" in line1:
       result1.append(line1)
   for line2 in f2:
     if "acqParams" in line2:
       result2.append(line2)
   if result1 != result2:
     return False
   else:
     return True

#---- check if acqParams are identecal
def diffSysGeo():
   result1=[]
   result2=[]
   f1 = open(TC_start + "/S2.1SinoHdrs.txt", "r")
   f2 = open(TC_start + "/S2.1ListHdrs.txt", "r")
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

# ------------------------------------ step 2 --------------------------------------------
#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "Is the Patient and Exam/Scan Data reported in "+'\n'+"Sinogram RDF file matches with the patient and " +RESET)
print (BLUE + "Exam information entered in Section 2.1 "+'\n'+"(SSVP.PAC.Acq4D.1154) ? " +RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE: Check manually' + RESET)
print

#----------- qustion ---------
time.sleep(1)
print (BLUE + "The Patient and Exam Data in the Sinogram file is:" +RESET)
OperatorID_Sino = find_Operator_Id("/S2.1SinoHdrs.txt")
PatientID_Sino = find_Patient_Id("/S2.1SinoHdrs.txt")
print PatientID_Sino
print OperatorID_Sino

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The Patient and Exam Data in the List file is:" +RESET)
OperatorID_List = find_Operator_Id("/S2.1ListHdrs.txt")
PatientID_List = find_Patient_Id("/S2.1ListHdrs.txt")
check_empty = split_string2(OperatorID_List) 
if check_empty[1]=="":
  print "NA"+'\n'+"NA"
else:
  print PatientID_List
  print OperatorID_List

#----------- qustion ---------
time.sleep(1)
print
print (BLUE + "The List Files Exam Data matches the Sino Files"+'\n'+"Exam Data for all parameters other than" +RESET)
print (BLUE + "a) Patient ID"+'\n'+"b) Operator"+'\n'+"c) Scan ID" +RESET)
ScanID_List= find_Scan_Id("/S2.1ListHdrs.txt")
ScanID_Sino= find_Scan_Id("/S2.1SinoHdrs.txt")

ExamData = True
if PatientID_Sino == PatientID_List or OperatorID_Sino == OperatorID_List or ScanID_List==ScanID_Sino:
  ExamData = False
else:
  ExamData = diffexamData()
YesNo(ExamData)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is List files' Acquisition Parameters' matches with"+'\n'+"the Sinogram files 'Acquisition Parameters'? " +RESET)
AcqParams= diffAcqParams()
YesNo(AcqParams)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is List files 'System Geometry' matches with"+'\n'+"the Sinogram files 'System Geometry Parameters'? " +RESET)
SysGeo= diffSysGeo()
YesNo(SysGeo)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is List files 'Detector Module Temperatures' matches with"+'\n'+"the Sinogram files 'Detector Module Temperatures'? " +RESET)

os.system("grep 'Module\[' "+TC_start + "/S2.1SinoHdrs.txt > A.txt")
os.system("grep 'Module\[' "+TC_start + "/S2.1ListHdrs.txt > B.txt")
os.system("diff A.txt B.txt > C.txt")
if os.stat("C.txt").st_size > 0:
  ModulesDiff = False
else:
  ModulesDiff = True
YesNo(ModulesDiff)
os.system("rm -rf A.txt B.txt C.txt")
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is List files 'Detector Module Serial Nos.' matches with"+'\n'+"the Sinogram files 'Detector Module Serial Nos.'? " +RESET)
YesNo(ModulesDiff)

#----------- qustion ---------
time.sleep(1)
print (BLUE + "Is List files 'Detector Block Valid Flags' matches with"+'\n'+"the Sinogram files 'Detector Block Valid Flag'? " +RESET)
YesNo(ModulesDiff)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1156")

os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1157/Acq4D_1157.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_1/Acq4D.1157/Acq4D_1157.py")




























