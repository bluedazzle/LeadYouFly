# coding: utf-8
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from kw import get_answer
from wechat_service import WechatService

# Create your views here.


@csrf_exempt
def wechat_service(req):
    WS = WechatService()
    if req.method == 'GET':
        signature = req.GET.get('signature', '')  # Request 中 GET 参数 signature
        timestamp = req.GET.get('timestamp', '')  # Request 中 GET 参数 timestamp
        nonce = req.GET.get('nonce', '')
        echostr = req.GET.get('echostr', '')
        if WS.wechat.check_signature(signature, timestamp, nonce):
            print True
            return HttpResponse(echostr)
        print False
        return HttpResponse(echostr)

    if req.method == 'POST':
        body_text = req.body
        print body_text
        response = WS.message_manage(body_text)
        return HttpResponse(response)
