#!/bin/bash
#This GUI using linux Default zenity popups
#Developed for PET/CT Automation testing and operations Using Python and Bash
#Created at 10/5/2020
#Author: Rani Mrih 

#VARS
Doc_Path="/usr/g/ctuser/EQ_Automation/Acq_4D_ListMode_Workflow_DOC1758729"
XRBB_Acq4D_Path="/usr/g/ctuser/EQ_Automation/XRBB_Acq_4D_ListMode_Workflow_DOC1758729"
EQ_Path="/usr/g/ctuser/EQ_Automation"

#---------------------------------------- Go Back to beginning function ---------------------------------------------------------------------
Go_To_Beginning(){
$EQ_Path/Automation_GUI.sh
}

#-----------------------------clean logs after running from special chars (^M) and colors ---------------------------------------------------
Clean_Logs_function (){
Tmp="/usr/g/ctuser/EQ_Automation/Tmp_Log.log"
Tmp1="/usr/g/ctuser/EQ_Automation/NewFile.txt"
FinalLog="/usr/g/ctuser/EQ_Automation/Automation_Log.log"
# commands to clean
perl -pe 's/\x1b\[[0-9;]*[mG]//g' $Tmp > $Tmp1
col -bp < $Tmp1 >> $FinalLog
}

#---------------------------------------- Finish testing popup and Logs-----------------------------------------------------------------------
Finish_Function (){
zenity --question --text "\n\n\n\nDone Testing $1\nResults at: /usr/g/ctuser/EQ_Automation/Automation_Log.log\n\nView Logs ?" --width="500" --height="300" ;test=$? 
# zenity_info=$(zenity --info --text "\n\nDone Testing $1\n\nResults at: /usr/g/ctuser/EQ_Automation/Automation_Log.log" --width="400" --height="200")
 rm -rf $EQ_Path/User_Input_SINO.txt
 rm -rf $EQ_Path/User_Input_LIST.txt
 rm -rf $EQ_Path/NewFile.txt
 rm -rf $EQ_Path/Tmp_Log.log
if [[ $test == "0" ]]; then
  Zenity_Log=$(zenity --text-info --title="Automation log :" --width="850" --height="750" --filename=/usr/g/ctuser/EQ_Automation/Automation_Log.log )
  Go_To_Beginning
else
  Go_To_Beginning
fi
}

#---------------------------------------- Error Popup for empty TC -------------------------------------------------------------------

Error_Function (){
zenity_error=$( zenity --error --width="500" --height="300" --text "\n\n\n\nNo Automation process for this TC")
Go_To_Beginning
}

#---------------------------------------- Take sino and path from user ----------------------------------------------------------------

User_Input_SINO_Function(){
zenity_SINO_Input=$( zenity --entry --title="Insert SINO path" --width="500" --height="300" --text "\n\n\n\nEnter Sinogram path directory from $1  :\n\n")
echo $zenity_SINO_Input > /usr/g/ctuser/EQ_Automation/User_Input_SINO.txt
}
#---------------------------------------- Take second sino and path from user ----------------------------------------------------------------

User_Input_SINO_Function1(){
zenity_SINO_Input1=$( zenity --entry --title="Insert Second SINO path" --width="500" --height="300" --text "\n\n\n\nEnter Second Sinogram path directory from $1  :\n\n")
echo $zenity_SINO_Input1 > /usr/g/ctuser/EQ_Automation/User_Input_SINO1.txt
}

#---------------------------------------- Take list path from user -------------------------------------------------------------------

User_Input_LIST_Function(){
zenity_LIST_Input=$( zenity --entry --title="Insert LIST File path" --width="500" --height="300" --text "\n\n\n\nEnter LIST file path directory from $1 :\n\n")
echo $zenity_LIST_Input > /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt
}

#---------------------------------------- Take Second list path from user -------------------------------------------------------------------

User_Input_LIST_Function1(){
zenity_LIST_Input1=$( zenity --entry --title="Insert Second LIST File path" --width="500" --height="300" --text "\n\n\n\nEnter Second LIST file path directory from $1 :\n\n")
echo $zenity_LIST_Input1 > /usr/g/ctuser/EQ_Automation/User_Input_LIST1.txt
}

