import pandas as pd 
import requests
import json
from dotenv import load_dotenv
from functools import reduce
import operator
import os
import folium
from folium import Choropleth, Circle, Marker, Icon, Map

tok1 = os.getenv("tok1")
tok2 = os.getenv("tok2")

def Geoquery(coord, topic, tok1, tok2):

    city = {'type': 'Point', 'coordinates': coord}
    url_query = 'https://api.foursquare.com/v2/venues/explore'
    parametros = {
        "client_id": tok1,
        "client_secret": tok2,
        "v": "20180323",
        "ll": f"{city.get('coordinates')[0]},{city.get('coordinates')[1]}",
        "query": topic, 
        "limit": 100    
    }

    resp = requests.get(url= url_query, params = parametros).json()
    data = resp.get("response").get("groups")[0].get("items")
    mapa_nombre = ["venue", "name"]
    mapa_latitud = ["venue", "location", "lng"]
    mapa_longitud = ["venue", "location", "lat"]

    def getFromDict(diccionario,mapa):
        mapa_nombre = ["venue", "name"]
        mapa_latitud = ["venue", "location", "lng"]
        mapa_longitud = ["venue", "location", "lat"]
    
        return reduce(operator.getitem,mapa,diccionario)

    empty_list = []
    for dic in data:
        paralista = {}
        paralista["name"] = getFromDict(dic, mapa_nombre)
        paralista["latitud"]= getFromDict(dic, mapa_latitud)
        paralista["longitud"] = getFromDict(dic,mapa_longitud)
        empty_list.append(paralista)
    

    documents = []
    for dicc_1 in empty_list:
        temporal = {
         "name": dicc_1.get("name"),
        "location": {"type": "Point", "coordinates": [dicc_1.get("latitud"), dicc_1.get("longitud")]},
        }
        documents.append(temporal)
    city_venues = pd.DataFrame(documents)
    city_venues["place"] = topic
    city_venues.head()
    return city_venues.to_json(f"{topic}_venues_sf.json", orient="records")







def creatingPlaces(coordinates, distance, collection, city):
    coord_point = {"type":"Point", "coordinates": coordinates}
    query = {"location": {"$near": {"$geometry": coord_point,"$minDistance": 0  , "$maxDistance": distance}}}
    query_final = list(collection.find(query))
    city = pd.DataFrame(query_final)
    latitude = [lat["location"]["coordinates"][1] for lat in query_final]
    longitude = [long["location"]["coordinates"][0] for long in query_final]

    #De aquí añadimos las listas que nos interesen al DataFrame de la ciudad de San Francisco.
    city["latitude"] = latitude
    city["longitude"] = longitude


    city = city[city["latitude"].notna()]
    city = city[city["longitude"].notna()]
    
    return city

def creatingMap(coordinates, distance, collection, city, coord):
    coord_point = {"type":"Point", "coordinates": coordinates}
    query = {"location": {"$near": {"$geometry": coord_point,"$minDistance": 0  , "$maxDistance": distance}}}
    query_final = list(collection.find(query))
    city = pd.DataFrame(query_final)

    latitude = [lat["location"]["coordinates"][1] for lat in query_final]
    longitude = [long["location"]["coordinates"][0] for long in query_final]

    #De aquí añadimos las listas que nos interesen al DataFrame de la ciudad de San Francisco.
    city["latitude"] = latitude
    city["longitude"] = longitude


    city = city[city["latitude"].notna()]
    city = city[city["longitude"].notna()]

    final_companies = city[city["place"] == "company"]

    map_1 = folium.Map(location = coord, zoom_start = 15)
    for i, row in final_companies.iterrows():
        distrito = {
            "location":[row["latitude"], row["longitude"]],
            "tooltip": [row["name"]]}
        icon = Icon(color = "red",
                    prefix = "fa",
                    icon = "map-pin",
                    icon_color = "black")
        
        Marker(**distrito,icon = icon ).add_to(map_1)
        
    return map_1, 
   