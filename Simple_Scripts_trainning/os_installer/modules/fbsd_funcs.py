from __future__ import print_function
import os
import socket
import sys
from modules.gen_funcs import ipmireset

def conf_build_freebsd(_os,fnames,freebsdsite,args):
    from modules.misc_funsc import get_site
    import modules.presets as globvars
    w_w_d = '/auto/GLIT/SCRIPTS/AUTOINSTALL/Multihost/'
    msg = "MENU TITLE The Automatically PXE Installation System Menu\n"
    default = "DEFAULT FreeBSD_%s\n" % _os
    if 'ai' in _os.lower():
        pref = _os.split('-')[0].lower()+'-pxeboot'
        rest = _os.strip('AI-')+'.0'
        result = pref +'.'+freebsdsite[1] +'.'+ rest
    else:
        result = 'pxeboot.'+freebsdsite[1]+'.'+_os+'.0'

    string = "LABEL FreeBSD_%s\n\tkernel /FreeBSD/%s/%s\n" % (_os,freebsdsite[1],result)

    try:
        for key in fnames:
            site_details = get_site(list(fnames[key]['host'].keys())[0],'freebsd')
            host_site = get_site(socket.gethostbyname(socket.gethostname()),'freebsd')[1]

            if 'DMZ' in site_details[1] or 'E2E' in site_details[1]:
                w_d =  os.path.join(globvars.base_loc_dmz,site_details[-1]+globvars.base_lin_config_loc)
            if 'DMZ' in host_site:
                w_d = os.path.join(globvars.base_loc,globvars.base_lin_config_loc)
            else:
                w_d = os.path.join(globvars.base_loc,globvars.base_lin_config_loc)

            if os.path.exists(w_d):
                if os.path.isdir(w_d):
                    filetrgt = open(os.path.join(w_d,list(fnames[key]['host'].values())[0]),'w')
                    filetrgt.write(msg)
                    filetrgt.write(default)
                    filetrgt.write(string)
                    filetrgt.close()

                    try:
                        pid = os.fork()

                        if pid == 0:
                            os.setsid()
                            prog = "%s" % (os.path.join(w_w_d,"wait.sh"))
                            a = os.path.join(w_d,list(fnames[key]['host'].values())[0])
                            string = ["-x",prog,a, "300"]
                            os.execlp("bash",*string)

                    except Exception as e:

                        print("failed to remove the mac file")
                        sys.exit(2)
    except Exception as e:
        print(e)
        sys.exit(1)

    ipmireset(fnames[key]['ilo']['ip'],args)
