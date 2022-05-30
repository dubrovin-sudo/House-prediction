import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def corr_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Visualize correlation matrix
    :param df: Original DataFrame
    :return: corr DataFrame
    """
    corrmat = df.corr()
    fig, axes = plt.subplots(figsize=(15, 15))
    sns.heatmap(
        corrmat, annot=True, cmap="YlGnBu", linewidths=0.1, annot_kws={"fontsize": 10}
    )

    return corrmat


def spearman(df: pd.DataFrame, corrmat: pd.DataFrame) -> pd.DataFrame:
    """
    Visualize sorted spearman correlations' coefficients
    :param df: Original DataFrame
    :param corrmat: corr DataFrame
    :return: features
    """
    features = corrmat[["price"]].sort_values(["price"], ascending=False)
    features = [f for f in features.index if f != "price"]
    spr = pd.DataFrame()
    spr["feature"] = features
    spr["spearman"] = [df[f].corr(df["price"], "spearman") for f in features]
    spr = spr.sort_values("spearman")
    plt.figure(figsize=(15, 10))
    sns.barplot(data=spr, y="feature", x="spearman", orient="h")

    return features
