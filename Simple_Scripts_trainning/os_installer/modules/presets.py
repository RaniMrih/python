import os,platform
"""
    stuff which should be common both to dmz and regular site
"""
sites_conf = '/auto/GLIT/CONF/CORE/sites.ini'
base_loc = '/auto'
base_win_config_loc = 'GLIT/autoinstall/osList'
base_lin_config_loc = 'GLIT/PXE/tftpboot/pxelinux.cfg'
base_lin_grub_config_loc = 'GLIT/PXE/tftpboot/boot/grub'
base_lin_grub_config_loc_arm = 'GLIT/PXE/tftpboot/boot'



win_labels_file = "Images.xml"
linux_labels_file = 'default-labels'
grub_labels_file = 'grub.cfg'
freebsd_struct = 'PXE/tftpboot/FreeBSD'

"""
    path to glit in case of dmz and we are here
"""

base_loc_dmz = '/.autodirect/.lits'
dir_prefix = 'GLIT'

"""
    list url in dmz
"""
list_url = 'http://webrepo/list-export/list'
