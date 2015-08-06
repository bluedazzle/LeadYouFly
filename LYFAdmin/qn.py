# -*- coding: utf-8 -*-
from qiniu import Auth
from qiniu import put_data
from qiniu import BucketManager, PersistentFop, build_op, op_save

import ujson

ACCESS_KEY = 'yNkIkBJv92stxKg8yNs2n1wcOiaqPE7wy0ZyGdwy'
SECRET_KEY = 'U8EitYYdhQ4_9hxvQuR6z0mPjnj5IDzovo81pqN7'
BUCKET_NAME = 'leadyoufly'
QINIU_DOMAIN = 'http://7xkveq.com2.z0.glb.qiniucdn.com/'

video_convert_param = 'avthumb/mp4'
video_poster_param = 'vframe/jpg/offset/5/w/900/h/500'


def upload_file_qn(ufile, file_name, sign='default'):
    full_name = sign + '_' + file_name
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME)
    ret, info = put_data(token, full_name, ufile)
    if info.status_code == 200:
        return True, ujson.loads(info.text_body)['key']
    else:
        return False, None


def list_file(filter_str=()):
    q = Auth(ACCESS_KEY, SECRET_KEY)
    bucket = BucketManager(q)
    ret, eof, info = bucket.list(BUCKET_NAME)
    if info.status_code == 200:
        file_list = ujson.loads(info.text_body)['items']
        if len(filter_str) != 0:
            for i in filter_str:
                file_list = [itm for itm in file_list if i in itm['key']]
            return True, file_list
        else:
            return True, file_list
    else:
        return False, None



def data_handle(file_name, saved_name, handle_method):
    pipeline = 'lyf'
    q = Auth(ACCESS_KEY, SECRET_KEY)
    pfop = PersistentFop(q, BUCKET_NAME, pipeline)
    op = op_save(handle_method, BUCKET_NAME, saved_name)
    ops = []
    ops.append(op)
    ret, info = pfop.execute(file_name, ops, 1)
    print(info)
