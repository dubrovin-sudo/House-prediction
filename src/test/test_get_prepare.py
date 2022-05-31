import numpy as np

from src.models.prepare import cli_prepare_data
from click.testing import CliRunner


# Initialize runner
runner = CliRunner()


def test_cli_command():
    result = runner.invoke(
        cli_prepare_data,
        "data/processed/df_spb_processed.csv data/processed/x_trainval.npy "
        "data/processed/y_trainval.npy data/processed/x_test.npy "
        "data/processed/y_test.npy",
    )
    assert result.exit_code == 0


def test_output():
    x_trainval = np.load("data/processed/x_trainval.npy")
    # y_trainval = np.load("data/processed/x_trainval.npy")
    x_test = np.load("data/processed/x_trainval.npy")
    # y_test = np.load("data/processed/x_trainval.npy")
    assert x_trainval.shape[1] == 16
    assert x_test.shape[1] == 16
