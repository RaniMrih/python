from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import range
import os
import sys
import linecache
import fileinput
import simplejson as json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import getpass
import socket
from modules.gen_funcs import mac_get
#from modules.gen_funcs import ipmireset
from modules.gen_funcs import conf_build
from modules.winjson import json_build

def xml_parse(f_name):
    list_key = []
    res_dct = {}
    linenum = []
    try:
#    f_name = os.path.join(os.path.join(src_loc,f_n))
#    if os.path.exists(f_name):
        for line in fileinput.input(f_name):
            if '<image id' in line or '</image>' in line:
                linenum.append(fileinput.filelineno())



        for num in linenum:
            try:
                for i in range(num,linenum[linenum.index(num) + 1]):
                    text = linecache.getline(f_name,i)
                    if "image id" in text:
                        cur_key = text.split('=')[-1][1:-3]
                        list_key.append(cur_key)
                        if cur_key not in res_dct:
                            res_dct[cur_key]={}
                        else:
                            print(res_dct,'key found: ',cur_key)
                    if "<name>" in text and "path" in linecache.getline(f_name,i-1):
                        val = text.split()[0].lstrip("<name>") + " " + " ".join(text.split()[1:-1]) + " " + text.split()[-1].rstrip('</name>')
                        res_dct[cur_key]['name'] = val
                    if "<size>" in text:
                        val = text.split('size>')[1].rstrip('</')
                        res_dct[cur_key]['size'] = val
                    if text == "<modifiers>":
                        if 'modifiers' not in res_dct[cur_key]:
                            res_dct[cur_key]['modifiers']=[]
                        else:
                            print(res_dct,'key found: ',cur_key)
                    if "modifier id" in text:
                        if 'modifiers' not in res_dct[cur_key]:
                            res_dct[cur_key]['modifiers']=[]
                            res_dct[cur_key]['modifiers'].append(text.split("=")[-1][1:-3])
                        else:
                            res_dct[cur_key]['modifiers'].append(text.split("=")[-1][1:-3])


                    if text == "<customizations>":
                        if 'customizations' not in res_dct[cur_key]:
                            res_dct[cur_key]['customizations']=[]

                        else:
                            print(res_dct,'key found: ',cur_key)
                    if "customization id" in text:
                        if 'customizations' not in res_dct[cur_key]:
                            res_dct[cur_key]['customizations']=[]
                            res_dct[cur_key]['customizations'].append(text.split("=")[-1][1:-3])
                        else:
                            res_dct[cur_key]['customizations'].append(text.split("=")[-1][1:-3])


            except IndexError:
                for i in range(num,linenum[-1]):
                    text = linecache.getline(f_name,i)
                    if "image id" in text:
                        cur_key = text.split('=')[-1].strip('>')
                        if cur_key not in res_dct:
                            res_dct[cur_key]={}
                        else:
                            print(res_dct,'key found: ',cur_key)
                    if "<name>" in text and "path" in linecache.getline(f_name,i-1):
                        val = text.split()[0].lstrip("<name>") + " " + " ".join(text.split()[1:-1]) + " " + text.split()[-1].rstrip('</name>')
                        res_dct[cur_key]['name'] = val
                    if "<size>" in text:
                        val = text.split('size>')[1].rstrip('</')
                        res_dct[cur_key]['size'] = val
                    if text == "<modifiers>":
                        if 'modifiers' not in res_dct[cur_key]:
                            res_dct[cur_key]['modifiers']=[]
                        else:
                            print(res_dct,'key found: ',cur_key)
                    if "modifier id" in text:
                        if 'modifiers' not in res_dct[cur_key]:
                            res_dct[cur_key]['modifiers']=[]
                            res_dct[cur_key]['modifiers'].append(text.split("=")[-1][1:-3])
                        else:
                            res_dct[cur_key]['modifiers'].append(text.split("=")[-1][1:-3])


                    if text == "<customizations>":
                        if 'customizations' not in res_dct[cur_key]:
                            res_dct[cur_key]['customiaztions']=[]

                        else:
                            print(res_dct,'key found: ',cur_key)
                    if "customization id" in text:
                        if 'customizations' not in res_dct[cur_key]:
                            res_dct[cur_key]['customizations']=[]
                            res_dct[cur_key]['customizations'].append(text.split("=")[-1][1:-3])
                        else:
                            res_dct[cur_key]['customizations'].append(text.split("=")[-1][1:-3])


    except Exception as e:
        raise e

    return res_dct,list_key

def choices_print(res_dct,list_key):
    print("\n\nWindows Choices:\n")
    Labe = 30
    Siz  = 5
    Modifier = 30
    Customizatio = 45
    print('|{:^{}}|{:^{}}|{:^{}}|{:^{}}|'.format('Label',Labe,'Customization',Customizatio,'Modifiers',Modifier,'Size',Siz))
    print('-' * (Labe+Siz+Modifier+Customizatio+5))
    print('-' * (Labe+Siz+Modifier+Customizatio+5))
    #for i in list_key:
        #print i
    for k in list_key:
        try:
