from dataset_functions import *

if __name__ == "__main__":
    directory = f"{os.path.abspath(os.getcwd())}/data/"
    # Download datasets
    get_all(directory)
    get_subways(directory)
