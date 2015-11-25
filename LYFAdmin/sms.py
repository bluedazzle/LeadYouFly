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
    if str(rescode) == '0':
        return True
    else:
        return False


def send_order_msg(order_id, phone, qq, send_phone):
    order_str = '''您有新的订单，请飞一样的前去处理吧！订单号%s，学员手机号%s，QQ号%s
    快快联系学员，教得他飞起来吧！Enjoy it~''' % (order_id, phone, qq)
    req_url = 'http://222.73.117.158:80/msg/HttpBatchSendSM?' \
              'account=%(account)s&pswd=%(password)s&mobile=%(phone)s&msg=' \
              '%(content)s&needstatus=true' % {'account': SMS_ACCOUNT,
                                               'password': SMS_PASSWD,
                                               'phone': send_phone,
                                               'content': order_str}
    result = requests.get(req_url)
    print result.content
    rescode = str(result.content)[0:16].split(',')[1]
    if str(rescode) == '0':
        return True
    else:
        return False


def send_confirm_msg(phone, mentor_phone):
    o_str = '''亲爱的学员，您的订单已通知给教练了！请小等一会儿，教练稍后就会联系您！教练联系电话：{0}
您也可以在【个人中心-我的订单】中查询教练联系方式。
飞吧，好好玩游戏！'''.format(mentor_phone)
    req_url = 'http://222.73.117.158:80/msg/HttpBatchSendSM?' \
              'account=%(account)s&pswd=%(password)s&mobile=%(phone)s&msg=' \
              '%(content)s&needstatus=true' % {'account': SMS_ACCOUNT,
                                               'password': SMS_PASSWD,
                                               'phone': phone,
                                               'content': o_str}
    result = requests.get(req_url)
    rescode = str(result.content)[0:16].split(',')[1]
    print result.content
    if str(rescode) == '0':
        return True
    else:
        return False

