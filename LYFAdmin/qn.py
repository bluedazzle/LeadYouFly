# -*- coding: utf-8 -*-
from qiniu import Auth
from qiniu import put_data
from qiniu import BucketManager, PersistentFop, build_op, op_save
from qiniu.services.storage.uploader import put_stream, _form_put
from qiniu.utils import file_crc32

import time
import ujson
import os

ACCESS_KEY = 'yNkIkBJv92stxKg8yNs2n1wcOiaqPE7wy0ZyGdwy'
SECRET_KEY = 'U8EitYYdhQ4_9hxvQuR6z0mPjnj5IDzovo81pqN7'
BUCKET_NAME = 'leadyoufly'
QINIU_DOMAIN = 'http://7xkveq.com2.z0.glb.qiniucdn.com/'

VIDEO_CONVERT_PARAM = 'avthumb/mp4'
VIDEO_POSTER_PARAM = 'vframe/jpg/offset/5/w/900/h/500'


def upload_file_qn(ufile, file_name, sign='default'):
    full_name = sign + '_' + file_name
    full_name = full_name.decode('utf-8')
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME)
    ret, info = put_data(token, full_name, ufile)
    if info.status_code == 200:
        return True, ujson.loads(info.text_body)['key']
    else:
        return False, info


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
        return False, info



def data_handle(file_name, saved_name, handle_method):
    pipeline = 'lyf'
    q = Auth(ACCESS_KEY, SECRET_KEY)
    pfop = PersistentFop(q, BUCKET_NAME, pipeline)
    op = op_save(handle_method, BUCKET_NAME, saved_name)
    ops = []
    ops.append(op)
    ret, info = pfop.execute(file_name, ops, 1)
    if info.status_code == 200:
        return True, info.text_body
    else:
        return False, info


def delete_data(file_name):
    q = Auth(ACCESS_KEY, SECRET_KEY)
    bucket = BucketManager(q)
    ret, info = bucket.delete(BUCKET_NAME, file_name)
    if info.status_code == 200:
        return True, info.text_body
    else:
        return False, info.text_body


def put_block_data(key, file_data, params=None, mime_type='application/octet-stream', check_crc=False,
                   progress_handler=None, sign='default'):
    """上传分片二进制流到七牛
    Args:
        key:              上传文件名
        file_path:        上传文件的路径
        params:           自定义变量，规格参考 http://developer.qiniu.com/docs/v6/api/overview/up/response/vars.html#xvar
        mime_type:        上传数据的mimeType
        check_crc:        是否校验crc32
        progress_handler: 上传进度
        upload_progress_recorder: 记录上传进度，用于断点续传
    Returns:
        一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
        一个ResponseInfo对象
    """
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME)
    full_name = sign + '_' + key
    ret = {}
    size = file_data.size
    if size > 1024 * 1024 * 8:
        ret, info = put_stream(token, full_name, file_data, size, params,
                               mime_type, progress_handler)
    else:
        return upload_file_qn(file_data, key, sign)
    if info.status_code == 200:
        return True, ujson.loads(info.text_body)['key']
    return False, info


