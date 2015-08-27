from alipay import Alipay

ALIPAY_PID = ''
ALIPAY_KEY = ''
ALIPAY_EML = ''



def create_alipay_order(order_id, subject, fee):
    alipay = Alipay(pid=ALIPAY_PID, key=ALIPAY_KEY, seller_email=ALIPAY_EML)
    order_url = alipay.create_direct_pay_by_user_url(out_trade_no=order_id,
                                     subject=subject,
                                     total_fee=fee,
                                     return_url='your_order_return_url',
                                     notify_url='your_order_notify_url')
    return order_url