import jwt
import time


key = "swordoly"
# exp = time.time() + 7*24*60*60 #一周后过期

# token = jwt.encode(payload=payload, key=key, algorithm='HS256').decode('utf-8')

def encode(payload) ->str:
    return jwt.encode(payload=payload, key=key, algorithm='HS256')

def decode(token):
    return jwt.decode(token,key,'HS256')