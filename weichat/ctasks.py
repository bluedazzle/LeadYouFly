# coding: utf-8
from __future__ import unicode_literals

import json
import logging

import datetime
import requests

from celery import Celery
from wechat_sdk import WechatBasic
from PIL import Image, ImageOps, ImageDraw, ImageFont
import urllib, cStringIO, StringIO

app = Celery('weichat.ctasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


# app.config_from_object('celery_config')


def upload_picture(url, token, appid, secret):
    # ext = str(url).split('.')[-1]
    wechat = WechatBasic(token, appid, secret)
    img_req = requests.get(url)
    print url
    try:
        tmp_io = StringIO.StringIO(img_req.content)
        res = wechat.upload_media('image', tmp_io, extension='jpg')
        print 'UPLOAD TO WECHAT', res
        return res.get('media_id', '')
    except Exception, e:
        print 'ERROR IN UPLOAD', e
        return None


@app.task
def gen_pic_and_send(nick, avatar, qr_url, openid, token, appid, secret, num):
    logging.info('Start notify url to baidu')
    st = datetime.datetime(2018, 4, 29)
    now = datetime.datetime.now()
    day = unicode((st - now).days)
    MEDIA_TMP = './static/tmp/'
    # region = Image.open(cStringIO.StringIO(urllib.urlopen(qr_url).read()))
    # base_img = Image.open('bb.jpg')
    base_img = Image.open('{0}bbj.jpg'.format(MEDIA_TMP))
    base_img = base_img.convert('RGBA')
    box = (150, 586, 240, 676)
    ava_box = (220, 100, 320, 200)
    # box = (180, 632, 250, 702)
    # ava_box = (178, 500, 238, 560)
    # region.thumbnail((140, 140))
    # qr
    # region.thumbnail((90, 90))
    # base_img.paste(region, box)
    avatar = Image.open(cStringIO.StringIO(urllib.urlopen(avatar).read()))
    avatar = avatar.convert('RGBA')
    # avatar.show()
    # size = (120, 120)
    size = (100, 100)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    final1 = Image.new("RGBA", base_img.size)
    final1.paste(base_img, (0, 0))
    final1.paste(output, ava_box, output)
    # final1.show()
    draw = ImageDraw.Draw(final1)
    ttfont = ImageFont.truetype("{0}fzpc.ttf".format(MEDIA_TMP), 20)
    ttfont1 = ImageFont.truetype("{0}hr.ttf".format(MEDIA_TMP), 100)
    # ttfont = ImageFont.truetype("hr.ttf", 20)
    # ttfont1 = ImageFont.truetype("hr.ttf", 100)
    draw.text((234, 200), nick, font=ttfont, fill=(0, 0, 0, 255))
    draw.text((240, 381), day, font=ttfont1, fill=(255, 160, 29, 255))
    # draw.text((187, 592), nick, font=ttfont)
    # save_path = '{0}.jpg'.format(openid)
    save_path = '{0}{1}.jpg'.format(MEDIA_TMP, openid)
    final1 = final1.convert('RGB')
    final1.save(save_path, quality=100)
    mid = upload_picture('http://sy.chafanbao.com/static/tmp/{0}.jpg'.format(openid), token, appid, secret)
    wechat = WechatBasic(token, appid, secret)
    token = wechat.grant_token()['access_token']
    req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'.format(token)
    # message = message.decode('utf-8')
    data = {'touser': openid,
            'msgtype': 'image',
            'image': {'media_id': mid}}
    result = requests.post(req_url, data=json.dumps(data))
    return json.loads(result.content)


@app.task
def gen_qh_pic_and_send(nick, avatar, qr_url, openid, token, appid, secret, num):
    logging.info('Start gen qh pic')
    MEDIA_TMP = './static/tmp/'
    # region = Image.open(cStringIO.StringIO(urllib.urlopen(qr_url).read()))
    # base_img = Image.open('{0}baseq1.png'.format(MEDIA_TMP))
    base_img = Image.open('baseq1.png')
    box = (150, 586, 240, 676)
    ava_box = (28, 113, 128, 213)
    # box = (180, 632, 250, 702)
    # ava_box = (178, 500, 238, 560)
    # region.thumbnail((140, 140))
    # qr
    # region.thumbnail((90, 90))
    # base_img.paste(region, box)
    avatar = Image.open(cStringIO.StringIO(urllib.urlopen(avatar).read()))
    # size = (120, 120)
    size = (100, 100)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    final1 = Image.new("RGBA", base_img.size)
    final1.paste(base_img, (0, 0), base_img)
    final1.paste(output, ava_box, output)
    draw = ImageDraw.Draw(final1)
    ttfont = ImageFont.truetype("fzpc.ttf", 20)
    # ttfont = ImageFont.truetype("{0}fzpc.ttf".format(MEDIA_TMP), 20)
    draw.text((85, 225), nick, font=ttfont)
    draw.text((85, 252), '1', font=ttfont)
    # draw.text((187, 592), nick, font=ttfont)
    # save_path = '{0}{1}.jpg'.format(MEDIA_TMP, openid)
    save_path = '{0}.jpg'.format(openid)
    final1 = final1.convert('RGB')
    final1.save(save_path, quality=100)
    # mid = upload_picture('http://sy.chafanbao.com/static/tmp/{0}.jpg'.format(openid), token, appid, secret)
    # wechat = WechatBasic(token, appid, secret)
    # token = wechat.grant_token()['access_token']
    # req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'.format(token)
    # # message = message.decode('utf-8')
    # data = {'touser': openid,
    #         'msgtype': 'image',
    #         'image': {'media_id': mid}}
    # result = requests.post(req_url, data=json.dumps(data))
    # return json.loads(result.content)


@app.task
def send_pic(openid, token, appid, secret):
    mid = upload_picture('http://sy.chafanbao.com/static/tmp/{0}.jpg'.format(openid), token, appid, secret)
    wechat = WechatBasic(token, appid, secret)
    token = wechat.grant_token()['access_token']
    req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'.format(token)
    # message = message.decode('utf-8')
    data = {'touser': openid,
            'msgtype': 'image',
            'image': {'media_id': mid}}
    result = requests.post(req_url, data=json.dumps(data))
    return json.loads(result.content)


if __name__ == '__main__':
    gen_pic_and_send('rapospectre',
                     'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKMdylic8UUD4zsQU4Bz58HoLLMmD7z1YfFQ4HyyoIDmhzktSZTSzG3vkcVsfLHFWXy3b4XeAppPTw/132',
                     '', 'xxx', 'xxx', 'xxx', '', 1)
