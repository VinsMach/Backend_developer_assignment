#!/usr/bin/env python


from flask import Flask
from flask_jsonrpc import JSONRPC
from flask import request

import json
from math import sin, cos, sqrt, atan2, radians
import array
import wget
import os

app = Flask(__name__)

filePath = '/root/flask-jsonrpc/Elenco-Farmacie.geojson';
jsonrpc = JSONRPC(app, '/', enable_web_browsable_api=True)
if os.path.exists(filePath):
    os.remove(filePath)
url = "https://dati.regione.campania.it/catalogo/resources/Elenco-Farmacie.geojson"
filename = wget.download(url)

@jsonrpc.method('SearchNearestPharmacy')
def index(currentLocation,range,limit):
    R = 6373.0
    result = []
    totale_risultati = 0
    with open(filename) as json_file:
        data = json.load(json_file)
        for p in data['features']:
            lat1 = radians(p['geometry']['coordinates'][1])
            lon1 = radians(p['geometry']['coordinates'][0])
            lat2 = radians(currentLocation['latitude'])
            lon2 = radians(currentLocation['longitude'])

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = round(R * c)
            if distance < range:
                location_in = {'latitude': p['geometry']['coordinates'][1], 'longitude':p['geometry']['coordinates'][0]}
                info = {'name':p["properties"]["Descrizione"] , 'distance': distance, 'location': location_in}

                result.append(info)

    result.sort(key=myFunc)
    return {'pharmacies': result[:limit]}

def myFunc(e):
  return e['distance']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
                                                      
