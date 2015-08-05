import time
import os
import random
from PIL import Image
from django.utils import timezone

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