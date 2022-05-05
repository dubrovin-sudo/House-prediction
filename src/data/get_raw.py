import os
import kaggle
import zipfile
import click
import pandas as pd


def get_raw(output_all="data/raw/all_v2.csv") -> None:
    """
    Function load data from Kaggle and create pd.DataFrame
    :param output_all:
    :return:
    """

    name = "russia-real-estate-20182021"
    if os.path.isfile(output_all):
        print(f"You already have {output_all} dataset!")
        df = pd.read_csv(output_all)
        print(df.head(5))
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
        print(df.head(5))



@click.command()
@click.argument('output_all', type=click.Path())
def cli_get_raw(output_all: str) -> None:
    """
    get_raw for terminal
    :param: output_all:
    :param: output_region:
    :return:
    """
    get_raw(output_all)


if __name__ == "__main__":
    cli_get_raw()
