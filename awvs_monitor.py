#coding=utf-8
import json
import requests
import datetime
import time
requests.packages.urllib3.disable_warnings()

def awvs_processing_monitor():
    headers = {
        'X-Auth' : '1986ad8c0a5b3df4d7028d5f3c06e936c8f1ac88af5b34a58a6dcef0bcc63972b',
        'content-type' : 'application/json'
            }
    try:
        json_scans_resp =  json.loads(requests.get('https://127.0.0.1:3443/api/v1/scans?q=status:processing', headers = headers, timeout=5, verify = False).content)
        for x in json_scans_resp.values()[1]:
            scan_id = x['scan_id']
            print '[+]Process scan_id %s' % (scan_id)
            json_scan_resp = json.loads(requests.get('https://127.0.0.1:3443/api/v1/scans/'+scan_id, headers = headers, timeout=5, verify = False).content)
            past = json_scan_resp['current_session']['start_date'].split('.')[0]
            start_date = datetime.datetime.strptime(past, "%Y-%m-%dT%H:%M:%S")
            now = datetime.datetime.now()
            now_time = now.strftime('%Y-%m-%d %H:%M:%S')
            now_date = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
            timespan = (now_date - start_date).total_seconds() //60 //60
            print timespan
            if timespan >= 2:
                status_code = requests.post('https://127.0.0.1:3443/api/v1/scans/'+scan_id + '/abort', headers = headers, timeout=5, verify = False).status_code
                if status_code == 204:
                    print 'Kill scan_id %s' % (scan_id)

    except Exception, e:
        print e

if __name__ == '__main__':
    while(1):
        awvs_processing_monitor()
        time.sleep(360)
        
        
        


