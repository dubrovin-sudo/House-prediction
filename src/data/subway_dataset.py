from dataset_functions import *

df_subway = get_subways()
df_subway.to_csv('../../data/processed/spb_subways', index=False)
