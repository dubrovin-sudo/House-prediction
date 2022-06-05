import click
import pandas as pd
import numpy as np

from typing import Tuple
from sklearn.model_selection import train_test_split


def prepare_data(
        df_processed='../../data/processed/df_spb_processed.csv',
        df_prepared=(
                '../../data/processed/df_trainval.csv',
                '../../data/processed/df_test.csv'
        ),
) -> None:
    """
    Function for preparing data
    :param df_processed:
    :param df_prepared:
    :return:
    """

    df = pd.read_csv(df_processed)
    # df = df.drop_duplicates(subset=['geo_lat', 'geo_lon', 'area', 'level'], keep='last')

    df_train = df.sample(frac=0.8, random_state=2707, ignore_index=True)
    df_test = df.drop(df_train.index)
    # save
    df_train.to_csv(df_prepared[0], index=False)
    df_test.to_csv(df_prepared[1], index=False)


@click.command()
@click.argument('df_processed', type=click.Path(exists=True))
@click.argument('df_prepared', type=click.Path(), nargs=2)
def cli_prepare_data(df_processed: str, df_prepared: Tuple[str]) -> None:
    """
    Function for preparing data
    :param df_processed:
    :param df_prepared:
    :return:
    """
    prepare_data(df_processed, df_prepared)
    print('Data split and ready for test ')
    # python3.8 prepare.py '../../data/processed/df_spb_processed.csv' '../../data/processed/x_trainval.npy'
    # '../../data/processed/y_trainval.npy' '../../data/processed/x_test.npy' '../../data/processed/y_test.npy'


if __name__ == "__main__":
    cli_prepare_data()