# cant use .format as need to work on python2.4.3 too ,ASS!!!
            #print "%8s %3s %35s %1s %7s %2s %1s %2s %1s%2s %1s%2s %-20s %2s%4s %1s %20s" % ( \
            #        k,":",res_dct[k]['name'],":", \
            #        "variants" ,"::","size",":", \
            #        res_dct[k]['size'],":","modifiers",":", \
            #        ",".join(res_dct[k]['modifiers']),":",'customisations',":",",".join(res_dct[k]['customizations']) \
            #        )
            if os.path.exists('/images'):
                print('|{:^{}}|{:^{}}|{:^{}}|{:^{}}|'.format(k,Labe,",".join(res_dct[k]['customizations']),Customizatio,'----',Modifier,'----',Siz))
            else:
                print('|{:^{}}|{:^{}}|{:^{}}|{:^{}}|'.format(k,Labe,",".join(res_dct[k]['customizations']),Customizatio,",".join(res_dct[k]['modifiers']),Modifier,res_dct[k]['size'],Siz))

        except KeyError:
            print('|{:^{}}|{:^{}}|{:^{}}|{:^{}}|'.format(k,Labe,'----',Customizatio,'----',Modifier,res_dct[k]['size'],Siz))





def check_restparams(args,label):
    if args.targetHost is None:
        msg = "Please supply host/s to install on\nfor reference '%s win -h'\n\nregards ItDevOps" % os.path.realpath(__file__)
        raise Exception(msg)
    if args.osname is None:
        msg = "Please supply image name and options\nfor reference '%s win -h'\n\nregards ItDevOps" % os.path.realpath(__file__)
        raise

    fnames = mac_get(args.targetHost,'win')

    if args.single or args.multi:
        for h in args.targetHost:
            json_param = build_config(args,label)
            if args.single is True:
                json_param1 = "".join(json_param)
                json_param1 = json_param1.replace("{","[{").replace("}","}]").replace(": ",":").replace(", ",",")
            if args.multi is True:
                json_param1 = "".join(json_param)
                json_param2 = json_param1[0].replace("{","[{")
                json_param3 = json_param1[-1].replace("}","}]")
                json_param1 = json_param1.replace("}{","},{").replace(": ",":").replace(", ",",")
                json_param1 = json_param2 + json_param1[1:-1] + json_param3
            #print json_param1
            #print json_param2
            #print json_param3


            machine_param = h
            ipmi_param = fnames[h]['ilo']['ip']
            if ipmi_param == 'virtual':
                #raise Exception('Virtual machines not implemented yet')
                print("Virtual")

            ipmi_user_param = args.ipmiuser
            ipmi_password_param = args.ipmipassword
            portal_user_param = getpass.getuser()
            data = urllib.parse.urlencode({"type":"linux","machine":machine_param,"user":ipmi_user_param,"ipmi":ipmi_param,"password":ipmi_password_param,"portal_user":portal_user_param,"json":json_param1})
            print("Data :", data)
            #print "json1 :",json_param1
            full_url = "http://%s/autoinstall/direct.php" % get_win_site(h)
            print(full_url)
            request = urllib.request.Request(full_url,data)
            response = urllib.request.urlopen(request)
            print(response.read())
            response.close()



    args.filepath=None
    args.os="WIN_Autodeploy"
    args.ipmiUsername = args.ipmiuser
    args.ipmiPassword = args.ipmipassword
    args.rreboot=False

    if args.automation == False:
        #warn = raw_input("\n\nBe aware: you going to install os on multiple hosts - this is unreversable.\nAre YOU SURE ?(y/n) :")
        warn = "y"
        if warn == "y":

            conf_build(args.os,mac_get(args.targetHost,"linux"),args)
        else:
            print("Bye!!")
            sys.exit()

    else:
        conf_build(args.os,mac_get(args.targetHost,"linux"),args)

def build_config(args,label):
    failed = []

    res_dct = label
    if args.multi:
        string = []
        arr = []
        for k in res_dct:
            if "safe" in k.lower():
                image = k
                string.append(json.dumps({"image":image,"size":res_dct[k]['size']}))

        #check if valid names in osname
        for image in args.osname:
            if check_image_inxml(res_dct,image):
                res = json_build(res_dct,image,string)

            else:
                print("Non existent entries: %s \n\nplease re enter\n\nregards ItDevOps" % image)
                sys.exit(2)
        return res

    if args.single:
        if len(args.osname) > 1 :
            print("In single mode - please insert only 1 image name\n\nRegards ItDevOps\n")
            sys.exit(2)
        else:
            string = []
            for image in args.osname:
                if check_image_inxml(res_dct,image) == True:
                    return json_build(res_dct,image,string)

                else:
                    print("Non existent entries: %s \n\nplease re enter\n\nregards ItDevOps" % image)
                    sys.exit(2)



def check_image_inxml(res_dct,image):
    for k in res_dct:
        if image.split(":")[0] == k:
            stat = True
            break
        else:
            stat = False

    return stat

def get_win_site(_hostname):
    from modules.misc_funsc import get_site,ini_parse
    import modules.presets
    resdct = ini_parse(modules.presets.sites_conf)
    host_site = get_site(socket.gethostbyname(socket.gethostname()),'freebsd')[1]
    url = resdct[host_site]['lab_wds'][0]
    return url
