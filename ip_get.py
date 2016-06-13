#!/usr/bin/env python
#coding=utf-8

import urllib2
import urllib
import socket
import requests
import socket
import re
from bs4 import BeautifulSoup
socket.setdefaulttimeout(2)
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
timeout=5 # in seconds 
socket.setdefaulttimeout(timeout)

global headers,ipfile


headers = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"
  }

def xici_proxy():
    resp = requests.get('http://www.xici.net.co/nt/1',headers = headers).content
    soup = BeautifulSoup(resp)
    odds = soup.find_all('tr',attrs = {'class':'odd'})
    for item in odds:
        item = item.find_all('td')
        ip = item[1].text
        port= item[2].text
        protocol = item[5].text
        #print ip,port,protocol
        proxyConfig = ip+':'+str(port)
        proxy_test(proxyConfig,protocol,ip,port)

def _66ip_proxy():
    resp = requests.get('http://www.66ip.cn/mo.php?sxb=&tqsl=50&port=&export=&ktip=&sxa=&textarea=',headers = headers).content
    proxyConfigs = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+",resp)
    for proxyConfig in  proxyConfigs:
        ip = proxyConfig.split(':')[0]
        port = proxyConfig.split(':')[1]
        for protocol in ['https','http']:
            proxy_test(proxyConfig,protocol,ip,port)

    #soup = BeautifulSoup(resp)
    #trs = soup.find_all('tr',attrs = {'class':'container'}
    #for tr in trs:
    #    td = tr.find_all('td')

def cz88_proxy():
    range_items = ["index.shtml"]+ ['http_%s.shtml' % n for n in range(2, 11)]
    for item in range_items:
        resp = requests.get('http://www.cz88.net/proxy/'+item,headers = headers).content
        soup = BeautifulSoup(resp)
        div = soup.find('div',attrs = {'class':'box694'})
        lis = div.find_all('li')
        for li in lis:
            ip = li.find('div',attrs = {'class':'ip'}).text
            port = li.find('div',attrs = {'class':'port'}).text
            proxyConfig = ip+":"+port
            proxy_test(proxyConfig,'https',ip,port)

def ip181_proxy():
    for item in range(1,11):
        resp = requests.get('http://www.ip181.com/daili/'+str(item)+".html",headers = headers).content
        soup = BeautifulSoup(resp)
        tbody = soup.find('tbody')
        trs = tbody.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            ip = tds[0].text
            port = tds[1].text
            protocol = tds[3].text.lower()
            proxyConfig = ip+":"+port
            if "," in protocol:
                for item in protocol.split(','):
                    proxy_test(proxyConfig,item,ip,port)
            else:
                proxy_test(proxyConfig,protocol,ip,port)


def ipcn_proxy():
    for item in ["","2"]:
        resp = requests.get('http://proxy.ipcn.org/proxylist'+item+".html",headers = headers).content
        proxyConfigs = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+",resp)
        for proxyConfig in  proxyConfigs:
            ip = proxyConfig.split(':')[0]
            port = proxyConfig.split(':')[1]
            for protocol in ['https','http']:
                proxy_test(proxyConfig,protocol,ip,port)


def proxy_test(proxyConfig,protocol,ip,port):
    try:
        if not re.search(r"\d+\.\d+\.\d+\.\d+",ip):
            print "[x]Proxy requests error."
            return
        speed_test = urllib.urlopen('http://www.baidu.com', proxies={protocol.lower():proxyConfig}).read()
        if "baidu" not in ''.join(speed_test):
            print "[x]Proxy requests error."
            return
        print '[+]ip:'+proxyConfig+" for "+protocol
        ipfile.writelines(protocol.lower()+' '+ip+' '+port+'\n')
    except Exception,e:
        print e
        return


if __name__ == "__main__":
    ipfile = open('ip_list.txt','w+')
    #_66ip_proxy()
    #xici_proxy()
    #cz88_proxy()
    #ip181_proxy()
    #ipcn_proxy()
    ipfile.close()
