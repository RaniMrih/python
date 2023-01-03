#!/usr/bin/env python
import os ,re ,sys,traceback
import time
import xml.etree.ElementTree as ElementTree
from auto_lib.Init_test import Globals

#Colors :
RESET = '\33[0m'
GREEN = '\33[92m'
BLUE = '\33[34m'
RED = '\33[31m'
YELLOW = '\33[33m'
EQ_Path='/usr/g/ctuser/EQ_Automation'
xml_path="/usr/g/ctuser/EQ_Automation/GUI_Config/xml_files/"
Docs_Dictionary= {"1": "DMI-Acq4D_ListMode_Workflow_DOC1758729", "2": "XRBB-Acq4D_ListMode_Workflow_DOC1758729", "3": "Empty","4":"Empty"}

#------------------------------------- if need to run automation without GUI for debugging
def Manual_Automation_Run():
  steps_list=[]
  TCs_list=[]
  TC_Number=""
  Doc_Name=""
  choose_doc=""
  choose_TC=""
  choose_step=""

  #start manuall Automation run and choose document
  print '\n'+RED+"Manual Automation run : "+RESET+'\n'
  for key in sorted(Docs_Dictionary.keys()) :
    print key ," - ", Docs_Dictionary[key]
  print
  while choose_doc == "" :
    choose_doc = raw_input(BLUE + "Enter Doc number from the list to run : "+ RESET)

  #bring TCs of the doc from xml and display TCs to choose
  for key in sorted(Docs_Dictionary.keys()) :
    if choose_doc == key:
      Doc_Name = Docs_Dictionary[key]
      full_file = (xml_path + Doc_Name+'.xml')
      dom = ElementTree.parse(full_file)
      root=dom.getroot()
      for child in root:
        TCs_list.append(child.tag)
  print
  for item in TCs_list:
    print item
  print
  while choose_TC == "" :
    choose_TC = raw_input(BLUE + "Enter TC from the list to run : "+RESET+"TC_")

  #bring all TC steps from xml and display eo choose
  print
  TC_Number= "TC_" + choose_TC
  TCs = dom.findall(TC_Number+'/step')
  for c in TCs:
    steps_list.append(c.text)
    print c.text
  print
  while choose_step == "" :
    choose_step = raw_input(BLUE + "Enter step from the list to run : "+RESET)
  print

  #check if config DMI / DMI-DR
  start_test = False
  if Doc_Name.startswith("DMI"):
    Config=" DMI "
  else:
    Config=" XRBB "

  if choose_step == steps_list[0]:
    # running on steps inside the choosen TC list
    for STEP in steps_list:
      try:
          time.sleep(1)
          if not start_test:
            start_test = True
            # send to Globals class in init_test the TC and the step number
            G = Globals(TC_Number, STEP, Config ,Doc_Name)
            # use function print_headers in generic_func, determine if step is leading
            print_headers(TC_Number, STEP, True , Config)
          else:
            print_headers(TC_Number, STEP, False ,Config)
          print
          # this moduLe connect the doc+TC+step number to execute function
          moduLe = Doc_Name+"." + TC_Number+ ".Acq4D_" + STEP
          # this load_module is built in function in python(learn)
          m = load_module(moduLe)
          #the result will be returned with True/False
          result = m.execute(TC_Number, STEP, G ,run_mode="manually")
          step_result("Acq4D_"+STEP, result)
      except:
          print()
          traceback.print_exc()
          step_result("Acq4D_" + STEP, False)
  else:
    STEP=choose_step
    index = steps_list.index(STEP)
    for STEP in steps_list[index:]:
      try:
         time.sleep(1)
         # send to Globals class in init_test the TC,step number,Sinos and list pathes
         G = Globals(TC_Number, STEP, Config ,Doc_Name)
         G.Sinos_path = read_file(G.Output_Directory,"/SINOSPath"+TC_Number+".txt")
         G.sinos_files = count_files("SINO0", G.Sinos_path)
         G.Lists_path = read_file(G.Output_Directory,"/LISTSPath"+TC_Number+".txt")
         G.lists_files = count_files("LIST0", G.Lists_path)
         
         print_headers(TC_Number, STEP, False ,Config)
         print
         # this moduLe connect the doc+TC+step number to execute function
         moduLe = Doc_Name+"." + TC_Number+ ".Acq4D_" + STEP
         # this load_module is built in function in python(learn)
         m = load_module(moduLe)
         #the result will be returned with True/False
         result = m.execute(TC_Number, STEP, G ,run_mode="manually")
         step_result("Acq4D_"+STEP, result)
      except:
         print()
         traceback.print_exc()
         step_result("Acq4D_" + STEP, False)

#------------------------------------- YesNo function
def YesNo(YN):
    time.sleep(0.1)
    if YN == True:
        print (GREEN + "[X] Yes" + RESET)
        print ("[ ] No")
    else:
        print ("[ ] Yes")
        print (RED +"[X] No" + RESET)
    print

#------------------------------------- print empty qustion
def print_question(a_q):
    time.sleep(0.1)
    print
    print (BLUE + a_q + RESET)
    print "[ ] Yes"
    print "[ ] No"

