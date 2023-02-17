from builtins import str
import subprocess as sub
import shlex
import sys
import os

def prereq():
    try:
        ipmi = sub.Popen(shlex.split('ipmitool -h'),stderr = sub.PIPE, stdout = sub.PIPE)
        stdout,stderr = ipmi.communicate()
        ipmi.wait()
        if ipmi.returncode != 0:
            msg = 'check if ipmitool installed, returncode of ipmitool -h is : %s' % ipmi.returncode
            raise Exception(msg)
    except OSError:
        msg = 'check if ipmitool installed , failed to find it on the path'
        raise Exception(msg)

    try:
        #Fixing issue of Python 3 lacks of support in MySQLdb
        #ref https://stackoverflow.com/questions/4960048/how-can-i-connect-to-mysql-in-python-3-on-windows
        try:
            import MySQLdb
        except ImportError:
            try:
                import pymysql
                pymysql.install_as_MySQLdb()
                import MySQLdb
            except ImportError as e:
                s = str(e)
                if "mysql" in s.lower():
                    msg = "please install pymysql via 'pip install pymysql'"
                raise Exception(msg)

        import argparse
        import simplejson as json
        import netaddr
    except ImportError as e :
        s = str(e)
        if "mysql" in s.lower():
            msg = "please install MySQL-python"
        if "argparse" in s.lower():
            msg = "please install python-setuptools and than run: \neasy_install argparse OR pip install argparse\n"
        if "simplejson" in s.lower():
            msg = "please install python-setuptools and than run: \neasy_install simplejson OR install from packages - usually python-simplejson\n"
        if "netaddr" in s.lower():
            msg = "please install python-setuptools and than run: \neasy_install netaddr OR pip install netaddr\n"


        raise Exception(msg)



def check_path(base_loc):
    if not os.path.exists(base_loc):
        msg = "\nERROR: Please fix nfs mounts , cant find relevant pathes : %s \n" % base_loc
        raise Exception(msg)



    if len(os.listdir(base_loc)) == 0:
        msg = "\nERROR: Please fix nfs mounts, looks stall as %s is empty\n" % base_loc
        raise Exception(msg)


    return True

def check_user(automation):
    if (os.getuid() == 0) and (automation == False):
        msg = "ERROR: This script should be run by regular user\n"
        raise Exception(msg)
