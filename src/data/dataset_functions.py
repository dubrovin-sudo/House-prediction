import os
import kaggle
import zipfile
import requests
import pandas as pd


def get_all(path: str) -> pd.DataFrame:
    """
    Function load data from Kaggle and create pd.DataFrame
    :param path:
    :return:
    """
    kaggle.api.authenticate()
    name = "russia-real-estate-20182021"
    if os.path.isfile(f"{path}/raw/all_v2.csv"):
        print(f"You already have the full dataset!")
        df_spb = pd.read_csv(f"{path}/raw/df_spb.csv")
        print(df_spb.head(5))
    else:
        print(f"Downloading dataset : {name}!")

        kaggle.api.dataset_download_file(
            f"mrdaniilak/{name}",
            file_name="all_v2.csv",
            path=f"{path}/raw/",
        )

        with zipfile.ZipFile(f"{path}/raw/all_v2.csv.zip", "r") as zip_ref:
            zip_ref.extractall(f"{path}/raw")
        os.remove(f"{path}/raw/all_v2.csv.zip")

    df = pd.read_csv(f"{path}/raw/all_v2.csv")
    df_spb = df[df["region"] == 2661]
    df_spb.to_csv(f"{path}/raw/df_spb.csv", index=False)
    return df_spb


def get_subways(path: str) -> pd.DataFrame:
    """
    Function create a DataFrame with metro stations' data
    :param path:
    :return:
    """
    if os.path.isfile(f"{path}/external/spb_subways.csv"):
        print(f"You already have the spb_subways dataset!")
        df_subway = pd.read_csv(f"{path}/external/spb_subways.csv")
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
                    "StationName": [element["tags"]["name"]],
                    "lat": [element["lat"]],
                    "lon": [element["lon"]],
                }

                df_subway = pd.concat(
                    [df_subway, pd.DataFrame(data=data)], axis=0, ignore_index=True
                )
        df_subway.to_csv(f"{path}/external/spb_subways.csv", index=False)
        return df_subway
