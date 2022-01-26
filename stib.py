import pycurl
import requests
import base64
import json
import datetime

# TODO : faire la différence entre le temps affiché et actuel (real time)

now = datetime.datetime.now()

def until(temps):
    obj = datetime.datetime.strptime(temps, "%Y-%m-%dT%H:%M:%S%z")
    temps_stib = datetime.datetime(obj.year, obj.month, obj.day,obj.hour, obj.minute, obj.second)
    temps_present = datetime.datetime(now.year, now.month, now.day,now.hour, now.minute, now.second)
    td = temps_stib - temps_present
    td = td.total_seconds()
    td /= 60
    # print("temps restant : ",int(td))
    return  int(td)

bonaventure = [1755,1746,1768,1711,1680]


accessKeys = 'GFlpfof6tMWyLC6HwUeonUwV43Ua:DMYHLByDdb0rcBOxSdXwVx8zrSYa'

# conversion de accessKeys en base64
base64AccessKeys=base64.b64encode(accessKeys.encode('ascii')).decode('ascii')

# headers pour la requete HTTP
headers={ 'Authorization': 'Basic ' + base64AccessKeys }

# demande du bearer token
reponse = requests.post('https://opendata-api.stib-mivb.be/token', headers=headers, data='grant_type=client_credentials')

# affichage de la réponse à la demande, elle contient le bearer token à utiliser pour la suite
#print(reponse.text)
bearerToken=reponse.json()['access_token']

# nouveau headers à utiliser pour les autres requêtes
headers={ 'Authorization': 'Bearer ' + bearerToken }

transport = {}

# for i in bonaventure:
#
#     message = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/MessageByLine/' + str(i)
#
#     time = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/' + str(i)
#
#     resp = requests.get(time,headers=headers)
#
#     info = requests.get(message,headers=headers)
#
#     get = resp.text
#
#     #print(get)
#
#     get = json.loads(resp.text)
#
#     texte = ""
#     valeur = 0
#
#     for j in get['points'][0]['passingTimes']:
#         # print(j['lineId'],j['destination']['fr'])
#         #print(j['expectedArrivalTime'])
#         # print(until(j['expectedArrivalTime']))
#         texte += str(j['lineId']) + " " + str(j['destination']['fr']) + " " +str(until(j['expectedArrivalTime'])) + "\n"
#     transport[valeur] = texte
#
#     valeur +=1
#     print(transport)

#Faire un dico avec les valeurs de chaque arret ?

def arret(i):

    message = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/MessageByLine/' + str(i)

    time = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/' + str(i)

    resp = requests.get(time,headers=headers)

    info = requests.get(message,headers=headers)

    get = resp.text

    #print(get)

    get = json.loads(resp.text)

    texte = ""

    for j in get['points'][0]['passingTimes']:
        # print(j['lineId'],j['destination']['fr'])
        # print(j['expectedArrivalTime'])
        # print(until(j['expectedArrivalTime']))
        texte += str(j['lineId']) + " " + str(j['destination']['fr']) + " " + str(until(j['expectedArrivalTime']))+"\n"
    return texte

print(arret(1746))
