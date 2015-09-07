# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from LYFAdmin.message import ORDER_BUY_MES, create_new_message

from LYFAdmin.models import Order, PayInfo, CashRecord, MoneyRecord
from LYFAdmin.online_pay import check_notify_id
from LYFAdmin.order_operation import create_charge_record, create_money_record
from LYFAdmin.sms import send_order_msg
from LYFAdmin.utils import check_start_time


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
                if order.status == 6:
                    order.status = 1
                    order.teach_start_time = check_start_time(order.teach_by)
                    order.if_pay = True
                    order.save()
                create_charge_record(order.belong, price, order_id=order_id)
                send_order_msg(str(order.order_id).encode('utf-8'),
                               str(order.belong.phone).encode('utf-8'),
                               str(order.belong.qq).encode('utf-8'),
                               str(order.teach_by.phone).encode('utf-8'))
                order.teach_by.iden_income += order.order_price
                order.teach_by.save()
                order_mes = ORDER_BUY_MES % str(order.belong.nick).encode('utf-8')
                create_new_message(order_mes, belong=order.belong)
            elif status == 'TRADE_FINISHED':
                order.status = 3
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
            cash_rec = CashRecord.objects.get(record_id=c_id)
            cash_rec.success = True
            cash_rec.save()
            mentor = cash_rec.belong
            mentor.iden_income -= float(cash_rec.money)
            mentor.save()
            create_money_record(mentor, u'支出',
                                -float(cash_rec.money),
                                '提款到支付宝%s' % str(cash_rec.alipay_account).encode('utf-8'))
        return HttpResponse('success')
    else:
        return HttpResponse('fail')
