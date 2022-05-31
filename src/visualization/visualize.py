import pandas as pd
import matplotlib.pyplot as plt


def feature_importance(df: pd.DataFrame, grid):
    """
    Function draws features importance
    :param df: Original DataFrame
    :param model:
    :return:
    """
    importance = pd.DataFrame(
        {
            "features": df.columns,
            "importance": grid.best_estimator_.steps[1][1].feature_importances_,
        }
    )
    importance.sort_values(by="importance", inplace=True)

    plt.figure(figsize=(8, 8))
    plt.barh(importance["features"], importance["importance"])
    plt.title("LGBM Feature Importance")
    plt.show()
