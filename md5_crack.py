# -*- coding=utf-8 -*-
import sys
import socket
import urllib
import re
import string
import urllib2
import threading
import HTMLParser
import cookielib

def showInfo():
    print """
     命令格式：md5_crack.py -hash md5hash \n
			or md5_crack.py -dic
           """

    #print "trying www.cmd5.com    ====>"
    #try:
    #	if crack_md5(HASH):
    #		return True
    #except:
    #	pass


#From http://md5cracker.org/
#list_of_result=[]   #存放结果
#thread_pool=[]   
comcn_tmp=[]

#global f,s

class timer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, HASH):  
        threading.Thread.__init__(self)  
        self.HASH = HASH    
   
    def run(self):  
        try:
            if crack_md5asia(self.HASH):
                return True
        except Exception,e:
            print e
            pass
        
        try:
            if crack_cc(self.HASH):
                return True
        except Exception,e:
            print e
            pass
        
        try:
            if crack_silic(self.HASH):
                return True
        except Exception,e:
            print e
            pass
        
        try:
            if crack_comcn(self.HASH):
                return True
        except Exception,e:
            print e
            pass

        try:
            if crack_somd5(self.HASH):
                return True
        except Exception,e:
            print e
            pass
        
        print "[x]HASH Crack: "+self.HASH+" failed."
        f.writelines(HASH+'\n')
        return False 
              


class Parselinks(HTMLParser.HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag == 'input':
            for name,value in attrs:
                if name == 'name':
                    if value != 'sand':
                        continue
                    else:
                        count=0
                        for name,value in attrs:
                            count=count+1
                            if count == 3: 
                                comcn_tmp.append(value)

        if tag == 'input':
            for name,value in attrs:
                if name == 'name':
                    if value != 'token':
                        continue
                    else:
                        count=0
                        for name,value in attrs:
                            count=count+1
                            if count == 3: 
                                comcn_tmp.append(value)


#From http://www.md5.asia/
def crack_md5asia(Hash):   
    str_url=["http://md5ss.sinaapp.com/md5_decode.php?decoder=5&timeout=10&hash=",Hash]
    url="".join(str_url)
    #print url
            
    try:
        sock=urllib.urlopen(url)
        htmlSources=sock.read()
    except:
        #print "Not Found"
        return False
    else:
        sock.close()
    #本来这个地方，应该比较"未找到,"，但是由于编码的问题，会出问题。因此，改为16进制了。
    if string.find(htmlSources,"\346\234\252\346")!=-1:
        return False
        #print "Not Found2"
    else:
        print "Password Found:",htmlSources
        s.writelines(HASH+' '+resp+'\n')
        print 'asia:',resp
        return True
        #exit(1)


def crack_comcn(HASH):

    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    parsed = Parselinks()
    parsed.feed(urllib.urlopen('http://www.md5.com.cn').read())
    post_data = {'md': HASH ,'sand':comcn_tmp[0],'token':comcn_tmp[1],'submit':'MD5+Crack'}
    post_data_urlencode = urllib.urlencode(post_data)
    requrl = "http://www.md5.com.cn/md5reverse"
    req = urllib2.Request(url = requrl,data =post_data_urlencode)
    req.add_header('Referer', "http://www.md5.com.cn/")
    resps = urllib2.urlopen(req)
    match = re.findall('Result:.*green">.*<\/span',resps.read())
    re_match=re.findall('green">.*<\/span><div',match[0])[0][7:-11]
    #print re_match[0][7:-11]
    s.writelines(HASH+' '+re_match+'\n')
    print 'comcn:',re_match
    return True



def crack_silic(HASH):
    post_data = {'isajax':'1' ,'md5':HASH}
    post_data_urlencode = urllib.urlencode(post_data)
    requrl = "http://cracker.blackbap.org/?do=search&language=en"
    req = urllib2.Request(url = requrl,data =post_data_urlencode)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    #print res
    resp = re.findall('Password <strong>.*<\/strong>',res)[0][17:-9]
    #print resp
    s.writelines(HASH+' '+resp+'\n')
    print 'silic:',resp
    return True

def crack_cc(HASH):
    url='http://www.md5.cc/ShowMD5Info.asp?GetType=ShowInfo&no-cache=0.4669540437658686&md5_str='+HASH+'&_='
    request = urllib2.Request(url)
    request.add_header('Referer', "http://www.md5.cc/")
    res=urllib2.urlopen(request).read()
    resp = re.findall('25px">.*<\/span>',res)[0][6:-7].strip()
    #print resp[6:-7].strip()
    s.writelines(HASH+' '+resp+'\n')
    print "cc:",resp
    return True

def crack_somd5(HASH):

    resp=urllib.urlopen('http://www.somd5.com/somd5-md5-js.html').read()
    ajax_data=re.findall('isajax=.*&',resp)[0][7:-1]
    post_data = {'isajax':ajax_data,'md5':HASH}
    post_data_urlencode = urllib.urlencode(post_data)
    requrl = "http://www.somd5.com/somd5-index-md5.html"
    req = urllib2.Request(url = requrl,data =post_data_urlencode)
    resps = urllib2.urlopen(req).read()
    match = re.findall('<h1.*line;">.*<\/h1',resps)[0]
    re_match = re.findall('">.*</',match)[0][2:-2]
    s.writelines(HASH+' '+resp+'\n')
    print "somd5",resp
    return True


if '__main__' == __name__:         

    print """
     =~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~=
     +-----------DemonSpider-----------+
     +--------Md5-Cracker--V1.0--------+
     +----------www.dawner.info--------+
     +--md5_crack.py for single or dic-+
     ===================================
                    = =
                   == ==
                ===<-|->===
                 ====D====
                  ===e===
                   ==m==
                    =o=
                     n
    """
    global f,s

    if len(sys.argv)<2 :
         print "参数错误"
         showInfo()
         exit(1)
     
    cmds = ['-hash','-dic']
    #print sys.argv[1]+'=='
    #print sys.argv[2]+'=='
    #print len(sys.argv)
     
    s=open('success_result.txt','w+')
    f=open('fail_result.txt','w+')
    cmd = sys.argv[1]
    if len(sys.argv) == 3 :
        Hash=sys.argv[2]
         
    if 0 == cmds.count(cmd):  
        print cmd
        print "参数错误"
        showInfo()
        exit(1)
    else:
        print 'Start working,Please waiting...'
        if cmd == '-hash':
            if len(Hash)==16 or len(Hash)==32:
                crack_thread = timer(Hash)
                crack_thread.start()
                #crack_thread.setDamon()
                crack_thread.join()
            else:
                print "Hash长度出错."
        elif cmd == 'dic':
            for line in open('hash.txt','r'):
                if len(line.strip())==16 or len(line.strip())==32:
                    crack_thread = timer(line.strip())
                    crack_thread.start()
                    #crack(line.strip())
                else:
                    continue
    s.close()
    f.close()
    print "Crack ending...."


        
            #f.writelines()








