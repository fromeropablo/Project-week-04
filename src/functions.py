import pandas as pd 
from functools import reduce
import operator
import requests
import json

def getgetFromDict(diccionario,mapa):
    mapa_nombre_comp =  ["name"]
    mapa_latitud_comp = ["offices", "latitude"]
    mapa_longitud_comp = ["offices", "longitude"]
    return reduce(operator.getitem,mapa,diccionario)

mapa_nombre_comp =  ["name"]
mapa_latitud_comp = ["offices", 0, "latitude"]
mapa_longitud_comp = ["offices", 0, "longitude"]

def createList(json_companies):
    companies_list = []
    for dic in json_companies:
        paralista = {}
        paralista["name"] = getgetFromDict(dic, mapa_nombre_comp)
        paralista["latitud"]= getgetFromDict(dic, mapa_latitud_comp)
        paralista["longitud"] = getgetFromDict(dic,mapa_longitud_comp)
        companies_list.append(paralista)
    
    documents = []
    for diccionario in companies_list:
        temporal = {
        "name": diccionario.get("name"),
        "location": {"type": "Point", "coordinates": [diccionario.get("latitud"), diccionario.get("longitud")]},
        }
        documents.append(temporal)
    companies_venues = pd.DataFrame(documents)
    companies_venues["place"] = "company"
    return companies_venues.to_json("companies_venues.json", orient="records")