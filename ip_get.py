#!/usr/bin/env python
#coding=utf-8

import urllib2
import urllib
import socket
import requests
import socket
import re
import threading
from bs4 import BeautifulSoup
socket.setdefaulttimeout(2)
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
timeout=3 # in seconds 
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
        t = proxy_test(proxyConfig,protocol,ip,port)
        t.start()
        t.join()

def _66ip_proxy():
    resp = requests.get('http://www.66ip.cn/mo.php?sxb=&tqsl=50&port=&export=&ktip=&sxa=&textarea=',headers = headers).content
    proxyConfigs = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+",resp)
    for proxyConfig in  proxyConfigs:
        ip = proxyConfig.split(':')[0]
        port = proxyConfig.split(':')[1]
        for protocol in ['https','http']:
            t = proxy_test(proxyConfig,protocol,ip,port)
            t.start()
            t.join()


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
            t = proxy_test(proxyConfig,'https',ip,port)
            t.start()
            t.join()

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
                    t = proxy_test(proxyConfig,protocol,ip,port)
                    t.start()
                    t.join()
            else:
                t = proxy_test(proxyConfig,protocol,ip,port)
                t.start()
                t.join()


def ipcn_proxy():
    for item in ["","2"]:
        resp = requests.get('http://proxy.ipcn.org/proxylist'+item+".html",headers = headers).content
        proxyConfigs = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+",resp)
        for proxyConfig in  proxyConfigs:
            ip = proxyConfig.split(':')[0]
            port = proxyConfig.split(':')[1]
            for protocol in ['https','http']:
                t = proxy_test(proxyConfig,protocol,ip,port)
                t.start()
                t.join()


#国外的代理
def ljf_proxy():
    proxy_urls = [
            #OPENSSL需要高版本
            #"https://www.us-proxy.org/",
            "http://free-proxy-list.net/uk-proxy.html",
            "http://www.sslproxies.org/"
            ]
    for proxy_url in proxy_urls:
        resp = requests.get(proxy_url ,headers = headers).content
        soup = BeautifulSoup(resp)
        tbody = soup.find('tbody')
        trs = tbody.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            ip = tds[0].text
            port = tds[1].text
            protocol = tds[3].text.lower()
            proxyConfig = ip+":"+port
            for protocol in ['https','http']:
                t = proxy_test(proxyConfig,protocol,ip,port)
                t.start()
                t.join()


class proxy_test(threading.Thread):
    def __init__(self, proxyConfig,protocol,ip,port):  
        threading.Thread.__init__(self)  
        self.proxyConfig = proxyConfig
        self.protocol = protocol
        self.ip = ip
        self.port = port
   
    def run(self):
        try:
            if not re.search(r"\d+\.\d+\.\d+\.\d+",self.ip):
                print "[x]Proxy requests error."
                return
            speed_test = urllib.urlopen('http://www.baidu.com', proxies={self.protocol.lower():self.proxyConfig}).read()
            if "baidu" not in ''.join(speed_test):
                print "[x]Proxy requests error."
                return
            print '[+]ip:'+self.proxyConfig+" for "+self.protocol
            ipfile.writelines(self.protocol.lower()+' '+self.ip+' '+self.port+'\n')
        except Exception,e:
            print e
        return




if __name__ == "__main__":
    ipfile = open('ip_list.txt','w+')
    #_66ip_proxy()
    #xici_proxy()
    #cz88_proxy()
    #ip181_proxy()
    ipcn_proxy()
    #ljf_proxy()
    ipfile.close()
