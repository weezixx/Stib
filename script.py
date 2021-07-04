import pycurl
import requests
import base64
import json

# TODO : faire la différence entre le temps affiché et actuel (real time)


def encode(message):

    message_bytes = message.encode('ascii')

    base64_bytes = base64.b64encode(message_bytes)

    base64_message = base64_bytes.decode('ascii')

    #print(base64_message)
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


message = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/MessageByLine/8031'

time = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/1746'

#url = 'https://opendata-api.stib-mivb.be/NetworkDescription/4.0/PassingTimeByPoint/8031'

headers = {'Accept': 'application/json','Authorization':'Bearer  80e5da470868266c4ac70c269f6fc02f '}

#headers = {"grant_type":"client_credentials","Authorization":"Basic "+consumer_key_64+":"+consumer_secret_64",'https://opendata-api.stib-mivb.be/token'}

resp = requests.get(time,headers=headers)

info = requests.get(message,headers=headers)

#req_json = requests.get(url, headers=headers)

#req_python = json.loads(req_json.text)

get = resp.text

print(resp.text)

print(info.text)

get = json.loads(resp.text)

# numéro de ligne + destination
print(get['points'][0]['passingTimes'][0]['lineId'], get['points'][0]['passingTimes'][0]['destination']['fr'])
print(get['points'][0]['passingTimes'][0]['expectedArrivalTime'])

print(get['points'][1]['passingTimes'][0]['lineId'], get['points'][1]['passingTimes'][0]['destination']['fr'])
print(get['points'][1]['passingTimes'][0]['expectedArrivalTime'])

print(len(get))

t = requests.get(url_token,headers)

#print(t)
