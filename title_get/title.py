#!/usr/bin/env python
#coding=utf-8

import requests
import re
import sys
#from Threads import ThreadPool
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
#import socket
#socket.setdefaulttimeout(5)

headers = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
 }



def view(url):
    try:
        r = requests.get(url,  headers= headers ,timeout = 5 ,verify = False)
        status = r.status_code
        title = re.search(r"<title>(.*)</title>", r.content).group()[7:-8]
        if status == 200:
            o.writelines('<tr><th><a href="'+url+'" target="_blank">'+url+'</a> </th><th>'+title+'</th><th>'+str(status)+'</th></tr>')
        oo.writelines(url+'\n')
    except Exception,e:
        print e
        pass

global output_file
input_file = raw_input("Url filename:")
output_file = raw_input("Save filename:")
thread_count = raw_input("Thread num:")


oo = open(output_file+'.txt', 'a+')
o = open(output_file+'.html', 'a+')

o.writelines('''
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
<tr><th>URL地址</th><th>标题</th><th>返回码</th></tr>
''')


#tp = ThreadPool(int(thread_count))

pool = Pool(int(thread_count))

#lines = open(input_file,'r').readlines()
urls = []
for line in open(input_file ,'r').readlines():
    url =  line.strip().replace('\t',' ').split(' ')[0]
    if '.' not in url:
        continue
    print url
    if '@' in url or re.search('\/\d+$', url):
        continue
    if 'http' not in url:
        url = 'http://'+ url
    urls.append(url)
pool.map(view, urls)

o.writelines('</table>')
o.close()
oo.close()
#view('https://www.baidu.com')

