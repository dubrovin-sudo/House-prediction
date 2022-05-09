import pandas as pd
import click

REGION_ID = 2661


def select_region(input_file="data/raw/all_v2.csv",
                  output_file="data/raw/df_spb.csv",
                  region=REGION_ID) -> None:
    """
    Function select specific region from all data
    :param input_file:
    :param output_file:
    :param region:
    :return:
    """

    df_all = pd.read_csv(input_file)
    df_region = df_all[df_all["region"] == region]
    df_region.to_csv(output_file, index=False)


@click.command()
@click.argument('input_file', type=click.Path())
@click.argument('output_file', type=click.Path())
@click.argument('region', type=click.INT)
def cli_select_region(input_file="data/raw/all_v2.csv",
                      output_file="data/raw/df_spb.csv",
                      region=REGION_ID) -> None:
    """
    select_region for terminal
    :param: output_all:
    :param: output_region:
    :return:
    """
    select_region(input_file, output_file, region)


if __name__ == "__main__":
    cli_select_region()
