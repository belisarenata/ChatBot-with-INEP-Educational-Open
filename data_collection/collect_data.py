import data_reformating, download_data, crawler

# Is this working? Who knows!

def execute(
    re_request_pages: bool | None = True,
    redownload_technical_notes: bool | None = False,
    extract_xlsx_from_zipped_files: bool | None = True,
    recreate_dataframes_parquet: bool | None = True,
    recreate_csv_files: bool | None = False,
    indicators_names: str | None = None,
    redownload_data: bool | None = False,
):
    crawler.execute(re_request_pages, redownload_technical_notes)
    download_data.execute(redownload_data, indicators_names)
    data_reformating.execute(
        extract_xlsx_from_zipped_files,
        recreate_dataframes_parquet,
        recreate_csv_files,
        indicators_names,
    )


if __name__ == "__main__":
    execute()
