# coding: utf-8
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from wechat_sdk import WechatBasic
from kw import get_answer

# Create your views here.


@csrf_exempt
def wechat_service(req):
    from wechat_service import WechatService
    WS = WechatService()
    if req.method == 'GET':
        # WS.create_pic('test', 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1506546292291&di=d6d521043a6052b5e7ab256a08b9b8c9&imgtype=0&src=http%3A%2F%2Fv1.qzone.cc%2Favatar%2F201310%2F12%2F15%2F42%2F5258fd6f0db4b914.jpg%2521200x200.jpg', 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQGK8DwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyY3ZNbDBVZktheFUxMDAwMHcwN3IAAgR6ystZAwQAAAAA', 'ttttt')
        signature = req.GET.get('signature', '')  # Request 中 GET 参数 signature
        timestamp = req.GET.get('timestamp', '')  # Request 中 GET 参数 timestamp
        nonce = req.GET.get('nonce', '')
        echostr = req.GET.get('echostr', '')
        if WS.wechat.check_signature(signature, timestamp, nonce):
            return HttpResponse(echostr)
        return HttpResponse(echostr)

    if req.method == 'POST':

        body_text = req.body
        response = WS.message_manage(body_text)
        return HttpResponse(response)


@csrf_exempt
def qh_service(req):
    from ws import WechatService
    WS = WechatService()
    if req.method == 'GET':
        signature = req.GET.get('signature', '')  # Request 中 GET 参数 signature
        timestamp = req.GET.get('timestamp', '')  # Request 中 GET 参数 timestamp
        nonce = req.GET.get('nonce', '')
        echostr = req.GET.get('echostr', '')
        if WS.wechat.check_signature(signature, timestamp, nonce):
            return HttpResponse(echostr)
        return HttpResponse(echostr)

    if req.method == 'POST':

        body_text = req.body
        response = WS.message_manage(body_text)
        return HttpResponse(response)


class ZPView(TemplateView):
    template_name = 'zp.html'
