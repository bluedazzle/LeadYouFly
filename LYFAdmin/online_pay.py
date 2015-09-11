# -*- coding: utf-8 -*-
from alipay import Alipay
import requests
from urllib import urlencode
from LeadYouFly.settings import HOST


ALIPAY_PID = '2088021077647325'
ALIPAY_KEY = 'f6nhdtxet02q0swn216rtoq0m9m9xnie'
ALIPAY_EML = '765566978@qq.com'


RETURN_URL = '%suser/my_orders' % HOST

NOTIFY_URL = '%salipay_notify/' % HOST

BATCH_NOTIFY_URL = '%sbatch_notify/' % HOST

def create_alipay_order(order_id, subject, fee):
    alipay = Alipay(pid=ALIPAY_PID, key=ALIPAY_KEY, seller_email=ALIPAY_EML)
    order_url = alipay.create_direct_pay_by_user_url(out_trade_no=order_id,
                                     subject=subject,
                                     total_fee=fee,
                                     return_url=RETURN_URL,
                                     notify_url=NOTIFY_URL)
    return order_url


def create_batch_trans(batch_list, account_name, batch_no):
    alipay = Alipay(pid=ALIPAY_PID, key=ALIPAY_KEY, seller_email=ALIPAY_EML)
    batch_url = alipay.create_batch_trans_notify_url(batch_list, account_name=account_name, batch_no=batch_no, notify_url=BATCH_NOTIFY_URL)
    return batch_url


def check_notify_id(notify_id):
    params = {'partner': ALIPAY_PID,
              'notify_id': notify_id,
              'service': 'notify_verify'}
    encode_dict_str = urlencode(params)
    req_url = 'https://mapi.alipay.com/gateway.do?%s' % encode_dict_str
    res = requests.get(req_url)
    return res.content
