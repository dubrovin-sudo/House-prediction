import os
import pandas as pd
import sys
from time import sleep
import numpy as np
import click
from src.features.features_functions import nearest_node


def subway_features(input_data: str, input_subways: str, output: str) -> None:
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

        data = pd.read_csv(input_data)
        df_spb_subway = data.copy()
        subways = pd.read_csv(input_subways)

        stations_array = ["" for _ in range(len(data))]
        distance_array = np.zeros(len(data))
        for i in range(len(data)):
            df_near_sub = nearest_node(
                lat=data["geo_lat"][i], lon=data["geo_lon"][i], df_geo=subways
            )
            stations_array[i] = df_near_sub["StationName"]
            distance_array[i] = df_near_sub["distance"]

            # отображение прогресса расчетов
            sys.stdout.write("\r")
            sys.stdout.write("%d%%" % (100 * i / len(data)))
            sys.stdout.flush()
            sleep(0.0001)

        df_spb_subway["StationName"] = stations_array
        df_spb_subway["SubwayDistance"] = distance_array
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
