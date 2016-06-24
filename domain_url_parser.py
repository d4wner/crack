#!/usr/bin/env python
#coding=utf-8

import sys
import re
import requests
import threading
import Queue


class D(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while  True:
            url = self.queue.get()
            self.exec_request(url)
            self.queue.task_done()

    def exec_request(self, url):
        try:
            status = requests.get(url,timeout=3).status_code
            if status in [200,301,302,403,404,500]:
                print url+" "+str(status)
                r.writelines(url+"\n")
        except Exception,e:
            print "[x]"+url+": "+str(e)




if __name__ == "__main__":
    
    filename = sys.argv[1]

    global r,urls
    urls = []
    r = open('url_covert.txt',"w+")

    with open(filename,"r") as f:
        for line in f.readlines():
            hosts = []
            host = line.strip().split(' ')[0]
            hosts.append(host)
            match = re.search(r'\d+\.\d+\.\d+\d+\.\d+',line.strip())
            if match:
                ip = match.group()
                hosts.append(ip)
            for protocol in ['http://','https://']:
                for host_item in hosts:
                    url = protocol+host_item
                    urls.append(url)
    try:
        queue = Queue.Queue()
        for i in range(20):
            t = D(queue)
            t.setDaemon(True)
            t.start()
        for url in urls:
            queue.put(url)
        queue.join()
    except Exception,e:
        print e
    r.close()

