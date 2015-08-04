#-*- coding: utf-8 -*-
#origin author = 'newbie'
#recoding author = 'demon'
import re
import sys,getopt
import Queue
import threading
import urllib2
import time
from bs4 import BeautifulSoup
import socket
#socket.setdefaulttimeout(2)
import linecache
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#####################
global r
proxy_file = ""
threads = 5
output = "result.txt"
source_url = ""

'''Default settings'''
#####################

def usage():
    print'''This program made by newbie008@wooyun.org and recoding by demon version 2.0 

Usage:python main.py [-u|-o|-p|-d|-t]

-u:url single url eg:'https://www.baidu.com'
-o:output eg:'123.txt'
-p:proxy  eg:'ip_list.txt'
-d:dictionary file_ext:txt  eg 'asp:aspx:php'
-t:threads  eg:'5'
-s source_url file,multi urls,not be with -u eg:'source.txt'

eg:
python path_bruter.py -u http://www.bstaint.net -d x:c -t 8 -o result.txt
python path_bruter.py -s url.txt -d x -t 10 -o result.txt


'''
#admin=['-admin','2013','adminer','_admin','2012','_2012''2008','_system','_sys_admin']
resp_code = [200,302,403,500]
'''You can choose the resp_code you need here.'''
error_flag = [u'页面不存在',u'页面没找到','404']
dir=[]

def proxy(ip_file,host):
    ''' eg: http 192.168.1.1 1010 '''
    ip = open(ip_file,'r')
    count = len(open(ip_file,'rU').readlines())
    random_num=random.randrange(1,count, 1)
    line = linecache.getline(ip_file,random_num).strip()
    #for line in ip.readlines():
    #line = line.strip()
    proxyConfig = line.split(' ')[1]+':'+line.split(' ')[2]
    protocol = line.split(' ')[0]
    try:
        #proxy_resp = urllib.urlopen(host, proxies={protocol.lower():proxyConfig}).read()
        opener = urllib2.build_opener(urllib2.ProxyHandler({protocol:proxyConfig}))
        #urllib2.install_opener(opener)
        return opener
    except Exception,e:
        print '[!]Error: '+str(e)
        proxy(ip_file,host)

queue = Queue.Queue()
class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):        
        pass

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue,proxy_file):
        threading.Thread.__init__(self)
        self.queue = queue
        self.proxy_file = proxy_file
        #self.exception=exception
    def run(self):
        while True:
            #grabs host from queue
            try:
                host = self.queue.get()
                if host == "":
                    return None
            except Exception,e:
                print e
            #grabs urls of hosts and look 200 is ok?          
            try:
                if self.proxy_file != "":
                    opener = proxy(self.proxy_file,host)
                else:
                    opener = urllib2.build_opener(RedirectHandler)
            except Exception,e:
                print "[x]opener error:"+str(e)
            try:
                #opener = urllib2.build_opener(RedirectHandler)
                response=opener.open(host+'/')
                #:Wprint response
                for flag in error_flag:
                    if flag in response.read():
                        print 'Diy 404 Error..'
                        respcode = "404"
                        break
                    else:
                        #print "?a??"
                        respcode= response.getcode()
                result =  '[+]%s  %s'%(respcode,host)
                #print response.getcode()
                if response.getcode() in resp_code:
                    r.writelines(result+'\n')

            except urllib2.HTTPError, e:
                print '[+]%s  %s'%(e.code,host)
                result = '[+]%s  %s'%(e.code,host)
                if e.code in resp_code:
                    r.writelines(result+'\n')

            except urllib2.URLError,e:
                print '[+]%s  can not visit'%host
                #result = '[+]%s \t can not visit'%host
            #print "test end..."+host.strip()
            self.queue.task_done()
start = time.time()
#def main():
###################################################

if __name__ == '__main__':
    if len (sys.argv) < 2:
        usage()
        sys.exit(1)
    else:
        try:
            opts,args = getopt.getopt(sys.argv[1:], "hu:o:d:p:t:s:");
            for opt,arg in opts:
                if opt =="-h":
                    usage();
                    sys.exit(1);
                elif opt == "-u":
                    target=arg
                    #target_url=re.match(r'\w+:\/\/\w+\.(.*?)\.\w+',arg).group(1)                    
                elif opt == "-o":
                    output=arg
                    #FileScan(file)
                elif opt == "-d":
                    dic_path = arg
                elif opt == "-p":
                    proxy_file = arg
                elif opt == "-t":
                    threads = int(arg)
                elif opt == "-s":
                    source_url = arg
        except:
            usage()
            sys.exit(1)
    ###################################################
        dic = []
        if ":" in dic_path:
            #for item in dic_path.split('|'):
                #dic.append(item)
            try:
                for item in dic_path.split(':'):
                    f = open(item+'.dic')
                    for line in f.readlines():
                        #print line.strip()
                        dic.append(line.strip())

            except Exception,e:
                print e
                #return None
            print '[+]Dic has been added...'
        elif ":" not in dic_path and dic_path != "":
            f = open(dic_path+'.dic')
            for line in f.readlines():
               # print line.strip()
                dic.append(line.strip())
        else:
            print "[x]Dic path error!"
            exit(0)
    ###################################################

    ###################################################
    #spawn a pool of threads, and pass them queue instance
    r = open(output,'w+')
    #if proxy_file == "":
    print 'Scan starting...'
    for i in range(threads):
        t = ThreadUrl(queue,proxy_file)
        t.setDaemon(True)
        t.start()
        #put the hosts to queue
    for line in dic:
        #hosts=target+'/'+line+'/'
        if source_url != "":
            for target_url in open(source_url,'r'):
                target = target_url.strip()
                hosts=target+'/'+line
                queue.put(hosts)

        else:
            hosts=target+'/'+line
            #print hosts+'......'
            queue.put(hosts)
    queue.join()
    r.close()
    print "Elapsed Time: %s" % (time.time() - start)
