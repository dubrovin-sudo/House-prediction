import json
import click
import joblib as jb
import numpy as np

from typing import Tuple
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def evaluate(
    model_path="../../models/model.clf",
    results_path="../../reports/figures/results.json",
    df_test=("../../data/processed/x_test.npy", "../../data/processed/y_test.npy"),
) -> None:
    """
    Function for score metrics saved of model
    :param df_test:
    :param model_path:
    :param results_path:
    :return:
    """
    x_test = np.load(df_test[0])
    y_test = np.load(df_test[1])

    model = jb.load(model_path)

    y_pred = model.predict(x_test)
    score = dict(
        r2=r2_score(y_test, y_pred),
        mse=mean_squared_error(y_test, y_pred),
        mae=mean_absolute_error(y_test, y_pred),
    )
    print(f'Coefficient of determination of model is {score["r2"]}')
    print(f'MSE metric of model is {score["mse"]}')
    print(f'MAE metric of model is {score["mae"]}')
    json.dump(score, open(results_path, "w"))


@click.command()
@click.argument("model_path", type=click.Path(exists=True))
@click.argument("results_path", type=click.Path())
@click.argument("df_test", type=click.Path(), nargs=2)
def cli_evaluate(model_path: str, results_path: str, df_test: Tuple[str]) -> None:
    """

    :param model_path:
    :param results_path:
    :param df_test:
    :return:
    """
    evaluate(model_path, results_path, df_test)
    # python3.8 evaluate.py "../../models/model.clf" "../../reports/figures/results.json"
    # "../../data/processed/x_test.npy" "../../data/processed/y_test.npy"


if __name__ == "__main__":
    cli_evaluate()
