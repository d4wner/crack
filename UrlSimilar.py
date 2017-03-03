#coding=utf-8
#author:404 not found
#site:http:www.95sec.com
import hashlib
import urlparse
import sys

hash_size=199999


def urlsimilar(url):
    tmp=urlparse.urlparse(url)
    #print tmp
    scheme=tmp[0]
    netloc=tmp[1]
    path=tmp[2][1:]
    query=tmp[4]
    #print path
    #First get tail
    #print path.split('/')
    if len(path.split('/'))>1:
        tail=path.split('/')[-1].split('.')[-1]
        #print tail
    elif len(path.split('/'))==1:
        tail=path
        #print tail
    else:
        tail='1'
     #Second get path_length
    path_length=len(path.split('/'))-1
    #Third get directy list except last
    path_list=path.split('/')[:-1]+[tail]
    #print path_list
    #Fourth hash
    path_value=0
    #print path_length
    for i in range(path_length+1):
        if path_length-i==0:
            path_value+=hash(path_list[path_length-i])%98765
            #print path_value
        else:
            #print i
            path_value+=len(path_list[path_length-i])*(10**(i+1))
            #print path_list[path_length-i],path_value
    #get host hash value
    netloc_value=hash(hashlib.new("md5",netloc).hexdigest())%hash_size
    #print type(netloc_value+path_value)
    url_value=hash(hashlib.new("md5",str(path_value+netloc_value)).hexdigest())%hash_size
    
    return url_value

if __name__=='__main__':
    #pass
    #url='http://auto.sohu.com/7/0903/70/column213227075.shtml'
    #first=urlsimilar(url)
    #url='http://auto.sohu.com/7/4354/34/column443243545.shtml'
    #second=urlsimilar(url)
    url1 = sys.argv[1]
    url2 = sys.argv[2]
    first=urlsimilar(url1)
    second=urlsimilar(url2)
    if first==second:
        print "URL similar"
    else:
        print  "URL not similar"
