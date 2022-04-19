import pandas as pd
import requests
# import json

def get_subways():
    '''
    Функция для формирования DataFrame с данными о метро СПб
    :param:
    :return: df_subways:
    '''

    overpass_url = "https://maps.mail.ru/osm/tools/overpass/api//interpreter"
    overpass_query = """ 
    [out:json];
    area["ISO3166-2"="RU-SPE"][admin_level=4];
    (node["station"="subway"](area);
     way["station"="subway"](area);
     rel["station"="subway"](area);
    );
    out center;
    """
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    data = response.json()

    df_subways = pd.DataFrame(columns=['StationName', 'lat', 'lon'])

    for i, element in enumerate(data['elements']):

        if element['type'] == 'node':

            data = {'StationName': [element['tags']['name']],
                    'lat': [element['lat']],
                    'lon': [element['lon']]}

            df_subways = pd.concat([df_subways, pd.DataFrame(data=data)],
                                   axis=0,
                                   ignore_index=True)

    return df_subways
