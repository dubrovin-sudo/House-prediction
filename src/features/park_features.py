import os
import pandas as pd
import numpy as np
import click
from src.features.process_external import dist_calc


def park_features(input_data="data/interim/clean_raw_data.csv",
                  input_parks="data/external/spb_parks.csv",
                  output="data/interim/parks_features.csv") -> None:
    """
    Функция для добавления новых характеристик, связанных с парками
    (id ближайшего парка, расстояние до ближайшего парка)
    :param: input_data: основной файл с квартирами;
    :param: input_parks: файл с данными о парках;
    :param: output: выходной файл с новыми характеристиками.
    :return:
    """

    if os.path.isfile(output):
        print(f"You have already created park features")
        df = pd.read_csv(output)
        print(df.head(5))
    else:

        df_spb_park = pd.DataFrame()
        data = pd.read_csv(input_data)
        parks = pd.read_csv(input_parks)

        lat1 = data.loc[:, 'geo_lat'].values
        lat1 = lat1.reshape((lat1.shape[0], 1))

        lon1 = data.loc[:, 'geo_lon'].values
        lon1 = lon1.reshape((lon1.shape[0], 1))

        lat2 = parks['lat'].values
        lon2 = parks['lon'].values

        distance = dist_calc(lat1, lon1, lat2, lon2)

        index = np.argmin(distance, axis=1)
        df_spb_park['park_id'] = parks.loc[index, 'park'].values
        df_spb_park['park_distance'] = distance.min(axis=1)

        print(df_spb_park.head(5))
        df_spb_park.to_csv(output, index=False)


@click.command()
@click.argument('input_data', type=click.Path())
@click.argument('input_parks', type=click.Path())
@click.argument('output', type=click.Path())
def cli_park_features(input_data: str, input_parks: str, output: str) -> None:
    """
    Функция для добавления новых характеристик, связанных с метро
    (наименование ближайшей станции, расстояние до ближайшей станции)
    :param: data: основной DataFrame с квартирами;
    :param:       subway: DataFrame с данными о станциях метро;
    :return:
    """
    park_features(input_data, input_parks, output)


if __name__ == "__main__":
    cli_park_features()
