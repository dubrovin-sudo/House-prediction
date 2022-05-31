import pandas as pd
import click

# Constants
MIN_AREA = 20  # Outlier range for floor area
MAX_AREA = 200

MIN_KITCHEN = 6  # Outlier range for kitchen area
MAX_KITCHEN = 30

MIN_PRICE = 1_500_000  # Outlier range for price
MAX_PRICE = 50_000_000

MIN_SQM_PRICE = 75_000  # Outlier range for price per sq. meter
MAX_SQM_PRICE = 250_000


def clean_data(input_file="data/raw/df_spb.csv",
               output_file="data/interim/clean_raw_data.csv") -> None:
    """
    Function removes excess columns and enforces
    correct data types.
    :param input_file: Original DataFrame
    :param output_file:
    :return:
    """
    df = pd.read_csv(input_file)
    # Fix negative values
    df["rooms"] = df["rooms"].apply(lambda x: 0 if x < 0 else x)
    df["price"] = df["price"].abs()
    # Drop prices and area outliers
    df = df[(df["area"] <= MAX_AREA) & (df["area"] >= MIN_AREA)]
    df = df[(df["price"] <= MAX_PRICE) & (df["price"] >= MIN_PRICE)]
    # Drop outliers based on price per square meter
    # df["sqm_price"] = df["price"] / df["area"]
    # df = df[(df["sqm_price"] >= MIN_SQM_PRICE) & (df["sqm_price"] <= MAX_SQM_PRICE)]
    # Fix kitchen area
    df.loc[
        (df["kitchen_area"] >= MAX_KITCHEN) | (df["area"] <= MIN_AREA), "kitchen_area"
    ] = 0

    df.drop(["time", "region"], axis=1, inplace=True)

    df.to_csv(output_file, index=False)


@click.command()
@click.argument('input_file', type=click.Path())
@click.argument('output_file', type=click.Path())
def cli_clean_raw(input_file="data/raw/df_spb.csv",
                  output_file="data/interim/clean_raw_data.csv") -> None:
    """
    select_region for terminal
    :param: output_all:
    :param: output_region:
    :return:
    """
    clean_data(input_file, output_file)


if __name__ == "__main__":
    cli_clean_raw()
