from __future__ import print_function
#from modules.args import args

from future import standard_library
standard_library.install_aliases()
from builtins import range
try:
    import MySQLdb
except ImportError:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        import MySQLdb
    except ImportError as e:
        raise "Error is"

import subprocess as sub
import os
import shlex
import getpass
import traceback
import sys
import socket
import datetime
import shutil

def exportweb():
    string = "/usr/bin/curl -s -k -o /dev/null https://tools.mellanox.com/lit/index/export"
    p = sub.Popen(shlex.split(string),stdout = sub.PIPE,stderr = sub.PIPE)
    stdout,stderr = p.communicate()
    #print stdout
    return p.returncode
    #if p.returncode == 0:
    #    return '0'
    #else:
    #    return '0'

def mac_get(hostname,ostype):
    from modules.presets import list_url
    from modules.misc_funsc import get_site,ini_parse
    import modules.presets
    import urllib.request, urllib.error, urllib.parse

#refactor here , got unneeded lines
    resdct = ini_parse(modules.presets.sites_conf)
    host_site = get_site(socket.gethostbyname(socket.gethostname()),'freebsd')[1]

    fnames = {}

    if 'dmz' in host_site.lower() or 'e2e' in host_site.lower():
        print('Running from host in dmz - will not update dhcp')
        list_file = urllib.request.urlopen(list_url).readlines()
        for host in hostname:
            fnames[host] = {
                            'host':{},
                            'ilo':{}
                            }
            for i in list_file:
                if host in i and 'ilo' not in i:
                    ip = i.split(';')[0]
                    mac = i.split(';')[1].replace(' ','')
                    fnames[host]['host'][ip] = "%s" %("01-"+"-".join(mac.split(":")).lower())

                if 'ilo' in i and host in i:
                    ip = i.split(';')[0]
                    fnames[host]['ilo']['ip'] = ip

        for host in fnames:
            if 'ip' not in fnames[host]['ilo']:
                fnames[host]['ilo']['ip'] = 'virtual'



        return fnames

    try:
        db = MySQLdb.connect(host="litdb.labs.mlnx", user="lit", passwd="3tango",db="lit")
        cur = db.cursor()

    except Exception:
        msg = "failed to connect to db please check"
        raise Exception(msg)

    for entry in hostname:

        string = "select name,ip,mac from machines where active = '1' and name in ('%s') or ip in ('%s');" % (entry,entry)

        try:
            cur.execute(string)
            dbret = cur.fetchall()
            site = get_site(dbret[0][1],'freebsd')
            #print site
            #print resdct
            pxeip = resdct[site[-1]]['lab_pxe'][0]

            if not len(dbret) == 0:
                string = "select name,ip from machines where name in ('%s-ilo');" % dbret[0][0]
                cur.execute(string)
                iloname = cur.fetchall()
                '''
                    updating db
                '''

                """
                    check if you need to change next server ip
                """
                string = "select next_server,filename from machines where name  in ('%s') or ip in ('%s');" %(entry,entry)
                cur.execute(string)
                nextserver = cur.fetchall()
###############################################################################################################################################SINAN FIX, Next Server, PPC#
                #if args.grub:

                #string = "update machines set filename = '/boot/grub/powerpc-ieee1275/core.elf',next_server = '%s' where name in ('%s');" %  (nextserver[0][0],dbret[0][0])

                #else:

                string = "update machines set filename = 'pxelinux.0',next_server = '%s' where name in ('%s');" %  (nextserver[0][0],dbret[0][0])

                print('Changing next server to %s' % (nextserver[0][0]))
                cur.execute(string)
                db.commit()
                export = exportweb()
###########################################################################################################################################################################
                if export != 0:
                    msg = 'failed to export dhcp data'
                    raise Exception(msg)
                fnames[entry] = {
                                      'host':{},
                                      'ilo':{}
                                       }
                fnames[entry]['host'][dbret[0][1]] = "%s" %("01"+"-"+"-".join(dbret[0][-1].split(":")).lower())
                if len(iloname) > 0:
                    fnames[entry]['ilo']['ip'] = iloname[0][1]
                else:
                    fnames[entry]['ilo']['ip'] = 'virtual'


            else:
                raise Exception('empty result from db')

        except Exception as e:
            msg = "failed to retriev values from db, please check. %s" % e
            raise Exception(msg)


    return fnames




