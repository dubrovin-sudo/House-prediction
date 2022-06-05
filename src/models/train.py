import os

import click
import mlflow
from pycaret.regression import *
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

remote_mlflow_server_uri = os.getenv('MLFLOW_TRACKING_URI')
mlflow.set_tracking_uri(remote_mlflow_server_uri)
mlflow.set_experiment('init')
def train(
        df_train_path='../../data/processed/df_trainval.csv',
        # df_test_path="../../data/processed/df_test.npy",
        # model_path="../../models/model.clf",
        # results_path="../../reports/figures/results.json"
) -> None:
    """
    Function for train model
    :param df_train_path:
    :param df_test_path:
    :return:
    """
    df_train = pd.read_csv(df_train_path)

    with mlflow.start_run():
        reg = setup(data=df_train,
                    target='price',
                    categorical_features=['building_type', 'object_type',
                                          'levels', 'year', 'month', 'subway',
                                          # 'level',
                                          ],
                    # ordinal_features={'rooms':[0,1,2,3,4,5,6,7,8,9]},
                    high_cardinality_features=['subway'],
                    train_size=0.75,

                    preprocess=True,

                    normalize=True,
                    normalize_method='zscore',
                    transformation=True,

                    # pca=True,
                    # pca_components=15,

                    remove_outliers=False,
                    remove_perfect_collinearity=False,
                    transform_target=True,

                    fold_strategy='kfold',
                    fold=2,

                    silent=True,

                    log_experiment=True,
                    session_id=2700,
                    experiment_name='pycaret_experiments',
                    log_plots = True,
                    # log_profile=True,
                    # profile=True,
                    )

        lgbm = create_model('lightgbm',
                            fold=2)

        tuned_lgbm = tune_model(lgbm,
                                early_stopping=True,
                                optimize='R2',
                                search_library='optuna',
                                fold=2)

        final_lgbm = finalize_model(tuned_lgbm)



@click.command()
@click.argument("df_train_path", type=click.Path(exists=True), nargs=1)
# @click.argument("df_test_path", type=click.Path(), nargs=2)
# @click.argument("model_path", type=click.Path())
# @click.argument("results_path", type=click.Path())
def cli_train(df_train_path: str,
              # df_test_path: str,
              # model_path: str,
              # results_path: str
              ) -> None:
    """
    Function for train model
    :param df_train_path:
    # :param df_test:
    # :param model_path:
    # :param df_train:
    :return:
    """
    train(df_train_path,
          # df_test_path,
          # model_path,
          # results_path
          )
    print('Model saved!')
    # python3.8 train.py '../../models/model.clf' '../../data/processed/x_trainval.npy'
    # '../../data/processed/y_trainval.npy'
    # mlflow server --backend-store-uri sqlite:///mydb.sqlite --default-artifact-root ./mlruns/artifacts --host 0.0.0.0


if __name__ == "__main__":
    cli_train()
