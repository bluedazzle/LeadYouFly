# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LYFAdmin.models import Order, PayInfo, CashRecord, MoneyRecord
from LYFAdmin.online_pay import check_notify_id
from LYFAdmin.order_operation import create_charge_record, create_money_record


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
                create_charge_record(order.belong, price, order_id=order_id)
            elif status == 'TRADE_FINISHED':
                order.status = 3
            order.if_pay = True
            order.save()
            return HttpResponse('success')
        else:
            return HttpResponse('no exist')
    else:
        return HttpResponse('success')


@csrf_exempt
def alipay_batch_notify(req):
    check_id = req.POST.get('notify_id', None)
    res_code = check_notify_id(check_id)
    if res_code == 'true':
        c_id = req.POST.get('batch_no', None)
        s_detail = req.POST.get('success_details', None)
        if s_detail and s_detail != '':
            cash_rec = CashRecord.objects.get(id=c_id)
            cash_rec.success = True
            cash_rec.save()
            mentor = cash_rec.belong
            create_money_record(mentor, '支出',
                                cash_rec.money,
                                '提款到支付宝%s' % cash_rec.alipay_account)
        return HttpResponse('success')
    else:
        return HttpResponse('fail')
