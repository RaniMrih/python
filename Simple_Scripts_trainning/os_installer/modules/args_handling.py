from __future__ import print_function
from builtins import input
import sys
import os
from modules.misc_funsc import parse_hosts
from modules.gen_funcs import mac_get
from modules.gen_funcs import ipmireset
from modules.gen_funcs import conf_build
from modules.winlabels import choices_print
from modules.winlabels import check_restparams
from modules.fbsd_funcs import conf_build_freebsd

def lin_args(args,labels):
    if args.oslist:
        if args.grub==True:
            for item in labels:
                if not  item.startswith("#"):
                    print(item)
        else:
            for item in sorted(labels):
                if not item.startswith("#"):
                    print(item)
    else:
        if args.filepath == None and args.targetHost == None:
            msg = "No target hosts or file with hosts were specified\n\nrefer to %s linux -h\n\nRegards ItDevOps" % os.path.realpath(__file__)
            raise Exception(msg)

        if args.automation == False and args.quiet == False:
            warn = input("\n\nBe aware: you going to install os on multiple hosts - this is irreversible.\nAre YOU SURE ?(y/n) :")
            if warn == "y":
                if args.filepath is not None:
                    if os.path.isfile(args.filepath):
                        try:
                            hosts = parse_hosts(args.filepath)
                            conf_build(args.os,mac_get(hosts,"linux"),args)
                        except Exception as e:
                            raise e

                if args.targetHost is not None:
                    conf_build(args.os,mac_get(args.targetHost,"linux"),args)
                    #ipmireset(args.targetHost,args)


            else:
                print("Bye!!")
                sys.exit(0)

        else:
            if args.filepath is not None:
                if os.path.isfile(args.filepath):
                    try:
                        hosts = parse_hosts(args.filepath)
                        conf_build(args.os,mac_get(hosts,"linux"),args)
                    except Exception as e:
                        raise e


            if args.targetHost is not None:
                conf_build(args.os,mac_get(args.targetHost,"linux"),args)

def win_args(args,label,list_key):
    if args.oslist:
        choices_print(label,list_key)
        sys.exit()
    if args.targetHost is not None:

        if args.multi is False and args.single is False:
            msg = "No mode is supplied (single/multi)\n\nPlease run '%s win -h'\n\nregards ItDevOps\n" % os.path.realpath(__file__)
            sys.exit(msg)

        if args.multi and args.single:
            msg = "\n--single and --multi are mutually exclusive, please choose one of them\n\nfor reference run '%s win -h'\n\nregards ItDevOps\n" % os.path.realpath(__file__)
            sys.exit(msg)

        if args.multi or args.single:
            check_restparams(args,label)
    else:
        msg = "Please supply host/s to install on\nfor reference:\n\nPlease run '%s win -h'\n\nregards ItDevOps\n" % os.path.realpath(__file__)
        sys.exit(msg)


def freebsd_args(args,label,freebsdsite):

    if args.oslist:
        for i in label:
            if '-'  in i:
                print(i)

        sys.exit()
    if args.filepath == None and args.targetHost == None:
        msg = "No target hosts or file with hosts were specified\n\nrefer to %s freebsd -h\n\nRegards ItDevOps" % os.path.realpath(__file__)
        raise Exception(msg)

    if args.automation == False and args.quiet == False:
        warn = input("\n\nBe aware: you going to install os on multiple hosts - this is irreversible.\nAre YOU SURE ?(y/n) :")
        if warn == "y":

            if args.filepath is not None:
                if os.path.isfile(args.filepath):
                    try:
                        hosts = parse_hosts(args.filepath)
                        conf_build_freebsd(args.os,mac_get(hosts,"freebsd"),freebsdsite,args)
                    except Exception as e:
                        raise Exception(e)

#                ipmireset(hosts,args)

            if args.targetHost is not None:
                conf_build_freebsd(args.os,mac_get(args.targetHost,"freebsd"),freebsdsite,args)
#                ipmireset(args.targetHost,args)

        else:
            print("Bye!!")
            sys.exit()

    else:
        if args.filepath is not None:
            if os.path.isfile(args.filepath):
                try:
                    hosts = parse_hosts(args.filepath)
                    conf_build_freebsd(args.os,mac_get(hosts,"freebsd"),freebsdsite,args)
                except Exception as e:
                    raise Exception(e)


        if args.targetHost is not None:
            conf_build_freebsd(args.os,mac_get(args.targetHost,"freebsd"),freebsdsite,args)
