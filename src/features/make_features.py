import pandas as pd
from features_functions import *

# чтение данных
df_subways = pd.read_csv("../../data/external/spb_subways")
df_spb = pd.read_csv("../../data/raw/df_spb")

# формирование данных с новыми характеристиками
df_spb_subway = subway_feature(df_spb, df_subways)
