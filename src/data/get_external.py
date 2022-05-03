import os
import click
import requests
import pandas as pd


def get_external(feature: str) -> None:
    """
    Function create a DataFrame with features data and add it to data/external
    :rtype: object
    :param feature:
    :return:
    """
    output_path = "data/external/spb_" + f"{feature}s.csv"
    if os.path.isfile(output_path):
        print(f"You already have the spb_{feature}s dataset!")
        df_feature = pd.read_csv(output_path)
        print(df_feature.head(5))

    else:
        overpass_url = "https://maps.mail.ru/osm/tools/overpass/api//interpreter"
        if feature == "subway":
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

            df_feature = pd.DataFrame(columns=[f"{feature}s", "lat", "lon"])

            for i, element in enumerate(data["elements"]):

                if element["type"] == "node":  # subways
                    data = {
                        f"{feature}s": [element["tags"]["name"]],
                        "lat": [element["lat"]],
                        "lon": [element["lon"]],
                    }
                    df_feature = pd.concat(
                        [df_feature, pd.DataFrame(data=data)], axis=0, ignore_index=True
                    )
                elif element["type"] == "relation":  # parks
                    data = {
                        f"{feature}s": [element["id"]],
                        "lat": [element["center"]["lat"]],
                        "lon": [element["center"]["lon"]],
                    }

                    df_feature = pd.concat(
                        [df_feature, pd.DataFrame(data=data)], axis=0, ignore_index=True
                    )
            print(df_feature.head(5))
            df_feature.to_csv(output_path, index=False)

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
                        [df_feature, pd.DataFrame(data=data)], axis=0, ignore_index=True
                    )
                elif element["type"] == "relation":  # parks
                    data = {
                        f"{feature}s": [element["id"]],
                        "lat": [element["center"]["lat"]],
                        "lon": [element["center"]["lon"]],
                    }

                    df_feature = pd.concat(
                        [df_feature, pd.DataFrame(data=data)], axis=0, ignore_index=True
                    )
            print(df_feature.head(5))
            df_feature.to_csv(output_path, index=False)


@click.command()
@click.argument("feature", type=click.Argument)
def cli_get_subways(feature: str) -> None:
    """
    Function for calling from CLI
    create a DataFrame with feature data
    :param feature:
    :return:
    """
    get_external(feature)


if __name__ == "__main__":
    cli_get_subways()
