import time
import os
import random
import string
import hashlib
import ujson


from PIL import Image
from django.utils import timezone

from LYFAdmin.models import Admin

UPLOAD_PATH = os.path.dirname(os.path.dirname(__file__)) + '/static'

def upload_picture(pic_file, folder='hero/'):
    pic_name = str(int(time.time())) + str(random.randint(10000, 99999)) + '.png'
    pic_path = '/upload/' + folder + pic_name
    save_path = UPLOAD_PATH + pic_path
    img = Image.open(pic_file)
    img.save(save_path, "png")
    return pic_path, save_path


def datetime_to_string(datetimet, str_format='%Y-%m-%d %H:%M:%S'):
    if datetimet.tzinfo is None:
        return datetimet.strftime(str_format)
    time_str = datetimet.astimezone(timezone.get_current_timezone())
    return time_str.strftime(str_format)


def create_token(count=32):
    return string.join(
        random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba+=', count)).replace(" ", "")


def auth_admin(account, password):
    admin = Admin.objects.filter(account=account)
    if admin.exists():
        admin = admin[0]
        hash_passwd = hashlib.md5(password).hexdigest()
        if admin.password == hash_passwd:
            admin.token = create_token()
            admin.save()
            return admin
        else:
            return None
    else:
        return None


def encodejson(status, body):
    tmpjson={}
    tmpjson['status'] = status
    tmpjson['body'] = body
    return ujson.dumps(tmpjson)