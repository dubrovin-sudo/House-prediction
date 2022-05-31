from src.features.select_region import cli_select_region
from click.testing import CliRunner


# Initialize runner
runner = CliRunner()


def test_cli_command():
    result = runner.invoke(
        cli_select_region, "data/raw/all_v2.csv data/raw/df_spb.csv 2661"
    )
    assert result.exit_code == 0
