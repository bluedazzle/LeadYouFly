# -*- coding: utf-8 -*-
import datetime

from LYFAdmin.models import Message, Student

REG_MES = '''Hi，欢迎来到这里！我是运营团队的小飞~
我们致力于为每一位热爱游戏，渴望超越的玩家提供最专业的游戏教学服务。
从现在开始，我会在前进的道路上陪伴着你哦~ 你的教练，在严阵以待，飞吧，%s！
如有任何疑问，请戳常见问题，或联系我的QQ：765566978'''

EXP_MES = '''小飞迫不及待地告诉你，你获得了%s点积分，目前是%s级学员，再有%s分就可以进阶为下一级学员啦！'''

LVLUP_MES = '''哈~你已成为%s级学员，真是可喜可贺！继续加油，小飞在这条道路上一直陪着你！'''

ORDER_BUY_MES = '''亲爱的%s，你的订单已经成功通知给教练啦！泡杯茶稍等一下，教学马上开始哦！
  记得要保证教练可以联系到你，你也可以在我的订单中查看教练的联系方式~
  如果遇到坑爹教练什么的，都可以提供证明进行投诉。
  小飞祝你学习愉快，早日成神！'''

ORDER_CMMNT_MES = '上个课程完成了，相信你一定有所收获，小飞提醒你记得要给教练评价，要知道教练也是需要意见和鼓励的啊！'


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
