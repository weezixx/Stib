import pycurl
import requests
import base64
import json

# TODO : faire la différence entre le temps affiché et actuel (real time)




bonaventure = [1755,1746,1768,1711,1680]



accessKeys = 'GFlpfof6tMWyLC6HwUeonUwV43Ua:DMYHLByDdb0rcBOxSdXwVx8zrSYa'

# conversion de accessKeys en base64
base64AccessKeys=base64.b64encode(accessKeys.encode('ascii')).decode('ascii')

# headers pour la requete HTTP
headers={ 'Authorization': 'Basic ' + base64AccessKeys }

# demande du bearer token
reponse = requests.post('https://opendata-api.stib-mivb.be/token', headers=headers, data='grant_type=client_credentials')

# affichage de la réponse à la demande, elle contient le bearer token à utiliser pour la suite
print(reponse.text)
bearerToken=reponse.json()['access_token']

# nouveau headers à utiliser pour les autres requêtes
headers={ 'Authorization': 'Bearer ' + bearerToken }



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
