# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from weichat.wechat_service import WechatService

from django.core.management.base import BaseCommand
from weichat.models import Promotion

class Command(BaseCommand):
    def handle(self, *args, **options):
        wx = WechatService()
        promotion_list = Promotion.objects.all()
        for promotion in promotion_list:
            user_info = wx.wechat.get_user_info(promotion.open_id)
            sex = '男'
            if str(user_info['sex']) == '2':
                sex = '女'
            elif str(user_info['sex']) == '0':
                sex = '未知'
            promotion.sex = sex
            promotion.save()
        print 'mission complete!'