def ipmireset(hosts,args):
    #print hosts
    #print args
    log_location = "/auto/GLIT/LOGS/AUTOINSTALL/Multihost/install_log.log"
    do_reboot = "/auto/GLIT/SCRIPTS/AUTOINSTALL/Multihost/do_reboot.sh"
    set_pxe = "/auto/GLIT/SCRIPTS/AUTOINSTALL/Multihost/set_pxe_once.sh"
    rreboot = "/auto/LIT/SCRIPTS/rreboot.w"
    if args.rreboot == False:
        if hosts == 'virtual':
            print("pxe file created, booting vm from pxe is not implemente yet, please restart your vm and boot to pxe. In 10min file will be erased")
            return
        string = set_pxe + " %s %s %s" % (hosts,args.ipmiUsername,args.ipmiPassword)
        try:
            #print string
            proc = sub.Popen(string.split(),stdout=sub.PIPE,stderr=sub.PIPE)
            out,err = proc.communicate()
            proc.wait()
            if proc.returncode != 0:
                msg = "ERROR occured:\nstderr %s\nstdout %s" % (err,out)
                print("Please open a ticket to labs_support asking to fix ILO and attaching this string: %s" % string)
                raise Exception(msg)

            else:
                print("setted %s to pxeboot" % hosts)
        except OSError:
            msg = "\nERROR: please install ipmitools\n if for some reason you cannot provide this package\n put your machine manually to pxe and reboot it\n"
            raise Exception(msg)




        string = do_reboot + " %s %s %s" % (hosts,args.ipmiUsername,args.ipmiPassword)
        #print string
        proc = sub.Popen(string.split(),stdout=sub.PIPE,stderr=sub.PIPE)
        out,err = proc.communicate()
        proc.wait()
        if proc.returncode != 0:
            msg = "\nERROR occured: %s\n" % err
            msg = msg + "Also maybe this machine not provided with ipmi, ensure it boots with pxe and restart it manually or with remote reboot script\n"
            raise Exception(msg)
        else:
            print("%s is restarting \nregards eit_os\n" % hosts)

    if args.rreboot == True:
        string = rreboot + " %s REBOOT" % hosts
        print("string is: ",string)
        try:
            proc = sub.Popen(string.split(),stdout=sub.PIPE,stderr=sub.PIPE)
            out,err = proc.communicate()
            proc.wait()
            if proc.returncode != 0:
                msg = "ERROR occured in execution of rreboot : %s " % out
                raise Exception(msg)

            else:
                print("Remote reboot signaled for %s" % hosts)
        except OSError:
            msg = "\nERROR: failed to find /auto/LIT/SCRIPTS/rreboot.w, check automounts\n"
            raise Exception(msg)


    username = getpass.getuser()
    machine = socket.gethostname()

    f_tgt = open(log_location,'a')
    _date = datetime.datetime.strftime(datetime.datetime.now(),"%F:%H:%m")
    string = "\n%s : \t%s :\t%s started installation of %s on %s\n" % (_date,machine,username,args.os,hosts)
    f_tgt.write(string)
    f_tgt.close()

def conf_build(_os,fnames,args):
    from modules.misc_funsc import get_site
    import modules.presets as globvars
    res = None
    w_w_d = '/auto/GLIT/SCRIPTS/AUTOINSTALL/Multihost/'

    if hasattr(args,'grub') and args.grub == True:
        w_d = os.path.join(globvars.base_loc,globvars.base_lin_grub_config_loc)
        #print _os,fnames
        conf_build_grub(_os,fnames,args)

    else:
        for key in fnames:
            site_details = get_site(list(fnames[key]['host'].keys())[0],'freebsd')
            host_site = get_site(socket.gethostbyname(socket.gethostname()),'freebsd')[1]
            #print host_site
            w_d = os.path.join(globvars.base_loc,globvars.base_lin_config_loc)

            if 'DMZ' in site_details[1] or 'E2E' in site_details[1]:
                w_d =  os.path.join(globvars.base_loc_dmz,site_details[-1]+globvars.base_lin_config_loc)
