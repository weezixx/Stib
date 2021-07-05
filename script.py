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

bonaventure = [1755,1746,1768,1711]


url_token = "https://opendata-api.stib-mivb.be/token"

consumer_key = "xptyNr3nnlk2hzxInUpOQUD3SAka"
#
consumer_key_64 = str(encode(consumer_key))
#
consumer_secret = "kucY0Z71BKyubZxJPPQFQMeWhn0a"
#
consumer_secret_64 = str(encode(consumer_secret))
#req_json = requests.get(url, headers=headers)
# print(resp.text)

# print(info.text)
#headers = {"grant_type":"client_credentials","Authorization":"Basic "+consumer_key_64+":"+consumer_secret_64",'https://opendata-api.stib-mivb.be/token'}

headers = {'Accept': 'application/json','Authorization':'Bearer  bfecc8937563333da081e38e5981baff '}

for i in bonaventure:

    message = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/MessageByLine/' + str(i)

    time = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/' + str(i)

    resp = requests.get(time,headers=headers)

    info = requests.get(message,headers=headers)

    get = resp.text

    print(get)

    get = json.loads(resp.text)

# numéro de ligne + destination
# print(get['points'][0]['passingTimes'][0]['lineId'], get['points'][0]['passingTimes'][0]['destination']['fr'])
# print(get['points'][0]['passingTimes'][0]['expectedArrivalTime'])
#
# print(get['points'][0]['passingTimes'][0]['lineId'], get['points'][0]['passingTimes'][1]['destination']['fr'])
# print(get['points'][0]['passingTimes'][1]['expectedArrivalTime'])

    print(len(get))


    for j in range(len(get)+1):

        print(get['points'][0]['passingTimes'][j]['lineId'], get['points'][0]['passingTimes'][j]['destination']['fr'])
        print(get['points'][0]['passingTimes'][j]['expectedArrivalTime'])
