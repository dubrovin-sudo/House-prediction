import click
import numpy as np
import joblib as jb
import lightgbm as lgb

from typing import Tuple
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GridSearchCV


def train(
        model_path="../../models/model.clf",
        df_train=(
                '../../data/processed/x_trainval.npy',
                '../../data/processed/y_trainval.npy',
        ),
) -> None:
    """
    Function for train model
    :param df_train:
    :param model_path:
    :return:
    """
    x_trainval = np.load(df_train[0])
    y_trainval = np.load(df_train[1])

    LGBregressor = lgb.LGBMRegressor
    pipe = make_pipeline(RobustScaler(), LGBregressor(random_state=42))
    param_grid = {
        "lgbmregressor__max_depth": [11],
        "lgbmregressor__n_estimators": [1000],
        "lgbmregressor__learning_rate": [0.1],
        # "lgbmregressor__num_thread": [-1],
    }
    model = GridSearchCV(pipe, param_grid, scoring="r2", cv=5, n_jobs=-1)
    model.fit(x_trainval, y_trainval)

    jb.dump(model, model_path)


@click.command()
@click.argument("df_train", type=click.Path(exists=True), nargs=2)
@click.argument("model_path", type=click.Path())
def cli_train(df_train: Tuple[str], model_path: str) -> None:
    """
    Function for train model
    :param model_path:
    :param df_train:
    :return:
    """
    train(df_train,model_path)
    print('Model saved!')
    # python3.8 train.py '../../models/model.clf' '../../data/processed/x_trainval.npy'
    # '../../data/processed/y_trainval.npy'


if __name__ == "__main__":
    cli_train()
