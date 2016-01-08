# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from weichat.wechat_service import WechatService
from django.core.management.base import BaseCommand
from weichat.models import Promotion
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        wx = WechatService()
        promotion_list = Promotion.objects.all()
        total = promotion_list.count()
        for i, promotion in enumerate(promotion_list):
            try:
                user_info = wx.wechat.get_user_info(promotion.open_id)
                sex = '男'
                get_sex = str(user_info.get('sex', '1'))
                if get_sex == '2':
                    sex = '女'
                elif get_sex == '0':
                    sex = '未知'
                if promotion.sex != '女':
                    promotion.sex = sex
                    promotion.save()
                print 'total:{0}, current{1}, sex:{2}'.format(total, i, get_sex)
            except:
                print 'a'
        print 'mission complete!'