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
num =[]
sinosList = ["00","09","12","15"]
Sixteen = False
Equal = False
PWD = '/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196'
Step_Pass=True

print
print (GREEN + ":::::::::::::::::::::::::::::::::::::::::::::: Running XRBB TC_2.5 Step 1196 , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print (GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all TC 2.5 press ctrl+c to stop ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + RESET )
print
time.sleep(2)
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

#---- split line to array according to ','
def split_string(line):
   list_string=line.split(',')
   return list_string

#---- check if "Scan Description", "Database Scan ID (and alias examData.scanIdDicom", "Scan ID" diffrent
def diffScanDescription(item):
   result2=""
   for i in sinosList:
     f1 = open(PWD+"/Tell2.4.SINO00" + i, "r")
     f2 = open(PWD+"/Tell2.5.SINO00" + i, "r")
     for line1 in f1:
       if item in line1:
         result1=line1
     for line2 in f2:
       if item in line2:
         result2=line2
     if result1 == result2:
       return False

#---- check if other examData are identecal
def diffexamData():
   result2=""
   for i in sinosList:
     f1 = open(PWD+"/Tell2.4.SINO00" + i, "r")
     f2 = open(PWD+"/Tell2.5.SINO00" + i, "r")
     for line1 in f1:
       if "examData" in line1:
         result1=line1
     for line2 in f2:
       if "examData" in line2:
         result2=line2
     if result1 != result2:
       return False
#---- check if "Event Source", simulation data", "start condition", "Retro flag" diffrent
def diffAcqParams1(item):
   result2=""
   for i in sinosList:
     f1 = open(PWD+"/Tell2.4.SINO00" + i, "r")
     f2 = open(PWD+"/Tell2.5.SINO00" + i, "r")
     for line1 in f1:
       if item in line1:
         result1=line1
     for line2 in f2:
       if item in line2:
         result2=line2
     if result1 == result2:
       return False

#---- check if other acqParams are identecal
def diffAcqParams2():
   result2=""
   for i in sinosList:
     f1 = open(PWD+"/Tell2.4.SINO00" + i, "r")
     f2 = open(PWD+"/Tell2.5.SINO00" + i, "r")
     for line1 in f1:
       if "acqParams" in line1:
         for item in paramsList1:
           if item in line1:
             continue;
           else:
             result1=line1
     for line2 in f2:
       if "acqParams" in line2:
         for item in paramsList1:
           if item in line2:
             continue;
           else:
             result2=line2
     if result1 != result2:
       return False

#---- sum CPM Conic Loss and check within 0.1%
def checkCPMLoss():
   result1 = ""
   result2 = ""
   sum=0
   Within0_1=True
   DiffCpmLoss=0
   for i in sinosList:
     f1 = open(PWD+"/Tell2.4.SINO00" + i, "r")
     f2 = open(PWD+"/Tell2.5.SINO00" + i, "r")
     for line1 in f1:
       if "Total coincidence events lost" in line1:
         result1=line1.replace(": Total coincidence events lost in latter stages of CPM",'')
         result1=result1.rstrip('\n')
     for line2 in f2:
       if "Total coincidence events lost" in line2:
         result2=line2.replace(": Total coincidence events lost in latter stages of CPM",'')
         result2=result2.rstrip('\n')
     #acoording to doors :  %DiffCpmLoss = (abs(Live CPM loss- Replay CPM loss) / Live CPM loss) * 100.0
     DiffCpmLoss = (float(result1) - float(result2)) / float(result1)
     DiffCpmLoss *=100
     if DiffCpmLoss < 0:
       DiffCpmLoss *= -1
     if DiffCpmLoss > 0.1:
       Within0_1 =False
   YesNo(Within0_1)

#---- diff signature and valid flag
#---- grep -v in bash greps only relevant modules and delete other
def checkSignature_ValidFlag():
   result1=""
   result2=""
   for i in sinosList:
     if i == "00":
       os.system("grep -v 'BS Module\|Singles\|BMD Module\|Block Mux\|BBD Module\|Block Busy' Tell2.4.SINO00"+i+" | grep 'Module' >"+PWD+"/A.txt")
       os.system("grep -v 'BS Module\|Singles\|BMD Module\|Block Mux\|BBD Module\|Block Busy' Tell2.5.SINO00"+i+" | grep 'Module' >"+PWD+"/B.txt")
     else:
       os.system("grep -v 'BS Module\|Singles\|BMD Module\|Block Mux\|BBD Module\|Block Busy' Tell2.4.SINO00"+i+" | grep 'Module' >>"+PWD+"/A.txt")
       os.system("grep -v 'BS Module\|Singles\|BMD Module\|Block Mux\|BBD Module\|Block Busy' Tell2.5.SINO00"+i+" | grep 'Module' >>"+PWD+"/B.txt")
     os.system("diff A.txt B.txt > C.txt")
     if os.stat("C.txt").st_size > 0:
       ModulesDiff = False
     else:
       ModulesDiff = True
    
   YesNo(ModulesDiff)       

#--- check Modules temperature for sino15
def checkTemperature15():
   os.system("grep -v 'BS Module\|Singles\|BMD Module\|Block Mux\|BBD Module\|Block Busy' Tell2.4.SINO0015 | grep 'Module' >"+PWD+"/A.txt")
   os.system("grep -v 'BS Module\|Singles\|BMD Module\|Block Mux\|BBD Module\|Block Busy' Tell2.5.SINO0015 | grep 'Module' >"+PWD+"/B.txt")
   os.system("diff A.txt B.txt > C.txt")
   if os.stat("C.txt").st_size > 0:
     TempDiff = False
   else:
     TempDiff = True
   YesNo(TempDiff)

#--- check system geometry
def checkSysGeo():
   result1=""
   result2=""
   for i in sinosList:
     if i == "00":
       os.system("grep 'sysGeo' Tell2.4Geo.SINO00"+i+ ">" +PWD+"/A.txt")
       os.system("grep 'sysGeo' Tell2.5Geo.SINO00"+i+ ">" +PWD+"/B.txt")
     else:
       os.system("grep 'sysGeo' Tell2.4Geo.SINO00"+i+ ">>" +PWD+"/A.txt")
       os.system("grep 'sysGeo' Tell2.5Geo.SINO00"+i+ ">>" +PWD+"/B.txt")
# diff txt file via bash
     os.system("diff A.txt B.txt > diffSysGeo.txt")    
# check if file is empty python  
   if os.stat("diffSysGeo.txt").st_size > 0:
     YesNo(False)
   else:
     YesNo(True)
#------------------------------------- step 2 (first) --------------------------------------------
# if user entered path in zenity popup
if os.path.exists('/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt'):
  # grep sinos  path
  f = open( "/usr/g/ctuser/EQ_Automation/User_Input_SINO.txt" , "r")
  for line in f:
    SinosDirectory2_5 = line.strip('\n')
  print "Enter Sinograms path directory from" + BLUE + " section 2.5 :" +RESET + SinosDirectory2_5
else:
  #use of raw_input() from user
  SinosDirectory2_5 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.5 :" + RESET)
  # while SinosDirectory2_5 is empty
  while SinosDirectory2_5 == "":
    SinosDirectory2_5 = raw_input("Enter Sinograms path directory from" + BLUE + " section 2.5 again:" + RESET)


f=open("SINOSPath2_5.txt", "w+")
f.write(SinosDirectory2_5)
f.close()

os.system("rm -rf /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt")


time.sleep(1)
print (BLUE + "2) Number RDF Files :" + RESET)

#this method counts files number in directory
for item in os.listdir(SinosDirectory2_5):
  if item.startswith('SINO'):
    num.append(item)
print len(num)
print
#------------------------------------- step 3 (second) --------------------------------------------
#Create rdfTell files
print ("Creating Tell2.5 files ...")
os.system("rdfTeller -r  ' -h  efadS -v -Ha -S'  -f Tell2.5 "+ SinosDirectory2_5 +"/SINO*")
print
#----------- qustion ---------
time.sleep(1)
print (BLUE + "3) The RDF Exam/Scan Data information is same "+'\n'+"other than following parameters?" +RESET)
print (BLUE + "a) Scan Description"+'\n'+"b) Database Scan ID (and alias"+'\n'+"examData.scanIdDicom" +RESET)
print (BLUE + "c) Scan ID (RDF pathname seed in hex) and alias "+'\n'+"examData.scanID"+RESET)

#copy TellGeo2.4 and Tell2.4.SINO000, 09, 12, 15 to PWD
for x in sinosList:
  os.system("cp ~/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1193/Tell2.4.SINO00"+ x +" "+PWD)
  os.system("cp ~/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_4/Acq4D.1189/Tell2.4Geo.SINO00"+ x +" "+PWD)

#list of params that need to check
paramsList =["Scan Description","Database Scan ID","examData.scanId","examData.scanID"]

#send to diff function one by one from paramsList
x = True
for item in paramsList:
   x1 = diffScanDescription(item)
   if x1 == False:
     x = False

#send to diff to check other "examData"
x1 = diffexamData()
if x1 == False:
  x=False

#send to YesN0 function True/False
YesNo(x)
#----------- qustion ---------
time.sleep(1)
print (BLUE + "The Acquisition  Parameters should match for all"+'\n'+"parameters other than mentioned below?" +RESET)
print (BLUE + "a) Event Source"+'\n'+"b) Event Simulation Data" +RESET)
print (BLUE + "c) Start Condition"+'\n'+"d) Retro Scan flag" +RESET)

#list of params that need to check
paramsList1 =["eventSource","eventSimulation","startCondition","retroScan"]
x=True
for item1 in paramsList1:
   x1 = diffAcqParams1(item1)
   if x1 ==False:
     x=False

x2 = diffAcqParams2()
if x2 == False:
  x=False

#send to YesN0 function True/False
YesNo(x)
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Difference in CPM Coinc Losses between live and"+'\n'+"the replay are within 0.1%?" +RESET)
checkCPMLoss()
#----------- qustion ---------
time.sleep(1)
print (BLUE + "Detector Module Signature Data 'Serial Numbers'"+'\n'+"and 'Block Valid Flags' Match? " +RESET)
checkSignature_ValidFlag()
#----------- qustion ---------
time.sleep(1)
print (BLUE + "The Detector Module Signature Data"+'\n'+"'Temperatures' for the SINO0015 files match?" +RESET)
checkTemperature15()
#----------- qustion ---------
time.sleep(1)

# rdfTeller create Tell2.5Geo for all sinos
print ("Creating Tell2.5Geo files, please wait ...")
os.system("rdfTeller -r  ' -h  g -v -Ha -S' -f Tell2.5Geo "+ SinosDirectory2_5 +"/SINO*")

print (BLUE + "4) System Geometry  Headers Match?"+RESET)
checkSysGeo()
#----------- qustion ---------
print (BLUE + "5) Are the rdfTell output files:"+'\n'+"Tell2.4.SINO*, Tell2.5.SINO* and Tell2.5Geo.SINO*" +RESET)
print (BLUE + "for frames 0. 9 , 12, 15 printed and labeled as"+'\n'+"'SSVP.PAC.Acq4D.1196 2.4_Sino'," +RESET)
print (BLUE + "'SSVP.PAC.Acq4D.1196 2.5_Sino',"+'\n'+"SSVP.PAC.Acq4D.1196 2.4_SinoGeo" +RESET)
print (BLUE + "and 'SSVP.PAC.Acq4D.1196 2.5_SinoGeo'"+'\n'+"respectively. and initialed, dated and included as " +RESET)
print (BLUE + "part of Test Results?"+RESET)
print "[ ] Yes"
print "[ ] No"
print (YELLOW + 'NOTE :Files Tell2.4.SINO*, Tell2.5.SINO* and Tell2.5Geo.SINO* at : ~/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1196' + RESET)

#-- determine if step Pass/Fail
time.sleep(1)
Step_Result("Acq4D.1196")


os.system("chmod +x /usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1197/Acq4D_1197.py")
os.system("/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729/TC_2_5/Acq4D.1197/Acq4D_1197.py")