############################################# Main Screen Choose What Operation popup ######################################################################################
zenity_choose_Operation=$(
        zenity --radiolist --list --title="Choose Operation to perform " --width="800" --height="750" \
        --column="         Select         " --column="Choose your operation :          " --column="Status"\
        " " "V&V Automation Testing     " "OK"\
        " " "PAARTF Test     " "In Progress"\
        " " "Remove Files     " "In Progress"\
        " " "Copy Files" "Develop"\
        " " "diff Files" "Develop"\
        " " "diff Directories" "Develop"\
        " " "Change File Name   " "Develop"\
        " " "Manual Mount USB   " "Develop"\
        " " "ln -sf ListFile Link   " "Develop"\
        " " "rdfTell   " "Develop"\
        " " "rdfTeller   " "Develop"\
        " " "ListTool   " "Develop"\
        " " "ListDecode   " "Develop"\
        " " "coinLossCk   " "Develop"\
)
################################################### Screen to Choose file to remove  #######################################################################################

if [[ $zenity_choose_Operation == "Remove Files     " ]]; then
zenity_remove_file=$(
      zenity --file-selection --title="Select a File to remove !" --width="800" --height="800")

  if [[ $zenity_remove_file == "" ]]; then
   Go_To_Beginning
  fi 
fi

################################################### PAARTF test choose in a new Zenity screen  ###############################################################################

if [[ $zenity_choose_Operation == "PAARTF Test     " ]]; then
chmod +x $EQ_Path/GUI_Config/Choose_PAARTF_Test.sh
$EQ_Path/GUI_Config/Choose_PAARTF_Test.sh
fi

############################################# Screen includes Docs to run Auto Testing #######################################################################################
if [[ $zenity_choose_Operation == "V&V Automation Testing     " ]]; then
zenity_choose_document=$(
        zenity --radiolist --list --title="Choose Document to run" --width="800" --height="750" \
        --column="         Select         " --column="Document"\
	"" "DMI    - Acq4D_ListMode_Workflow_DOC1758729"\
        "" "DMI    - Recon_Auto_Test_DOC1766793"\
        "" "XRBB - Acq4D_ListMode_Workflow_DOC1758729"\
        "" "XRBB - Recon_Auto_Test_DOC1766793"\
        "" "Doc Number xxx"\
        "" "Doc Number xxx"\
        "" "Doc Number xxx"\
)
if [[ $zenity_choose_document == "" ]]; then
  Go_To_Beginning
fi
#---------------------------
if [[ $zenity_choose_document == "DMI    - Recon_Auto_Test_DOC1766793" ]]; then
chmod +x $EQ_Path/GUI_Config/DMI_ReconAutoTest_DOC1766793.sh
$EQ_Path/GUI_Config/DMI_ReconAutoTest_DOC1766793.sh
fi

#---------------------------
if [[ $zenity_choose_document == "XRBB - Recon_Auto_Test_DOC1766793" ]]; then
chmod +x $EQ_Path/GUI_Config/XRBB_ReconAutoTest_DOC1766793.sh
$EQ_Path/GUI_Config/XRBB_ReconAutoTest_DOC1766793.sh
fi

#---------------------------
if [[ $zenity_choose_document == "XRBB - Acq4D_ListMode_Workflow_DOC1758729" ]]; then
chmod +x $EQ_Path/GUI_Config/XRBB_Acq4D_DOC1758729.sh
$EQ_Path/GUI_Config/XRBB_Acq4D_DOC1758729.sh
fi
#---------------------------
if [[ $zenity_choose_document == "DMI    - Acq4D_ListMode_Workflow_DOC1758729" ]]; then

  zenity_choose_TC=$(
  zenity --radiolist --list --title="Choose TC to run DMI - Acq4D_DOC1758729" --width="800" --height="750" \
  --column="         Select         " --column="TC in Baseline" --column="TC in Columbia" --column="Name"\
  "" "TC 2.1" "TC 2.1" "Multi-Static ViP Record at High Count Rate"\
  "" "TC 2.2" "TC 2.2" "Multi-Static ViP Replay at High Count Rate"\
  "" "TC 2.3.1" "TC 2.3.1" "External Device - Multi-Static ViP Replay MFOV Gated"\
  "" "TC 2.3.2" "TC 2.3.2" "Derived (DDG) - Multi-Static ViP Replay MFOV Gated"\
  "" "TC 2.4" "TC 2.4" "Dynamic ViP Record at High Count Rate"\
  "" "TC 2.5" "TC 2.5" "Dynamic ViP Replay of High Count Rate"\
  "" "TC 2.6" "TC 2.6" "Dynamic ViP Replay To Reframed "\
  "" "TC 2.7" "TC 2.7" "Dynamic ViP Replay To Static "\
  "" "TC 2.8" "TC 2.8" "Sinogram progress through the time frame"\
  "" "TC 2.9" "TC 2.9" "Gated ViP Record High Count Rate "\
  "" "TC 2.10" "TC 2.10" "Gated NO ViP Record High Count Rate"\
  "" "TC 2.11" "Galileo" "No Automation"\
  "" "TC 2.12" "Galileo" "No Automation"\
  "" "TC 2.13" "Galileo" "No Automation"\
  "" "TC 2.14" "TC 2.11" "Gated ViP Replay To Cardiac Trigger Signal"\
  "" "TC 2.15" "TC 2.12" "No Automation"\
  "" "TC 2.16.1" "TC 2.13.1" "External Device - Q-Static and Vip Record 5MCPS"\
  "" "TC 2.16.2" "TC 2.13.2" "Derived (DDG) - Q-Static and Vip Record 5MCPS"\
  "" "TC 2.17" "TC 2.14" "10-Hour List Record"\
  "" "TC 2.18" "TC 2.15" "No Automation "\
  "" "TC 2.19" "Galileo" "No Automation"\
  "" "TC 2.20" "TC 2.16" "Singles and Deadtime Losses on Boundary"\
  "" "TC 2.21" "TC 2.17" "Concurrency - Pet Recon and Scan Data Manager concurrent activities"\
  "" "TC 2.22" "Galileo" "No Automation"\

)
# -------------------------------- if user press cancel back to begging------------------------------------
if [[ $zenity_choose_TC == "" ]]; then
  Go_To_Beginning
