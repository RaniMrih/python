from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True

    #copy TC_2_1 sinos path to TC_2_2
    os.system("cp "+G.EQ_Path+"/"+G.Doc_Name+"/TC_2_1/Outputfiles/SINOSPathTC_2_1.txt "+G.Output_Directory)

    #Read sinos path
    SinosDirectory2_1= read_file(G.Output_Directory ,"/SINOSPathTC_2_1.txt")
    SinosDirectory2_2= read_file(G.Output_Directory ,"/SINOSPath"+tc+".txt")

    #create files to compare
    print_result("Creating LiveHdrs_2.1.tell file, please wait...")
    os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SinosDirectory2_1[0]+"/SINO* > "+G.Output_Directory+"/LiveHdrs_2.1.tell")
    print_result("Creating ReplayHdrs_2.2.tell file, please wait...")
    os.system("rdfTeller -r '-h efadgS -Ha -v -S' "+SinosDirectory2_2[0]+"/SINO* > "+G.Output_Directory+"/ReplayHdrs_2.2.tell")
    
    #----------- question ---------
    print_fact_prefix("5. a) The RDF Exam/Scan Data should match for all"+'\n'+"the parameters other than following parameters ?")
    print_fact_prefix("i) Scan Description"+'\n'+"ii) Database Scan ID and alias examData.scanIdDicom"+'\n'+"iii) Scan ID (RDF pathname seed in hex) and alias examData.scanID")
    
    os.system("grep 'Scan Description =\|Database Scan ID\|examData.scanIdDicom\|Scan ID\|examData.scanID|examData.scanDescription:' "+G.Output_Directory+"/LiveHdrs_2.1.tell > "+G.Output_Directory+"/A.txt")
    os.system("grep 'Scan Description =\|Database Scan ID\|examData.scanIdDicom\|Scan ID\|examData.scanID|examData.scanDescription:' "+G.Output_Directory+"/ReplayHdrs_2.2.tell > "+G.Output_Directory+"/B.txt")
    #----------------------------
    os.system("grep -v 'Scan Description =\|Database Scan ID\|examData.scanIdDicom\|Scan ID\|examData.scanID\|examData.scanDescription:' "+G.Output_Directory+"/LiveHdrs_2.1.tell | grep 'examData'> "+G.Output_Directory+"/C.txt")
    os.system("grep -v 'Scan Description =\|Database Scan ID\|examData.scanIdDicom\|Scan ID\|examData.scanID\|examData.scanDescription:' "+G.Output_Directory+"/ReplayHdrs_2.2.tell | grep 'examData'> "+G.Output_Directory+"/D.txt")
    
    #diff files 
    os.system("diff "+G.Output_Directory+"/A.txt "+G.Output_Directory+"/B.txt > "+G.Output_Directory+"/diff.txt")
    os.system("diff "+G.Output_Directory+"/C.txt "+G.Output_Directory+"/D.txt > "+G.Output_Directory+"/diff1.txt")

    Diff=True
    if os.stat(G.Output_Directory + "/diff.txt").st_size == 0 or os.stat(G.Output_Directory + "/diff1.txt").st_size > 0:
      Diff = False
      step_pass=False
    
    YesNo(Diff)

    #----------- qustion ---------
    print_fact_prefix ("All other not identified RDF Exam Information matchs ?")
    if os.stat(TC_start + "/diff1.txt").st_size == 0:
      YesNo(True)
    else:
      YesNo(False)
      step_pass=False

    #----------- qustion ---------
    print_fact_prefix ("5. b) Acq Parameters Header Matchs for all "+'\n'+"parameters except :"+'\n'+"i) Event Source"+'\n'+"ii) Event Simulation Data"+'\n'+"iii) Start Condition"+'\n'+"iv) Retro Scan flag")
    print_fact_prefix("and possibly the 'Table Location' ")
    # check table location
    TableLocation=False
    ScanID_List= find_tag(G.Output_Directory , "/S2.1ListHdrs.txt", 'Scan ID')




  #Not finished









    return step_pass
