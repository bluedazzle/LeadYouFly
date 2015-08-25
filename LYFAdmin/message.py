# -*- coding: utf-8 -*-
import datetime

from LYFAdmin.models import Message, Student

REG_MES = '欢迎您，%s'
LVLUP_MES = ''
ORDER_BUY_MES = ''
ORDER_CMMNT_MES = ''
MENTOR_RES_MES = ''


def create_new_message(content, belong, send_all=False):
    new_mes = Message(content=content,
                      belong=belong,
                      send_all=send_all)
    new_mes.save()
    return True


def push_custom_message(content, push_list=(), send_all=False):
    if send_all:
        create_new_message(content, None, True)
    else:
        for itm in push_list:
            stu_list = Student.objects.filter(account=itm)
            if stu_list.exists():
                stu = stu_list[0]
                create_new_message(content, stu)
    return True