fi

# ------------------------------------ if user Coose invalid TC ---------------------------------------------
if [[ $zenity_choose_TC == "TC 2.22" ]] || [[ $zenity_choose_TC == "TC 2.19" ]] || [[ $zenity_choose_TC == "TC 2.18" ]] || [[ $zenity_choose_TC == "TC 2.15" ]] || [[ $zenity_choose_TC == "TC 2.13" ]] || [[ $zenity_choose_TC == "TC 2.12" ]] || [[ $zenity_choose_TC == "TC 2.11" ]]; then
  Error_Function
fi

#-------------------------------- run TC 2.17 according to baseline document----------------------------------
if [[ $zenity_choose_TC == "TC 2.17" ]]; then
TC="TC2.17"
chmod +x $Doc_Path/TC_2_17/Acq4D.1272/Acq4D_1272.py
cd $Doc_Path/TC_2_17/Acq4D.1272/
#--- store user input for sino and list path
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_17/Acq4D.1272/Acq4D_1272.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#------------------------------- run TC 2.16.1 according to baseline document --------------------------------
if [[ $zenity_choose_TC == "TC 2.16.1" ]]; then
TC="TC2.16.1"
chmod +x $Doc_Path/TC_2_16_1/Acq4D.1318/Acq4D_1318.py
cd $Doc_Path/TC_2_16_1/Acq4D.1318/
#--- store user input for sino and list path
User_Input_SINO_Function $TC
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_16_1/Acq4D.1318/Acq4D_1318.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.16.2 according to baseline document --------------------------------
if [[ $zenity_choose_TC == "TC 2.16.2" ]]; then
TC="TC_2.16.2"
Path=""
chmod +x $Doc_Path/TC_2_16_2/Acq4D.1410/Acq4D_1410.py
cd $Doc_Path/TC_2_16_2/Acq4D.1410/
#--- store user input for sino and list path
User_Input_SINO_Function $TC
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_16_2/Acq4D.1410/Acq4D_1410.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC 
fi

