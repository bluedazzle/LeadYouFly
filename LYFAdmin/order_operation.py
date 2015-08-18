# from LYFAdmin.models import Order, Student, Mentor, MoneyRecord, CashRecord, ChargeRecord


import time
import datetime


def create_order_id(stu_id, men_id):
    date_str = str(datetime.date.today()).replace('-', '')
    auto_num = Order.objects.filter(create_time__year=datetime.date.year,
                                    create_time__month=datetime.date.month,
                                    create_time__day=datetime.date.day).count() + 1
    auto_num = 1
    new_id = '%s%06i%06i%06i' % (date_str, stu_id, men_id, auto_num)
    return new_id


print create_order_id(1, 1)