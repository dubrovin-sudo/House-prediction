import os
import sys
import click
import numpy as np
import pandas as pd
from time import sleep

from src.data.process_external import add_to_interim
from src.data.get_external import get_external


def get_interim(feature: str) -> None:
    """
    Функция для добавления новых характеристик, связанных с выбранной
    feature (имя feature, расстояние до feature)
    :param feature:
    :return:
    """
    input_path = "data/raw/df_spb.csv"
    external_path = "data/external/spb_" + f"{feature}s.csv"
    interim_path = "data/interim/spb_house_with_" + f"{feature}.csv"

    # check data in interim folder
    if os.path.isfile(interim_path):
        print(f"You have already added {feature} data to interim dataset")
        df_interim = pd.read_csv(interim_path)
        print(df_interim.head(5))

    # check data in external folder, preprocess and add them to interim
    elif os.path.isfile(external_path):
        # print(f"You have already downloaded {feature} data to external dataset")
        add_to_interim(input_path, external_path, interim_path, feature)

    # download data in external, preprocess and add them to interim
    else:
        get_external(feature)
        add_to_interim(input_path, external_path, interim_path, feature)


@click.command()
@click.argument("feature", type=click.Path())
def cli_subway_features(feature: str) -> None:
    """
    Функция для добавления новых характеристик, связанных с выбранной
    feature (имя feature, расстояние до feature)
    :param feature:
    :return:
    """
    get_interim(feature)


if __name__ == "__main__":
    cli_subway_features()
