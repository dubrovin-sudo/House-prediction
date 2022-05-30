import os
import click
import requests
import pandas as pd


def get_subways(output_subway="data/external/spb_subways.csv") -> None:
    """
    Function create a DataFrame with features data and add it to data/external
    :param output_subway:
    :return:
    """
    if os.path.isfile(output_subway):
        print(f"You already have the spb_subways dataset!")
        df_feature = pd.read_csv(output_subway)
        print(df_feature.head(5))
    else:
        overpass_url = "https://maps.mail.ru/osm/tools/overpass/api//interpreter"
        overpass_query = """ 
                    [out:json];
                    area["ISO3166-2"="RU-SPE"][admin_level=4];
                    (node["station"="subway"](area);
                    );
                    out center;
                    """

        response = requests.get(overpass_url, params={"data": overpass_query})
        data = response.json()

        df_subway = pd.DataFrame(columns=["subway", "lat", "lon"])

        for i, element in enumerate(data["elements"]):

            if element["type"] == "node":
                data = {
                    "subway": [element["tags"]["name"]],
                    "lat": [element["lat"]],
                    "lon": [element["lon"]],
                }

                df_subway = pd.concat(
                    [df_subway, pd.DataFrame(data=data)], axis=0, ignore_index=True
                )

        print(df_subway.head(5))
        df_subway.to_csv(output_subway, index=False)


@click.command()
@click.argument("output_subway", type=click.Path())
def cli_get_subways(output_subway: str) -> None:
    """
    get_subway for terminal
    :param: output_subway:
    :return:
    """
    get_subways(output_subway)


if __name__ == "__main__":
    cli_get_subways()
