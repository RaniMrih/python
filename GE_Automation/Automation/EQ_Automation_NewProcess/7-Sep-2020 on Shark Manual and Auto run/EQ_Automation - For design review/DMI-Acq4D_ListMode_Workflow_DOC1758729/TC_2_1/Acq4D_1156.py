import os
from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True

    #----------- question ---------
    print_fact_prefix("Is the Patient and Exam/Scan Data reported in "+'\n'+"Sinogram RDF file matches with the patient and ")
    print_empty_question("Exam information entered in Section 2.1 "+'\n'+"(SSVP.PAC.Acq4D.1154) ? ")
    print_note ('NOTE: Check manually')

    #----------- question ---------
    print_fact_prefix ("The Patient and Exam Data in the Sinogram file is:")
    OperatorID_Sino = find_tag(G.Output_Directory , "/S2.1SinoHdrs.txt", 'Operator')
    PatientID_Sino = find_tag(G.Output_Directory , "/S2.1SinoHdrs.txt", 'patientID')
    print_result(PatientID_Sino)
    print_result(OperatorID_Sino)

    #----------- question ---------
    print_fact_prefix ("The Patient and Exam Data in the List file is:")
    OperatorID_List = find_tag(G.Output_Directory , "/S2.1ListHdrs.txt", 'Operator')
    PatientID_List = find_tag(G.Output_Directory , "/S2.1ListHdrs.txt", 'patientID')
    check_empty = split_string(OperatorID_List, ':')
    if check_empty[1]=="":
        print_result("NA"+'\n'+"NA")
    else:
        print_result(PatientID_List)
        print_result(OperatorID_List)

    #----------- question ---------
    print_fact_prefix("The List Files Exam Data matches the Sino Files"+'\n'+"Exam Data for all parameters other than")
    print_fact_prefix("a) Patient ID"+'\n'+"b) Operator"+'\n'+"c) Scan ID")
    ScanID_List= find_tag(G.Output_Directory , "/S2.1ListHdrs.txt", 'Scan ID')
    ScanID_Sino= find_tag(G.Output_Directory , "/S2.1SinoHdrs.txt", 'Scan ID')

    ExamData = True
    if PatientID_Sino == PatientID_List or OperatorID_Sino == OperatorID_List or ScanID_List==ScanID_Sino:
        ExamData = False
    else:
        ExamData = diff_files(G.Output_Directory + "/S2.1SinoHdrs.txt",G.Output_Directory + "/S2.1ListHdrs.txt", "examData")
    if ExamData:
        YesNo(True)
    else:
        YesNo(False)
        step_pass = False

    #----------- qustion ---------
    print_fact_prefix ("Is List files' Acquisition Parameters' matches with"+'\n'+"the Sinogram files 'Acquisition Parameters'? ")
    AcqParams= diff_files(G.Output_Directory + "/S2.1SinoHdrs.txt", G.Output_Directory + "/S2.1ListHdrs.txt", "acqParams")
    if (AcqParams):
        YesNo(True)
    else:
        YesNo(False)
        step_pass = False

    #----------- qustion ---------
    print_fact_prefix ("Is List files 'System Geometry' matches with"+'\n'+"the Sinogram files 'System Geometry Parameters'? ")
    SysGeo= diff_files(G.Output_Directory + "/S2.1SinoHdrs.txt", G.Output_Directory + "/S2.1ListHdrs.txt", "sysGeo")
    if (SysGeo):
        YesNo(True)
    else:
        YesNo(False)
        step_pass = False

    #----------- question ---------
    print_fact_prefix ("Is List files 'Detector Module Temperatures' matches with"+'\n'+"the Sinogram files 'Detector Module Temperatures'? ")
    os.system("grep 'Module\[' "+G.Output_Directory + "/S2.1SinoHdrs.txt > A.txt")
    os.system("grep 'Module\[' "+G.Output_Directory + "/S2.1ListHdrs.txt > B.txt")
    os.system("diff A.txt B.txt > C.txt")
    if os.stat("C.txt").st_size > 0:
        ModulesDiff = False
        step_pass = False
    else:
        ModulesDiff = True
    YesNo(ModulesDiff)
    os.system("rm -rf A.txt B.txt C.txt")
    #----------- qustion ---------
    print_fact_prefix ("Is List files 'Detector Module Serial Nos.' matches with"+'\n'+"the Sinogram files 'Detector Module Serial Nos.'? ")
    YesNo(ModulesDiff)

    #----------- qustion ---------
    print_fact_prefix ("Is List files 'Detector Block Valid Flags' matches with"+'\n'+"the Sinogram files 'Detector Block Valid Flag'? ")
    YesNo(ModulesDiff)

    return step_pass


