import numpy as np
import sys
from time import sleep

import pandas as pd


def dist_calc(lat1: float, lon1: float, lat2:float, lon2:float, r_earth=6371.009e3)->float:
    """
    Функция для расчета расстояниz между
    двумя географическими координатами
    :param lat1:
    :param lon1: координаты в градусах первой точки;
    :param lat2:
    :param lon2: координаты в градусах первой точки;
    :param r_earth: радиус Земли.
    :return: растояние между двумя точками, м.
    """
    lat1 *= np.pi / 180
    lon1 *= np.pi / 180
    lat2 *= np.pi / 180
    lon2 *= np.pi / 180

    delta_x = np.cos(lat2) * np.cos(lon2) - np.cos(lat1) * np.cos(lon1)
    delta_y = np.cos(lat2) * np.sin(lon2) - np.cos(lat1) * np.sin(lon1)
    delta_z = np.sin(lat2) - np.sin(lat1)
    c = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
    delta_sigma = 2 * np.arcsin(c / 2)

    distance = delta_sigma * r_earth

    return distance


def nearest_node(lat: float, lon: float, df_geo: pd.DataFrame, point_lat='lat'
                 , point_lon='lon')->pd.core.series.Series:
    """
    Функция поиска ближайшей к указанной точке (lat, lon)
    координаты из набора координат в df_geo
    :param lat:
    :param lon: координаты  точки в градусах;
    :param df_geo: DataFrame с проименованными координатными точками;
    :param point_lat: наименование столбцов в df_geo, содержащих координаты
    :param point_lon: точек.

    :return: DataFrame со столбцами: 'name', 'lat', 'lon', 'distance',
                                     и соответствующим им значениям для
                                     найденной ближайшей точки
    """
    df = df_geo.copy()

    df['distance'] = [dist_calc(lat, lon, df_lat, df_lon) for df_lat, df_lon in
                      zip(df[point_lat], df[point_lon])]

    df.sort_values(['distance'], ignore_index=True, inplace=True)

    return df.loc[0]


def subway_feature(data: pd.DataFrame, subway: pd.DataFrame)->pd.DataFrame:
    """
    Функция для добавления новых характеристик, связанных с метро
    (наименование ближайшей станции, расстояние до ближайшей станции)
    :param: data: основной DataFrame с квартирами;
            subway: DataFrame с данными о станциях метро;

    :return: new_data: DataFrame data с добавленными характеристиками 'SubwayName' и
                       "SubwayDistance"
    """

    new_data = data.copy()

    stations_array = ['' for _ in range(len(new_data))]
    distance_array = np.zeros(len(new_data))
    for i in range(len(new_data)):
        df_near_sub = nearest_node(lat=data['geo_lat'][i], lon=data['geo_lon'][i],
                                   df_geo=subway)
        stations_array[i] = df_near_sub['StationName']
        distance_array[i] = df_near_sub['distance']


        # отображение прогресса расчетов
        sys.stdout.write('\r')
        sys.stdout.write("%d%%" % (100 * i/len(new_data)))
        sys.stdout.flush()
        sleep(0.0001)

    new_data['StationName'] = stations_array
    new_data['SubwayDistance'] = distance_array

    return new_data
