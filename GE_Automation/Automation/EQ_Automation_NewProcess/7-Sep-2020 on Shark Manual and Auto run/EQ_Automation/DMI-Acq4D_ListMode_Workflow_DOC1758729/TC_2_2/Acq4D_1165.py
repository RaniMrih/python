from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True

    if run_mode == "auto":
      #popup to store user input
      User_Input_popup(tc, G.TC_WD , step , "both")

    #take user input, send TC and PWD
    User_Input(tc , G.TC_WD)
    #------------------------------------- step 1 -----------------------------------------
    G.Sinos_path = read_file(G.Output_Directory,"/SINOSPath"+tc+".txt")
    G.LISTS_Path = read_file(G.Output_Directory,"/LISTSPath"+tc+".txt")
    print_result("Creating S2.2Sino.txt file ...")
    os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+G.Sinos_path[0]+"/SINO* > "+G.Output_Directory+"/S2.2Sino.txt")
    #----------- question ---------
    print_fact_prefix("Is the S2.2Sino.txt file produced ?")
    if os.path.exists(G.Output_Directory+'/S2.2Sino.txt'):
      YesNo(True)
    else:
      YesNo(False)
      step_pass = False

    return step_pass
