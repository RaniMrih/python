from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True
    
    
    if run_mode == "auto":
      #popup to store user input
      User_Input_popup(tc, G.TC_WD , step , "both")

    #take user input, send TC and PWD
    User_Input(tc , G.TC_WD)
    #------------------------------------- step 1 -----------------------------------------
    #----------- question ---------
    print_empty_question("1) Scan completed normally ?")

    #----------- question ---------
    print_fact_prefix("Number of Sinogram Files:")
    G.Sinos_path = read_file(G.Output_Directory,"/SINOSPath"+tc+".txt")
    G.sinos_files = count_files("SINO0", G.Sinos_path[0])
    print len(G.sinos_files)

    #----------- question ---------
    print_fact_prefix("The name of Sinogram Files present :")
    for item in G.sinos_files:
      print item
    #----------- question ---------
    print_fact_prefix("Is there a 3 Sinogram Files, with filenames"+'\n'+"(SINO0000, SINO0001, SINO0002) ?")
    if len(G.sinos_files) == 3 and str(G.sinos_files[0])== "SINO0000" and str(G.sinos_files[1])== "SINO0001" and str(G.sinos_files[2])== "SINO0002":
      YesNo(True)
    else:
      YesNo(False)
      step_pass = False

    #----------- question ---------
    print_fact_prefix("Number of List Files:")
    G.Lists_path = read_file(G.Output_Directory,"/LISTSPath"+tc+".txt")
    G.lists_files = count_files("LIST0", G.Lists_path[0])
    print len(G.lists_files)

    #----------- question ---------
    print_fact_prefix("The name of the List Files found is :")
    for item in G.lists_files:
      print item

    #----------- question ---------
    print_fact_prefix("Is there a 3 List Files, with filenames"+'\n'+"(LIST0000.BLF, LIST0001.BLF, LISTO0002.BLF) ?")
    if len(G.lists_files) == 3 and str(G.lists_files[0])== "LIST0000.BLF" and str(G.lists_files[1])== "LIST0001.BLF" and str(G.lists_files[2])== "LIST0002.BLF":
      YesNo(True)
    else:
      YesNo(False)
      step_pass = False

    return step_pass



