"""
    Código básico para ir extrayendo datos de AQICN y cargándolos en estructuras de Pandas
    La idea es que luego esto lo copiemos ya dentro del proyecto de Django cuando tengamos
    claro el sitio donde copiarlo

"""

import pandas as pd
import numpy as np
import requests as rq
from apis.exceptions import APIRequestException

base_url = "https://api.waqi.info/"
#base_url = "http://mrworldwide.proxy/aqicn/"
token = "b7818feb850f1306340bd0465824027131b20af8"

datos_posibles = ["co", "dew", "h", "no2", "o3", "p", "pm10", "pm25", "r", "so2", "t", "w", "wg"]

# Obtener los datos de una ciudad
# Esta función acepta una ciudad (string)
# y devuelve un DataFrame que contiene los datos de polución
# del aire disponibles para esa ciudad

def get_datos_ciudad(ciudad):
    resp = rq.get(base_url+"feed/"+ciudad+"/?token="+token)

    if (resp.status_code > 400) or (resp.json()['status'] != "ok"):
        raise APIRequestException("HTTP Error")

    try:
        datos_ciudad = resp.json()['data']['iaqi']
    except ValueError:
        raise Exception("JSON Decode Error")

    #Extraemos los valores que nos devuelve la API, y los que no, los rellenamos con "N/A"

    serie_ciudad = pd.Series(datos_ciudad).apply(lambda x: x['v']).reindex(datos_posibles).fillna("N/A")
    serie_ciudad.name = ciudad

    df = pd.concat([serie_ciudad],axis=1).transpose()
    df.index.name = "Ciudad"
    df.columns.name = "Indicadores"
    return df


def get_datos_coords(lat=None, lon=None):
    if lat is None or lon is None:
        raise ValueError("No se indicaron coordenadas")

    resp = rq.get(base_url+"feed/geo:"+str(lat)+";"+str(lon)+"/?token="+token)

    if (resp.status_code > 400) or (resp.json()['status'] != "ok"):
        raise APIRequestException("HTTP Error")

    jsondata = resp.json()
    datos_loc = jsondata['data']['iaqi']
    nombre_loc = jsondata['data']['city']['name']

    serie = pd.Series(datos_loc).apply(lambda x: x['v']).reindex(datos_posibles).fillna("N/A")
    serie.name = nombre_loc

    df = pd.concat([serie],axis=1).transpose()

    df.index.name = "Ciudad"
    df.columns.name = "Indicadores"
    return df
