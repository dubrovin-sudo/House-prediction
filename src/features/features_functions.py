import numpy as np
import pandas as pd

def dist_calc(lat1, lon1, lat2, lon2, r_earth=6371.009e3):
    """
    Функция для расчета расстояниz между
    двумя географическими координатами
    :param lat1:
           lon1: координаты в градусах первой точки;
           lat2:
           lon2: координаты в градусах первой точки;
           r_earth: радиус Земли.
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


def nearest_node(lat, lon, df_geo, point_name, point_lat='lat', point_lon='lon'):
    '''
    Функция поиска ближайшей к указанной точке (lat, lon)
    координаты из набора координат в df_geo
    :param lat:
           lon: координаты  точки в градусах;
           df_geo: DataFrame с проименованными координатными точками;
           name: наименование столбца в df_geo, содержащего названия точек;
           point_lat, point_lon: наименование столбцов в df_geo, содержащих координаты
                                 точек.
    :return: DataFrame со столбцами: 'name', 'lat', 'lon', 'distance',
                                     и соответствующим им значениям для
                                     найденной ближайшей точки
    '''
    df = df_geo.copy()
    #     lat_array = df[point_lat].values
    #     lon_array = df[point_lon].values

    df['distance'] = [dist_calc(lat, lon, df_lat, df_lon) for df_lat, df_lon in
                      zip(df[point_lat], df[point_lon])]

    df.sort_values(['distance'], ignore_index=True, inplace=True)

    return df.loc[0]


#     return df[df['distance']==df['distance'].min()].reset_index(drop=True).loc[0]

def subway_feature(data, subway):
    '''
    Функция для добавления новых характеристик, связанных с метро
    (наименование ближайшей станции, расстояние до ближайшей станции)
    :param: data: основной DataFrame с квартирами;
            subway: DataFrame с данными о станциях метро;

    :return: new_data: DataFrame data с добавленными характеристиками 'SubwayName' и
                       "SubwayDistance"
    '''

    new_data = data.copy()

    stations_array = ['' for i in range(len(new_data))]
    distance_array = np.zeros(len(new_data))
    for i in range(len(new_data)):
        df_near_sub = nearest_node(lat=data['geo_lat'][i], lon=data['geo_lon'][i],
                                   df_geo=subway,
                                   point_name='StationName')
        stations_array[i] = df_near_sub['StationName']
        distance_array[i] = df_near_sub['distance']
    new_data['StationName'] = stations_array
    new_data['SubwayDistance'] = distance_array

    return new_data







