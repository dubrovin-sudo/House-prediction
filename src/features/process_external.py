import sys
from time import sleep

import numpy as np
import pandas as pd


def dist_calc(
    lat1: np.ndarray, lon1: np.ndarray,
    lat2: np.ndarray, lon2: np.ndarray,
    r_earth=6371.009e3
) -> np.ndarray:
    """
    Функция для расчета расстояниz между
    двумя географическими координатами
    :param lat1:
    :param lon1: координаты в градусах квартир;
    :param lat2:
    :param lon2: координаты в градусах станций метро;
    :param r_earth: радиус Земли.
    :return: массив расстояний между всеми квартирами и всеми станциями метро.
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


def add_to_interim(
    input_path: str, external_path: str, interim_path: str, feature
) -> None:
    """
    Функция для добавления новых характеристик, связанных с выбранной
    feature (имя feature, расстояние до feature) в папку data/interim
    :param input_path:
    :param external_path:
    :return:
    """
    data = pd.read_csv(input_path)
    df_interim = data.copy()
    new_features = pd.read_csv(external_path)

    features_array = ["" for _ in range(len(data))]
    distance_array = np.zeros(len(data))
    print(f"Process and pushing {feature} data to interim")
    for i in range(len(data)):
        df_near_sub = nearest_node(
            lat=data["geo_lat"][i], lon=data["geo_lon"][i], df_geo=new_features
        )
        features_array[i] = df_near_sub[f"{feature}s"]
        distance_array[i] = df_near_sub["distance"]

        # отображение прогресса расчетов
        sys.stdout.write("\r")
        sys.stdout.write("%d%%" % (100 * i / len(data)))
        sys.stdout.flush()
        sleep(0.0001)

    df_interim[f"{feature}s"] = features_array
    df_interim[f"{feature}Distance"] = distance_array
    print(df_interim.head(5))
    df_interim.to_csv(interim_path, index=False)
