from apis import worldbank as wb, restcountries as rc
from apis.exceptions import APIRequestException
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests as rq
import concurrent
import os


def get_ind_value(code, ind, session):
    serieind = wb.get_indicator(code, ind, session).value
    try:
        valor = serieind[serieind.last_valid_index()]
    except KeyError:
        # No hay last valid index porque no hay datos
        raise APIRequestException("No data for this country")
    return {code: valor}

  
def get_ind_global(ind):
    # Saco la información de todos los países del mundo
    allcountries = rc.get_all_countries()
    # Me quedo con una lista de los alpha3code, para consultar worldbank
    codes = allcountries.index.to_list()
    # Creo una sesión HTTP y la reutilizo para todas las peticiones, evitando
    # repetir el handshake TCP cada vez
    session = rq.Session()

    # Para cada uno de los 250 países, creo un job que hace la petición, obtengo el
    # future asociado y lo meto en una lista
    # Uso 8 threads por cada core que tenga el sistema, ya que son threads que la
    # mayor parte del tiempo se la pasan esperando por la red, no tienen apenas
    # carga computacional

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()*8) as executor:
        # Mando a ejecución todas las peticiones
        valores = [executor.submit(get_ind_value, code, ind, session) for code in codes]
        # Ahora que tengo los valores, creo la serie
        serietodos = pd.Series(dtype="float64", name=ind)
        # Valores es una lista de "Futures"
        # Para cada uno obtengo su "result", que puede ser
        # o un diccionario o que salte una excepción
        # Si el resultado todavía no está, el método result bloquea hasta que esté
        # Con esto construyo la serie
        for v in valores:
            try:
                serietodos = serietodos.append(pd.Series(data=v.result()))
            except APIRequestException:
                #Un error significa que el país no estaba en WorldBank
                #Puede pasar ya que Restcountries también contempla regiones administrativas
                #que formalmente no son países, como los territorios de ultramar británicos
                #Simplemente ignoramos y seguimos
                continue;

    # Cierro la sesión HTTP antes de salir
    session.close()

    # Devuelvo la serie con los valores
    return serietodos

def top_n_indicador(ind, n=10):
    # Me quedo con los N top países
    return get_ind_global(ind).nlargest(n, keep="all")

def graph_topn(ind, n=10, filename=None):
    # Peticion a la API
    serietop = top_n_indicador(ind, n)

    # Construyo el gráfico
    graf = serietop.plot.bar(figsize=(10,8))

    # Si es el caso, lo guardo
    if filename is not None:
        plt.savefig(filename)

   # Cierro la gráfica para evitar que se superponga la siguiente
    plt.close()

    # Devuelvo la serie para poder reutilizarla si fuera necesario
    return serietop


# Dado un indicador y un par de países, saca un gráfico comparando
# la relación entre los dos. El parámetro "tipo" indica si va a ser
# un gráfico de líneas ("l") o de dispersión de puntos ("d")
def graph_comparacion(ind, pais1, pais2, filename=None, tipo="l"):
    # Hacemos la consulta del indicador a la API de Worldbank, y nos quedamos con
    # una serie temporal con los valores en crudo (columna "value")
    # Y descartamos los valores nulos
    ind1 = wb.get_indicator(pais1, ind).value.dropna()
    # Le damos un nombre a la Serie
    ind1.name = pais1

    ind2 = wb.get_indicator(pais2, ind).value.dropna()
    ind2.name = pais2

    df = pd.concat([ind1, ind2], axis=1)

    if tipo=="d":
        df.plot.scatter(x=ind1.name, y=ind1.name, figsize=(10,8))
    elif tipo=="l":
        df.plot(figsize=(10,8))
    else:
        raise TypeError("Unknown type: "+tipo)

    if filename is not None:
        plt.savefig(filename)

    # Cierro la gráfica para evitar que se superponga la siguiente
    plt.close()

    return df


def graph_1dataXcountries(ind, paises, filename=None):
    # Construimos el dataframe con todos los países
    data = []
    for pais in paises:
        try:
            data.append(wb.get_indicator(pais, ind))
        except APIRequestException:
            continue;

    series = []
    for ind in data:
        serie = ind.value.dropna()
        serie.name = ind.countryName.iloc[0]
        series.append(serie)

    df = pd.concat(series, axis=1)

    df.plot(figsize=(10,8))

    # Guardamos
    if filename is not None:
        plt.savefig(filename)

    # Cierro la gráfica para evitar que se superponga la siguiente
    plt.close()

    # Devolvemos el dataframe
    return df

def graph_Xdata1country(inds, pais, filename=None):
    data = []
    for ind in inds:
        try:
            data.append(wb.get_indicator(pais, ind))
        except APIRequestException:
            continue;

    series = []
    for ind in data:
        serie = ind.value.dropna()
        serie.name = ind.indicatorName.iloc[0]
        series.append(serie)

    df = pd.concat(series, axis=1)

    df.plot(figsize=(10,8))

    if filename is not None:
        plt.savefig(filename)

    # Cierro la gráfica para evitar que se superponga la siguiente
    plt.close()

    return df

def graph_histograma(ind, filename=None):
    indglobal = get_ind_global(ind)
    indglobal.plot.hist(figsize=(10,8), bins=16)

    if filename is not None:
        plt.savefig(filename)

    # Cierro la gráfica para evitar que se superponga la siguiente
    plt.close()

    return indglobal
