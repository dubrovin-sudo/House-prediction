import os
import click
import pandas as pd


def get_processed(output_processed="data/processed/df_spb_processed.csv") -> None:
    """
    Function concats DataFrames and add it to data/processed
    :param output_processed:
    :return:
    """

    if os.path.isfile(output_processed):
        print(f"You already have the df_spb_processed.csv dataset!")
        df_feature = pd.read_csv(output_processed)
        print(df_feature.head(5))

    else:
        for dirname, _, filenames in os.walk("data/interim"):
            filenames.remove(".gitkeep")
            feature = ["park", "subway"]
            for i, filename in enumerate(filenames):
                if filename != filenames[0]:
                    df_interim = pd.read_csv(f"data/interim/{filenames[0]}")
                    df_interim_add = pd.read_csv(f"data/interim/{filename}")

                    df_processed = pd.concat(
                        [
                            df_interim,
                            df_interim_add[[f"{feature[i]}s", f"{feature[i]}Distance"]],
                        ],
                        axis=1,
                    )

        df_processed.to_csv(output_processed, index=False)


@click.command()
@click.argument("output_processed", type=click.Path())
def cli_get_processed(output_processed: str) -> None:
    """
    Function for calling from CLI
    create a DataFrame with feature data
    :param output_processed:
    :return:
    """
    get_processed(output_processed)


if __name__ == "__main__":
    cli_get_processed()