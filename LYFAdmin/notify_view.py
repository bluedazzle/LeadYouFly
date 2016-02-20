# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from LYFAdmin.message import ORDER_BUY_MES, create_new_message

from LYFAdmin.models import Order, PayInfo, CashRecord, MoneyRecord
from LYFAdmin.online_pay import check_notify_id
from LYFAdmin.order_operation import create_charge_record, create_money_record
from LYFAdmin.sms import send_order_msg, send_confirm_msg
from LYFAdmin.utils import check_start_time

import xmltodict
import datetime
from LYFAdmin.wechat_pay import dict_to_xml


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
                    if order.order_type == 1:
                        order.status = 1
                        start_time = check_start_time(order.teach_by)
                        order.teach_start_time = start_time
                        order.teach_end_time = start_time + datetime.timedelta(hours=1.5)
                        order.if_pay = True
                        order.save()
                        create_charge_record(order.belong, price, order_id=order_id)
                        send_order_msg(str(order.order_id).encode('utf-8'),
                                       str(order.belong.phone).encode('utf-8'),
                                       str(order.belong.qq).encode('utf-8'),
                                       str(order.teach_by.phone).encode('utf-8'))
                        order.teach_by.iden_income += order.mentor_money
                        order.teach_by.total_income += order.mentor_money
                        order.teach_by.commission += order.platform_money
                        order.teach_by.save()
                        send_confirm_msg(str(order.belong.phone), str(order.teach_by.phone))
                        order_mes = ORDER_BUY_MES % order.belong.nick
                        create_new_message(order_mes, belong=order.belong)
                    else:
                        order.status = 2
                        order.teach_start_time = order.class_info.class_time
                        order.if_pay = True
                        order.save()
                        order.class_info.get_apply_number()
                        create_charge_record(order.belong, price, order_id=order_id)
                        order_mes = ORDER_BUY_MES % order.belong.nick
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
        f_detail = req.POST.get('fail_details', '')
        cash_rec = CashRecord.objects.get(record_id=c_id)
        if s_detail and s_detail != '':
            if cash_rec.success is not True:
                cash_rec.success = True
                cash_rec.info = s_detail
                cash_rec.save()
                mentor = cash_rec.belong
                mentor.iden_income -= float(cash_rec.money)
                mentor.save()
                create_money_record(mentor, u'支出',
                                    -float(cash_rec.money),
                                    '提款到支付宝%s' % str(cash_rec.alipay_account).encode('utf-8'))
        elif f_detail != '':
            if cash_rec.success is not True:
                cash_rec.success = False
                cash_rec.info = f_detail
                cash_rec.save()
                # mentor = cash_rec.belong
                # mentor.iden_income -= float(cash_rec.money)
                # mentor.cash_income += float(cash_rec.money)
                # mentor.save()
        return HttpResponse('success')
    else:
        return HttpResponse('fail')


@csrf_exempt
def wechat_notify(req):
    body = {}
    data = xmltodict.parse(req.body)['xml']
    return_code = data['return_code']
    if return_code == 'SUCCESS':
        result_code = data['result_code']
        if result_code == 'SUCCESS':
            order_no = data['out_trade_no']
            price = float(data['total_fee']) / 100
            order_list = Order.objects.filter(order_id=order_no)
            if not order_list.exists():
                body['return_code'] = 'FAIL'
                body['return_msg'] = 'order {0} is not exist'.format(order_no)
                return HttpResponse(dict_to_xml(body), content_type='application/xml')
            order = order_list[0]
            if order.status == 6:
                if order.order_type == 1:
                    order.status = 1
                    start_time = check_start_time(order.teach_by)
                    order.teach_start_time = start_time
                    order.teach_end_time = start_time + datetime.timedelta(hours=1.5)
                    order.if_pay = True
                    order.save()
                    create_charge_record(order.belong, price, order_id=order_no)
                    send_order_msg(str(order.order_id).encode('utf-8'),
                                   str(order.belong.phone).encode('utf-8'),
                                   str(order.belong.qq).encode('utf-8'),
                                   str(order.teach_by.phone).encode('utf-8'))
                    order.teach_by.iden_income += order.mentor_money
                    order.teach_by.total_income += order.mentor_money
                    order.teach_by.commission += order.platform_money
                    order.teach_by.save()
                    send_confirm_msg(str(order.belong.phone), str(order.teach_by.phone))
                    order_mes = ORDER_BUY_MES % order.belong.nick
                    create_new_message(order_mes, belong=order.belong)
                else:
                    order.status = 2
                    order.teach_start_time = order.class_info.class_time
                    order.if_pay = True
                    order.save()
                    order.class_info.get_apply_number()
                    create_charge_record(order.belong, price, order_id=order_no)
                    order_mes = ORDER_BUY_MES % order.belong.nick
                    create_new_message(order_mes, belong=order.belong)
        body['return_code'] = 'SUCCESS'
        body['return_msg'] = 'OK'
        return HttpResponse(dict_to_xml(body), content_type='application/xml')