#------------------------------------- print note in yellow
def print_note(message):
    print YELLOW + message + RESET
    print

#------------------------------------- print real qustion
def print_fact_prefix(header):
    time.sleep(0.1)
    print
    print (BLUE + header + RESET)


def print_result(value):
    print(value)

def print_error(err_msg):
    print (RED + err_msg + RESET)


#----------------------------------- check if step pass or fail according to yes/no
def Step_Result(StepNum,Step_Pass):
   if Step_Pass == False:
     print (RED + "                                                       ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                       ---- Step "+StepNum+" Passed ----" + RESET)


#-----------------------------------------popup to store user input in txt files, if received:
# both - user need to insert Sinos and Lists files pathes 
def User_Input_popup(TC, TC_WD , step , popup_type):
   TC=TC.replace("_",'.')
   if popup_type == "both":
     SINOS_Path=os.popen('zenity --entry --title="Insert SINO path" --width="500" --height="300" --text "\n\n\nEnter Sinograms path directory from "'+TC+'" Scan from step "'+step+'" : \n\n\n"')
     SINOS_Path=SINOS_Path.read()
     LISTS_Path=os.popen('zenity --entry --title="Insert SINO path" --width="500" --height="300" --text "\n\n\nEnter Lists path directory from "'+TC+'" Scan from step "'+step+'" : \n\n\n"')
     LISTS_Path=LISTS_Path.read()
     #write the input data to files to read
     write_file(EQ_Path+'/User_Input_SINO.txt',SINOS_Path)
     write_file(EQ_Path+'/User_Input_LIST.txt',LISTS_Path)

   if popup_type == "only_sino":
     SINOS_Path=os.popen('zenity --entry --title="Insert SINO path" --width="500" --height="300" --text "\n\n\nEnter Sinograms path directory from "'+TC+'" Scan from step "'+step+'" : \n\n\n"')
     SINOS_Path=SINOS_Path.read()
     #write the input data to files to read
     write_file(EQ_Path+'/User_Input_SINO.txt',SINOS_Path)

   if popup_type == "only_list":
     LISTS_Path=os.popen('zenity --entry --title="Insert SINO path" --width="500" --height="300" --text "\n\n\nEnter Lists path directory from "'+TC+'" Scan from step "'+step+'" : \n\n\n"')
     LISTS_Path=LISTS_Path.read()
     #write the input data to files to read
     write_file(EQ_Path+'/User_Input_LIST.txt',LISTS_Path)
          

#------------------------------------ function to take user input from zenity GUI or manually for debugging.
def User_Input(TC,PWD):
   # if user entered path in zenity popup
   if os.path.exists(EQ_Path+'/User_Input_SINO.txt'):
     # grep sinos  path
     f = open( EQ_Path+'/User_Input_SINO.txt' , 'r')
     for line in f:
       SinosDirectory = line.strip('\n')
     f = open( EQ_Path+'/User_Input_LIST.txt' , "r")
     for line in f:
       ListsDirectory = line.strip('\n')
     print "Enter Sinograms path directory from" + BLUE + " section "+TC+" : " +RESET + SinosDirectory
     print "Enter LIST path directory from" + BLUE + " section "+TC+" : " +RESET + ListsDirectory
   else:
     #use of raw_input()
     SinosDirectory = raw_input("Enter Sinograms path directory from" + BLUE + " section "+ TC +" : "+ RESET)

     # while SinosDirectory is empty
     while SinosDirectory == "":
       SinosDirectory = raw_input("Enter Sinograms path directory from" + BLUE + " section "+ TC + " again :" + RESET)
     ListsDirectory = raw_input("Enter Lists path directory from" + BLUE + " section "+ TC +" : " + RESET)

     # while ListsDirectory is empty
     while ListsDirectory == "":
       ListsDirectory = raw_input("Enter Lists path directory from" + BLUE + " section "+TC+"again :" + RESET)

     # if /Outputfiles/ not exist mkdir
     write_file("SINOSPath" + TC + ".txt", SinosDirectory)
     write_file("LISTSPath" + TC + ".txt", ListsDirectory)
     if os.path.exists(PWD + '/Outputfiles/'):
       os.system("mv LISTSPath"+TC+".txt SINOSPath"+TC+".txt "+PWD+"/Outputfiles/")
     else:
       os.system("mkdir "+PWD+"/Outputfiles/")
       os.system("mv LISTSPath"+TC+".txt SINOSPath"+TC+".txt "+PWD+"/Outputfiles/")

     #Remove the input files from zenity user input
     os.system("rm -rf "+EQ_Path+"/User_Input_SINO.txt")
     os.system("rm -rf "+EQ_Path+"/User_Input_LIST.txt")

#------------------------------------- print empty qustion
def print_empty_question(a_q):
    time.sleep(0.1)
    print
    print (BLUE + a_q + RESET)
    print "[ ] Yes"
    print "[ ] No"

