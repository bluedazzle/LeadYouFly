# coding: utf-8
from __future__ import unicode_literals
from models import Question
import requests
import hashlib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

api_host = 'http://ask.1006.tv'
app_name = 'loldata'
key = 'kbpRXtPWoDuM2'
channel = '9'


def get_xcode(*args):
    md5 = hashlib.md5()
    params = ''
    for arg in args:
        params += arg
    params = params.encode('utf-8')
    md5.update(params)
    return md5.hexdigest()


def get_answer(question=''):
    xcode = get_xcode(app_name, channel, key)
    urls = '{0}/foundNewUser/{1}/?channel={2}&xcode={3}'.format(api_host, app_name, channel, xcode)
    r1 = requests.get(urls)
    user_id = json.loads(r1.content)['result']
    xcode = get_xcode(user_id, question, key)
    req_data = {'user': user_id,
                'question': question,
                'channel': channel,
                'xcode': xcode,
                'mid': 0,
                'chat_type': 0}
    r2 = requests.post('http://ask.1006.tv/question/loldata', data=req_data)
    err_code = json.loads(r2.content)['error_code']
    if err_code != 0:
        return Question.objects.get(question='nonoreply')
    answer = json.loads(r2.content)['result']['answer']
    answer_image = json.loads(r2.content)['result']['answer_images']
    answer = unicode(answer).replace('小问', '小飞')
    answer = answer.replace('快问', '小飞')
    answer = answer.replace('1006', '小飞')
    answer = answer.replace('的指导员', '')
    if u'张建奇' in question:
        answer = u'叫你爸爸做什么？'
    if u'这里是游戏问答平台，你能换个游戏问题么？' in answer:
        answer = u'小飞只会回答游戏相关的问题哦～'
    answer = '{0}\n <a href="http://lol.fibar.cn/search_teacher"> 来飞吧游戏教练，让教练一对一教你{1}</a>'.format(answer, question)
    new_question = Question(question=question, answer=answer)
    if answer_image != '':
        new_question.image = answer_image
        new_question.have_image = True
    new_question.save()
    return new_question





