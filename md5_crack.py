# -*- coding=gbk -*-
import sys
import socket
import urllib
import re
import string
import urllib2
import threading

def showInfo():
    print """
     命令格式：MD5Crack.py -hash md5hash
           """
def MD5Crack(Hash):
    print "trying md5cracker.org    ====>"
    MD5Crack_md5cracker(Hash)
    print "trying www.md5.asia    ====>"
    MD5Crack_md5asia(Hash)
    print "trying www.xmd5.com    ====>"
    MD5Crack_xmd5(Hash)
   
#From http://md5cracker.org/
list_of_result=[]   #存放结果
thread_pool=[]   
def MD5Crack_md5cracker(Hash):
    if len(Hash)!=32:   #这个网站只支持32位的
        print "Not Found"
        return
    str_url=["http://md5cracker.org/hash.php?hash=","&id=","0"]
    str_url.insert(1,Hash)

    global g_mutex
    g_mutex=threading.Lock()    #初始化互斥量
   
    nrange=range(1,14)
    for i in nrange:
        str_url[3]=str(i)
        url="".join(str_url)
        #print url

        #开线程
        th=threading.Thread(target=md5crackerCommon,args=(i ,url))
        thread_pool.append(th)
        th.start()

    #阻塞主线程。collect all threads
    pos=1
    for pos in nrange:
        threading.Thread.join(thread_pool[pos-1])

    if len([result for result in list_of_result if result!="no"]):   #存在不是“no”的情况，说明找到
        print "Password Found:",[result for result in list_of_result if result!="no"][0]
        exit(1)
    else:
        print "Not Found"
   

def md5crackerCommon(t_id,url):   
    passPattern = re.compile(r'#--#([\d|\D]*)#--#')
    conststr="-www-md5cracker-org"
   
    try:
        sock=urllib.urlopen(url)
        htmlSources=sock.read()
    except:
        return
    else:       #如果没有urlopen成功，sock是不存在的。这里用个else正好!
        sock.close()

    result=passPattern.search(htmlSources).groups()[0]
    if len(result):         #返回结果为0，则代表没有超时
        if string.find(result,conststr)==-1:    #返回-1，代表不存在，即正确
            pass
        else:
            result="no"
    else:
        result="no"

    g_mutex.acquire()
    ######################受互斥量保护区代码##################################
    list_of_result.append(result)
    ########################################################################
    g_mutex.release()

#From http://www.md5.asia/
def MD5Crack_md5asia(Hash):   
    str_url=["http://www.md5.asia/md5_decode.php?decoder=1&timeout=10&hash=",Hash]
    url="".join(str_url)
    #print url
            
    try:
        sock=urllib.urlopen(url)
        htmlSources=sock.read()
    except:
        print "Not Found"
        return
    else:
        sock.close()
    #本来这个地方，应该比较"未找到,"，但是由于编码的问题，会出问题。因此，改为16进制了。
    if string.find(htmlSources,"\346\234\252\346")!=-1:
        print "Not Found"
    else:
        print "Password Found:",htmlSources
        exit(1)

#From www.xmd5.com
#由于需要使用Referer，需要使用urllib2。如果values不需要，则以None代替
def MD5Crack_xmd5(Hash):   
    str_url=["http://www.xmd5.com/md5/search.asp?hash=",Hash]
    url="".join(str_url)
    #print url
   
    #Referer: http://www.xmd5.com/md5/getpass.asp?info=admin
    #对于XMD5这个网站，必须要这一项，否则无法正常查询。不管hash是什么，都是这个固定的值！
    headers = { 'Referer' : 'http://www.xmd5.com/md5/getpass.asp?info=admin' }      
    req = urllib2.Request(url,None,headers)
    try:
        response = urllib2.urlopen(req)
        htmlSources = response.read()
    except:
        print "Not Found"
        return
    else:
        response.close()

    #使用正则表达式得到结果
    passPattern = re.compile(r'size="3">([\d|\D]*)&nbsp;&nbsp;>>>Good Luck !<<<')
    dic=passPattern.search(htmlSources)     #返回可能是空的，即表示没有破解成功
    if dic is None:
        print "Not Found"
    else:
        result=dic.groups()[0]  #查询结果
        print "Password Found:",result
        exit(1)

#    print htmlSources

if '__main__' == __name__:         
    if len(sys.argv)!=3 :
         print "参数错误"
         showInfo()
         exit(1)
     
    cmds = ['-hash']
     
    cmd = sys.argv[1]
    Hash=sys.argv[2]
         
    if 0 == cmds.count(cmd):  
        print cmd
        print "参数错误"
        showInfo()
        exit(1)
    else:
        #print 'Start working,Please waiting...'
        if cmd == '-hash':
            if len(Hash)==16 or len(Hash)==32:
                MD5Crack(Hash)                               
