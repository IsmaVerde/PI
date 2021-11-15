import pandas as pd
import numpy as np
import requests as rq
from apis.exceptions import APIRequestException
import json
from os import path

# Código para construir un DataFrame con la información de los 250 países
# del API Restcountries

# Al final no usé la librería python porque creo que es más sencillo
# meter directamente el JSON en Pandas para crear las Series

base_url = "https://restcountries.eu/rest/v2/"
#base_url = "http://mrworldwide.proxy/restcountries/rest/v2/"

def stringListToString(inputlist):
    ret = ""
    for item in inputlist:
        ret = ret + str(item) + ", "

    return ret[0:-2]

def jsonToSeries(pais):
    # Identificamos la Serie correspondiente a cada país por su código ISO de 3 caracteres
    # Así es sencillo luego usarlos en la api del worldbank porque usa los mismos códigos
    serie_pais = pd.Series(data=pais, name=pais['alpha3Code'])
    serie_pais.drop("alpha3Code", inplace=True)

    # También cambiamos el campo "name" a "countryName" porque "name" es el nombre de la propia Serie
    serie_pais.rename(index={'name': 'countryName'}, inplace=True)

    #El TLD viene como una lista de un solo elemento
    #Solo hay un par de regiones que tienen 2 TLDs. Para esas almacenamos solo el primero
    serie_pais.topLevelDomain = serie_pais.topLevelDomain[0]

    #Solo hay 3 regiones que tienen más de un prefijo telefónico
    #Para esas, almacenamos un string en lugar de una string list
    serie_pais.callingCodes = stringListToString(serie_pais.callingCodes)

    #De las monedas en curso nos quedamos solo con el nombre de la principal
    serie_pais.currencies = serie_pais.currencies[0]['name']

    #De los idiomas nos quedamos solo con el nombre, y los guardamos como
    #un solo string
    serie_pais.languages = stringListToString([x['name'] for x in serie_pais.languages])

    #Las traducciones las vamos a ignorar ya que añaden complicación al DataFrame innecesariamente
    serie_pais.drop("translations", inplace=True)

    #De los bloques regionales igual, nos quedamos solo con los nombres como un string
    serie_pais.regionalBlocs = stringListToString([x['name'] for x in serie_pais.regionalBlocs])

    #Los nombres alternativos igual
    serie_pais.altSpellings = stringListToString(serie_pais.altSpellings)

    #Las coordenadas igual
    serie_pais.latlng = stringListToString(serie_pais.latlng)

    #Las zonas horarias
    serie_pais.timezones = stringListToString(serie_pais.timezones)

    #Las fronteras
    # serie_pais.borders = stringListToString(serie_pais.borders)

    #Por último, cambio los valores vacíos, nulos o "NaN" por el string "N/A"
    return serie_pais.replace(["", " ", None, np.nan], "N/A")

#Esta función siempre devuelve un DataFrame de una sola fila, ya que el código ISO3
#es único. Para sacar la Serie correspondiente, basta con hacer .iloc[0] sobre el DataFrame
######
######  IMPORTANTE
######
"""
Durante el último día de testing del proyecto, la API restcountries.eu empezó
a dar problemas, timeouts y errores 500. Por este motivo, decidimos
descargarnos a local el fichero restcountries_all.json y reescribir las funciones
para que usasen ese fichero
"""
"""
def get_countries_by_name(name):
    resp = rq.get(base_url+"name/"+name)

    if (resp.status_code > 400):
        raise APIRequestException("HTTP Error")

    return pd.concat([jsonToSeries(pais) for pais in resp.json()], axis=1).transpose()
"""
"""
def get_country_by_code(code):
    resp = rq.get(base_url+"alpha/"+code)

    if (resp.status_code > 400):
        raise APIRequestException("HTTP Error")

    return pd.concat([jsonToSeries(resp.json())], axis=1).transpose()
"""
"""
def get_all_countries():
    resp = rq.get(base_url+"all")
    if (resp.status_code > 400):
        raise APIRequestException("HTTP Error")

    data = resp.json()

    return pd.concat([jsonToSeries(pais) for pais in data], axis=1).transpose()
"""

def get_countries_by_name(name):
    allc = get_all_countries()
    return allc.loc[allc.countryName == name]

def get_country_by_code(code):
    return get_all_countries().loc[code].to_frame().transpose()

def get_jsonfile_path():
    current_path = path.dirname(path.abspath(__file__))
    return path.join(current_path,"restcountries_all.json")

def get_all_countries():    
    with open(get_jsonfile_path()) as f:
        data = json.load(f)
        
    return pd.concat([jsonToSeries(pais) for pais in data], axis=1).transpose()

def get_all_names():
    return get_all_countries().countryName.to_list()

def get_iso3code(name):
    return get_countries_by_name(name).iloc[0].name

def get_name_from_iso3(code):
    return get_country_by_code(code).iloc[0].countryName
