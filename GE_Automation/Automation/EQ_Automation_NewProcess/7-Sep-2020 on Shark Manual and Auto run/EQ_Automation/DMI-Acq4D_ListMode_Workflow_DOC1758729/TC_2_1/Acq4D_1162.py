import os
from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True
 #   if run_mode == "manually":
 #     #read the created txt pathes in Output directory for TC
 #     SINOS_Path = read_file(G.Output_Directory,"/SINOSPath"+tc+".txt")
 #     LISTS_Path = read_file(G.Output_Directory,"/LISTSPath"+tc+".txt")

    # ------------------------------------ step 1 --------------------------------------------
    print_result("Creating coinLossCK.csv, please wait..")
    os.system("coinLossCk -v -c " + G.Sinos_path[0] + "/SINO*")
    os.system("mv coinLoss.csv " +G.Output_Directory)

    #----------- question ---------
    print_fact_prefix ("1) Sinogram Sorter"+'\n'+"Coinc Loss (%)")
    SorterLossList=[]
    Within_1 =True
    i=0
    for line in open( G.Output_Directory + "/coinLoss.csv", "r"):
    # this to avoid hader
       if i == 0:
         i+=1
         continue
       else:
         line1=line.split(',')
         i+=1
         SorterLossList.append(line1[3])
    for i in range (0,3):
      print "Frame "+str(i+1)+" = "+ str(SorterLossList[i]) + " %"
      if float(SorterLossList[i]) > 1.0:
        Within_1=False
        step_pass = False


    #----------- question ---------
    print_fact_prefix ("For all bed location Sinogram  Files (SINO0000, "+'\n'+"SINO0001 & SINO0002),  the Sorter Coinc Loss % is  < 1.0 %?")
    YesNo(Within_1)

    # ------------------------------------ step 2 --------------------------------------------
    print_result("Creating ListLoss0-2.txt, please wait...")
    for i in range (0,3):
      os.system("ListTool -Ml -Sl  -f ListLoss"+str(i)+".csv " + G.Lists_path[0] + "/LIST000"+str(i)+".BLF > "+G.Output_Directory+"/ListLoss"+str(i)+".txt")
      os.system("mv ListLoss"+str(i)+".csv "+G.Output_Directory)

    #----------- qustion ---------
    LisTLossInAligned=[]
    Within_1 =True
    print_fact_prefix ("2) List File overall aligned "+'\n'+"Coinc Loss (%)")
    for i in range (0,3):
      result = collect_values1(G.Output_Directory+ "/ListLoss"+str(i)+".txt" , 'list loss in aligned')
      result=Take_Only_number(result[0])
      LisTLossInAligned.append(result)
      print "LIST000"+str(i)+".BLF = "+ str(LisTLossInAligned[i])+ " %"
      if float(LisTLossInAligned[i]) > 1.0:
        Within_1=False
        step_pass = False

    #----------- qustion ---------
    print_fact_prefix ("For all bed location List Files (LIST0000, LIST0001 "+'\n'+"& LIST0002), the overall frame Coinc loss is < 1.0 %")
    YesNo(Within_1)

   # ------------------------------------ step 3 --------------------------------------------
   #----------- qustion ---------
    MaxListLoss=[]
    Within_1 =True
    print_fact_prefix ("3) List File Max 1 sec Coinc Loss")
    for i in range (0,3):
      result = collect_values1(G.Output_Directory+ "/ListLoss"+str(i)+".txt" , 'Maximum list loss')
      result=result[0].split(':')
      MaxListLoss.append(result[1].strip('\n'))
      print "LIST000"+str(i)+".BLF = "+ str(MaxListLoss[i])+ " %"
      if float(MaxListLoss[i]) > 1.0:
        Within_1=False

    #----------- qustion ---------
    Sorter_Loss_csv=[]
    Within_50=True
    print_fact_prefix ("List File Max 1 sec Coinc Loss expressed as a "+'\n'+"percentage of the Prompt rate for same interval :")

    for i in range (0,3):
      param = ","+str(MaxListLoss[i]).lstrip()
      result = collect_values1(G.Output_Directory+ "/ListLoss"+str(i)+".csv" , param)
      result = result[0].split(',')
      Sorter_Loss_csv.append(result[5])
      print "LIST000"+str(i)+".BLF = "+str(Sorter_Loss_csv[i])
      if float(Sorter_Loss_csv[i]) > 50.0:
        Within_50=False
        step_pass = False
  # ------------------------------------ step 4 --------------------------------------------
    #----------- qustion ---------
    print_fact_prefix ("4) For all bed location List Files (LIST0000, "+'\n'+"LIST0001 & LIST0002), the Max List Coinc Loss at"+'\n'+"any one sec interval is < 50.0 % ?")
    YesNo(Within_50)

    #----------- qustion ---------
    print_empty_question("List File Max 1 sec Coinc Loss expressed as a "+'\n'+"percentage of the Prompt rate for same interval :")
    print_note("NOTE: ListToolPlot.py Not found, perform manually.")

    return step_pass
