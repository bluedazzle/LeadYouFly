from alipay import Alipay

ALIPAY_PID = '1'
ALIPAY_KEY = '1'
ALIPAY_EML = '1'



def create_alipay_order(order_id, subject, fee):
    alipay = Alipay(pid=ALIPAY_PID, key=ALIPAY_KEY, seller_email=ALIPAY_EML)
    order_url = alipay.create_direct_pay_by_user_url(out_trade_no=order_id,
                                     subject=subject,
                                     total_fee=fee,
                                     return_url='http://www.fibar.cn/test',
                                     notify_url='http://www.fibar.cn/test')
    return order_url