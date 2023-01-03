#!/usr/bin/env python
import os
from auto_lib.generic_funcs import *

def execute(tc, step, G, run_mode="auto"):
    step_pass = True

    #read the created txt pathes in Output directory for TC
    SINOS_Path = read_file(G.Output_Directory,"/SINOSPath"+tc+".txt")
    LISTS_Path = read_file(G.Output_Directory,"/LISTSPath"+tc+".txt")

    #create rdfTeller files for sino and list
    print_result("Creating S2.1Sino.txt file ...")
    os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SINOS_Path[0]+"/SINO* > "+G.Output_Directory+"/S2.1Sino.txt")
    print_result("Creating S2.1SinoHdrs.txt file ...")
    os.system("rdfTeller -r '-h eag -Ha -v' "+SINOS_Path[0]+"/SINO* > "+G.Output_Directory+"/S2.1SinoHdrs.txt")
    print_result("Creating S2.1ListHdrs.txt file ...")
    os.system("rdfTeller -r '-h eag -Ha -v' "+LISTS_Path[0]+"/LIST* >  "+G.Output_Directory+"/S2.1ListHdrs.txt")

    #check that files created successfully in TC Output directory
    print_fact_prefix ("Is the S2.1Sino.txt, S2.1SinoHdrs.txt &"+'\n'+"S2.1ListHdrs.txt files were produced ?")
    if os.path.exists(G.Output_Directory+'/S2.1Sino.txt') and os.path.exists(G.Output_Directory+'/S2.1ListHdrs.txt'):
        YesNo(True)
    else:
        YesNo(False)
        step_pass = False

    return step_pass
