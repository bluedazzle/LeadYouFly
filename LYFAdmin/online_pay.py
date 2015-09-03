from alipay import Alipay

ALIPAY_PID = '2088021077647325'
ALIPAY_KEY = 'f6nhdtxet02q0swn216rtoq0m9m9xnie'
ALIPAY_EML = '765566978@qq.com'

HOST = 'http://www.fibar.cn/'

RETURN_URL = '%suser/my_orders' % HOST

NOTIFY_URL = '%salipay_notify/' % HOST

def create_alipay_order(order_id, subject, fee):
    alipay = Alipay(pid=ALIPAY_PID, key=ALIPAY_KEY, seller_email=ALIPAY_EML)
    order_url = alipay.create_direct_pay_by_user_url(out_trade_no=order_id,
                                     subject=subject,
                                     total_fee=fee,
                                     return_url=RETURN_URL,
                                     notify_url=NOTIFY_URL)
    return order_url
