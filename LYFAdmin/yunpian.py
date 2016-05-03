# -*-coding:utf-8-*-

# author: jacky
# Time: 15-12-15
# Desc: 短信http接口的python代码调用示例
# https://www.yunpian.com/api/demo.html
# https访问，需要安装  openssl-devel库。apt-get install openssl-devel

from __future__ import unicode_literals

import httplib
import urllib
import json

API_KEY = '43d849d573a5617ae3cb31980160a513'

# 服务地址
sms_host = "sms.yunpian.com"
voice_host = "voice.yunpian.com"
# 端口号
port = 443
# 版本号
version = "v2"
# 查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
# 智能匹配模板短信接口的URI
sms_send_uri = "/" + version + "/sms/single_send.json"
# 模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_single_send.json"
# 语音短信接口的URI
sms_voice_send_uri = "/" + version + "/voice/send.json"


# 语音验证码

def get_user_info(apikey=API_KEY):
    """
    取账户信息
    """
    conn = httplib.HTTPSConnection(sms_host, port=port)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn.request('POST', user_get_uri, urllib.urlencode({'apikey': apikey}))
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_sms(phone, verify, apikey=API_KEY):
    """
    通用接口发短信
    """
    text = '【飞吧游戏教练】您的验证码是{0}'.format(verify).encode('utf-8')
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile': phone})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    json_res = json.loads(response_str)
    if json_res.get('code') == 0:
        return True
    return False


def send_order_msg(order_id, phone, qq, send_phone, apikey=API_KEY):
    text = '【飞吧游戏教练】您有新的订单，请飞一样的前去处理吧！订单号%s，学员手机号%s，QQ号%s快快联系学员，教得他飞起来吧！Enjoy it~'.format(order_id, phone, qq).encode('utf-8')
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile': send_phone})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    json_res = json.loads(response_str)
    if json_res.get('code') == 0:
        return True
    return False


def send_confirm_msg(phone, mentor_phone, apikey=API_KEY):
    text = '【飞吧游戏教练】亲爱的学员，您的订单已通知给教练了！请小等一会儿，教练稍后就会联系您！教练联系电话：{0}您也可以在 个人中心-我的订单 中查询教练联系方式。飞吧，好好玩游戏！'.format(mentor_phone).encode('utf-8')
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile': phone})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    json_res = json.loads(response_str)
    print json_res
    if json_res.get('code') == 0:
        return True
    return False
