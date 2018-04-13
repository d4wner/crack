#coding=utf-8
import os
import re
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import argparse
from subprocess import Popen,PIPE 

class hunter_plugin:

    def __init__(self, args):
        self.args = args

    def exploit(self):
        sub_domains = []
        pool = Pool(int(self.args.thread))

        for sub_domain in open(self.args.input_file, 'r').readlines():
            sub_domains.append(sub_domain)

        host_assets = pool.map(self.scaner, sub_domains)
      
        host_assets = [strs for strs in host_assets if strs not in [None]]
        host_assets = list(set(host_assets))
        output = open(self.args.output_name , 'w+')
        for item in host_assets:
            output.writelines(item+'\n')
        print host_assets



    #��ʼɨ��
    def scaner(self,sub_domain):
        result = self.cSgment(sub_domain)
        if not "networkbad" in result:
            print sub_domain  + result
            if not "cdn" in result:
                return result
        else:
            result2 = self.cSgment(sub_domain)
            if not "networkbad" in result2:
                print sub_domain +  result2
                if not "cdn" in result2:
                    return result2
                    #writeFile("result.txt", result2 + "\n")
            else:
                print sub_domain.strip() + ":(Unreachable or bad network...)"

        
    def cSgment(self,sub_domain):
        lookStr = self.nsLookUp(sub_domain)
        listIp = self.fetIp(lookStr)
        #print listIp
        if len(listIp)==0:
            return "networkbad"

        if self.checkCdn(listIp):
            strIp = ""
            for i in listIp:
                strIp = strIp + i + ","
            return strIp[:-1] + " (May have enabled cdn...)"

        return self.makeCSeg(listIp)
    #ʹ��nslookup������в�ѯ
    def nsLookUp(self, sub_domain):
        #cmd = 'nslookup %s 8.8.8.8' % sub_domain
        result = ""
        try:
            cmd = 'nslookup %s 8.8.8.8' % sub_domain
            handle = os.popen(cmd , 'r')
            result = handle.read()
            #handle = Popen(['nslookup',sub_domain,'8.8.8.8'], shell=True, stdin=PIPE, stdout=PIPE)
            #handle.wait()
            #result = handle.stdout.read()
        except Exception,e:
            pass
        return result

    
    #��ȡnslookup�����ѯ�Ľ�������ip
    def fetIp(self,result):
        ips = re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])', result)   
        ips = list(set(ips))
        for ip in ips:
            if ip in ['8.8.8.8','114.114.114.114','127.0.0.1']:
                ips.remove(ip)
            elif re.match(r'^10(\.([2][0-4]\d|[2][5][0-5]|[01]?\d?\d)){3}$|^172\.([1][6-9]|[2]\d|3[01])(\.([2][0-4]\d|[2][5][0-5]|[01]?\d?\d)){2}$|^192\.168(\.([2][0-4]\d|[2][5][0-5]|[01]?\d?\d)){2}$', ip):
                ips.remove(ip)
        return ips
        
    #����Ƿ�ʹ��cdn
    def checkCdn(self,ips):
        if len(ips)>1:
            return True
        return False
    
    #����c��
    def makeCSeg(self,ips):
        if not self.checkCdn(ips):
            ipStr = "".join(ips)
            end = ipStr.rfind(".") 
            #return ipStr[0:end+1] + "1-" + ipStr[0:end+1] + "254"
            return ipStr[0:end+1] + "1-254"








if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='[+]host_asset_single script v1.0')
    parser.add_argument('-i', '--input_file',  type=str , required=True,  help="Input file for this scan")
    parser.add_argument('-t' , '--thread',  type=int,  default=10,  help='Threads for this bitch script')
    parser.add_argument('-o', '--output_name',  type=str,  required=True ,   help="Output name for this scan")
    args = parser.parse_args()
    print '[+]Input doamin_file:%s'%(args.input_file)
    print '[+]Output ip_asset:%s'%(args.output_name)
    host_asseter = hunter_plugin(args)
    results = host_asseter.exploit()

