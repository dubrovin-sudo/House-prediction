import os
import click
import requests
import pandas as pd


def get_parks(output_park="data/external/spb_parks.csv") -> None:
    """
    Function create a DataFrame with features data and add it to data/external
    :param output_park:
    :return:
    """
    if os.path.isfile(output_park):
        print(f"You already have the spb_parks dataset!")
        df_feature = pd.read_csv(output_park)
        print(df_feature.head(5))
    else:
        overpass_url = "https://maps.mail.ru/osm/tools/overpass/api//interpreter"

        overpass_query = """
                [out:json][timeout:25];
                area["ISO3166-2"="RU-SPE"][admin_level=4];
                (
                  relation["leisure"="park"](area);
                );
                out center;
                """

        response = requests.get(overpass_url, params={"data": overpass_query})
        data = response.json()

        df_park = pd.DataFrame(columns=["park", "lat", "lon"])

        for i, element in enumerate(data["elements"]):
            if element["type"] == "relation":  # parks

                data = {
                    "park": [element["id"]],
                    "lat": [element["center"]["lat"]],
                    "lon": [element["center"]["lon"]],
                }

                df_park = pd.concat(
                    [df_park, pd.DataFrame(data=data)], axis=0, ignore_index=True)

        print(df_park.head(5))
        df_park.to_csv(output_park, index=False)


@click.command()
@click.argument('output_park', type=click.Path())
def cli_get_parks(output_park: str) -> None:
    """
    get_parks for terminal
    :param: output_subway:
    :return:
    """
    get_parks(output_park)


if __name__ == "__main__":
    cli_get_parks()
