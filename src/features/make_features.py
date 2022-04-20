import pandas as pd
from features_functions import *

# чтение данных
directory = f"{os.path.abspath(os.getcwd())}/data"
print(directory)
df_subways = pd.read_csv(f"{directory}/external/spb_subways.csv")
df_spb = pd.read_csv(f"{directory}/raw/df_spb.csv")

# формирование данных с новыми характеристиками
df_spb_subway = subway_feature(df_spb, df_subways)
