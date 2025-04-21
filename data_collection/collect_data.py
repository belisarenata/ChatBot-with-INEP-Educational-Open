import data_reformating, download_data

# Is this working? Who knows!

def execute(
    extract_xlsx_from_zipped_files: bool | None = True,
    recreate_dataframes_parquet: bool | None = True,
    recreate_csv_files: bool | None = True,
    indicators_names: str | None = None,
    redownload_data: bool | None = True,
):
    download_data.execute(redownload_data, indicators_names)
    data_reformating.execute(
        extract_xlsx_from_zipped_files,
        recreate_dataframes_parquet,
        recreate_csv_files,
        indicators_names,
    )


if __name__ == "__main__":
    execute()
