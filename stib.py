#import pycurl
from http.client import responses

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

# 1755 = 14 -> UZ => https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22UZ-VUB%22&limit=100&refine=pointid%3A1755

# 1746 = 83 -> Berchem => https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DE%20BERCHEM%22&limit=20&refine=pointid%3A1746
#
# 1746  13 -> Étang noir => https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22ETANG%20NOIR%22&limit=20&refine=pointid%3A1746

# 1768 = 14 -> Gare du Nord => https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DU%20NORD%22&limit=100&refine=pointid%3A1768

# 1680 = 9 -> Grand Bigard => https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GROOT-BIJGAARDEN%22&limit=100&refine=pointid%3A1680

id_client = "d05070c0ca9a4c70b39e756102fa7aaf"

client_secret = "aad935215db54b858dabcef022472d9a"


accessKeys = '736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62'

# conversion de accessKeys en base64
base64AccessKeys=base64.b64encode(accessKeys.encode('ascii')).decode('ascii')

data = {
  "grant_type": "weezixx@hotmail.com",
  "client_id": "d05070c0ca9a4c70b39e756102fa7aaf",
  "client_secret": "aad935215db54b858dabcef022472d9a"
}
# headers={ 'Authorization': "736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62" }

api_key = {}

api_key['Authorization'] = f'Basic {str(base64.b64encode((id_client + ":" + client_secret).encode("utf-8")), "utf-8")}'

#url = 'https://stibmivb.opendatasoft.com/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/'

url = "https://stibmivb.opendatasoft.com/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?limit=100"

url2 = "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DE%20BERCHEM%22&limit=20&refine=pointid%3A1746"

session = requests.session()

params = {
    'apikey': '736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62'
}

headers = {'user-agent': 'pyStibHa (weezixx@hotmail.com)'}

response = session.get(url=url2, params=params, headers=headers)

response = response.json()

# response = requests.get("https://stibmivb.opendatasoft.com/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?limit=100",headers = headers, data='grant_type=client_credentials')
print("réponse de la réponse : ",json.dumps(response, indent=2))
response2 = requests.get(url2,
                        auth=requests.auth.HTTPBasicAuth(
                            id_client, client_secret))

# print("réponse de la réponse2 : ",response2.text)


# url = "https://stibmivb.opendatasoft.com/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?limit=100"
#
# # demande du bearer token
# reponse = requests.get(url, headers=headers, data='grant_type=client_credentials')
#
# test = requests.get(response, headers=headers)
#
# get = test.text
#
# print(get)

# affichage de la réponse à la demande, elle contient le bearer token à utiliser pour la suite
#print(reponse.text)
# bearerToken=response.json()['access_token']
#
# # nouveau headers à utiliser pour les autres requêtes
# headers={ 'Authorization': 'Bearer ' + bearerToken }

transport = {}

#Faire un dico avec les valeurs de chaque arret ?

# def arret(i):
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
#
#     for j in get['points'][0]['passingTimes']:
#         # print(j['lineId'],j['destination']['fr'])
#         # print(j['expectedArrivalTime'])
#         # print(until(j['expectedArrivalTime']))
#         texte += str(j['lineId']) + " " + str(j['destination']['fr']) + " " + str(until(j['expectedArrivalTime']))+"\n"
#     return texte
#
# print(arret(1746))
