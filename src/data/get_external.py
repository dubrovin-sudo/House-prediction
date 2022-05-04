import os
import click
import requests
import pandas as pd


def get_external(
    output_park="data/external/spb_parks.csv",
    output_subway="data/external/spb_subways.csv"
) -> None:
    """
    Function create a DataFrame with features data and add it to data/external
    :param output_subway:
    :param output_park:
    :return:
    """
    outputs = [output_park, output_subway]
    for path, feature in enumerate(["park", "subway"]):
        if os.path.isfile(outputs[path]):
            print(f"You already have the spb_{feature}s dataset!")
            df_feature = pd.read_csv(outputs[path])
            print(df_feature.head(5))

        else:
            overpass_url = "https://maps.mail.ru/osm/tools/overpass/api//interpreter"
            if feature == "subway":
                overpass_query = """ 
                [out:json];
                area["ISO3166-2"="RU-SPE"][admin_level=4];
                (node["station"="subway"](area);
                 way["statio    :param feature:n"="subway"](area);
                 rel["station"="subway"](area);
                );
                out center;
                """

                response = requests.get(overpass_url, params={"data": overpass_query})
                data = response.json()

                df_feature = pd.DataFrame(columns=[f"{feature}s", "lat", "lon"])

                for i, element in enumerate(data["elements"]):

                    if element["type"] == "node":  # subways
                        data = {
                            f"{feature}s": [element["tags"]["name"]],
                            "lat": [element["lat"]],
                            "lon": [element["lon"]],
                        }
                        df_feature = pd.concat(
                            [df_feature, pd.DataFrame(data=data)],
                            axis=0,
                            ignore_index=True,
                        )
                    elif element["type"] == "relation":  # parks
                        data = {
                            f"{feature}s": [element["id"]],
                            "lat": [element["center"]["lat"]],
                            "lon": [element["center"]["lon"]],
                        }

                        df_feature = pd.concat(
                            [df_feature, pd.DataFrame(data=data)],
                            axis=0,
                            ignore_index=True,
                        )
                print(df_feature.head(5))
                df_feature.to_csv(outputs[path], index=False)

            elif feature == "park":
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

                df_feature = pd.DataFrame(columns=[f"{feature}s", "lat", "lon"])

                for i, element in enumerate(data["elements"]):

                    if element["type"] == "node":  # subways
                        data = {
                            f"{feature}s": [element["tags"]["name"]],
                            "lat": [element["lat"]],
                            "lon": [element["lon"]],
                        }
                        df_feature = pd.concat(
                            [df_feature, pd.DataFrame(data=data)],
                            axis=0,
                            ignore_index=True,
                        )
                    elif element["type"] == "relation":  # parks
                        data = {
                            f"{feature}s": [element["id"]],
                            "lat": [element["center"]["lat"]],
                            "lon": [element["center"]["lon"]],
                        }

                        df_feature = pd.concat(
                            [df_feature, pd.DataFrame(data=data)],
                            axis=0,
                            ignore_index=True,
                        )
                print(df_feature.head(5))
                df_feature.to_csv(outputs[path], index=False)


@click.command()
@click.argument("output_park", type=click.Path())
@click.argument("output_subway", type=click.Path())
def cli_get_external(output_park: str, output_subway: str) -> None:
    """
    Function for calling from CLI
    create a DataFrame with feature data
    :param output_subway:
    :param output_park:
    :return:
    """
    get_external(output_park, output_subway)


if __name__ == "__main__":
    cli_get_external()
