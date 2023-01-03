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

#---------------------------------------- Take list path from user -------------------------------------------------------------------

User_Input_LIST_Function(){
zenity_LIST_Input=$( zenity --entry --title="Insert LIST File path" --width="500" --height="300" --text "\n\n\n\nEnter LIST file path directory from $1 :\n\n")
echo $zenity_LIST_Input > /usr/g/ctuser/EQ_Automation/User_Input_LIST.txt
}

#############################################  Choose PAARTF Test to run  ######################################################################################
zenity_choose_PAARTF=$(
        zenity --radiolist --list --title="Choose PAARTF sequence " --width="800" --height="750" \
        --column="         Select         " --column="Choose PAARTF sequence          " --column="Status"\
        " " "ART-SWVP_sequence     " "Develop"\
        " " "DDWaveGen_sequence     " "Not Applicable"\
        " " "DPT_sequence     " "Develop"\
        " " "DataAcq_sequence" "Develop"\
        " " "DetCalServer_sequence" "Develop"\
        " " "DetectorCal_sequence" "Develop"\
        " " "RDA_sequence   " "Develop"\
        " " "ScanreqMgr   " "Develop"\
)
################################################### PAARTF test choose TC in a new Zenity screen  ###############################################################################

if [[ $zenity_choose_PAARTF == "" ]]; then
  Go_To_Beginning
fi

if [[ $zenity_choose_PAARTF == "DataAcq_sequence" ]]; then
chmod +x $EQ_Path/GUI_Config/DataAcq_Choose_TC.sh
$EQ_Path/GUI_Config/DataAcq_Choose_TC.sh
fi


if [[ $zenity_choose_PAARTF == "XXXXX" ]]; then
#chmod +x $EQ_Path/GUI_Config/Choose_PAARTF_Test.sh
#$EQ_Path/GUI_Config/Choose_PAARTF_Test.sh
  Go_To_Beginning
fi

if [[ $zenity_choose_PAARTF == "DDWaveGen_sequence     " ]]; then
Error_Function 
fi

