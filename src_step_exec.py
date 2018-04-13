#coding=utf-8

import os
import subprocess 
#import shlex 
import sys
import time
import re
import argparse

teemo_outputdir = "/root/tools/teemo/output/"
teemo_base_dir = "/root/tools/teemo/"
teemo_base_cmd = "python "+ teemo_base_dir +"/teemo.py -d %s"

title_base_dir = "/root/tools/crack/title_get/"
title_outputdir = title_base_dir + "output_txt/"
title_base_cmd = "python "+ title_base_dir +"title.py -i " + teemo_outputdir + "%s*.txt -o %s"

bbscan_base_dir = "/root/tools/BBScan/"
bbscan_outputdir = bbscan_base_dir+"report/"
bbscan_base_cmd = "python " + bbscan_base_dir +"BBScan.py -f " + title_outputdir + "%s*.txt"


#def pid_monitor():
    #轮询进程

def keyword_monitor(keyword):
    print "[+]Running command %s..." % (keyword)
    p1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', keyword], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=p2.stdout, stdout=subprocess.PIPE)

    lines = p3.stdout.readlines()
    if len(lines) > 0:
        #return
        return False
    sys.stderr.write('Process[%s] is done.\n' % (keyword))
    return True
    #subprocess.call(cmd, shell=True)


#def cmd_exec(command):
    #args = shlex.split(command) 
    #p = subprocess.Popen(args) 
    #return p.pid

def cmd_exec(command):
    try:
        p = subprocess.Popen(command, shell=True)
        #需要后台运行，不知道这个用不用加nohup
        #nohuo获取一个进程的pid，如果派生出多个pid，原生的会一直存在么。

    except Exception,e:
        #print e
        return False
    
    while(1):
        time.sleep(10)
        value = keyword_monitor(command)
        if value:
            return

def step_exec(domain):
    try:
        resp_teemo = cmd_exec(teemo_base_cmd % (domain))
        os.chdir('title_get/')
        resp_title = cmd_exec(title_base_cmd %(domain , domain))
        os.chdir('../')
        resp_bbscan = cmd_exec(bbscan_base_cmd % (domain))
    except Exception,e:
        print e
    
    
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='[+]src_step_exec script v1.0')
    #parser.add_argument('-o', '--output_name',  type=str,  required=True ,   help="Output name for this scan")
    #parser.add_argument('-i', '--input_rule',  type=str , required=True,  help="Input command rules file for this scan, %s prepared")
    parser.add_argument('-d' , '--domain',  type=str,  default="",  help='the domain prepared for this scan')
    parser.add_argument('-df' , '--domain_file',  type=str, default="",  help='the domain file prepared for this scan')
    args = parser.parse_args()
    if args.domain_file:
        for domain_line in open(args.domain_file ,'r').readlines():
            step_exec(domain_line.strip())
            #for rule_line in open(args.input_rule ,'r').readlines():
                #command = rule_line.strip() % (domain_line.strip())
                #resp = cmd_exec(command)
    elif args.domain:
        #for rule_line in open(args.input_rule ,'r').readlines():
        #    command = rule_line.strip() % (args.domain)
        step_exec(args.domain)
        #resp = cmd_exec(command)
    else:
        print "[+]Try to input the domain or the domain file you wanna to scan."


