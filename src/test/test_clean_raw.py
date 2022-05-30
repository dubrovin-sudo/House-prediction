import pandas as pd
import great_expectations as ge

from src.features.clean_raw import cli_clean_raw
from click.testing import CliRunner


# Initialize runner
runner = CliRunner()


def test_cli_command():
    result = runner.invoke(cli_clean_raw, 'data/raw/df_spb.csv data/interim/clean_raw_data.csv')
    assert result.exit_code == 0


def test_output():
    df = pd.read_csv('data/interim/clean_raw_data.csv')
    df_ge = ge.from_pandas(df)

    expected_columns = ['price', 'date', 'geo_lat', 'geo_lon', 'building_type', 'level',
                        'levels', 'rooms', 'area', 'kitchen_area', 'object_type']
    assert df_ge.expect_table_columns_to_match_ordered_list(column_list=expected_columns).success is True
    assert df_ge.expect_column_values_to_be_of_type(column='price', type_='int64').success is True
    assert df_ge.expect_column_values_to_not_be_null(column='geo_lat').success is True





