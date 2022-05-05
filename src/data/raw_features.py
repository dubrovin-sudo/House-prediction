import numpy as np
import pandas as pd
import click


def raw_features(input_file="data/interim/clean_raw_data.csv",
                 output_file="data/interim/raw_features.csv") -> None:
    """
    Function adds features based on raw data.
    :param input_file: Cleaned DataFrame
    :param output_file: features, based on raw data
    :return:
    """
    # Apartment floor in relation to total number of floors.
    df_raw = pd.read_csv(input_file)
    df = pd.DataFrame()

    df["level_to_levels"] = df_raw["level"] / df_raw["levels"]

    # Average size of room in the apartment.11111
    df["area_to_rooms"] = (df_raw["area"] / df_raw["rooms"]).abs()

    # Fix division by zero.
    df.loc[df["area_to_rooms"] == np.inf, "area_to_rooms"] = df_raw.loc[
        df["area_to_rooms"] == np.inf, "area"]

    # Delete region and change data format
    df["date"] = pd.to_datetime(df_raw["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    df.drop(["date"], axis=1, inplace=True)

    df.to_csv(output_file, index=False)


@click.command()
@click.argument('input_file', type=click.Path())
@click.argument('output_file', type=click.Path())
def cli_raw_features(input_file: str, output_file: str) -> None:
    """
    raw_features for terminal
    :param: output_all:
    :param: output_region:
    :return:
    """
    raw_features(input_file, output_file)


if __name__ == "__main__":
    cli_raw_features()
