import os
from auto_lib.generic_funcs import *

def execute(tc, step, G , run_mode="auto"):
    step_pass = True
 #   if run_mode == "manually":
 #     #read the created txt pathes in Output directory for TC
 #     SINOS_Path = read_file(G.Output_Directory,"/SINOSPath"+tc+".txt")
 #     LISTS_Path = read_file(G.Output_Directory,"/LISTSPath"+tc+".txt")

    # ------------------------------------ step 1 --------------------------------------------
    #----------- question ---------
    print_fact_prefix ("1a) The list file 'Time Markers' per list is:")
    TimeMarkersList=[]
    for i in range(0,3):
       vals = collect_values1(G.Output_Directory+ "/ListOut_f"+str(i)+".txt" , 'Time Markers:')
       vals=vals[0].split()
       TimeMarkersList.append(vals[2])
       print "Time Markers LIST000"+str(i+1)+" = "+ str(TimeMarkersList[i])

    #----------- question ---------
    print_fact_prefix ("'Time Markers' for the first (bed loc) list file is at"+'\n'+"least 129000 but less than 131000 ?")
    if int(TimeMarkersList[0]) > 131000 or int(TimeMarkersList[0]) < 129000:
      YesNo(False)
      step_pass = False
    else:
      YesNo(True)

    #----------- question ---------
    print_fact_prefix ("'Time Markers' for the 2nd & 3rd (bed loc) list"+'\n'+"files is at least 99000 but less than 101000 ?")
    if int(TimeMarkersList[1]) > 101000 or int(TimeMarkersList[1]) < 99000 or int(TimeMarkersList[2]) > 101000 or int(TimeMarkersList[2]) < 99000:
      YesNo(False)
      step_pass = False
    else:
      YesNo(True)

    #----------- question ---------
    print_fact_prefix ("1b) The list file 'Phys2' per list is:")
    Phys2List=[]
    for i in range(0,3):
       vals = collect_values1(G.Output_Directory+ "/ListOut_f"+str(i)+".txt" , 'Phys2')
       vals=vals[0].split(':')
       Phys2List.append(vals[4])
       print "Phys2 LIST000"+str(i+1)+" = "+ str(Phys2List[i])

    #----------- question ---------
    print_fact_prefix ("Total 'Phys2 (Respiratory) Triggers' for the first "+'\n'+"(bed loc) list file are > 120 but less than 135 ?")
    if int(Phys2List[0]) > 135 or int(Phys2List[0]) < 120:
      YesNo(False)
      step_pass = False
    else:
      YesNo(True)

    #----------- question ---------
    print_fact_prefix ("Total 'Phys2 (Respiratory) Triggers' for the 2nd & "+'\n'+"3rd (bed loc) list file are > 90 but less than 105 ?")
    if int(Phys2List[1]) > 105 or int(Phys2List[1]) < 90 or int(Phys2List[2]) > 105 or int(Phys2List[2]) < 90:
      YesNo(False)
      step_pass = False
    else:
      YesNo(True)
    # ------------------------------------ step 2 --------------------------------------------
    #----------- question ---------
    print_fact_prefix ("2) Is the evidence of TOF info per Prompt"+'\n'+"inspected, including TOF values that are changing ?")
    os.system("ssh ctuser@par ListDecode "+G.Lists_path[0]+"/LIST0000.BLF | head -40 > "+G.Output_Directory+"/TOF.txt")
    os.system("ssh ctuser@par ListDecode "+G.Lists_path[0]+"/LIST0001.BLF | head -40 >> "+G.Output_Directory+"/TOF.txt")
    os.system("ssh ctuser@par ListDecode "+G.Lists_path[0]+"/LIST0002.BLF | head -40 >> "+G.Output_Directory+"/TOF.txt")

    TOFList=[]
    for line in open(G.Output_Directory + "/TOF.txt" , "r"):
      line = line.rstrip()
      if re.search('TOF', line):
        TOFList.append(line)

    if len(TOFList)==117:
      YesNo(True)
    else:
      YesNo(False)
      step_pass = False

    return step_pass
