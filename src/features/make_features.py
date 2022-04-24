from src.features.subway_features import subway_features


RAW_DF_SPB_PATH = "data/raw/df_spb.csv"
SPB_SUB_PATH = "data/external/spb_subways.csv"
SPB_SUB_FEATURE_PATH = "data/interim/spb_house_with_subway.csv"


if __name__ == "__main__":
    # Download datasets
    subway_features(RAW_DF_SPB_PATH, SPB_SUB_PATH, SPB_SUB_FEATURE_PATH)
