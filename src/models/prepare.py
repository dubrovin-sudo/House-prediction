import click
import pandas as pd
import numpy as np

from typing import Tuple
from sklearn.model_selection import train_test_split


def prepare_data(
        df_processed='../../data/processed/df_spb_processed.csv',
        df_prepared=(
                '../../data/processed/x_trainval.npy',
                '../../data/processed/y_trainval.npy',
                '../../data/processed/x_test.npy',
                '../../data/processed/y_test.npy'
        ),
) -> None:
    """
    Function for preparing data
    :param df_processed:
    :param df_prepared:
    :return:
    """

    df = pd.read_csv(df_processed)
    df = df.select_dtypes(exclude=['object'])
    df = df.drop_duplicates(subset=['geo_lat', 'geo_lon', 'area', 'level'], keep='last')

    x_full = df.drop(['price'], axis=1).values
    y_full = df['price'].values

    x_trainval, x_test, y_trainval, y_test = train_test_split(
        x_full, y_full, random_state=42
    )
    # save to npy file
    np.save(df_prepared[0], x_trainval)
    np.save(df_prepared[1], y_trainval)
    np.save(df_prepared[2], x_test)
    np.save(df_prepared[3], y_test)


@click.command()
@click.argument('df_processed', type=click.Path(exists=True))
@click.argument('df_prepared', type=click.Path(), nargs=4)
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