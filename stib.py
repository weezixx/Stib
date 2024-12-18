#import pycurl
from http.client import responses

import requests
import base64
import json
from datetime import datetime

arrets = ["https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22UZ-VUB%22&limit=100&refine=pointid%3A1755",
          "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DE%20BERCHEM%22&limit=20&refine=pointid%3A1746",
          "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22ETANG%20NOIR%22&limit=20&refine=pointid%3A1746",
          "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DU%20NORD%22&limit=100&refine=pointid%3A1768",
          "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GROOT-BIJGAARDEN%22&limit=100&refine=pointid%3A1680"]

id_client = "d05070c0ca9a4c70b39e756102fa7aaf"

client_secret = "aad935215db54b858dabcef022472d9a"


data = {
  "grant_type": "weezixx@hotmail.com",
  "client_id": "d05070c0ca9a4c70b39e756102fa7aaf",
  "client_secret": "aad935215db54b858dabcef022472d9a"
}

api_key = {}

api_key['Authorization'] = f'Basic {str(base64.b64encode((id_client + ":" + client_secret).encode("utf-8")), "utf-8")}'

session = requests.session()

params = {
    'apikey': '736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62'
}

headers = {'user-agent': 'pyStibHa (weezixx@hotmail.com)'}


for i in range(4):

    response = session.get(url=arrets[i], params=params, headers=headers)
    response = response.json()
    response = json.dumps(response, indent=2)

    data = json.loads(response)

    data = data['results']

    data2 = json.loads(data[0]['passingtimes'])


    temps1 = data2[0]["expectedArrivalTime"]
    temps2 = data2[1]["expectedArrivalTime"]

    ligne = data2[0]["lineId"]

    dest = data2[0]["destination"]["fr"]

    start1 = temps1.find("T") + 1
    start2 = temps2.find("T") + 1

    end1 = temps1.find("+")
    end2 = temps2.find("+")

    temps1 = temps1[start1:end1]
    temps2 = temps2[start2:end2]

    heure1,minute1,seconde1 =temps1.split(":")
    heure2, minute2, seconde2 = temps2.split(":")

    rightnow = datetime.now()

    interval1 = datetime(year=rightnow.year,month=rightnow.month,day=rightnow.day,hour=int(heure1), minute=int(minute1), second=int(seconde1)) - rightnow
    interval2 = datetime(year=rightnow.year, month=rightnow.month, day=rightnow.day, hour=int(heure2),minute=int(minute2), second=int(seconde2)) - rightnow


    print(ligne," destination : ",dest,":",round(interval1.seconds/60), round(interval2.seconds / 60))