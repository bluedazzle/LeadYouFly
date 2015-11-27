# coding: utf-8
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from kw import get_answer

# Create your views here.

ACCESS_TOKEN = '2RGp6ozXkHZg17x8d3pSxd9qtOTWECGdvAzPg77jiUBQH5ij87-TeNPQKPQrH_lN78zk8eDvQS3cuM8ZceUguNpJGFjZgjLBjIvkVTckbsgZNYhAJAGUF'

@csrf_exempt
def wechat_service(req):
    if req.method == 'GET':
        token = ACCESS_TOKEN  # 你的微信 Token
        signature = req.GET.get('signature', '')  # Request 中 GET 参数 signature
        timestamp = req.GET.get('timestamp', '')  # Request 中 GET 参数 timestamp
        nonce = req.GET.get('nonce', '')
        echostr = req.GET.get('echostr', '')
        wechat = WechatBasic(token=token)
        if wechat.check_signature(signature, timestamp, nonce):
            print True
            return HttpResponse(echostr)
        print False
        return HttpResponse(echostr)

    if req.method == 'POST':
        body_text = req.body
        wechat = WechatBasic(token=ACCESS_TOKEN)
        wechat.parse_data(body_text)
        message = wechat.get_message()
        if message.type == 'text':
            answer = get_answer(message.content)
            response = wechat.response_text(answer)
        else:
            response = wechat.response_text(u'小飞现在还不能理解其他类型的消息呢～请输入文字')
        return HttpResponse(response)
