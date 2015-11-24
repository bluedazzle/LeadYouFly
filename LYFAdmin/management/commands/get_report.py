# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from LYFAdmin.models import Student
import datetime
import time
from django.utils.timezone import get_current_timezone
from django.db.models import Q

from dss.Serializer import serializer

class Command(BaseCommand):
    def handle(self, *args, **options):
        start_time = args[0]
        end_time = args[1]
        s_date_time = datetime.datetime(*time.strptime(start_time, "%Y%m%d")[:6])
        e_date_time = datetime.datetime(*time.strptime(end_time, "%Y%m%d")[:6])
        s_date_time = s_date_time.replace(tzinfo=get_current_timezone())
        e_date_time = e_date_time.replace(tzinfo=get_current_timezone())
        user_list = Student.objects.filter(create_time__range=(s_date_time, e_date_time))
        s_user_list= serializer(user_list, datetime_format='string', output_type='dict')
        for i, user in enumerate(user_list):
            user_order = user.stu_orders.filter(Q(status=1) | Q(status=2) | Q(status=3) | Q(status=4))
            total_money = 0.0
            for order in user_order:
                total_money += float(order.order_price)
            s_user_list[i]['total'] = total_money

        p_50 = 0
        p_100 = 0
        p_400 = 0
        p_800 = 0
        p_2000 = 0
        total_money = 0.0
        total_p = user_list.count()
        for itm in s_user_list:
            total_money += itm['total']
            if itm['total'] >= 50:
                p_50 += 1
                p_100 += 1
                p_400 += 1
                p_800 += 1
                p_2000 += 1
                continue
            elif itm['total'] >= 100:
                p_100 += 1
                p_400 += 1
                p_800 += 1
                p_2000 += 1
                continue
            elif itm['total'] >= 400:
                p_400 += 1
                p_800 += 1
                p_2000 += 1
            elif itm['total'] >= 800:
                p_800 += 1
                p_2000 += 1
                continue
            elif itm['total'] >= 2000:
                p_2000 += 1
                continue

        percent_100 = (p_100 + p_400 + p_800 + p_2000) / total_p
        result = u'''消费金额：{0}
2000以上人数：{1}
800以上人数：{2}
400以上人数：{3}
100以上人数：{4}
50以上人数：{5}
过百元用户占比：{6}'''.format(total_money, p_2000, p_800, p_400, p_100, p_50, percent_100)
        print result