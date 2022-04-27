from src.data.get_raw import get_raw
from src.data.get_subways import get_subways

SPB_SUB_PATH = "data/external/spb_subways.csv"
ALL_PATH = "data/raw/all_v2.csv"
SPB_PATH = "data/raw/df_spb.csv"

if __name__ == "__main__":
    # Download datasets
    get_raw(ALL_PATH, SPB_PATH)
    get_subways(SPB_SUB_PATH)
