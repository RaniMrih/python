#!bin/bash


2.1

SINOS : /petRDFS/ATSOLOLM1  Fake (0-2) short path
LIST  : /petLists/QOTAGJYS2 (0-2) short path
-----------------------------------------------------------
Static Replay : 2.2 
SINO : /petRDFS/ATSOLOLM1  Fake (0-2) short path
LIST  : /petLists/QOTAGJYS2 (0-2) short path
-------------------------------------------------------
External Gated : 2.3.1
SINOS : /petRDFS/ATSOLOLT | Original (0,10,20,29) , Fake (0-29)
-----------------------------------------------------
Derived DDG Gated : 2.3.2
SINOS Step 1448 : /petRDFS/ATSOLOLM1 Fake (0-2) short path
SINOS Step 1415 : /petRDFS/ATSOLOLT | Original (0,10,20,29) , Fake (0-29)
LISTS Step 1448 : /petLists/QOTAGJYS2 (0-2) short path

-----------------------------------------------------------
Dynamic : 2.4
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLM  Fake (0-15) short path
(FROM 2.1 ) LIST LIVE :/petLists/QOTAGJYS (0) short path
------------------------------------------------------------------
2.5
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLM  Fake (0-15) short path
-----------------------------------------------------------------
2.6
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLM  Fake (0-15) short path
-----------------------------------------------------------------
2.7
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLS  Fake (0) short path
-----------------------------------------------------------------
2.8
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLM  Fake (0-15) short path
-----------------------------------------------------------------
2.9
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLK  Fake (0-9) short path
(FROM 2.1 ) LIST LIVE :/petLists/QOTAGJYS (0) short path
-----------------------------------------------------------------
2.10
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLK  Fake (0-7) short path
-----------------------------------------------------------------
2.11 
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLK  Fake (0-9) short path
----------------------------------------------------------------
2.14
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLK  Fake (0-9) short path
----------------------------------------------------------------
2.16.1
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLK  Fake (0-9) short path
(FROM 2.1 ) LIST LIVE :/petLists/QOTAGJYS1 Fake (0-9) short path
----------------------------------------------------------------
2.16.2
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLK  Fake (0-9) short path
(FROM 2.1 ) LIST LIVE :/petLists/QOTAGJYS1 Fake (0-9) short path
----------------------------------------------------------------
2.17
(FROM 2.1 ) LIST LIVE :/petLists/QOTAGJYS (0) short path
----------------------------------------------------------------
2.20
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLD  Fake (0) short path
(FROM 2.1 ) LIST LIVE :/petLists/QOTAGJYS (0) short path
----------------------------------------------------------------
2.21
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLD  Fake (0) short path
(FROM 2.3.1) SINOS :/petRDFS/ATSOLOLD  Fake (0) short path
(FROM 2.1 ) LIST LIVE :/petLists/QOTAGJYS (0) short path
(FROM 2.1 ) LIST LIVE :/petLists/QOTAGJYS (0) short path


#Bold in zenity
zenity --list --radiolist --text "<b>Please</b>"

#zenity editable text
zenity --text-info --title="Automation log :" --width="950" --height="700" --filename=/usr/g/ctuser/EQ_Automation/Automation_Log.log --editable

#conected users 
who - currentlly logged
whoami - my user name 
last - all history

#1-clean logs from all colors
perl -pe 's/\x1b\[[0-9;]*[mG]//g' $Tmp > $Tmp1
#2-clean logs after script command from ^M (special chrecters)
col -bp < $Tmp1 >> $FinalLog


#chmod for all directories and subdirectories
chmod -R 777 ./

#python lines
print (BLUE + ""+'\n'+"" +RESET)

#grep sed and replace 
grep -rl '   Scan Description = Static Record 2.1 fixed' ReplayHdrs_2.2.tell | xargs sed -i 's/   Scan Description = Static Record 2.1 fixed/   Scan Description = Static ViP Replay 2.2 /g'
#grep few params together
grep 'eventSource\|eventSimulationData\|startCondition\|retroScan' $PWD/LiveHdrs_2.1.tell > A.txt

## gerp file and cuts "milliseconds" after the number and "Frame Duration" before number
grep -m1 'Frame Duration' ~/EQ_Automation/Scripts/Acq4D.1165/S2.1Sino.txt | sed 's|\(.*\) milliseconds.*|\1|' | sed 's|\(.*\)   Frame Duration   = *|\1|'

#greps word remove it and remove everything before
sed -n -e 's/^.*Module //p'

#this sed greps the word remove every thing before it
 sed 's/^.*\(Module*\)/\1/g'

#this grep cuts only the word
 sed 's|\(.*\)Module*|\1|'

#this grep cuts from "Module" to the end of the line
grep 'Singles Block Max Counts' S2.1Sino.txt | sed 's|\(.*\)Module.*|\1|'

#this method for float calculation
result=$(echo "$ReplayDuration2_3_1 /  $OriginDuration2_1 " | bc )
result1=$(echo "$ReplayDuration2_3_1 /  $OriginDuration2_1 " | bc -l )
result2="$result$result1"
diff=$(echo "$result2 * $OriginPrompts2_1" | bc

# round numbers
H_Limit=$(printf "%.0f\n" $H_Limit)

# math floats to see zero at line beggining
X=$(echo "${ArrSumBinDwell[$i]} ${ArrFrameDuration[$i]}" |  awk '{printf "%f", $1 / $2}')
echo ${BLUE}"bed $j :"${reset}
echo $X %

#grep words start with 'S' the wc -l conts  
ls /petRDFS/XOIATRMM/AVEWDJMT/ATSOLOLT | grep ^S | wc -l

#cmd remove all files except one
find . ! -name 'Acq4D_1154.py' -type f -exec rm -f {} +

#---------------------------zenity with dropdown list by mistake
# 1 - Sinos and Lists files pathes
os.popen('zenity --entry --title="Insert SINO path" --width="500" --height="400" --text "\n\n\nEnter Sinogram path directory from "'+TC+" Scan from step "+step+" : \n\n\n")
# change buttons text
zenity --question --title="" --text "Choose A or B" --ok-label="Start Automation" --cancel-label="Go Back"
#list
zenity --list --cancel-label="Go Back" --column="Column 1"


#    '2.3.1':[ '1179', '1180', '1181', '1182', '1183', '1185', '1363','1364'],
#    '2.3.2':[ '1415', '1416', '1417', '1418', '1419', '1420', '1421','1422','1448'],
#    '2.4' : ['1189','1190','1192','1193'],
#    '2.5' : ['1196','1197','1199','1201','1202'],
#    '2.6' : ['1204','1206'],
#    '2.7' : ['1209','1210','1211'],
#    '2.8' : ['1328'],
#    '2.9' : ['1215','1216','1217','1218','1383'],
#    '2.10': ['1223','1225','1384','1385'],
#    '2.11': ['1228','1385'],
#    '2.14': ['1242','1243','1245'],
#    '2.16.1':['1318','1319'],
#    '2.16.2':['1410','1411'],
#    '2.17': ['1272','1273','1274','1275'],
#    '2.20': ['1282'],
#    '2.21': ['1287','1289','1290','1291']