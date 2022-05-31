import os
import click
import pandas as pd

MAX_SUBWAY_DISTANCE = 20000


def get_processed(input_clear_raw="data/interim/clean_raw_data.csv",
                  input_parks="data/interim/parks_features.csv",
                  input_subways="data/interim/subways_features.csv",
                  input_raw_features="data/interim/raw_features.csv",
                  output_file="data/processed/df_spb_processed.csv"
                  ) -> None:
    """
    Function concats DataFrames, final process and add it to data/processed
    :param input_clear_raw:
    :param input_parks:
    :param input_subways:
    :param input_raw_features:
    :param output_file:
    :return:
    """

    if os.path.isfile(output_file):
        print(f"You already have the df_spb_processed.csv dataset!")
        df_feature = pd.read_csv(output_file)
        print(df_feature.head(5))

    else:
        df_clean_raw = pd.read_csv(input_clear_raw)
        df_parks = pd.read_csv(input_parks)
        df_subways = pd.read_csv(input_subways)
        df_raw_features = pd.read_csv(input_raw_features)
        # concatenate all datasets
        df = pd.concat([df_clean_raw, df_parks, df_subways, df_raw_features], axis=1)

        # final preprocessing
        df.drop('date', axis=1, inplace=True)
        df.loc[df['subway_distance'] >= MAX_SUBWAY_DISTANCE, 'subway'] = 'Без метро'
        df.drop('park_id', axis=1, inplace=True)
        df['year_month'] = df['year'] + (df['month'] - 1) / 12

        df.to_csv(output_file, index=False)


@click.command()
@click.argument("input_clear_raw", type=click.Path())
@click.argument("input_parks", type=click.Path())
@click.argument("input_subways", type=click.Path())
@click.argument("input_raw_features", type=click.Path())
@click.argument("output_file", type=click.Path())
def cli_get_processed(input_clear_raw: str,
                      input_parks: str,
                      input_subways: str,
                      input_raw_features: str,
                      output_file: str) -> None:
    """
    Function for calling from CLI
    create a DataFrame with feature data
    :param input_clear_raw:
    :param input_parks:
    :param input_subways:
    :param input_raw_features:
    :param output_file:
    :return:
    """
    get_processed(input_clear_raw,
                  input_parks,
                  input_subways,
                  input_raw_features,
                  output_file)


if __name__ == "__main__":
    cli_get_processed()
