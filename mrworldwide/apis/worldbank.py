"""
   Código para extraer datos del API de Worldbank y cargarlos en estructuras de datos de Pandas
"""

# # https://datahelpdesk.worldbank.org/knowledgebase/topics/1255


import pandas as pd
import numpy as np
import requests as rq
from os import path
from apis.exceptions import APIRequestException

base_url = "http://api.worldbank.org/"

indicators_url = base_url+"v2/indicator"
countries_url = base_url+"v2/country"
topics_url = base_url+"v2/topic"

# Devueve un dataframe con información sobre los distintos temas que trata
# el índice es el "id" del tema, y los atributos son el nombre y una descripción

def get_topics_list():
    resp = rq.get(topics_url+"?format=json&per_page=100")

    if resp.status_code > 400:
       raise APIRequestException("HTTP Error")

    try:
        jsondata = resp.json()[1] #Dejo la primera entrada porque es información de paginación
    except ValueError:
        raise APIRequestException("JSON Decode failed")

    series_temas = [(pd.Series(data=tema, name=tema['id']).drop("id")) for tema in jsondata]

    dataframe_temas = pd.concat(series_temas, axis=1).transpose()
    dataframe_temas.index.name = "id"
    dataframe_temas.columns = ["topicName", "description"]

    return dataframe_temas


# Devuelve un dataframe con los IDs, nombres y descripciones de todos los indicadores de un tema
# Se espera que se pase el ID del tema (obtenido a través de la anterior función)
def get_indicators_from_topic(topic):
    resp = rq.get(topics_url+"/"+topic+"/indicator"+"?format=json&per_page=20000")

    if resp.status_code > 400:
        raise APIRequestException("HTTP Error")

    try:
        jsondata = resp.json()[1]
    except ValueError:
        raise APIRequestException("JSON Decode failed")

    series_indics = []

    for indic in jsondata:
        # Creamos la serie y ponemos el ID como nombre de la serie
        serie = pd.Series(data=indic, name=indic['id']).drop("id")

        # Renombramos a indicatorName para evitar confusiones
        serie.rename(index={'name': 'indicatorName'}, inplace=True)

        # Sacamos los "topics" ya que no van a hacernos falta
        # (ya sabíamos el topic para pedir el indicador)
        serie.drop("topics", inplace=True)

        # Separamos el "source" que es un diccionario en sus campos "sourceID" y "SourceName"
        tsourceID = serie.source['id']
        tsourceName = serie.source['value']
        serie.drop("source", inplace=True)

        # Y reindexamos para tenerla ordenada
        serie = serie.reindex(
            pd.Index(data=
                     ["indicatorName", "unit", "sourceID",
                      "sourceName", "sourceNote", "sourceOrganization"]))

        serie.sourceID = tsourceID
        serie.sourceName = tsourceName

        # La añadimos a la lista

        series_indics.append(serie)

    # Montamos el DataFrame
    dataframe_indicadores = pd.concat(series_indics, axis=1).transpose()
    dataframe_indicadores.index.name = "indicatorID"

    return dataframe_indicadores


# Esta función devuelve un dataframe con los valores asociados al indicador en el país indicados,
# organizados de forma que cada columna del dataframe corresponde a un período de tiempo.
# Los nombres de las columnas indican el periodo al que se refiere (p.e: 2018, 2019, 2020...)
# Las filas dependen del indicador en cuestión, pero hay siempre una fila "value" que tiene
# el valor en crudo

# Opcionalmente podemos pasarle un objeto de sesión para que las consultas usen un socket
# ya establecido, en lugar de crear uno nuevo cada vez.

def get_indicator(country, indicator, session=None):
    if session is None:
        resp = rq.get(countries_url+"/"+country+"/indicator/"+indicator+"?format=json&per_page=500")
    else:
        resp = session.get(countries_url+"/"+country+"/indicator/"+indicator+"?format=json&per_page=500")

    if resp.status_code > 400:
        raise APIRequestException("HTTP Error")

    try:
        jsondata = resp.json()[1]
        if jsondata is None:
            raise APIRequestException("No data was returned")
        jsondata.reverse() # La API los entrega de más reciente a más antiguo
    except (ValueError, IndexError, TypeError):
        raise APIRequestException("JSON Decode failed")
    except:
        raise APIRequestException("Unknown Error")

    series_inds = []

    for year in jsondata:
        serie_ind = pd.Series(data=year, name=year['date']).drop("date")

        #Desgranamos Indicador y Country, que son diccionarios, en sus dos componentes:

        tindicator_id = serie_ind.indicator['id']
        tindicator_name = serie_ind.indicator['value']

        tcountry_id = serie_ind.country['id']
        tcountry_name = serie_ind.country['value']

        serie_ind.drop("indicator", inplace=True)
        serie_ind.drop("country", inplace=True)

        serie_ind = serie_ind.reindex(
            pd.Index(["indicatorId", "indicatorName", "countryId", "countryName",
                                     "countryiso3code", "value", "unit", "obs_status", "decimal"]))

        serie_ind.indicatorId = tindicator_id
        serie_ind.indicatorName = tindicator_name
        serie_ind.countryId = tcountry_id
        serie_ind.countryName = tcountry_name

        series_inds.append(serie_ind)

    dataframe_ind = pd.concat(series_inds, axis=1).transpose()
    # Convertimos el índice a serie temporal para poder tratarlo
    # más fácilmente luego
    dataframe_ind.index = pd.to_datetime(dataframe_ind.index)
    dataframe_ind.index.name = "Periodo"

    return dataframe_ind

# Funciones de utilidad para pasar de un código de indicador a su nombre y viceversa:
# Lee los nombres de un fichero en local que contiene los indicadores que decidimos
# usar de entre los 18600 que tiene la API

def get_indicators_path():
    current_path = path.dirname(path.abspath(__file__))
    return path.join(current_path,"indicators.csv")

def get_indicator_names():
    return pd.read_csv(get_indicators_path(), delimiter=";", index_col="ID").to_dict()['Name']

def get_indicator_codes():
    return pd.read_csv(get_indicators_path(), delimiter=";", index_col="Name").to_dict()['ID']

def get_indicator_name(code):
    return get_indicator_names()[code]

def get_indicator_code(name):
    return get_indicator_codes()[name]

def get_indicator_definition(code):
    try:
        resp = rq.get(indicators_url+"/"+code+"?format=json")
        try:
            return resp.json()[1][0]['sourceNote']
        except:
            raise APIRequestException("No definition found for that indicator")
    except:
        raise APIRequestException("HTTP Connection Error to the worldbank API")

