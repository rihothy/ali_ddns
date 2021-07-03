from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient

import traceback
import requests
import time
import json
import re

def get_ip():
    res = requests.get('http://txt.go.sohu.com/ip/soip')

    return re.findall(r'\d+.\d+.\d+.\d+', res.text)[0]


def get_record(client, record_type, subdomain):
    request = DescribeSubDomainRecordsRequest()

    request.set_SubDomain(subdomain)
    request.set_accept_format('json')
    request.set_Type(record_type)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    response = json.loads(response)['DomainRecords']['Record'][0]

    return response['RecordId'], response['Value']


def update_record(client, record_type, record_id, ip):
    request = UpdateDomainRecordRequest()

    request.set_accept_format('json')
    request.set_RecordId(record_id)
    request.set_Type(record_type)
    request.set_Priority('5')
    request.set_TTL('600')
    request.set_Value(ip)
    request.set_RR('*')

    client.do_action_with_exception(request)


if __name__ == '__main__':
    try:
        new_ip = get_ip()
        client = AcsClient('xxx', 'xxx')
        record_id, old_ip = get_record(client, 'A', '*.honghim.com')

        if old_ip != new_ip:
            update_record(client, 'A', record_id, new_ip)

            with open('/home/pi/Documents/tools/ddns/log.txt', 'a') as log:
                tic = time.asctime(time.localtime(time.time()))
                log.write('{}:\nThe new ip is {}.\n'.format(tic, new_ip))
    except:
        with open('/home/pi/Documents/tools/ddns/log.txt', 'a') as log:
            tic = time.asctime(time.localtime(time.time()))
            log.write('{}:\n{}\n'.format(tic, traceback.format_exc()))