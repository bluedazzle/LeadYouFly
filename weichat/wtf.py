# coding: utf-8
import json
import requests

def send_message(open_id, message):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxed29f94c7e513349&secret=db22f19fa5b7f2da43feb4f5c4173bf9'
    result = requests.get(url)
    token = json.loads(result.content).get('access_token')
    req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'.format(token)
    data = {'touser': open_id,
            'msgtype': 'text',
            'text': {'content': message}}
    result = requests.post(req_url, data=json.dumps(data, ensure_ascii=False))
    print result.content
    return result.content