#last change anton 19/10/16 17:20
            if 'DMZ' in host_site :
                w_d = os.path.join(globvars.base_loc,globvars.base_lin_config_loc)
            try:
                if os.path.exists(w_d):
                    if os.path.isdir(w_d):
                        filetrgt = open(os.path.join(w_d,list(fnames[key]['host'].values())[0]),'w')


        #get the label and all of it from default and put it to file

                    if os.path.exists(os.path.join(w_d,'default-labels')) and os.path.isfile(os.path.join(w_d,'default')):
                        filesrc = open(os.path.join(w_d,'default-labels')).readlines()
                        labels_ids = [i for i in range(len(filesrc)) if  'LABEL' in filesrc[i] and not '#LABEL' in filesrc[i]]

                    if os.path.exists(os.path.join(w_d,'grub.cfg')) and os.path.isfile(os.path.join(w_d,'grub')):
                        filesrc = open(os.path.join(w_d,'grub.cfg')).readlines()
                        labels_ids = [i for i in range(len(filesrc)) if  'LABEL' in filesrc[i] and not '#LABEL' in filesrc[i]]

                    for line in filesrc:
                        if "LABEL" in line:
                            if not line.startswith("#"):
                                if _os == line.split()[-1]:
                                    curr_index = labels_ids[labels_ids.index(filesrc.index(line))]
                                    try:
                                        next_index = labels_ids[labels_ids.index(filesrc.index(line)) +1]
                                    except IndexError:
                                        next_index = -1
                                    body = filesrc[curr_index:next_index]

                                    msg = "MENU TITLE The Automatically PXE Installation System Menu"
                                    default = "DEFAULT %s" % _os
                                    if "win" in _os.lower():

                                        res = "\n%s\n%s\n\n\t%s\nAPPEND iso\nprompt 1\ntimeout 50\n" % (msg,default,"".join(body))
                                    else:
                                        if args.clean == False:
                                            cut = [ x for x in body if 'append' in x.lower() ]
                                            cut[0] = cut[0].replace('\n', ' department=%s user_notifier=%s osi_string %s\n' % (args.department, args.user_notifier, args.string))
                                            body[2] = cut[0]
                                            res = "\n%s\n%s\n\n\t%s\nIPAPPEND 2\nprompt 1\ntimeout 50\n" % (msg,default,"".join(body))
                                        else:
                                            cut = [ x for x in body if 'append' in x.lower() ]
                                            cut[0] = cut[0].replace('\n', ' clean\n')
                                            body[2] = cut[0]
                                            res = "\n%s\n%s\n\n\t%s\nIPAPPEND 2\nprompt 1\ntimeout 50\n" % (msg,default,"".join(body))

                    if res == None:
                        raise Exception("%s not found in pxe config file , please check the name" % _os)
                    #print "res",res
                    filetrgt.write(res)



                    try:
                        pid = os.fork()

                        if pid == 0:
                            os.setsid()
                            prog = "%s" % (os.path.join(w_w_d,"wait.sh"))
                            a = os.path.join(w_d,list(fnames[key]['host'].values())[0])
                            print("Creating MAC file at:",a)
                            string = ["-x",prog,a, "1200"]
                            os.execlp("bash",*string)

                    except Exception as e:
                        print("failed to remove the mac file")
                        sys.exit(2)


            except Exception as e:
                print(traceback.print_exc())
                print("error is: ",e)
                sys.exit(2)

            ipmireset(fnames[key]['ilo']['ip'],args)


def conf_build_grub(_os,fnames,args):
    import modules.presets as globvars
    import re
    w_w_d = '/auto/GLIT/SCRIPTS/AUTOINSTALL/Multihost/'
    #print _os,fnames
    if 'aarch64' in _os:
        w_d_file_loc = os.path.join(globvars.base_loc,globvars.base_lin_grub_config_loc_arm)
    else:
        w_d_file_loc = os.path.join(globvars.base_loc,globvars.base_lin_grub_config_loc)
    w_d = os.path.join(globvars.base_loc,globvars.base_lin_grub_config_loc)
    #print globvars.base_lin_grub_config_loc
    #print w_d
    #print _os
    #print fnames
    if os.path.exists(w_d) and os.path.isdir(w_d):
        for key in fnames:
            file_name = globvars.grub_labels_file+'-'+list(fnames[key]['host'].values())[0]
            filetrgt = open(os.path.join(w_d_file_loc,file_name),'w')
            #print os.path.join(w_d,file_name)
            if os.path.exists(os.path.join(w_d,globvars.grub_labels_file)):
                file_list = open(os.path.join(w_d,globvars.grub_labels_file))
                clean = [n for n in file_list.readlines() if not n.startswith('#')]
                filestr = ''.join(clean)
                #Amir solution:
                    #data = open('/auto/GLIT/PXE/tftpboot/boot/grub/grub.cfg').read()
                    #match = re.search(r'^menuentry "%s".*?\}' %_os,data, re.MULTILINE | re.DOTALL)
                    #print match.group(0)
                regex = re.compile(r'^(?=.*"%s")[^{]+{[^}]+}' % _os, re.MULTILINE | re.VERBOSE)
                res = re.findall(regex,filestr)
                if res == None or not res:
                    raise Exception("%s not found in pxe config file , please check the name" % _os)
                string_add_on =' department=%s user_notifier=%s osi_string %s\n' % (args.department, args.user_notifier, args.string)
                string = res[0].splitlines(res[0].count('\n'))
                for index,line in enumerate(string):
                    #print line
                    if line.strip().startswith('linux'):
                        new_line = line.strip('\n')+string_add_on
                        string[index] = new_line
                res=string
                #print ''.join(res)

                filetrgt.write("set default=0\n")
                filetrgt.write("set timeout=3\n")
                filetrgt.write(''.join(res))
                filetrgt.close()

            try:
                pid = os.fork()
                if pid == 0:
                    os.setsid()
                    prog = "%s" % (os.path.join(w_w_d,"wait.sh"))
                    a = os.path.join(w_d_file_loc,file_name)
                    print("Creating MAC file at:",a)
                    string = ["-x",prog,a, "1200"]
                    os.execlp("bash",*string)
            except Exception as e:
                print("failed to remove the mac file")
                sys.exit(2)
            #print fnames[key]
            #print fnames[key]['host'].iterkeys().next()
            ipmireset(fnames[key]['ilo']['ip'],args)
