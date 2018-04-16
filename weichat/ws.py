# coding: utf-8
from __future__ import unicode_literals
import StringIO
import json
import requests
import simplejson
from weichat.models import WeChatAdmin, Channel, Promotion, Question, WechatMessage
from wechat_sdk import WechatBasic
from kw import get_answer
import redis


class WechatService(object):
    # __isntance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance = super(WechatService, cls).__new__(cls, *args, **kwargs)

    def __init__(self, app_id=None, app_secret=None):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=1)
        if not app_id:
            self.wechat_admin = WeChatAdmin.objects.all().order_by('id')[1]
            self.wechat = WechatBasic(appid=self.wechat_admin.app_id,
                                      appsecret=self.wechat_admin.app_secret,
                                      token=self.wechat_admin.access_token)
        else:
            self.wechat_admin = None
            self.wechat = WechatBasic(appid=app_id, appsecret=app_secret)

        self.get_token()

    def get_token(self):
        token = self.redis.get('qh_wx_token')
        if not token:
            res = self.wechat.grant_token()
            token = res.get('access_token')
            self.redis.set('qh_wx_token', token, 3600)
            if self.wechat_admin:
                self.wechat_admin.access_token = token
                self.wechat_admin.save()
        return token

    def send_message(self, open_id, message):
        token = self.get_token()
        req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'.format(token)
        message = message.decode('utf-8')
        data = {'touser': open_id,
                'msgtype': 'text',
                'text': {'content': str('测试')}}
        result = requests.post(req_url, data=simplejson.dumps(data))
        return json.loads(result.content)

    def get_kefu_list(self):
        token = self.get_token()
        req_url = 'https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token={0}'.format(token)
        result = requests.get(req_url)
        return json.loads(result.content)

    def distribution_kefu(self, open_id, account, extra_mes):
        token = self.get_token()
        req_url = 'https://api.weixin.qq.com/customservice/kfsession/create?access_token={0}'.format(token)
        data = {'kf_account': account,
                'openid': open_id,
                'text': extra_mes}
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
        req_url = '''https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'''.format(
            self.wechat_admin.app_id, self.wechat_admin.app_secret, code)
        result = requests.get(req_url)
        return json.loads(result.content)

    def get_promotion_info(self, openID, channel=None):
        result = Promotion.objects.filter(open_id=openID)
        if result.exists():
            return result[0]
        user_info = self.wechat.get_user_info(openID)
        nick = user_info.get('nickname', None)
        city = user_info.get('city', None)
        province = user_info.get('province', None)
        sex = '男'
        if str(user_info.get('sex', 0)) == '2':
            sex = '女'
        elif str(user_info.get('sex', 0)) == '0':
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
                       'event': self.event_manage,
                       'voice': self.other_manage,
                       'click': self.click_manage
                       }
        is_pic, result = manage_dict[message.type](message)
        if is_pic:
            response = self.wechat.response_news(result)
        else:
            response = self.wechat.response_text(result)
        return response
        # return self.wechat.response_text('欢迎您关注中国石油青海销售分公司~')

    def click_manage(self, message):
        open_id = message.source
        print message.__dict__
        mid = self.create_channel(open_id)
        return False, '海报生成中,请稍后...'

    def text_manage(self, message):
        # exclude_words = ['狮子狗', '永猎双子', '寒冰射手']
        # new_reply = ['白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '摩羯', '水瓶', '双鱼']
        content = unicode(message.content)
        open_id = message.source
        if content == 'cm':
            print self.wechat.get_menu()
            return False, ''
        if content == 'mm':
            menu = {
                'button': [
                    {'name': '车主福利',
                     'sub_button': [
                         {
                             'type': 'view',
                             'name': '优惠集锦',
                             'url': 'https://mp.weixin.qq.com/mp/homepage?__biz=MzI5NjQ0NTQwOA==&hid=1&sn=9ba7e62ab89b1845613fd0ca698eac5a&scene=18&uin=&key=&devicetype=Windows+7&version=6206021b&lang=zh_CN&ascene=7&winzoom=1'
                         },
                         {
                             'type': 'view',
                             'name': '小新说车',
                             'url': 'https://mp.weixin.qq.com/mp/homepage?__biz=MzI5NjQ0NTQwOA==&hid=2&sn=1aed9c875448867a399265949b53cfdf&scene=18&uin=&key=&devicetype=Windows+7&version=6206021b&lang=zh_CN&ascene=7&winzoom=1'
                         },
                         {
                             'type': 'view',
                             'name': '爱车保养',
                             'url': 'http://mp.weixin.qq.com/s/3XI9-kJvYXCXHJWWIeUMDw'
                         },
                         {
                             'type': 'view',
                             'name': '昆仑之家',
                             'url': 'http://mp.weixin.qq.com/s/IZqPav9JEOT59196SkloFA'
                         },
                         {
                             'type': 'view',
                             'name': '跨界合作优惠',
                             'url': 'https://mp.weixin.qq.com/s/bww8CY09eLTjuapp6vDG8g'
                         },
                     ]},
                    {'name': '好客青海',
                     'sub_button': [
                         {
                             'type': 'view',
                             'name': '好客青海',
                             'url': 'http://55883069.m.weimob.com/vshop/55883069/Index?PageId=591449&IsPre=1&channel=menu&sionid=6b4237e6666944d988062452614c3f28'
                         },
                         {
                             'type': 'view',
                             'name': '天涯牧歌',
                             'url': 'http://m.qh.petro.tymg.vinotec.cn/adopt/index.aspx'
                         },
                         {
                             'type': 'view',
                             'name': '旅游卡激活',
                             'url': 'http://client-zsy-qh.sailouzai.com/'
                         },
                         {
                             'type': 'view',
                             'name': '测高原图腾',
                             'url': 'http://m.qh.petro.tymg.vinotec.cn/yunshan_login_2.aspx'
                         },
                     ]},
                    {
                        'name': '便捷服务',
                        'sub_button': [
                            {
                                'type': 'view',
                                'name': '今日油价',
                                'url': 'http://55883069.m.weimob.com/vshop/55883069/Index?PageId=643886&IsPre=1&channel=menu'
                            },
                            {
                                'type': 'view',
                                'name': '附近油站',
                                'url': 'http://www.95504.net/NewMapIndex/MapIndex.html'
                            },
                            {
                                'type': 'view',
                                'name': '油卡服务',
                                'url': 'http://www.95504.net/'
                            },
                            {
                                'type': 'view',
                                'name': '在线客服',
                                'url': 'http://55883069.im.m.weimob.com?channel=menu'
                            }
                        ]
                    }

                ]
            }
            self.wechat.create_menu(menu)
            return False, 'cm success'
        # if question == '抽奖':
        #     return False, '点击抽奖：http://www.fibar.cn/luckyDraw'
        # for itm in new_reply:
        #     if itm in unicode(message.content) and unicode(message.content) not in exclude_words and len(message.content) <= 3:
        #         self.news_reply_manage(open_id, itm)
        #         return False, '点击图文查看你的星座哟'
        # question = question.lower()
        # if question.startswith('qq'):
        #     self.get_qq(question, open_id)
        #     return False, 'QQ号绑定成功！'
        # user_list = Promotion.objects.filter(open_id=open_id)
        # new_message = WechatMessage(open_id=open_id,
        #                             content=question,
        #                             nick='')
        # if user_list.exists():
        #     user = user_list[0]
        #     user.reply = '{0}; 回复内容：{1}'.format(user.reply, question)
        #     user.save()
        #     new_message.nick = user.nick
        # new_message.save()
        # result = Question.objects.filter(question=question)
        # # if not result.exists():
        # #     result = Question.objects.filter(question__icontains=question)
        # if result.exists():
        #     if result[0].have_image:
        #         return True, self.upload_picture(result[0].image)
        #     return False, result[0].answer
        # answer = get_answer(question)
        # if answer.have_image:
        #     return True, self.upload_picture(answer.image)
        # else:
        #     return False, answer.answer
        if content == 'sc':
            return self.click_manage(message)
        return False, '欢迎关注'

    # def get_qq(self, message, open_id):
    #     user = Promotion.objects.get(open_id=open_id)
    #     message = message.replace('qq', '')
    #     user.qq = message
    #     user.save()
    #     return True


    # def news_reply_manage(self, open_id, content):
    #     reply_dict = {'白羊': {'title': '白羊座打游戏遇到坑货...', 'description': '白羊座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYLWVX3EUEQMEibA96ibxXVribdQvdnay90oB36fI8iaoBpHOhKJ1qUcEvQA/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366388&idx=1&sn=5fea602e1a1c80ae2f220d3beaf860fc#rd'},
    #                   '金牛': {'title': '金牛座打游戏遇到坑货...', 'description': '金牛座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYGSIMeDQpfO3pYAGy9fLyINNcM8POZ56vJQ7jTaUYqkicBlsjwkKJtcQ/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366574&idx=1&sn=bfaba59399f5cef31441d6a43b20ee70#rd'},
    #                   '双子': {'title': '双子座打游戏遇到坑货...', 'description': '双子座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FY9MLZ7s2AoWS8uvnvseGbI5T0yYH1ib8eOgcHiaUa70XPicZ1SYUiaPem3w/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366561&idx=1&sn=dcca9291f5ea3219db9f4ac91e6091ff#rd'},
    #                   '巨蟹': {'title': '巨蟹座打游戏遇到坑货...', 'description': '巨蟹座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYcYp9kHVia3fDWfLSSDTGBUvjGD1ys8LNpzwsibKVEfTGLPUcazXpicWAQ/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366583&idx=1&sn=34b51f06d9b33d2c78f1f35a345a3c77#rd'},
    #                   '狮子': {'title': '狮子座打游戏遇到坑货...', 'description': '狮子座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FY54uoAMvNLXMzKiaLxibTKU9VIto5xVIe2QK7cBrURojvI4NsjuaI6tDQ/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366595&idx=1&sn=a98f3b07a8de28f8e5b6a2a07bd53339#rd'},
    #                   '处女': {'title': '处女座打游戏遇到坑货...', 'description': '处女座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYffX5H8BQepX2jKAgKOkuE68QhUkwORhjmiaLmoGtqVTboWRAibrdN9Tw/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366607&idx=1&sn=a165af8d3288af2d92499c3354c3675a#rd'},
    #                   '天秤': {'title': '天秤座打游戏遇到坑货...', 'description': '天秤座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYHgdHeA4iaBygEyv5PMRDOJeAlhC7xnMcDicEHzJAOvOITTvhHw681FPw/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366626&idx=1&sn=5ac98699e3d25b27e646dd3f8d544c27#rd'},
    #                   '天蝎': {'title': '天蝎座打游戏遇到坑货...', 'description': '天蝎座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYpFfs6vb9dA6ybuVERqH48VLtWnQQLARibibeHLibnkDSJibBZyA5nvDTTg/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366637&idx=1&sn=0b717708d5b2f2939a9f80006624b61f#rd'},
    #                   '射手': {'title': '射手座打游戏遇到坑货...', 'description': '射手座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYtzvqZC3Yc4QoCvdb0AhjlF7SSic1oXicJ47dsMGEIRFkrj8DqS4NNia2A/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366667&idx=1&sn=1c255cd82abfdb3f8828ab6a634856ee#rd'},
    #                   '摩羯': {'title': '摩羯座打游戏遇到坑货...', 'description': '摩羯座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYbDlGrIMqjtLnNy9TxNicYh4a1UjZyWum31UBdpS01gbslHRIHvvupOg/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366693&idx=1&sn=e6da7a2d5348c5df470dbc44e027f3bc#rd'},
    #                   '水瓶': {'title': '水瓶座打游戏遇到坑货...', 'description': '水瓶座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYhKoMtBEc4RfrVXtnMFmT2UYpxu6ibMP6bm9EDic2YbR7pgNfXDbw2Mzg/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366723&idx=1&sn=6e5baf07ac2ccd190c3e7d96ec1f90cb#rd'},
    #                   '双鱼': {'title': '双鱼座打游戏遇到坑货...', 'description': '双鱼座打游戏遇到坑货', 'picurl': 'https://mmbiz.qlogo.cn/mmbiz/QuFfaBichozdPpkNa93EVvpLOsnyDT6FYib08WkRonp67zhpEHhtnVFC9lHcOZBa6BDUnt9JvyMFdEiaWNYzZxhjQ/0?wx_fmt=jpeg', 'url': 'http://mp.weixin.qq.com/s?__biz=MzI4ODAzNzI5OA==&mid=402366756&idx=1&sn=3125feb301deea415010ece29ba4f564#rd'},
    #
    #
    #     }
    #     article = [reply_dict.get(content, None)]
    #     return self.wechat.send_article_message(open_id, article)
    def create_channel(self, openid):
        from ctasks import gen_qh_pic_and_send, send_pic
        # cn = Channel.objects.filter(scene=openid)
        # if cn.exists():
        # send_pic.apply_async((openid, self.get_token(), self.wechat_admin.app_id, self.wechat_admin.app_secret))
        # return 'success'
        user_info = self.wechat.get_user_info(openid)
        # data = {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": openid}}}
        # ticket = self.wechat.create_qrcode(data)['ticket']
        # qr_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={0}'.format(ticket)
        name = user_info.get('nickname')
        qr_url = ''
        num = self.redis.get('qh_num')
        if not num:
            num = 299
            self.redis.set('qh_num', num)
        num = int(num)
        num += 56
        self.redis.set('qh_num', num)
        gen_qh_pic_and_send.apply_async((name, user_info.get('headimgurl'), qr_url, openid, self.get_token(),
                                         self.wechat_admin.app_id, self.wechat_admin.app_secret, unicode(num)))
        # path, mid = self.create_pic(name, , qr_url, openid)
        # channel = Channel()
        # channel.name = name
        # channel.scene = openid
        # channel.ticket = ticket
        # channel.pic = '/static/tmp/{0}.jpg'.format(openid)
        # channel.mid = ''
        # channel.save()
        pic = '/static/tmp/{0}.jpg'.format(openid)
        return pic

    def create_pic(self, nick, avatar, qr_url, openid):
        from PIL import Image, ImageOps, ImageDraw, ImageFont
        import urllib, cStringIO
        from LeadYouFly.settings import MEDIA_TMP
        region = Image.open(cStringIO.StringIO(urllib.urlopen(qr_url).read()))

        base_img = Image.open('{0}base.png'.format(MEDIA_TMP))
        # box = (360, 1265, 500, 1405)
        # ava_box = (357, 1000, 477, 1120)
        box = (180, 632, 250, 702)
        ava_box = (178, 500, 238, 560)
        # region.thumbnail((140, 140))
        region.thumbnail((70, 70))
        base_img.paste(region, box)
        avatar = Image.open(cStringIO.StringIO(urllib.urlopen(avatar).read()))
        # size = (120, 120)
        size = (60, 60)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        final1 = Image.new("RGBA", base_img.size)
        final1.paste(base_img, (0, 0), base_img)
        final1.paste(output, ava_box, output)
        draw = ImageDraw.Draw(final1)
        ttfont = ImageFont.truetype("{0}fzpc.ttf".format(MEDIA_TMP), 12)
        # draw.text((375, 1185), nick, font=ttfont)
        draw.text((187, 592), nick, font=ttfont)
        save_path = '{0}{1}.jpg'.format(MEDIA_TMP, openid)
        final1 = final1.convert('RGB')
        final1.save(save_path)
        mid = self.upload_picture('http://sy.datoushow.com/static/tmp/{0}.jpg'.format(openid))
        # try:
        #     tmp_io = StringIO.StringIO()
        #     final1.save(tmp_io, 'JPG')
        #     res = self.wechat.upload_media('image', tmp_io, extension='jpg')
        #     print 'upload pic to wechat as media', res
        #     mid = res.get('media_id', '')
        #     return '/static/tmp/{0}.jpg'.format(openid), mid
        # except Exception, e:
        #     print 'ERROR IN UPLOAD', e
        return '/static/tmp/{0}.jpg'.format(openid), mid

    def event_manage(self, message):
        open_id = message.source
        # print message.type
        if message.type == 'subscribe':
            # ticket = message.ticket
            # channel_list = Channel.objects.filter(ticket=message.ticket)
            # if channel_list.exists():
            #     channel = channel_list[0]
            #     promotion = self.get_promotion_info(open_id, channel)
            #     promotion.cancel = False
            #     promotion.save()
            # self.click_manage(message)
            # todo 关注发消息
            # mid = self.create_channel(open_id)
            #     return False, channel.welcome_text
            return False, '欢迎关注'
        elif message.type == 'unsubscribe':
            promotion = self.get_promotion_info(open_id)
            promotion.cancel = True
            promotion.save()
            return False, ''
            # elif message.type == 'view':
            # user_list = Promotion.objects.filter(open_id=open_id)
            # if user_list.exists():
            #     menu_dict = {'http://www.fibar.cn': '寻找教练',
            #                  'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI4ODAzNzI5OA==#wechat_webview_type=1&wechat_redirect': '发现好玩',
            #                  'http://forum.fibar.cn': '飞吧社区'}
            #     user = user_list[0]
            #     user.reply = '{0}; 点击菜单：{1}'.format(user.reply, menu_dict.get(message.key, '菜单'))
            #     user.save()
            # return False, ''
        elif message.type == 'event':
            # print message.__dict__
            if message.event_key == 'DQ001':
                self.click_manage(message)
        else:
            # promotion = self.get_promotion_info(open_id)
            # todo
            # mid = self.create_channel(open_id)
            return False, '欢迎关注'

    def res_new(self):
        article = {
            'url': 'https://mp.weixin.qq.com/s?__biz=MzI5NjQ0NTQwOA==&amp;mid=2247483918&amp;idx=1&amp;sn=a25a9d36daa85c46a34ca5b47e6f72d6&amp;chksm=ec457681db32ff9737df89e1c10c7958227176bc4a24c5d9a787924d6e20ff932f6f3e5fdaa2',
            'title': '十一出行，送你10元电子加油券',
            'description': '快来领取，顺便分享给朋友吧！',
            'picurl': 'https://mmbiz.qpic.cn/mmbiz_png/rfD6ospvicPVGfWKqXeCnxH5xX7o9zLAtNu4WkmYglzA5tk9oqS3u1z1OOdz1Sp6JOIHx6O6k6ocoibfGHppqlicg/0?wx_fmt=png'}
        news = self.wechat.response_news([article])
        return news

    def other_manage(self, message):
        return False, '我现在还不能识别其他类型的消息呢，请发文字～'

    def upload_picture(self, url):
        ext = str(url).split('.')[-1]
        img_req = requests.get(url)
        print url
        try:
            tmp_io = StringIO.StringIO(img_req.content)
            res = self.wechat.upload_media('image', tmp_io, extension='jpg')
            print 'UPLOAD TO WECHAT', res
            return res.get('media_id', '')
        except Exception, e:
            print 'ERROR IN UPLOAD', e
            return ''