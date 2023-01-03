import os
from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True

    # ------------------------------------ step 1 --------------------------------------------
    print_fact_prefix ("1) Scan Start Time : ")
    ScanStartSINO = collect_values(G.Output_Directory + "/S2.1Sino.txt", "Scan Start Time =")
    # remove spaces from string beginning lstrip()
    ScanStartSINO[0] = ScanStartSINO[0].lstrip()
    print_result(ScanStartSINO[0])
    print_fact_prefix ("Frame Start Time : ")
    FrameStartSINO = collect_values(G.Output_Directory + "/S2.1Sino.txt", "Frame Start Time =")
    FrameStartSINO[0] = FrameStartSINO[0].lstrip()
    print FrameStartSINO[0]

    #----------- question ---------
    print_fact_prefix ("Scan Start Time - Frame Start Time = ")
    t_delta = caculate_time_delta(ScanStartSINO[0], FrameStartSINO[0])
    print_result(t_delta)
    #----------- question ---------
    print_fact_prefix ("The Acquisition Start Time of the first "+'\n'+"frame is 30 second after the scan start time?")
    if t_delta == 30:
        YesNo(True)
    else:
        YesNo(False)
        step_pass = False

    # ------------------------------------ step 2 --------------------------------------------
    #----------- question ---------
    print_fact_prefix ("2) Frame Start Time (Coinc msec) in msec"+'\n'+"for each frame:")
    CoincList = collect_values(G.Output_Directory + "/S2.1Sino.txt", '(Coinc msec)')
    for i in range (0,3):
        print_result("Frame "+str(i+1)+"= "+ str(CoincList[i]))

    # ------------------------------------ step 3 --------------------------------------------
    # grep sinos  path
    print_result("Creating ListOut_f0.txt, ListOut_f1.txt' ListOut_f2.txt, please wait ...")
    i=0
    for F in G.lists_files:
        os.system("ssh ctuser@par ListDecode -s "+str(G.Lists_path[0])+'/'+ str(F) + " > "+G.Output_Directory+"/ListOut_f" + str(i)+ ".txt")
        i+=1
    #----------- question ---------
    print_fact_prefix ("3) 'First Time Mark' im msec for each"+'\n'+"frame:")
    TimeMarkList=[]
    for i in range(0,3):
       vals = collect_values1(G.Output_Directory+ "/ListOut_f"+str(i)+".txt" , 'First Time Mark')
       vals=vals[0].split()
       TimeMarkList.append(vals[3])
       print "Frame "+str(i+1)+" = "+ str(TimeMarkList[i])

    # ------------------------------------ step 4 --------------------------------------------
    #----------- question ---------
    print_fact_prefix ("4) The absolute difference in between the 'First Time'"+'\n'+"Time Mark' in the List file and the the 'Frame Start"+'\n'+"Time (Coinc msec)' of the sinogram file, per Frame is:")
    results=[]
    for i in range (0,3):
        diff=int(CoincList[i])-int(TimeMarkList[i])
        if diff < 0:
          diff*= -1
        results.append(diff)
        print "Frame "+str(i+1)+" = "+ str(diff)

    #----------- question ---------
    print_fact_prefix ("For Frame 1:"+'\n'+"Is the difference between the 'First Time Mark' in"+'\n'+"List file and 'Frame Start Time (Coinc msec)' in"+'\n'+"sinogram file is 30,000 (+/- 5) msec?")
    if results[0] > 30005 or results[0]<29995:
        YesNo(False)
        step_pass = False
    else:
        YesNo(True)

    #----------- qustion ---------
    print_fact_prefix ("For Frame 2 and 3:"+'\n'+"Is the difference between the 'First Time Mark' in"+'\n'+"List file and 'Frame Start Time (Coinc msec)' in"+'\n'+"sinogram file is <= 5msec ?")
    if results[1] > 5 or results[1]<-5 or results[2] > 5 or results[2] < -5:
        YesNo(False)
        step_pass = False
    else:
        YesNo(True)

    return step_pass
