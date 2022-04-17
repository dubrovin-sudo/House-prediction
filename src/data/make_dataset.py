import os
import kaggle
import zipfile


kaggle.api.authenticate()


def download_current_data():
    """
    Downloads the data
    """
    directory = f"{os.path.abspath(os.getcwd())}/data/external"
    name = "russia-real-estate-20182021"
    if os.path.isfile(f"{directory}/all_v2.csv"):
        print(f"You already have the newest data!")
    else:
        kaggle.api.dataset_download_file(
            f"mrdaniilak/{name}",
            file_name="all_v2.csv",
            path=directory,
        )
        print(f"Downloading dataset : {name}!")

        with zipfile.ZipFile(f"{directory}/all_v2.csv.zip", "r") as zip_ref:
            zip_ref.extractall(f"{directory}")
        os.remove(f"{directory}/all_v2.csv.zip")


if __name__ == "__main__":
    # Download, unzip
    download_current_data()