#------------------------------------- read files
def read_file(path,file_name):
   vals = []
   for line in open(path+file_name, "r"):
      line = line.rstrip()
      vals.append(line)
   return vals

#------------------------------------ function to print the start header of each step and TC start.
def print_headers(TC, step_id, is_leading, Config):
    print
    print (
            GREEN + "::::::::::::::::::::::::::::::::::::::::::::::: Running" +Config + TC +
            " Step " + step_id + " , Please wait... ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
            + RESET)
    if is_leading:
        print (
            GREEN + "::::::::::::::::::::::::::::::::::::::::::: This Script will run all " +
            TC + " press ctrl+c to stop :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" +
            RESET)
    print


#------------------------------------- count files in directory
def count_files(File , Path):
   SinosNum = []
   ListsNum = []

   if File == "SINO0":
     for item in os.listdir(Path):
        if item.startswith(File):
          SinosNum.append(item)
     return SinosNum
   elif File == "LIST0":
     for item in os.listdir(Path):
        if item.startswith(File):
          ListsNum.append(item)
     return ListsNum

def list_files(File , Path):
    # ---- count files in directory
   SinosNum = []
   ListsNum = []

   if File == "SINO00":
     for item in os.listdir(Path):
        if item.startswith(File):
          SinosNum.append(item)
     return SinosNum
   elif File == "LIST00":
     for item in os.listdir(Path):
        if item.startswith(File):
          ListsNum.append(item)
     return ListsNum

def set_directories_paths(TC, TC_start=''):
# deleted zenity part - refer to Gali code
    #use of raw_input()
    SinosDirectory = raw_input("Enter Sinograms path directory from" + BLUE + " section " + TC + " :" +RESET)
    ListsDirectory = raw_input("Enter Lists path directory from" + BLUE + " section " + TC + " :" + RESET)
    print

    # like : echo $SinosDirectory2_4 > SINOSPath2_4.txt
    write_file("SINOSPath" + TC + ".txt", SinosDirectory)
    write_file("LISTSPath" + TC + ".txt", ListsDirectory)

    return SinosDirectory, ListsDirectory

#------------------------------------- function to write files
def write_file(file_name, text):
    f = open(file_name, "w+")
    f.write(text)
    f.close()


def execute_step(TC, step_id):
    mod = __import__("Acq_4D_ListMode_Workflow_DOC1758729.TC_"+ TC+ ".Acq4D." + step_id)
    func = getattr(mod, "execute")
    func(TC, step_id)


def load_module(module):

    # module_path = "mypackage.%s" % module
    module_path = module

    if module_path in sys.modules:
        return sys.modules[module_path]

    return __import__(module_path, fromlist=[module])


#------------------------------------- function to find tags in txt
def find_tag(file_path , file_name , tag_name):
   for line in open(file_path+file_name, "r"):
     line = line.rstrip()
     if re.search(tag_name, line):
       name=line.replace(line[:9],'')
   return name


def diff_files(f1_name, f2_name, prefix, black_list=[]):
    from difflib import ndiff

    wrong_lines = []
    verified_ok = True
    f1 = open(f1_name).readlines()
    f2 = open(f2_name).readlines()

    for a_diff in ndiff(f1, f2):
        if a_diff.startswith('-'):
            if prefix in a_diff:
                if not any(s in a_diff for s in black_list):
                    verified_ok = False
                    wrong_lines.append(a_diff)
    if not verified_ok:
        print
        print_error("ERROR - Following lines differ unexpectedly: ")
        for l in wrong_lines:
            print_error(l)
    return verified_ok


#def split_string(line, seperate):
#   return line.split(seperate)

#---- split line to array according to  ' '
def split_string(line , operator):
   list_string=line.split(operator)
   return list_string

#-------------------- if step pass or fail according to returned value from script
def step_result(StepNum, Step_Pass):
   if Step_Pass == False:
     print (RED + "                                                        ---- Step "+StepNum+" Failed ----" + RESET)
     print
   else:
     print (GREEN + "                                                        ---- Step "+StepNum+" Passed ----" + RESET)
     print

#------------------ collect values from file with operator '=' to split
def collect_values(file_name, param, field_sep="="):
    vals = []
    for line in open(file_name, "r"):
        line = line.rstrip()
        if re.search(param, line):
            vals.append(split_string(line, field_sep)[1])
    return vals

#------------------ collect values from file without operator
def collect_values1(file_name, param):
    vals = []
    for line in open(file_name, "r"):
        line = line.rstrip()
        if re.search(param, line):
            vals.append(line)
    return vals

#------------------- calculate diff time function 
def caculate_time_delta(start, end, format='%a %b %d %H:%M:%S %Y'):
    from datetime import datetime

    tdelta1 = datetime.strptime(start, format) 
    tdelta2 = datetime.strptime(end, format)
    #tdelta in format 'D day, HH:SS:MM'
    # you may convert tdelta to seconds. e.g. tdelta.seconds
    tdelta = tdelta2 - tdelta1
    return tdelta.seconds

#------------------- Take Only float number 
def Take_Only_number(string):
   result=re.findall("\d+\.\d+", string)
   return result[0]

