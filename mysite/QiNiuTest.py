# -*- conding:utf-8 -*-

from qiniu import Auth, put_file, etag
import qiniu

access_key = '51t_4P-smSqNL53ufWbLNp_GWwLuSdexWgsywXCZ'
secret_key = 'YJhGt1VkvQc9z6q2Y3UhgdaIh6oPPrvGjaJ1DDGD'

q = Auth(access_key, secret_key)

bucket_name = 'jdoe'

key = 'mysite.jpg'

token = q.upload_token(bucket_name, key, 3600)

localfile = '/home/kameng/Projects/mysite/mysite/static/images/OIP.jpg'

ret, info = put_file(token, key, localfile)
print(info)

