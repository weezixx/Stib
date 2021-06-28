import pycurl
import requests
import base64
import json


def encode(message):

    message_bytes = message.encode('ascii')

    base64_bytes = base64.b64encode(message_bytes)

    base64_message = base64_bytes.decode('ascii')

    print(base64_message)
#
#
#
url_token = "https://opendata-api.stib-mivb.be/token"

consumer_key = "xptyNr3nnlk2hzxInUpOQUD3SAka"
#
consumer_key_64 = str(encode(consumer_key))
#
consumer_secret = "kucY0Z71BKyubZxJPPQFQMeWhn0a"
#
consumer_secret_64 = str(encode(consumer_secret))
#
# headers = {"grant_type":"client_credentials","Authorization":"Basic "+consumer_key_64+":"+consumer_secret_64}
#
#
# res = requests.get(url)
#
# resp = requests.get(url,headers=headers)
#
# print(resp)
#
# t = requests.get(url_token,headers)

message = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/MessageByLine/8031'

url = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/MessageByLine/1746'

#url = 'https://opendata-api.stib-mivb.be/NetworkDescription/4.0/PassingTimeByPoint/8031'

headers = {'Accept': 'application/json','Authorization':'Bearer 546d53924a629d1642512373700690e6'}

#headers = {"grant_type":"client_credentials","Authorization":"Basic "+consumer_key_64+":"+consumer_secret_64",'https://opendata-api.stib-mivb.be/token'}

resp = requests.get(message,headers=headers)

#req_json = requests.get(url, headers=headers)

#req_python = json.loads(req_json.text)

print(resp.text)

t = requests.get(url_token,headers)

print(t)
