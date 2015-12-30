# -*- coding: utf-8 -*-
from LYFAdmin.models import Order, Student, Mentor, MoneyRecord, CashRecord, ChargeRecord


import time
import datetime
from django.utils.timezone import get_current_timezone
from LeadYouFly.settings import WEBSITE_SIGN



# def create_order_id(stu_id, men_id):
#     date_str = str(datetime.date.today()).replace('-', '')
#     year, month, day = str(datetime.date.today()).split('-')
#     auto_num = Order.objects.filter(create_time__year=year,
#                                     create_time__month=month,
#                                     create_time__day=day).count() + 1
#     new_id = '%s%06i%06i%06i' % (date_str, stu_id, men_id, auto_num)
#     return new_id


def create_order_id(stu_id=None, men_id=None):
    order_id = '%s%s%s' % (WEBSITE_SIGN, str(datetime.date.today()).replace('-', '')[2:], str(time.time()).replace('.', ''))
    return order_id


def create_class_id(stu_id=None, class_id=None):
    order_id = 'C%s%s%s' % (WEBSITE_SIGN, str(datetime.date.today()).replace('-', '')[2:], str(time.time()).replace('.', ''))
    return order_id


def create_charge_record(student, money, ctype=1, order_id=None):
    '''
        type: 1、订单支付 2、充值
        money: 金额
    '''
    if ctype == 1:
        note = '来自支付订单%s' % str(order_id)
    else:
        note = '充值'
    charge_id = 'C%s%s' % (str(datetime.date.today()).replace('-', ''), str(time.time()).replace('.', ''))
    new_record = ChargeRecord(record_id=charge_id,
                              charge_number=money,
                              note=note,
                              belong=student
                              )
    new_record.save()
    return new_record


def create_cash_request(mentor, money, alipay_account, name):
    record_id = '%sR%s%s' % (WEBSITE_SIGN, str(datetime.date.today()).replace('-', ''), str(time.time()).replace('.', ''))
    new_request = CashRecord(record_id=record_id,
                             money=money,
                             alipay_account=alipay_account,
                             real_name=name,
                             belong=mentor)
    new_request.save()
    return new_request


def create_money_record(mentor, action, money, info):
    record_id = 'M%s%s' % (str(datetime.date.today()).replace('-', ''), str(time.time()).replace('.', ''))
    new_rec = MoneyRecord(record_id=record_id,
                          action=action,
                          income=money,
                          info=info,
                          belong=mentor)
    new_rec.save()
    return new_rec


def create_order(student, mentor, course, learn_area, learn_type, learn_hero, teach_long):
    new_id = create_order_id(student.id, mentor.id)
    teach_long_time = datetime.timedelta(hours=teach_long)
    teach_end = datetime.datetime.now(tz=get_current_timezone()) + teach_long_time
    new_order = Order(order_id=new_id,
                      order_price=course.price,
                      course_name=course.name,
                      course_intro=course.course_info,
                      learn_area=learn_area,
                      learn_type=learn_type,
                      learn_hero=learn_hero,
                      teach_end_time=teach_end,
                      teach_long=teach_long,
                      belong=student,
                      teach_by=mentor
                      )
    new_order.save()
    return new_order
