from qiniu import Auth
from qiniu import put_file

ACCESS_KEY = 'yNkIkBJv92stxKg8yNs2n1wcOiaqPE7wy0ZyGdwy'
SECRET_KEY = 'U8EitYYdhQ4_9hxvQuR6z0mPjnj5IDzovo81pqN7'
BUCKET_NAME = 'leadyoufly'

q = Auth(ACCESS_KEY, SECRET_KEY)

localfile = '/var/temp/sk.wav'
key = 'test_file.wav'
mime_type = "application/octet-stream"

token = q.upload_token(BUCKET_NAME, key)
ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
print(info)
assert ret['key'] == key
