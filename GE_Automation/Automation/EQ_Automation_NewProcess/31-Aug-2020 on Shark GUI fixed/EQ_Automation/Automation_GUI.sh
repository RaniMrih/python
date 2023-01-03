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


############################################# Screen includes all Doc TCs #######################################################################################

#---------------------------
if [[ $zenity_choose_document == "DMI    - Acq4D_ListMode_Workflow_DOC1758729" ]]; then

  zenity_choose_TC=$(
  zenity --radiolist --list --title="Choose TC to run DMI - Acq4D_DOC1758729" --width="800" --height="750"\
  --column="         Select         " --column="TC in Baseline" --column="TC in Columbia" --column="Name"\
  "" "TC_2_1" "TC_2_1" "Multi-Static ViP Record at High Count Rate"\
  "" "TC_2_2" "TC_2_2" "Multi-Static ViP Replay at High Count Rate"\
  "" "TC_2_3_1" "TC_2_3_1" "External Device - Multi-Static ViP Replay MFOV Gated"\
  "" "TC_2_3_2" "TC_2_3_2" "Derived (DDG) - Multi-Static ViP Replay MFOV Gated"\
  "" "TC_2_4" "TC_2_4" "Dynamic ViP Record at High Count Rate"\
  "" "TC_2_5" "TC_2_5" "Dynamic ViP Replay of High Count Rate"\
  "" "TC_2_6" "TC_2_6" "Dynamic ViP Replay To Reframed "\
  "" "TC_2_7" "TC_2_7" "Dynamic ViP Replay To Static "\
  "" "TC_2_8" "TC_2_8" "Sinogram progress through the time frame"\
  "" "TC_2_9" "TC_2_9" "Gated ViP Record High Count Rate "\
  "" "TC_2_10" "TC_2_10" "Gated NO ViP Record High Count Rate"\
  "" "TC_2_11" "Galileo" "No Automation"\
  "" "TC_2_12" "Galileo" "No Automation"\
  "" "TC_2_13" "Galileo" "No Automation"\
  "" "TC_2_14" "TC_2_11" "Gated ViP Replay To Cardiac Trigger Signal"\
  "" "TC_2_15" "TC_2_12" "No Automation"\
  "" "TC_2_16_1" "TC_2_13_1" "External Device - Q-Static and Vip Record 5MCPS"\
  "" "TC_2_16_2" "TC_2_13_2" "Derived (DDG) - Q-Static and Vip Record 5MCPS"\
  "" "TC_2_17" "TC_2_14" "10-Hour List Record"\
  "" "TC_2_18" "TC_2_15" "No Automation "\
  "" "TC_2_19" "Galileo" "No Automation"\
  "" "TC_2_20" "TC_2_16" "Singles and Deadtime Losses on Boundary"\
  "" "TC_2_21" "TC_2_17" "Concurrency - Pet Recon and Scan Data Manager concurrent activities"\
  "" "TC_2_22" "Galileo" "No Automation"\

)

# -------------------------------- if user press cancel back to begging------------------------------------
if [[ $zenity_choose_TC == "" ]]; then
  Go_To_Beginning
fi

# ------------------------------------ if user Coose invalid TC ---------------------------------------------
if [[ $zenity_choose_TC == "TC_2_22" ]] || [[ $zenity_choose_TC == "TC_2_19" ]] || [[ $zenity_choose_TC == "TC_2_18" ]] || [[ $zenity_choose_TC == "TC_2_15" ]] || [[ $zenity_choose_TC == "TC_2_13" ]] || [[ $zenity_choose_TC == "TC_2_12" ]] || [[ $zenity_choose_TC == "TC_2_11" ]]; then
  Error_Function
else
#-------------------------------- run TC_2_1 according to baseline document ----------------------------------
#if [[ $zenity_choose_TC == "TC_2_1" ]]; then

#remove spaces from string to send to exexute_wrapper.py
zenity_choose_document=${zenity_choose_document//[[:blank:]]/}
zenity_choose_TC=${zenity_choose_TC//[[:blank:]]/}

#echo $zenity_choose_TC
#chmod +x $Doc_Path/TC_2_1/Acq4D.1154/Acq4D_1154.py
#cd $Doc_Path/TC_2_1/Acq4D.1154/
#User_Input_SINO_Function $TC
#User_Input_LIST_Function $TC
#script -c $Doc_Path/TC_2_1/Acq4D.1154/Acq4D_1154.py $EQ_Path/Tmp_Log.log
#-- go to clean logs function and finish popup function
cd $EQ_Path $zenity_choose_document $zenity_choose_TC
python $EQ_Path/execute_wrapper.py $zenity_choose_document $zenity_choose_TC
#Clean_Logs_function
Finish_Function $TC
#fi
fi
fi
fi










