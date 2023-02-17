from __future__ import print_function
#where we call the modules and doing the job

import sys
import os
from modules.prechecks import check_user
from modules.prechecks import prereq as requiredstuff


def main():
    try:
#checks for required components for script to run on the host
        requiredstuff()
    except Exception as e:
        print("error is: ",e)
        sys.exit(1)

    try:
        from modules.prechecks import check_path
        from modules.misc_funsc import build_labels,siterelated
        from modules.args_handling import lin_args
        from modules.args_handling import win_args
        from modules.args_handling import freebsd_args
        from modules.args import parser_args
# get args from user input
        args = parser_args()
        check_user(args.automation)
#path checks to get the windows xml,if see more stuff - will add here
#        base_loc = "/auto"
#        check_path(base_loc)

#        win_labels_file = "Images.xml"
#        linux_labels_file = 'default-labels'
        labels = []
# Here we parse the labels for requested os type and do all the work
        #print args.site,args
        lin_labels,win_labels,freebsd_labels = siterelated(args.site,args)
        if sys.argv[1] == 'linux':
#            w_d = os.path.join(base_loc,'GLIT','PXE','tftpboot','pxelinux.cfg')
            if check_path(os.path.split(lin_labels)[0]):
                try:
                    #print sys.argv[1],args,lin_labels
                    labels = build_labels(sys.argv[1],args,lin_labels,'')
                    #print "gggG"
                    lin_args(args,labels)

                except Exception as e:
                    raise Exception(e)

        if sys.argv[1] == 'win':

            #w_d = os.path.join(base_loc,'GLIT/autoinst/osList/')
            if check_path(os.path.split(win_labels)[0]):
                try:
                    labels,list_key = build_labels(sys.argv[1],args,win_labels,'')
                    #print labels
                    #print list_key
                    win_args(args,labels,list_key)

                except Exception as e:
                    raise Exception(e)


        if sys.argv[1] == 'freebsd':
            labels,freebsdsite = build_labels(sys.argv[1],args)
            freebsd_args(args,labels,freebsdsite)





    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
