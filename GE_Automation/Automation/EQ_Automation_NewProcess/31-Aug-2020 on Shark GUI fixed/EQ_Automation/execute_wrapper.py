import os,time,traceback,sys
import xml.etree.ElementTree as ElementTree
from auto_lib.Init_test import Globals
from auto_lib.generic_funcs import *
xml_path="/usr/g/ctuser/EQ_Automation/GUI_Config/xml_files/"

#------------------------ if running manually without UI
if __name__ != "__main__":
  Manual_Automation_Run()

else:
  #-------------------------get the doc and TC name from Bash zenity UI
  Doc_Name = sys.argv[1]
  TC_Number = sys.argv[2]
  if Doc_Name.startswith("DMI"):
    Config=" DMI "
  else:
    Config=" XRBB "

  #-------------------------bring test scope and parse the xml config file
  steps_list=[]

  full_file = (xml_path + Doc_Name+'.xml')
  dom = ElementTree.parse(full_file)
  TCs = dom.findall(TC_Number+'/step')
  for c in TCs:
      steps_list.append(c.text)
  print steps_list

  #-------------------------Scope for Acq_4D_ListMode_Workflow_DOC1758729, onclude all TC's and steps.
  start_test = False

  # -------------------------running on steps inside the choosen TC list
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
          result = m.execute(TC_Number, STEP,G)
          step_result("Acq4D_"+STEP, result)
      except:
          print()
          traceback.print_exc()
          step_result("Acq4D_" + STEP, False)

