#!/usr/bin/env python
#coding=utf-8

import urllib2
import urllib
import socket
from bs4 import BeautifulSoup
socket.setdefaulttimeout(2)

ipfile = open('ip_list.txt','w+')
resp = urllib.urlopen('http://www.xici.net.co/nt/1').read()
soup = BeautifulSoup(resp)
odds = soup.find_all('tr',attrs = {'class':'odd'})
for item in odds:
    item = item.find_all('td')
    ip = item[2].text
    port= item[3].text
    protocol = item[6].text
    #print ip,port,protocol
    proxyConfig = ip+':'+str(port)
    try:
        speed_test = urllib.urlopen('http://www.baidu.com', proxies={protocol.lower():proxyConfig}).read()
        print '[+]ip:'+proxyConfig
        ipfile.writelines(protocol.lower()+' '+ip+' '+port+'\n')
    except Exception,e:
        print e
        continue
ipfile.close()



