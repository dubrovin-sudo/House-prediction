import os
import sys
import numpy as np
from time import sleep

import pandas as pd


def dist_calc(
    lat1: float, lon1: float, lat2: float, lon2: float, r_earth=6371.009e3
) -> float:
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
    c = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
    delta_sigma = 2 * np.arcsin(c / 2)

    distance = delta_sigma * r_earth

    return distance


def nearest_node(
    lat: float,
    lon: float,
    df_geo: pd.DataFrame,
    point_lat="lat",
    point_lon="lon",
) -> pd.core.series.Series:
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

    df["distance"] = [
        dist_calc(lat, lon, df_lat, df_lon)
        for df_lat, df_lon in zip(df[point_lat], df[point_lon])
    ]

    df.sort_values(["distance"], ignore_index=True, inplace=True)

    return df.loc[0]


# def subway_feature(data: pd.DataFrame, subway: pd.DataFrame) -> pd.DataFrame:
#     """
#     Функция для добавления новых характеристик, связанных с метро
#     (наименование ближайшей станции, расстояние до ближайшей станции)
#     :param: data: основной DataFrame с квартирами;
#             subway: DataFrame с данными о станциях метро;
#
#     :return: new_data: DataFrame data с добавленными характеристиками
#     'SubwayName' и 'SubwayDistance'
#     """
#
#     data_directory = f"{os.path.abspath(os.getcwd())}/data/"
#
#     if os.path.isfile(f"{data_directory}/interim/spb_house_with_subway.csv"):
#         print(f"You have already created subway features")
#         df_spb_subway = pd.read_csv(
#             f"{data_directory}/interim/spb_house_with_subway.csv"
#         )
#         print(df_spb_subway.head(5))
#     else:
#         df_spb_subway = data.copy()
#
#         stations_array = ["" for _ in range(len(df_spb_subway))]
#         distance_array = np.zeros(len(df_spb_subway))
#         for i in range(len(df_spb_subway)):
#             df_near_sub = nearest_node(
#                 lat=data["geo_lat"][i], lon=data["geo_lon"][i], df_geo=subway
#             )
#             stations_array[i] = df_near_sub["StationName"]
#             distance_array[i] = df_near_sub["distance"]
#
#             # отображение прогресса расчетов
#             sys.stdout.write("\r")
#             sys.stdout.write("%d%%" % (100 * i / len(df_spb_subway)))
#             sys.stdout.flush()
#             sleep(0.0001)
#
#         df_spb_subway["StationName"] = stations_array
#         df_spb_subway["SubwayDistance"] = distance_array
#
#         df_spb_subway.to_csv(
#             f"{data_directory}/interim/spb_house_with_subway.csv", index=False
#         )
#
#     return df_spb_subway
