import os
import kaggle
import zipfile
import pandas as pd
import click


def get_raw(output_all: str, output_region: str) -> None:
    """
    Function load data from Kaggle and create pd.DataFrame
    :param: output_all:
    :param: output_region:
    :return:
    """
    kaggle.api.authenticate()
    name = "russia-real-estate-20182021"
    if os.path.isfile(output_all):
        print(f"You already have the full dataset!")
        df = pd.read_csv(output_all)
        df_spb = df[df["region"] == 2661]
        df_spb.to_csv(output_region, index=False)
        print(df_spb.head(5))
    else:
        print(f"Downloading dataset : {name}!")

        kaggle.api.dataset_download_file(
            f"mrdaniilak/{name}",
            file_name="all_v2.csv",
            path="data/raw/",
        )

        with zipfile.ZipFile("data/raw/all_v2.csv.zip", "r") as zip_ref:
            zip_ref.extractall("data/raw")
        os.remove("data/raw/all_v2.csv.zip")

        df = pd.read_csv(output_all)
        df_spb = df[df["region"] == 2661]
        print(df_spb.head(5))
        df_spb.to_csv(output_region, index=False)


@click.command()
@click.argument('output_all', type=click.Path())
@click.argument('output_region', type=click.Path())
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
