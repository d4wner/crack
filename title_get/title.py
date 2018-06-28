#!/usr/bin/env python
#coding=utf-8

import requests
requests.packages.urllib3.disable_warnings()
import re
import sys
#from Threads import ThreadPool
""" from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool """
import threadpool
#import socket
#socket.setdefaulttimeout(5)
import chardet
import time
import datetime
import argparse
from IPy import IP
import io

headers = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
 }



def view(url):
    try:
        r = requests.get(url,  headers= headers ,timeout = 5 ,verify = False)
        if keyword_filter:
            str_type = chardet.detect(keyword_filter)['encoding'].lower()
            if str_type == 'utf-8':
                keyword_filter_new = keyword_filter.decode('utf-8')
            else:
                keyword_filter_new = unicode(keyword_filter,'gbk')
            if re.search(keyword_filter_new, r.text):
                print '[x]Found filter keyword!'
                return
        status = r.status_code
        try:
            title = re.search(r"<title>(.*)</title>", r.text).group()[7:-8].encode('gbk')
        except:
            title = re.search(r"<title>(.*)</title>", r.content).group()[7:-8]
        try:
            server = r.headers['Server']
        except:
            server = ''
        if status == 200:
            o.writelines(u'<tr><th><a href="'+url+'" target="_blank">'+url+'</a> </th><th>'+title+'</th><th>'+server+'</th><th>'+str(status)+'</th></tr>')
        oo.writelines(url+'\n')
    except Exception,e:
        pass
        #print e

if __name__ == '__main__':

    t = time.time()
    timing = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d-%H-%M-%S')

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='[+]Title_get script v2.0')
    parser.add_argument('-ot', '--output_txt',  type=str,  default="output_txt/",   help="Directory for scan url dir")
    parser.add_argument('-oh', '--output_html',  type=str,  default="output_html/",   help="Directory for scan url dir")
    parser.add_argument('-o', '--output_name',  type=str,  default=timing,   help="Output name for this scan")
    parser.add_argument('-i', '--input_file',  type=str , default='', help="Input file for this scan")
    parser.add_argument('-t' , '--thread',  type=int,  default=10,  help='Threads for this bitch script')
    parser.add_argument('-k' , '--keyword_filter',  type=str,  default='',  help='the keyword you do not want to see in the page')
    parser.add_argument('-n' , '--network',  type=str,  default='',  help='192.168.1.1/24')

    #args = parser.parse_args(['--version'])
    args = parser.parse_args()
    print '[+]Input filename:%s'%(args.input_file)
    print '[+]Output filename:%s'%(args.output_name)

    oo = io.open(args.output_txt + args.output_name  +'.txt', 'a+', encoding='utf-8')
    o = io.open(args.output_html + args.output_name +'.html', 'a+', encoding='utf-8')
    thread_count = args.thread

    o.writelines(u'''
    <head>
    <meta charset="utf-8"/>
    <title>Title探测</title>
    </head>

    <!-- Row Highlight Javascript -->
    <script>
    window.onload=function(){
    var tfrow = document.getElementById('tfhover').rows.length;
    var tbRow=[];
    for (var i=1;i<tfrow;i++) {
    tbRow[i]=document.getElementById('tfhover').rows[i];
    tbRow[i].onmouseover = function(){
    this.style.backgroundColor = '#ffffff';
    };
    tbRow[i].onmouseout = function() {
    this.style.backgroundColor = '#d4e3e5';
    };
    }
    };
    </script>
    <style type="text/css">
    table.tftable {font-size:12px;color:#333333;width:100%;border-width: 1px;border-color: #729ea5;border-collapse: collapse;}
    table.tftable th {font-size:12px;border-width: 1px;padding: 8px;border-style: solid;border-color: #729ea5;text-align:left;}
    table.tftable tr {background-color:#d4e3e5;}
    table.tftable td {font-size:12px;border-width: 1px;padding: 8px;border-style: solid;border-color: #729ea5;}
    </style>
    <table id="tfhover" class="tftable" border="1">
    <tr><th>URL地址</th><th>标题</th><th>容器</th><th>返回码</th></tr>
    ''')


    #tp = ThreadPool(int(thread_count))
    global keyword_filter
    keyword_filter = ""
    if args.keyword_filter:
        keyword_filter = args.keyword_filter

    #pool = Pool(int(thread_count))
    pool = threadpool.ThreadPool(int(thread_count))


    #lines = open(input_file,'r').readlines()
    urls = []
    if args.input_file:
        for line in open(args.input_file ,'r').readlines():
            url =  line.strip().replace('\t',' ').split(' ')[0]
            if '.' not in url:
                continue
            if '@' in url or re.search('\/\d+$', url):
                continue
            if 'http' not in url:
                url = 'http://'+ url
            urls.append(url)
    elif args.network:
        ips = IP(args.network) 
        for ip in ips:
            url = 'http://'+ str(ip)
            urls.append(url)
    else:
        print "[x]U haven't input now...."
        exit(0)
    #pool.map(view, urls)
    reqs = threadpool.makeRequests(view, urls)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

    o.writelines(u'</table>')
    o.close()
    oo.close()
    #view('https://www.baidu.com')

