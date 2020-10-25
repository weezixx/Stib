import pycurl
import requests
import base64


def encode(message):

    message_bytes = message.encode('ascii')

    base64_bytes = base64.b64encode(message_bytes)

    base64_message = base64_bytes.decode('ascii')

    print(base64_message)



url_token = "https://opendata-api.stib-mivb.be/token"

consumer_key = " xptyNr3nnlk2hzxInUpOQUD3SAka "

consumer_key_64 = str(encode(consumer_key))

consumer_secret = "kucY0Z71BKyubZxJPPQFQMeWhn0a"

consumer_secret_64 = str(encode(consumer_secret))

headers = {"grant_type":"client_credentials","Authorization":"Basic "+consumer_key_64+":"+consumer_secret_64}

#data = "grant_type":"client_credentials","Authorization" : "Basic BASE64KEY+:+SECRET""

t = requests.get(url_token,headers)

#print(t)

message = "https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/MessageByLine/53"

waiting_time = "https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/53"

position = "https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/VehiclePositionByLine/53"

headers = {"Authorization" : "Bearer 46996cf0b7bcccea99ad7b846d887b72"}


r = requests.get(waiting_time, headers = headers).json()

print(r)








