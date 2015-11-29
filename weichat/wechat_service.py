# coding: utf-8
from __future__ import unicode_literals
import json
from weichat.models import WeChatAdmin, Channel, Promotion
from wechat_sdk import WechatBasic
from kw import get_answer


class WechatService(object):
    # __isntance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance = super(WechatService, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        self.wechat_admin = WeChatAdmin.objects.all()[0]
        self.wechat = WechatBasic(appid=self.wechat_admin.app_id,
                                  appsecret=self.wechat_admin.app_secret,
                                  token=self.wechat_admin.access_token)


    def refresh_token(self):
        result = self.wechat.grant_token()
        token = result['access_token']
        self.wechat_admin.access_token = token
        self.wechat_admin.save()
        return token


    def create_promotion_qrcode(self, name, scene, welcome):
        data = {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": scene}}}
        ticket = self.wechat.create_qrcode(data)['ticket']
        new_channel = Channel(name=name,
                              scene=scene,
                              ticket=ticket,
                              welcome_text=welcome)
        new_channel.save()
        return new_channel


    def get_promotion_info(self, openID, channel=None):
        result = Promotion.objects.filter(open_id=openID)
        if result.exists():
            return result[0]
        nick = self.wechat.get_user_info(openID)['nickname']
        new_promotion = Promotion(open_id=openID,
                                  nick=nick,
                                  channel=channel)
        new_promotion.save()
        return new_promotion


    def message_manage(self, message_body):
        self.wechat.parse_data(message_body)
        message = self.wechat.get_message()
        manage_dict = {'text': self.text_manage,
                       'image': self.other_manage,
                       'video': self.other_manage,
                       'shortvideo': self.other_manage,
                       'link': self.other_manage,
                       'location': self.other_manage,
                       'subscribe': self.event_manage,
                       'unsubscribe': self.event_manage,
                       'scan': self.event_manage
                       }
        result = manage_dict[message.type](message)
        response_text = self.wechat.response_text(result)
        return response_text


    def text_manage(self, message):
        return get_answer(message.content)


    def event_manage(self, message):
        open_id = message.source
        if message.type == 'subscribe':
            channel_list = Channel.objects.filter(ticket=message.ticket)
            if channel_list.exists():
                channel = channel_list[0]
                promotion = self.get_promotion_info(open_id, channel)
                return promotion.channel.welcome_text
            else:
                return '嘿！欢迎关注飞吧游戏教练，直接输入文字提出LOL中遇到的任何问题，都可以第一时间得到解答，更有大神教练提供一对一游戏教学服务，讲道理的话，这里是教你快速上分的不二之选。'
        elif message.type == 'unsubscribe':
            promotion = self.get_promotion_info(open_id)
            promotion.cancel = True
            promotion.save()
            return ''
        else:
            promotion = self.get_promotion_info(open_id)
            return promotion.channel.welcome_text


    def other_manage(self, message):
        return '小飞现在还不能识别其他类型的消息呢，请发文字～'