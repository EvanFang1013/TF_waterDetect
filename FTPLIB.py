# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:30:15 2020

@author: 00047393
"""

from ftplib import FTP


def ftpsend(filename):
    #domain name or server ip:
    ftp = FTP('F12AENS')
    ftp.login(user='ens_ftp', passwd = 'ftpens')
    ftp.cwd('ENS_FILE/dat')
    with open(filename,'rb') as f:
        bufsize = 1024
        ftp.storbinary('STOR '+filename, f)
        ftp.quit()
    


