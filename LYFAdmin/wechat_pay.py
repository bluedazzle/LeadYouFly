# coding: utf-8
from __future__ import unicode_literals

import requests
import random
import string

def create_random_string(count=30):
    return string.join(
        random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890', count)).replace(" ", "")

def create_wepay_order(title, body, order_id, total_fee):
    pass