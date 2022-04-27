import os
import kaggle
import zipfile
import numpy as np
import pandas as pd
import click


def clean_data(df: str) -> pd.DataFrame:
    """
    Function removes excess columns and enforces
    correct data types.
    :param df: Original DataFrame
    :return: Updated DataFrame
    """
    # Constants
    MIN_AREA = 20  # Outlier range for floor area
    MAX_AREA = 200

    MIN_KITCHEN = 6  # Outlier range for kitchen area
    MAX_KITCHEN = 30

    MIN_PRICE = 1_500_000  # Outlier range for price
    MAX_PRICE = 50_000_000

    MIN_SQM_PRICE = 75_000  # Outlier range for price per sq. meter
    MAX_SQM_PRICE = 250_000

    # Fix negative values
    df["rooms"] = df["rooms"].apply(lambda x: 0 if x < 0 else x)
    df["price"] = df["price"].abs()
    # Drop prices and area outliers
    df = df[(df["area"] <= MAX_AREA) & (df["area"] >= MIN_AREA)]
    df = df[(df["price"] <= MAX_PRICE) & (df["price"] >= MIN_PRICE)]
    # Drop outliers based on price per square meter
    df["sqm_price"] = df["price"] / df["area"]
    df = df[(df["sqm_price"] >= MIN_SQM_PRICE) & (df["sqm_price"] <= MAX_SQM_PRICE)]
    # Fix kitchen area
    df.loc[
        (df["kitchen_area"] >= MAX_KITCHEN) | (df["area"] <= MIN_AREA), "kitchen_area"
    ] = 0

    # Delete region and change data format
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df = df[df["region"] == 2661]
    df.drop(["date", "time", "region"], axis=1, inplace=True)
    return df


def raw_features(df: str) -> pd.DataFrame:
    """
    Function adds features based on raw data.
    :param df: Cleaned DataFrame
    :return: Updated DataFrame
    """
    # Apartment floor in relation to total number of floors.
    df["level_to_levels"] = df["level"] / df["levels"]
    # Average size of room in the apartment.
    df["area_to_rooms"] = (df["area"] / df["rooms"]).abs()
    # Fix division by zero.
    df.loc[df["area_to_rooms"] == np.inf, "area_to_rooms"] = df.loc[
        df["area_to_rooms"] == np.inf, "area"
    ]
    return df


def get_raw(output_all: str, output_region: str) -> None:
    """
    Function load data from Kaggle and create pd.DataFrame
    :param: output_all:
    :param: output_region:
    :return:
    """
    name = "russia-real-estate-20182021"
    if os.path.isfile(output_all):
        print(f"You already have the full dataset!")
        df = pd.read_csv(output_all)
        df_spb = df.pipe(clean_data)
        df_spb = df_spb.pipe(raw_features)
        print(df_spb.head(5))
        df_spb.to_csv(output_region, index=False)
    else:
        print(f"Downloading dataset : {name}!")
        kaggle.api.authenticate()
        kaggle.api.dataset_download_file(
            f"mrdaniilak/{name}",
            file_name="all_v2.csv",
            path="data/raw/",
        )

        with zipfile.ZipFile("data/raw/all_v2.csv.zip", "r") as zip_ref:
            zip_ref.extractall("data/raw")
        os.remove("data/raw/all_v2.csv.zip")

        df = pd.read_csv(output_all)
        df_spb = df.pipe(clean_data)
        df_spb = df_spb.pipe(raw_features)
        print(df_spb.head(5))
        df_spb.to_csv(output_region, index=False)


@click.command()
@click.argument("output_all", type=click.Path())
@click.argument("output_region", type=click.Path())
def cli_get_raw(output_all: str, output_region: str) -> None:
    """
    Function load data from Kaggle and create pd.DataFrame
    :param: output_all:
    :param: output_region:
    :return:
    """
    get_raw(output_all, output_region)


if __name__ == "__main__":
    cli_get_raw()
