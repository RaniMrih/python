import os
from auto_lib.generic_funcs import *

def execute(tc, step, G, run_mode="auto"):
    step_pass = True

    # ------------------------------------ step 1 --------------------------------------------
    # append all first and last time marks from ListOut_f?.txt
    FirstTimeMarksList=[]
    LastTimeMarksList=[]
    for i in range(0,3):
       First = collect_values1(G.Output_Directory+ "/ListOut_f"+str(i)+".txt" , 'First Time Mark')
       First=First[0].split(':')
       First=First[1].split()
       FirstTimeMarksList.append(First[0])

       Last = collect_values1(G.Output_Directory+ "/ListOut_f"+str(i)+".txt" , 'First Time Mark')
       Last=Last[0].split(':')
       Last=Last[2].split()
       LastTimeMarksList.append(Last[0])

    #----------- question ---------
    print_fact_prefix ("1) Frame 0 Last Time Mark :")
    print str(LastTimeMarksList[0]) + " ms"

    #----------- question ---------
    print_fact_prefix ("Frame 1 First Time Mark :")
    print str(FirstTimeMarksList[1]) + " ms"

    #----------- question ---------
    print_fact_prefix ("Frame 1 Last Time Mark:")
    print str(LastTimeMarksList[1]) + " ms"

    #----------- question ---------
    print_fact_prefix ("Frame 2 First Time Mark:")
    print str(FirstTimeMarksList[2]) + " ms"

    # ------------------------------------ step 2 --------------------------------------------
    #----------- question ---------
    print_fact_prefix ("2) f0_f1_gap is :")
    result = int(FirstTimeMarksList[1]) - int(LastTimeMarksList[0])
    if result < 0 :
      result*=-1
    print str(result) + " ms"

    #----------- question ---------
    print_fact_prefix ("f1_f2_gap is :")
    result1 = int(FirstTimeMarksList[2]) - int(LastTimeMarksList[1])
    if result1 < 0 :
      result1*=-1
    print str(result1) + " ms"

    #----------- question ---------
    print_fact_prefix ("Is the f0_f1_gap greater than 1 second but less than"+'\n'+"five seconds ?")
    if result > 5000 or result < 1000 :
      YesNo(False)
      step_pass = False
    else:
      YesNo(True)

    #----------- question ---------
    print_fact_prefix ("Is the f2_f1_gap greater than 1 second but less than"+'\n'+"five seconds ?")
    if result1 > 5000 or result1 < 1000 :
      YesNo(False)
      step_pass = False
    else:
      YesNo(True)

    return step_pass





