from LYFAdmin.models import *
import LYFAdmin.sms
import random


def get_verify_code(phone):
    verify_code = random.randint(100000, 999999)
    sms_res = LYFAdmin.sms.send_msg(phone, verify_code)
    return True