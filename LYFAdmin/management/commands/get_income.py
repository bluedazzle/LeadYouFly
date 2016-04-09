# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from LYFAdmin.models import Mentor
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        mentor = Mentor.objects.get(account='18744885070')
        total = 0.0
        ti = 0.0
        for order in mentor.men_orders.all():
            if order.status != 3 and order.status != 4:
                continue
            if order.mentor_money == 0.0:
                total += order.order_price
            else:
                total += order.mentor_money
                ti += order.platform_money
        print 'total: {0}, tichen: {1}'.format(total, ti)