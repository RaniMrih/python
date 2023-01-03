#!/bin/bash
#This GUI using linux Default zenity popups
#Developed for PET/CT Automation testing and operations Using Python and Bash
#Created at 10/5/2020
#Author: Rani Mrih

#VARS
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

  zenity_choose_TC=$(
  zenity --radiolist --list --ok-label="A" --title="Choose TC to run XRBB - Recon_Auto_Test_DOC1766793"  --width="800" --height="750" \
  --column="         Select         " --column="TC in Baseline" --column="TC in Columbia" --column="Name"\
  "" "TC 2.1" "TC 2.1" "Recon Auto Test"\
  "" "TC 2.2" "TC 2.2" "Missing job and gold file"\
  "" "TC 2.3" "TC 2.3" "Measure Recon Time"\
  "" "   All" "   All" "Run all TCs together"

)
# -------------------------------- if user press cancel back to begging------------------------------------
if [[ $zenity_choose_TC == "" ]]; then
  Go_To_Beginning
fi

