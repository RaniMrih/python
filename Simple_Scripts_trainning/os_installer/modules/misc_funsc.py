from builtins import range
import os
import sys
import re
import socket
from modules.winlabels import xml_parse
from modules.prechecks import check_path
import modules.presets
import fileinput
import linecache
from netaddr import IPNetwork,IPAddress

def parse_hosts(filepath):
    hosts = []
    f_src = open(filepath,'r').readlines()
    for i in f_src:
        i = i.strip("\n").strip('\r')
        if len(i) > 0:
            hosts.append(i)
    return hosts

def ini_parse(parse_file):
    res_dct = {}
    sect_list = []
    for l in fileinput.input(parse_file):
        if l.startswith('[') and l.endswith(']\n'):
            sect_list.append(fileinput.lineno() )
        last_line = fileinput.lineno()
    fileinput.close()


    for sect in sect_list:
        try:
            for l in range(sect,sect_list[sect_list.index(sect)+1]):

                line = linecache.getline(parse_file,l)
                if line.startswith('['):
                    sitename = line.strip(']\n').strip('[')
                    res_dct[sitename] = {}
                elif line != '\n':
                    k = line.split('=')[0].strip(' ')
                    v = line.split('=')[1]
                    if 'lab_nets' in k:
                        v = [ x.strip('\n') for x in v.split() ]
                        res_dct[sitename][k] = v
                    elif 'lab_pxe' in k:
                        v = [ x.strip('\n') for x in v.split() ]
                        res_dct[sitename][k] = v
                    elif 'lab_wds' in k:
                        v = [ x.strip('\n') for x in v.split() ]
                        res_dct[sitename][k] = v
                    else:
                        pass

        except IndexError:
            for l in range(sect,last_line):
                line = linecache.getline(parse_file,l)
                if line.startswith('['):
                    sitename = line.strip(']\n').strip('[')
                    res_dct[sitename] = {}
                elif line != '\n':
                    k = line.split('=')[0].strip(' ')
                    v = line.split('=')[1]
                    if 'lab_nets' in k:
                        v = [ x.strip('\n') for x in v.split() ]
                        res_dct[sitename][k] = v
                    elif 'lab_pxe' in k:
                        v = [ x.strip('\n') for x in v.split() ]
                        res_dct[sitename][k] = v
                    elif 'lab_wds' in k:
                        v = [ x.strip('\n') for x in v.split() ]
                        res_dct[sitename][k] = v
                    else:
                        pass

    return res_dct


def get_site(_hostname,os,sitesdct = None):
#here add func to parse sites.ini /auto/GLIT/CONF/CORE/sites.ini
    f_file = modules.presets.sites_conf
    sites_dct = ini_parse(f_file)
    host_ip = socket.gethostbyname(_hostname)
#    if '127.0.0' in host_ip:
    if '127.0.0' or '127.0.1' in host_ip:
        host_ip = ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])


    #print "kkk",host_ip
    #host_ip = ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    #print "bbb",host_ip
    for site in sites_dct:
        if 'lab_nets' in sites_dct[site]:
            for subn in sites_dct[site]['lab_nets']:
                if IPAddress(host_ip) in IPNetwork(subn):
                    if os == 'freebsd':
                        if site.lower() == 'wap':
                            return ['GLIT','MTL']
                        else:
                            return ['GLIT',site]
                    return 'GLIT'




def lin_labels(label_file,args):
    filesrc = open(label_file).readlines()
    lista= []
    listb= []
    if hasattr(args,'grub') and args.grub == True:
        #print args
        labels_ids = [i for i in range(len(filesrc)) if re.findall(r'\menuentry "(.+?)\"',filesrc[i]) and not "#" in filesrc[i] and not "localboot" in filesrc[i].lower()]
        labels = []
        for l in labels_ids:
            if 'aarch' in filesrc[l].split('"')[1].replace("\"", ""):
                listb.append(filesrc[l].split('"')[1].replace("\"", ""))
            else:
                lista.append(filesrc[l].split('"')[1].replace("\"", ""))
            #removed for better sorted arch printing
            #labels.append(filesrc[l].split('"')[1].replace("\"", ""))
        labels = list(sorted(lista)+sorted(listb))
        #labels = list(set(labels))
        #print labels

    else:
        labels_ids = [i for i in range(len(filesrc)) if  'LABEL' in filesrc[i] and not "#" in filesrc[i]]
        labels = []
        for l in labels_ids:
            if not "localboot" in filesrc[l].split()[-1].lower():
                labels.append(filesrc[l].split()[-1])

        labels = list(set(labels))
    return labels

