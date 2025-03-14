import os
import json
import click
import mlflow
import numpy as np
import joblib as jb
import lightgbm as lgb

from typing import Tuple
from dotenv import load_dotenv
from mlflow.models.signature import infer_signature
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

load_dotenv()
remote_server_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(remote_server_uri)
# mlflow.set_experiment("real_estate")


def train(
    df_train=(
        "../../data/processed/x_trainval.npy",
        "../../data/processed/y_trainval.npy",
    ),
    df_test=("../../data/processed/x_test.npy", "../../data/processed/y_test.npy"),
    model_path="../../models/model.clf",
    results_path="../../reports/figures/results.json",
) -> None:
    """
    Function for train model
    :param df_test:
    :param results_path:
    :param df_train:
    :param model_path:
    :return:
    """

    with mlflow.start_run():
        mlflow.get_artifact_uri()
        print(mlflow.get_artifact_uri())

        x_trainval = np.load(df_train[0])
        y_trainval = np.load(df_train[1])

        # initialize and train model
        LGBregressor = lgb.LGBMRegressor
        pipe = make_pipeline(RobustScaler(), LGBregressor(random_state=42))
        param_grid = {
            "lgbmregressor__max_depth": [10, 11],
            "lgbmregressor__n_estimators": [1000],
            "lgbmregressor__learning_rate": [0.01, 0.1],
            # "lgbmregressor__num_thread": [-1],
        }
        params = {
            k.replace("lgbmregressor__", "") if "lgbmregressor__" in k else k: v
            for k, v in param_grid.items()
        }
        model = GridSearchCV(pipe, param_grid, cv=5, n_jobs=-1)
        model.fit(x_trainval, y_trainval)
        print(params)

        jb.dump(model, model_path)

        x_test = np.load(df_test[0])
        y_test = np.load(df_test[1])

        y_pred = model.predict(x_test)
        score = dict(
            r2=r2_score(y_test, y_pred),
            mse=mean_squared_error(y_test, y_pred),
            mae=mean_absolute_error(y_test, y_pred),
        )
        # Create an input example, signature to store in the MLflow model registry
        signature = infer_signature(x_test, y_pred)
        input_example = np.expand_dims(x_test[0], axis=0)

        mlflow.log_params(params)
        mlflow.log_artifact(model_path)
        mlflow.log_metrics(score)
        mlflow.lightgbm.log_model(
            lgb_model=model,
            artifact_path="model",
            registered_model_name="real_estate_lgbm",
            signature=signature,
            input_example=input_example,
        )

        print(f'Coefficient of determination of model is {score["r2"]}')
        print(f'MSE metric of model is {score["mse"]}')
        print(f'MAE metric of model is {score["mae"]}')
        json.dump(score, open(results_path, "w"))


@click.command()
@click.argument("df_train", type=click.Path(exists=True), nargs=2)
@click.argument("df_test", type=click.Path(), nargs=2)
@click.argument("model_path", type=click.Path())
@click.argument("results_path", type=click.Path())
def cli_train(
    df_train: Tuple[str], df_test: Tuple[str], model_path: str, results_path: str
) -> None:
    """
    Function for train model
    :param results_path:
    :param df_test:
    :param model_path:
    :param df_train:
    :return:
    """
    train(df_train, df_test, model_path, results_path)
    print("Model saved!")
    # python3.8 train.py '../../data/processed/x_trainval.npy'
    # '../../data/processed/y_trainval.npy'
    # '../../data/processed/x_test.npy' '../../data/processed/y_test.npy'
    # '../../models/model.clf'
    # '../../reports/figures/results.json'


if __name__ == "__main__":
    cli_train()
    # export MLFLOW_S3_ENDPOINT_URL=http://0.0.0.0:9000
    # export AWS_ACCESS_KEY_ID=minioadmin
    # export AWS_SECRET_ACCESS_KEY=minioadmin
    # Поднять модель через mlflow
    # mlflow models serve --no-conda -m
    # s3://arts/0/fdbe82916e074915ac7a1c15c86cafd9/artifacts/model -h 0.0.0.0 -p 8001
