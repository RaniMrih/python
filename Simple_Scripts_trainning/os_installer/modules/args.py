from __future__ import print_function
# here we handle the cmd args
import sys, getpass
import argparse

def parser_args():
    user = 'root'
    passwd = '3tango11'
    try:
        user_notifier = getpass.getuser()
    except:
        user_notifier = None
        print("User was not found!")

    parser = argparse.ArgumentParser(prog=sys.argv[0],description="this script installs os on host/s via pxe or windows wds",formatter_class=argparse.RawDescriptionHelpFormatter)
    subparser = parser.add_subparsers(description="linux - install oses from pxe,mainly linux or virtualization \
            \nwin - install windows oses via windows wds \
            \nfreebsd - install freebsd via pxe \
            \n\nevery mode got its help,please run %(prog)s linux -h or %(prog)s win -h to see the arguments",help="operating modes help")


    linux = subparser.add_parser('linux',
            description='%s' % 'In this mode script will use pxe configuration file to take image names from \
                    \n\n\tif ran with -l : will list oses and exit \
                    \n\tif ran with -f : will expect for a file containg list of hostname separated by new line \
                    \n\tif ran with -t : will expect for hostnames passed in command line separated by space \
            \n\n\tExample:\n\n\t%(prog)s  -f /tmp/hosts.txt -o RH6.4x64_new_local \
            \n\t%(prog)s  -t hostA hostB hostC -o RH6.4x64_new_local\n',
            formatter_class=argparse.RawDescriptionHelpFormatter )

    linux.add_argument('-f','--filepath',help='path to file with hostnames list in one column',required=False)
    linux.add_argument("-o","--os",help="os to install should be label from pxe, for example: RH6.4x64_new_local",required=False)
    linux.add_argument("-U","--ipmiUsername",required=False,help="User to connect with to ipmi ,by default: %(default)s",default="root")
    linux.add_argument("-P","--ipmiPassword",required=False,help="Password to connect with to ipmi, by default: %(default)s",default="3tango11")
    linux.add_argument("-r","--rreboot",required=False,help='initiate reboot of the host via pdu,assumes host will boot from pxe',action="store_true")
    linux.add_argument("-t","--targetHost",nargs='+',required=False,help="host to install on , l-ostest for example")
    linux.add_argument("-l","--oslist",help="list oses in pxe and exit",action="store_true"  )
    linux.add_argument("-a","--automation",help=argparse.SUPPRESS,action="store_true"  )
    linux.add_argument("-q","--quiet",help=argparse.SUPPRESS,action="store_true"  )
    linux.add_argument("--site",help='specify site to run at. doesnt work in dmz')
    linux.add_argument("-c","--clean",help='will install an almost clean OS',action="store_true"  )
    linux.add_argument("-u","--user_notifier",help='User name to send email notifications- default is taken from shell',default=user_notifier)
    linux.add_argument("-d","--department",help='Ignore- still in development',default='general' )
    linux.add_argument("-s","--string",help='Pass string argument as kernel parameter - IT usage')
    linux.add_argument("-g","--grub",help='When used, MAC file will be written to grub loader and not pxelinux(powerPC) - IT usage', action="store_true")

    wininst = subparser.add_parser('win',description='%s' % "In this mode script will take configuration used for http://mtl-wds-01.labs.mlnx \
            \n\n\tif ran with -l : will list oses and exit \
            \n\tif ran with --multi : will install accept more than one os name in -o switch \
            \n\tif ran with --single : will accept only one os name in -o switch \
            \n\n\tExample:\n\n\t%(prog)s --multi -t hostA hostB hostC -o WS2012STD:70 WS2008R2_ENT_x64 WS2008R2_ENT_x64:QA:Guest WS208R2_Std_x64:Regression:Guest:95 \
            \n\t%(prog)s --single -t hostA hostB hostC -o WS2008R2_Std_x64:Regression:Guest:95"
            ,formatter_class=argparse.RawDescriptionHelpFormatter)
    wininst.add_argument("--multi",help="multi boot installation,will start from safe os by default",required=False,action='store_true')
    wininst.add_argument("--single",help="self explaining",required=False,action='store_true')
    wininst.add_argument('-l',"--oslist",help="List Oses and their options and exit",action='store_true')
    wininst.add_argument('-t','--targetHost',help='host/s to install on,l-ostest for example,write hostnames separated by space',nargs='+',required=False)
    wininst.add_argument('-o','--osname',help='put the osnames like this: "ImageName:size:modifier:customisation",only the ImageName is required, if nothing else is provided - default params will be added, separate images with space',required=False,nargs="+")
    wininst.add_argument('-U','--ipmiuser',help='ipmiuser,default: root',required=False,default='root')
    wininst.add_argument('-P','--ipmipassword',help='ipmiuser,default: 3tango11',required=False,default='3tango11')
    wininst.add_argument("-a","--automation",help=argparse.SUPPRESS,action="store_true"  )
    wininst.add_argument("-q","--quiet",help=argparse.SUPPRESS,action="store_true"  )
    wininst.add_argument("--site",help='specify site to run at. not works in dmz')

    freebsd = subparser.add_parser('freebsd',
            description='%s' % 'In this mode script will create pxe configuration file to install freebsd \
                    \n\n\tif ran with -l : will list freebsd versions  and exit \
                    \n\tif ran with -f : will expect for a file containg list of hostname separated by new line \
                    \n\tif ran with -t : will expect for hostnames passed in command line separated by space \
            \n\n\tExample:\n\n\t%(prog)s  -f /tmp/hosts.txt -o 10-0-RELEASE-i386-add \
            \n\t%(prog)s  -t hostA hostB hostC -o 10-0-RELEASE-i386-add\n',
            formatter_class=argparse.RawDescriptionHelpFormatter )

    freebsd.add_argument('-f','--filepath',help='path to file with hostnames list in one column',required=False)
    freebsd.add_argument("-o","--os",help="os to install should be label from pxe, for example: 10-0-RELEASE-i386-add",required=False)
    freebsd.add_argument("-U","--ipmiUsername",required=False,help="User to connect with to ipmi ,by default: %(default)s",default="root")
    freebsd.add_argument("-P","--ipmiPassword",required=False,help="Password to connect with to ipmi, by default: %(default)s",default="3tango11")
    freebsd.add_argument("-r","--rreboot",required=False,help='initiate reboot of the host via pdu,assumes host will boot from pxe',action="store_true")
    freebsd.add_argument("-t","--targetHost",nargs='+',required=False,help="host to install on , l-ostest for example")
    freebsd.add_argument("-l","--oslist",help="list oses in pxe and exit",action="store_true"  )
    freebsd.add_argument("-a","--automation",help=argparse.SUPPRESS,action="store_true"  )
    freebsd.add_argument("-q","--quiet",help=argparse.SUPPRESS,action="store_true"  )
    freebsd.add_argument("--site",help='specify site to run at. not works in dmz')

    args = parser.parse_args()

    allargs = args

    return args
