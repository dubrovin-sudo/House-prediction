import os
import sys
import click
import numpy as np
import pandas as pd
from time import sleep

from src.data.process_external import add_to_interim
from src.data.get_external import get_external


def get_interim(
    input_raw_spb="data/raw/df_spb.csv",
    input_external_park="data/external/spb_parks.csv",
    input_external_subway="data/external/spb_subways.csv",
    output_interim_park="data/interim/spb_house_with_park.csv",
    output_interim_subway="data/interim/spb_house_with_subway.csv"
) -> None:
    """
    Функция для добавления новых характеристик, связанных с выбранной
    feature (имя feature, расстояние до feature)
    :param output_interim_subway:
    :param output_interim_park:
    :param input_external_subway:
    :param input_external_park:
    :param input_raw_spb:
    :return:
    """
    external = [input_external_park, input_external_subway]
    interim = [output_interim_park, output_interim_subway]
    for i, feature in enumerate(["park", "subway"]):
        external[i] = "data/external/spb_" + f"{feature}s.csv"
        interim[i] = "data/interim/spb_house_with_" + f"{feature}.csv"

        # check data in interim folder
        if os.path.isfile(interim[i]):
            print(f"You have already added {feature} data to interim dataset")
            df_interim = pd.read_csv(interim[i])
            print(df_interim.head(5))

        # check data in external folder, preprocess and add them to interim
        elif os.path.isfile(external[i]):
            # print(f"You have already downloaded {feature} data to external dataset")
            add_to_interim(input_raw_spb, external[i], interim[i], feature)

        # download data in external, preprocess and add them to interim
        else:
            get_external(feature)
            add_to_interim(input_raw_spb, external[i], interim[i], feature)


@click.command()
@click.argument("input_raw_spb", type=click.Path())
@click.argument("input_external_park", type=click.Path())
@click.argument("input_external_subway", type=click.Path())
@click.argument("output_interim_park", type=click.Path())
@click.argument("output_interim_subway", type=click.Path())
def cli_get_interim(
    input_raw_spb: str,
    input_external_park: str,
    input_external_subway: str,
    output_interim_park: str,
    output_interim_subway: str,
) -> None:
    """
    Функция для добавления новых характеристик, связанных с выбранной
    feature (имя feature, расстояние до feature)
    :param output_interim_subway:
    :param input_external_subway:
    :param input_external_park:
    :param input_raw_spb:
    :param output_interim_park:
    :return:
    """
    get_interim(
        input_raw_spb,
        input_external_park,
        input_external_subway,
        output_interim_park,
        output_interim_subway,
    )


if __name__ == "__main__":
    cli_get_interim()
