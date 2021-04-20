import pandas as pd 
from functools import reduce
import operator
import requests
import json

def getgetFromDict(diccionario,mapa):

    """

    In this function we create, firstly, three lists to get the name, latitude and longitude of every company from our collection.
    We use a reduce function to get it.

    """
    mapa_nombre_comp =  ["name"]
    mapa_latitud_comp = ["offices", "latitude"]
    mapa_longitud_comp = ["offices", "longitude"]
    return reduce(operator.getitem,mapa,diccionario)

mapa_nombre_comp =  ["name"]
mapa_latitud_comp = ["offices", 0, "latitude"]
mapa_longitud_comp = ["offices", 0, "longitude"]

def createList(json_companies):

    """
    
    In this function we begin creating an empty list which will be filled with dictionaries containing, among other, 
    the variables "name", "latitud" and "longitud" for every company
    extracted with the previous function inside this one.

    Afterwards, in the second part of the function, we create another empty list, which will be filled, through a for loop, with a "Type Point" to "register" 
    the coordinates of every company. Finally, we get a DataFrame from it and, immediately, we convert it to a json file and add it to our MongoDB collection.

    """
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