import mlflow
import numpy as np
import pytest

from src.models.train import cli_train
from click.testing import CliRunner
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient


# Initialize runner
runner = CliRunner()


# def test_cli_command():
#     result = runner.invoke(
#         cli_train,
#         "data/processed/x_trainval.npy data/processed/y_trainval.npy "
#         "data/processed/x_test.npy data/processed/y_test.npy "
#         "models/model.clf reports/figures/results.json",
#     )
#     assert result.exit_code == 0

# def test_score():
#     result = runner.invoke(
#         cli_train,
#         "data/processed/x_trainval.npy data/processed/y_trainval.npy "
#         "data/processed/x_test.npy data/processed/y_test.npy "
#         "models/model.clf reports/figures/results.json",
#     )
#     mlflow.get_artifact_uri()
#     client = MlflowClient()
#     experiment_id = '0'
#     run = client.create_run(experiment_id)
#     print(f'run id: {run.info.run_id}')
#     print('---')
#     accuracy = train(model, inputs = batches[0])
#     assert accuracy == pytest.approx((0.95, abs=0.05))


