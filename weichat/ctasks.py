# coding: utf-8
from __future__ import unicode_literals

import json
import logging
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
def gen_pic_and_send(nick, avatar, qr_url, openid, token, appid, secret):
    logging.info('Start notify url to baidu')
    MEDIA_TMP = './static/tmp/'
    region = Image.open(cStringIO.StringIO(urllib.urlopen(qr_url).read()))
    base_img = Image.open('{0}base0.png'.format(MEDIA_TMP))
    box = (150, 586, 240, 676)
    ava_box = (167, 471, 223, 527)
    # box = (180, 632, 250, 702)
    # ava_box = (178, 500, 238, 560)
    # region.thumbnail((140, 140))
    region.thumbnail((90, 90))
    base_img.paste(region, box)
    avatar = Image.open(cStringIO.StringIO(urllib.urlopen(avatar).read()))
    # size = (120, 120)
    size = (56, 56)
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
    draw.text((179, 552), nick, font=ttfont)
    # draw.text((187, 592), nick, font=ttfont)
    save_path = '{0}{1}.jpg'.format(MEDIA_TMP, openid)
    final1 = final1.convert('RGB')
    final1.save(save_path, quality=100)
    mid = upload_picture('http://sy.datoushow.com/static/tmp/{0}.jpg'.format(openid), token, appid, secret)
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
def send_pic(openid, token, appid, secret):
    mid = upload_picture('http://sy.datoushow.com/static/tmp/{0}.jpg'.format(openid), token, appid, secret)
    wechat = WechatBasic(token, appid, secret)
    token = wechat.grant_token()['access_token']
    req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'.format(token)
    # message = message.decode('utf-8')
    data = {'touser': openid,
            'msgtype': 'image',
            'image': {'media_id': mid}}
    result = requests.post(req_url, data=json.dumps(data))
    return json.loads(result.content)

