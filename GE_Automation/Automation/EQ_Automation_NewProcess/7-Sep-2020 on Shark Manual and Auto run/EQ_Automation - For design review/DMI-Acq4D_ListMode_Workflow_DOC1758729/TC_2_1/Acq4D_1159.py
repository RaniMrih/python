import os
from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True
 
    # ------------------------------------ step 1 --------------------------------------------
    #----------- question ---------
    print_fact_prefix ("'Frame Duration' of each sinogram file is :")
    SinoDurationList=[]
    SinoDuration = collect_values(G.Output_Directory + "/S2.1Sino.txt", "Frame Duration")
    for i in range (0,3):
      only_val=SinoDuration[i].split()
      SinoDurationList.append(only_val[0])
      print "Frame Duration "+str(i+1)+" = "+ str(SinoDurationList[i]) + " msec"

    #----------- question ---------
    print_fact_prefix ("Delta Time of each list file is :")
    DeltaTimeList=[]
    for i in range(0,3):
      delta_time = collect_values1(G.Output_Directory + "/ListOut_f"+str(i)+".txt", "Delta Time")
      delta_time=delta_time[0].split(':')
      DeltaTimeList.append(delta_time[3])
      print "Delta Time LIST000"+str(i+1)+" = "+ str(DeltaTimeList[i]) + " msec"

    #----------- question ---------
    print_fact_prefix ("Difference of 'Delta Time' in list file and 'Frame "+'\n'+"Duration in sinogram file is :")
    diff=[]
    for i in range (0,3):
      result= int(DeltaTimeList[i]) - int(SinoDurationList[i])
      diff.append(result)
      print "Frame "+str(i+1)+" = "+ str(result) + " msec"

    #----------- question ---------
    print_fact_prefix ("Is the difference of 'Delta Time' in list file and Frame "+'\n'+"Duration in sinogram file for frame 1 is 30 sceonds "+'\n'+"(+/- 5msec)?")
    if diff[0] > 30005 or diff[0] < 29995:
      YesNo(False)
      step_pass = False
    else:
      YesNo(True)

    #----------- question ---------
    print_fact_prefix ("Is the 'Delta Time' in list file and 'Frame Duration' in "+'\n'+"sinogram file for frame 2 and frame 3 are same  (+/- 5 msec) ?")
    if int(diff[1]) - int(diff[2]) > 5 or int(diff[1]) - int(diff[2]) < -5:
      YesNo(False)
      step_pass = False
    else:
      YesNo(True)

    return step_pass





