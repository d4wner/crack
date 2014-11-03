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
     命令格式：
     [mail_md5_crack.py -d]  or\n
     [mail_md5_crack.py -f filename]
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

def keywords_check():
    return True

def text_split(line):
    username=line.split('|')[0]
    col_hash=line.split('|')[1]
    server_name='mail.'+username.split('@')[1]
    line_result=username+'|'+col_hash+'|'+server_name
    return line_result

class timer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, line_result):  
        threading.Thread.__init__(self)  
        self.LINE = line_result
        self.HASH = line_result.split('|')[1]

    def run(self):  
        try:
            if crack_md5asia(self.HASH,self.LINE):
                return True
        except Exception,e:
            print "asia_error==>"
            print e
            pass
        
        try:
            if crack_comcn(self.HASH,self.LINE):
                return True
        except Exception,e:
            print "comcn_error==>"
            print e
            pass

        try:
            if crack_somd5(self.HASH,self.LINE):
                return True
        except Exception,e:
            print "somd5_error==>"
            print e
            pass
        
        try:
            if crack_cc(self.HASH,self.LINE):
                return True
        except Exception,e:
            print 'cc_error=>'
            print e
            pass
        print "[x]HASH Crack: "+self.HASH+" failed."
        s.writelines(self.LINE+'\n')
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
def crack_md5asia(HASH,LINE):   
    str_url=["http://md5ss.sinaapp.com/md5_decode.php?decoder=5&timeout=10&hash=",HASH]
    url="".join(str_url)
    try:
        sock=urllib.urlopen(url)
        resp=sock.read()
    except:
        print "asia not_found"
        return False
    else:
        sock.close()
        print "asia not_found"
    #本来这个地方，应该比较"未找到,"，但是由于编码的问题，会出问题。因此，改为16进制了。
    if string.find(resp,"\346\234\252\346")!=-1:
        return False
        #print "Not Found2"
    else:
        print "asia:"+resp
        s.writelines(LINE.split('|')[0]+'|'+resp+'|'+LINE.split('|')[2]+'\n')
        return True


def crack_comcn(HASH,LINE):

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
    #print resps.read()
    match = re.findall('green">.*<\/span',resps.read())
    re_match = match[1][7:-6]
    print 'comcn:',re_match
    s.writelines(LINE.split('|')[0]+'|'+re_match+'|'+LINE.split('|')[2]+'\n')
    return True



#def crack_silic(HASH,LINE):
#    post_data = {'isajax':'1' ,'md5':HASH}
#    post_data_urlencode = urllib.urlencode(post_data)
#    requrl = "http://cracker.blackbap.org/?do=search&language=en"
#    req = urllib2.Request(url = requrl,data =post_data_urlencode)
#    res_data = urllib2.urlopen(req)
#    res = res_data.read()
#    print res
#    resp = re.findall('Password <strong>.*<\/strong>',res)[0][17:-9]
#    print 'silic:',resp
#    s.writelines(LINE.split('|')[0]+'|'+resp+'|'+LINE.split('|')[2]+'\n')
#    return True

def crack_cc(HASH,LINE):
    url='http://www.md5.cc/ShowMD5Info.asp?GetType=ShowInfo&no-cache=0.4669540437658686&md5_str='+HASH+'&_='
    request = urllib2.Request(url)
    request.add_header('Referer', "http://www.md5.cc/")
    res=urllib2.urlopen(request,timeout=25).read()
    #print res
    resp = re.findall('25px">.*<\/span>',res)[0][6:-7].strip()
    #print resp[6:-7].strip()
    print "cc:",resp
    s.writelines(LINE.split('|')[0]+'|'+resp+'|'+LINE.split('|')[2]+'\n')
    return True

def crack_somd5(HASH,LINE):
    resp=urllib.urlopen('http://www.somd5.com/somd5-md5-js.html').read()
    ajax_data=re.findall('isajax=.*&',resp)[0][7:-1]
    post_data = {'isajax':ajax_data,'md5':HASH}
    post_data_urlencode = urllib.urlencode(post_data)
    requrl = "http://www.somd5.com/somd5-index-md5.html"
    req = urllib2.Request(url = requrl,data =post_data_urlencode)
    resps = urllib2.urlopen(req).read()
    match = re.findall('<h1.*line;">.*<\/h1',resps)[0]
    re_match = re.findall('">.*</',match)[0][2:-2]
    print "somd5",re_match
    s.writelines(LINE.split('|')[0]+'|'+re_match+'|'+LINE.split('|')[2]+'\n')
    return True


if '__main__' == __name__:         

    print """
     =~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~=
     +-----------DemonSpider-----------+
     +--------Md5-Cracker--V2.0--------+
     +----------www.dawner.info--------+
     +----mail_md5_crack.py for mail---+
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
    global s

    if len(sys.argv)<2 :
         print "参数错误"
         showInfo()
         exit(1)
     
    cmds = ['-dic']
     
    s=open('result_mail.txt','w+')
    cmd = sys.argv[1]
    if len(sys.argv) == 3 :
        diyname=sys.argv[2]
         
    if 0 == cmds.count(cmd) and cmd != '-d':  
        print cmd
        print "参数错误"
        showInfo()
        exit(1)
    else:
        print 'Start working,Please waiting...'
      
        if cmd == '-d':
            filename='hash.txt'
        elif cmd == '-f':
            filename=diyname
        else:
            showInfo()
            exit(0)
        for line in open(filename,'r'):
            line_result = text_split(line.strip())
            col_hash = line_result.split('|')[1]
            if len(col_hash)==16 or len(col_hash)==32:
                crack_thread = timer(line_result)
                crack_thread.start()
                crack_thread.join()
                #crack(line.strip())
            else:
                print "Hash长度出错."
                s.writelines(line_result+'\n')
                continue
    s.close()
    print "Crack ending...."


        
            #f.writelines()








