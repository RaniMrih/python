from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True

    SinosDirectory2_1= read_file(G.EQ_Path+"/"+G.Doc_Name+"/TC_2_1/Outputfiles","/SINOSPathTC_2_1.txt")
    SinosDirectory2_2= read_file(G.Output_Directory ,"/SINOSPathTC_2_2.txt")
    print_result("Creating LiveHdrs_2.1.tell file, please wait...")
    os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SinosDirectory2_1[0]+"/SINO* > "+G.Output_Directory+"/LiveHdrs_2.1.tell")
    print_result("Creating ReplayHdrs_2.2.tell file, please wait...")
    os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SinosDirectory2_2[0]+"/SINO* > "+G.Output_Directory+"/ReplayHdrs_2.2.tell")

    return step_pass
