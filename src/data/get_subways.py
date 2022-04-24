import os
import requests
import pandas as pd
import click


def get_subways(output_path: str) -> None:
    """
    Function create a DataFrame with metro stations' data
    :param output_path:
    :return:
    """
    if os.path.isfile(output_path):
        print(f"You already have the spb_subways dataset!")
        df_subway = pd.read_csv(output_path)
        print(df_subway.head(5))

    else:
        overpass_url = "https://maps.mail.ru/osm/tools/overpass/api//interpreter"
        overpass_query = """
        [out:json];
        area["ISO3166-2"="RU-SPE"][admin_level=4];
        (node["station"="subway"](area);
         way["station"="subway"](area);
         rel["station"="subway"](area);
        );
        out center;
        """
        response = requests.get(overpass_url, params={"data": overpass_query})
        data = response.json()

        df_subway = pd.DataFrame(columns=["StationName", "lat", "lon"])

        for i, element in enumerate(data["elements"]):

            if element["type"] == "node":
                data = {
                    "StationName": [element["tags"]["name"]], "lat": [element["lat"]],
                    "lon": [element["lon"]], }

                df_subway = pd.concat(
                    [df_subway, pd.DataFrame(data=data)], axis=0, ignore_index=True)
        print(df_subway.head(5))
        df_subway.to_csv(output_path, index=False)


@click.command()
@click.argument('output_path', type=click.Path())
def cli_get_subways(output_path: str) -> None:
    """
    Function for calling from CLI
    create a DataFrame with metro stations' data
    :param output_path:
    :return:
    """
    get_subways(output_path)


if __name__ == "__main__":
    cli_get_subways()
