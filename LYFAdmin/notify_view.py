from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LYFAdmin.models import Order, PayInfo


@csrf_exempt
def alipay_notify(req):
    order_id = req.POST.get('out_trade_no')
    price = req.POST.get('total_fee')
    buyer_email = req.POST.get('buyer_email')
    alipay_id = req.POST.get('trade_no')
    status = req.POST.get('trade_status')
    if status == 'TRADE_SUCCESS' or status == 'TRADE_FINISHED':
        order_list = Order.objects.filter(order_id=order_id)
        if order_list.exists():
            order = order_list[0]
            new_pay_info = PayInfo(order=order,
                                   pay_id=alipay_id,
                                   buyer_email=buyer_email,
                                   status_info=status,
                                   price=float(price))
            new_pay_info.save()
            if status == 'TRADE_SUCCESS':
                order.status = 1
            elif status == 'TRADE_FINISHED':
                order.status = 3
            order.if_pay = True
            order.save()
            return HttpResponse('success')
        else:
            return HttpResponse('no exist')
    else:
        return HttpResponse('success')