#-------------------------------- run TC 2.21 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.21" ]]; then
TC="TC_2.21"
chmod +x $Doc_Path/TC_2_21/Acq4D.1287/Acq4D_1287.py
cd $Doc_Path/TC_2_21/Acq4D.1287/
User_Input_SINO_Function $TC
User_Input_SINO_Function1 $TC
User_Input_LIST_Function $TC
User_Input_LIST_Function1 $TC
script -c $Doc_Path/TC_2_21/Acq4D.1287/Acq4D_1287.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function 
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.20 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.20" ]]; then
TC="TC_2.20"
chmod +x $Doc_Path/TC_2_20/Acq4D.1282/Acq4D_1282.py
cd $Doc_Path/TC_2_20/Acq4D.1282/
User_Input_SINO_Function $TC
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_20/Acq4D.1282/Acq4D_1282.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.14 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.14" ]]; then
TC="TC_2.14"
chmod +x $Doc_Path/TC_2_14/Acq4D.1242/Acq4D_1242.py
cd $Doc_Path/TC_2_14/Acq4D.1242/
User_Input_SINO_Function $TC
script -c $Doc_Path/TC_2_14/Acq4D.1242/Acq4D_1242.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.10 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.10" ]]; then
TC="TC_2.10"
chmod +x $Doc_Path/TC_2_10/Acq4D.1223/Acq4D_1223.py
cd $Doc_Path/TC_2_10/Acq4D.1223/
User_Input_SINO_Function $TC
script -c $Doc_Path/TC_2_10/Acq4D.1223/Acq4D_1223.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.9 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.9" ]]; then
TC="TC_2.9"
chmod +x $Doc_Path/TC_2_9/Acq4D.1215/Acq4D_1215.py
cd $Doc_Path/TC_2_9/Acq4D.1215/
User_Input_SINO_Function $TC
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_9/Acq4D.1215/Acq4D_1215.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.8 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.8" ]]; then
TC="TC_2.8"
chmod +x $Doc_Path/TC_2_8/Acq4D.1328/Acq4D_1328.py
cd $Doc_Path/TC_2_8/Acq4D.1328/
User_Input_SINO_Function $TC
#User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_8/Acq4D.1328/Acq4D_1328.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.7 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.7" ]]; then
TC="TC_2.7"
chmod +x $Doc_Path/TC_2_7/Acq4D.1209/Acq4D_1209.py
cd $Doc_Path/TC_2_7/Acq4D.1209/
User_Input_SINO_Function $TC
script -c $Doc_Path/TC_2_7/Acq4D.1209/Acq4D_1209.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.6 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.6" ]]; then
TC="TC_2.6"
chmod +x $Doc_Path/TC_2_6/Acq4D.1204/Acq4D_1204.py
cd $Doc_Path/TC_2_6/Acq4D.1204/
User_Input_SINO_Function $TC
script -c $Doc_Path/TC_2_6/Acq4D.1204/Acq4D_1204.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.5 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.5" ]]; then
TC="TC_2.5"
chmod +x $Doc_Path/TC_2_5/Acq4D.1196/Acq4D_1196.py
cd $Doc_Path/TC_2_5/Acq4D.1196/
User_Input_SINO_Function $TC
script -c $Doc_Path/TC_2_5/Acq4D.1196/Acq4D_1196.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.4 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.4" ]]; then
TC="TC_2.4"
chmod +x $Doc_Path/TC_2_4/Acq4D.1189/Acq4D_1189.py
cd $Doc_Path/TC_2_4/Acq4D.1189/
User_Input_SINO_Function $TC
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_4/Acq4D.1189/Acq4D_1189.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#---------------------------- run TC 2.3.2 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.3.2" ]]; then
TC="TC_2.3.2"
chmod +x $Doc_Path/TC_2_3_2/Acq4D.1448/Acq4D_1448.py
cd $Doc_Path/TC_2_3_2/Acq4D.1448/
User_Input_SINO_Function $TC
User_Input_SINO_Function1 $TC
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_3_2/Acq4D.1448/Acq4D_1448.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#----------------------------- run TC 2.3.1 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.3.1" ]]; then
TC="TC_2.3.1"
chmod +x $Doc_Path/TC_2_3_1/Acq4D.1179/Acq4D_1179.py
cd $Doc_Path/TC_2_3_1/Acq4D.1179/
User_Input_SINO_Function $TC
script -c $Doc_Path/TC_2_3_1/Acq4D.1179/Acq4D_1179.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.2 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.2" ]]; then
TC="TC_2.2"
chmod +x $Doc_Path/TC_2_2/Acq4D.1165/Acq4D_1165.py
cd $Doc_Path/TC_2_2/Acq4D.1165/
User_Input_SINO_Function $TC
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_2/Acq4D.1165/Acq4D_1165.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi

#-------------------------------- run TC 2.1 according to baseline document ----------------------------------
if [[ $zenity_choose_TC == "TC 2.1" ]]; then
TC="TC_2.1"
chmod +x $Doc_Path/TC_2_1/Acq4D.1154/Acq4D_1154.py
cd $Doc_Path/TC_2_1/Acq4D.1154/
User_Input_SINO_Function $TC
User_Input_LIST_Function $TC
script -c $Doc_Path/TC_2_1/Acq4D.1154/Acq4D_1154.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
Clean_Logs_function
Finish_Function $TC
fi
fi
#-- last
fi












