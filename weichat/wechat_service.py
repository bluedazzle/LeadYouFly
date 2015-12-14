# coding: utf-8
from __future__ import unicode_literals
import StringIO
import json
import requests
from weichat.models import WeChatAdmin, Channel, Promotion, Question, Message, WechatMessage
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


    def get_kefu_list(self):
        result = self.wechat.grant_token()
        token = result['access_token']
        req_url = 'https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token={0}'.format(token)
        result = requests.get(req_url)
        return json.loads(result.content)


    def distribution_kefu(self, open_id, account):
        result = self.wechat.grant_token()
        token = result['access_token']
        req_url = ' https://api.weixin.qq.com/customservice/kfsession/create?access_token={0}'.format(token)
        data = {'kf_account': account,
                'openid': open_id,
                'text': '学员问题咨询'}
        result = requests.post(req_url, data=json.dumps(data))
        return result


    def create_promotion_qrcode(self, name, scene, welcome, phone):
        data = {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": scene}}}
        ticket = self.wechat.create_qrcode(data)['ticket']
        new_channel = Channel(name=name,
                              scene=scene,
                              ticket=ticket,
                              welcome_text=welcome,
                              phone=phone)
        new_channel.save()
        return new_channel


    def get_user_info_by_code(self, code):
        req_url = '''https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'''.format(self.wechat_admin.app_id, self.wechat_admin.app_secret, code)
        result = requests.get(req_url)
        return json.loads(result.content)


    def get_promotion_info(self, openID, channel=None):
        result = Promotion.objects.filter(open_id=openID)
        if result.exists():
            return result[0]
        user_info = self.wechat.get_user_info(openID)
        nick = user_info['nickname']
        city = user_info['city']
        province = user_info['province']
        sex = '男'
        if user_info['sex'] == '2':
            sex = '女'
        elif user_info['sex'] == '0':
            sex = '未知'
        new_promotion = Promotion(open_id=openID,
                                  nick=nick,
                                  sex=sex,
                                  city=city,
                                  province=province,
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
                       'scan': self.event_manage,
                       'view': self.event_manage,
                       }
        is_pic, result = manage_dict[message.type](message)
        if is_pic:
            response = self.wechat.response_image(result)
        else:
            response = self.wechat.response_text(result)
        return response


    def text_manage(self, message):
        question = message.content
        open_id = message.source
        user_list = Promotion.objects.filter(open_id=open_id)
        new_message = WechatMessage(open_id=open_id,
                                    content=question,
                                    nick='')
        if user_list.exists():
            user = user_list[0]
            user.reply = '{0}; 回复内容：{1}'.format(user.reply, question)
            user.save()
            new_message.nick = user.nick
        new_message.save()
        result = Question.objects.filter(question=question)
        # if not result.exists():
        #     result = Question.objects.filter(question__icontains=question)
        if result.exists():
            if result[0].have_image:
                return True, self.upload_picture(result[0].image)
            return False, result[0].answer
        answer = get_answer(question)
        if answer.have_image:
            return True, self.upload_picture(answer.image)
        else:
            return False, answer.answer


    def event_manage(self, message):
        open_id = message.source
        if message.type == 'subscribe':
            channel_list = Channel.objects.filter(ticket=message.ticket)
            if channel_list.exists():
                channel = channel_list[0]
                promotion = self.get_promotion_info(open_id, channel)
                promotion.cancel = False
                promotion.save()
                return False, promotion.channel.welcome_text
            else:
                return False,  '''嘿！欢迎关注飞吧游戏教练。

直接发送文字消息，提出关于LOL的任何问题，小飞都会第一时间给你答复。Try it~[坏笑]

更有大神教练提供一对一游戏教学服务，讲道理的话，这里是教你快速上分的不二之选。'''
        elif message.type == 'unsubscribe':
            promotion = self.get_promotion_info(open_id)
            promotion.cancel = True
            promotion.save()
            return False, ''
        elif message.type == 'view':
            user_list = Promotion.objects.filter(open_id=open_id)
            if user_list.exists():
                menu_dict = {'http://www.fibar.cn': '寻找教练',
                             'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI4ODAzNzI5OA==#wechat_webview_type=1&wechat_redirect': '发现好玩',
                             'http://forum.fibar.cn': '飞吧社区'}
                user = user_list[0]
                user.reply = '{0}; 点击菜单：{1}'.format(user.reply, menu_dict.get(message.key, '菜单'))
                user.save()
            return False, ''
        else:
            promotion = self.get_promotion_info(open_id)
            return False, promotion.channel.welcome_text


    def other_manage(self, message):
        return False, '小飞现在还不能识别其他类型的消息呢，请发文字～'


    def upload_picture(self, url):
        ext = str(url).split('.')[-1]
        img_req = requests.get(url)
        print url
        try:
            tmp_io = StringIO.StringIO(img_req.content)
            res = self.wechat.upload_media('image', tmp_io, extension='jpg')
            print res
            return res.get('media_id', '')
        except Exception, e:
            print e