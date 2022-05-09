import os
import pandas as pd
import numpy as np
import click
from src.features.process_external import dist_calc


def subway_features(input_data="data/interim/clean_raw_data.csv",
                    input_subways="data/external/spb_subways.csv",
                    output="data/interim/subways_features.csv") -> None:
    """
    Функция для добавления новых характеристик, связанных с метро
    (наименование ближайшей станции, расстояние до ближайшей станции)
    :param: input_data: основной файл с квартирами;
    :param: input_subways: файл с данными о станциях метро;
    :param: output: выходной файл с новыми характеристиками.
    :return:
    """

    if os.path.isfile(output):
        print(f"You have already created subway features")
        df_spb_subway = pd.read_csv(output)
        print(df_spb_subway.head(5))
    else:

        df_spb_subway = pd.DataFrame()
        data = pd.read_csv(input_data)
        subways = pd.read_csv(input_subways)

        lat1 = data.loc[:, 'geo_lat'].values
        lat1 = lat1.reshape((lat1.shape[0], 1))

        lon1 = data.loc[:, 'geo_lon'].values
        lon1 = lon1.reshape((lon1.shape[0], 1))

        lat2 = subways['lat'].values
        lon2 = subways['lon'].values

        distance = dist_calc(lat1, lon1, lat2, lon2)

        index = np.argmin(distance, axis=1)
        df_spb_subway['subway'] = subways.loc[index, 'subway'].values
        df_spb_subway['subway_distance'] = distance.min(axis=1)

        print(df_spb_subway.head(5))
        df_spb_subway.to_csv(output, index=False)


@click.command()
@click.argument('input_data', type=click.Path())
@click.argument('input_subways', type=click.Path())
@click.argument('output', type=click.Path())
def cli_subway_features(input_data: str, input_subways: str, output: str) -> None:
    """
    Функция для добавления новых характеристик, связанных с метро
    (наименование ближайшей станции, расстояние до ближайшей станции)
    :param: data: основной DataFrame с квартирами;
    :param:       subway: DataFrame с данными о станциях метро;
    :return:
    """
    subway_features(input_data, input_subways, output)


if __name__ == "__main__":
    cli_subway_features()