def fbsdlabels(label_dir):
    freebsd_labels = []
    dir_lst = os.listdir(label_dir)
    for item in dir_lst:
        f_name = os.path.join(label_dir,item)
        if not os.path.islink(f_name) and os.path.exists(f_name):
            if 'pxeboot' in f_name:
                if  item.startswith('ai'):
                    pref = item.split('-')[0]
                    therest = ".".join(item.split('.')[2:-1])
                    entry = pref.upper()+'-' + therest
                    freebsd_labels.append(entry)
                else:
                    therest = ".".join(item.split('.')[2:-1])
                    freebsd_labels.append(therest)

    labels=list(set(freebsd_labels))
    return sorted(labels)

def build_labels(_os,args,label_file = None,site= None):

    if _os == 'linux':
        return lin_labels(label_file,args)

    if _os == 'win':
        return xml_parse(label_file)

    if _os == 'freebsd':
        if label_file == None:
            ip_addr = ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
            if args.site is not None:
                freebsdsite = ['GLIT',args.site]
                w_d = os.path.join(
                    modules.presets.base_loc,
                    freebsdsite[0],
                    modules.presets.freebsd_struct,
                    freebsdsite[1]
                )
            else:
                freebsdsite = get_site(ip_addr,'freebsd')
                w_d = os.path.join(
                    modules.presets.base_loc,
                    freebsdsite[0],
                    modules.presets.freebsd_struct,
                    freebsdsite[1]
                )
        else:
            w_d = label_file
            sites = ini_parse(modules.presets.sites_conf)
            for k in sites:
                if k.lower() == site.lower():
                    site_r = k
            freebsdsite = ['GLIT',site_r]
        if check_path(w_d):
            return fbsdlabels(w_d),freebsdsite


def siterelated(site = None,args = None ):
    try:
        if "127.0.0" in socket.gethostbyname(socket.gethostname()) or "127.0.1" in socket.gethostbyname(socket.gethostname()):
            ip_add=([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())\
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        else:
            ip_add=socket.gethostbyname(socket.gethostname())
            #print ip_add
        host_site = get_site(ip_add,'freebsd')[1]

        if 'dmz' in host_site.lower() or 'e2e' in host_site.lower():
            site = None
        if 'wap' in host_site.lower():
            site = 'MTL'
        if site == None:
            if hasattr(args,'grub') and args.grub==True:
                path_to_lin_labels = os.path.join(modules.presets.base_loc,modules.presets.base_lin_grub_config_loc,modules.presets.grub_labels_file)
                path_to_win_labels = os.path.join(modules.presets.base_loc,modules.presets.base_win_config_loc,modules.presets.win_labels_file)
            else:
                path_to_lin_labels = os.path.join(modules.presets.base_loc,modules.presets.base_lin_config_loc,modules.presets.linux_labels_file)
                path_to_win_labels = os.path.join(modules.presets.base_loc,modules.presets.base_win_config_loc,modules.presets.win_labels_file)
            return path_to_lin_labels,path_to_win_labels,None
    except Exception:
        sys.exit("Error in site/host resolving, please check DNS on running machine, or contact LABIT")

    sites = ini_parse(modules.presets.sites_conf)
    for k in sites:
        if k.lower() in site.lower():
            #print "lll",site,k,modules.presets.base_loc_dmz
            path_to_lin_labels = os.path.join(modules.presets.base_loc_dmz,k+modules.presets.base_lin_config_loc,modules.presets.linux_labels_file)
            path_to_win_labels = os.path.join(modules.presets.base_loc_dmz,k+modules.presets.base_win_config_loc,modules.presets.win_labels_file)
            path_to_freebsd_labels =  os.path.join(modules.presets.base_loc_dmz,k+modules.presets.dir_prefix,modules.presets.freebsd_struct,site)
            #print "kkkk", path_to_freebsd_labels
            return  path_to_lin_labels,path_to_win_labels,path_to_freebsd_labels
