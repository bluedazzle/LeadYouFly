# -*- coding: utf-8 -*-
import requests

SMS_ACCOUNT = 'jiang-01'
SMS_PASSWD = 'Txb123456'

def send_msg(phone, verify):
    req_url = 'http://222.73.117.158:80/msg/HttpBatchSendSM?' \
              'account=%(account)s&pswd=%(password)s&mobile=%(phone)s&msg' \
              '=您的验证码是：%(verify)s&needstatus=true' % {'account': SMS_ACCOUNT, 'password': SMS_PASSWD, 'phone': phone, 'verify': verify}
    result = requests.get(req_url)
    rescode = str(result.content)[0:16].split(',')[1]
    print rescode
    if str(rescode) == '0':
        return True
    else:
        return False
