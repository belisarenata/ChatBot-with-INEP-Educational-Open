import re
import zipfile
import polars as pl
import os
import shutil

# TODO: FIX extract zipped files. Rebase at 3a.m. is not always a good ideia, who could imagine?
# TODO: add parametrization by year



def extract_zipped_files(indicators_names: str | None = None):
    root_files_path = "files"
    file_format = "xlsx"

    downloaded_files_path = f"{root_files_path}/downloaded_data"
    sub_folders = os.listdir(downloaded_files_path)

    # List all files inside folders, indexed by indicator
    files_by_indicators = {
        folder: os.listdir(f"{downloaded_files_path}/{folder}")
        for folder in sub_folders if not folder.startswith('.')
    }

    for indicator, file_names in files_by_indicators.items():
        if indicators_names and indicator not in indicators_names:
            continue

        origin_path = f"{downloaded_files_path}/{indicator}"

        # If destiny folder doesn't exists, creates it
        destiny_path = f"{root_files_path}/{file_format}/{indicator}"
        os.makedirs(destiny_path, exist_ok=True)

        for file_name in file_names:
            # Get only numerical values from file
            year = re.sub(r"\D", "", file_name)

            # Non-standard named files requires ignoring extra numbers
            year = year[:4]

            file = f"{origin_path}/{file_name}"

            # Check if file is a zip folder
            if zipfile.is_zipfile(file):

                # Abre o arquivo ZIP
                with zipfile.ZipFile(file, "r") as zip_ref:

                    # Tenta encontrar o primeiro arquivo .xlsx no ZIP
                    xlsx_filename = next(
                        (f for f in zip_ref.NameToInfo if f.endswith(".xlsx")),
                        None,
                    )
                    # Verifica se o arquivo .xlsx foi encontrado
                    # Honestly, there's gotta be a better way to do it
                    if xlsx_filename:
                        with zip_ref.open(xlsx_filename) as inner_file:
                            # Use os.path.basename to get the last part of the file name
                            base_filename = os.path.basename(xlsx_filename)
                            with open(
                                f"{destiny_path}/{base_filename}", "wb"
                            ) as destiny_file:
                                destiny_file.write(inner_file.read())

            else:
                shutil.copy(file, f"{destiny_path}/{file_name}")


def create_file_on_new_format(
    indicators_names: str | None = None,
    recreate_csv_files: bool | None = True,
    recreate_parquet: bool | None = True,
):

    # Being overzealous, I'm always using O.G. file as input
    root_files_path = "files"
    xlsx_files_path = f"{root_files_path}/xlsx"
    sub_folders = os.listdir(xlsx_files_path)

    # List all files inside folders, indexed by indicator
    files_by_indicators = {
        folder: os.listdir(f"{xlsx_files_path}/{folder}") for folder in sub_folders
    }

    for indicator, file_names in files_by_indicators.items():
        if indicators_names and indicator not in indicators_names:
            continue

        # If destiny folder doesn't exists, creates it
        os.makedirs(f"{root_files_path}/dataframe_parquet/{indicator}", exist_ok=True)
        os.makedirs(f"{root_files_path}/csv/{indicator}", exist_ok=True)

        indicator_path = f"{xlsx_files_path}/{indicator}"
        for file_name in file_names:
            dataframe = pl.DataFrame()
            # Get only numerical values from file
            year = re.sub(r"\D", "", file_name)

            # Badly named files requires ignoring extra numbers
            year = year[:4]

            dataframe = pl.read_excel(f"{indicator_path}/{file_name}")

            if dataframe.is_empty:
                if recreate_parquet:
                    dataframe.write_parquet(
                        f"{root_files_path}/dataframe_parquet/{indicator}/{year}.parquet"
                    )

                if recreate_csv_files:
                    dataframe.write_csv(f"{root_files_path}/csv/{indicator}/{year}.csv")


def execute(
    extract_xlsx_from_zipped_files: bool | None = True,
    recreate_dataframes_parquet: bool | None = True,
    recreate_csv_files: bool | None = False,
    indicators_names: str | None = None,
):
    if extract_xlsx_from_zipped_files:
        extract_zipped_files()

    if recreate_dataframes_parquet or recreate_csv_files:
        create_file_on_new_format(
            indicators_names, recreate_csv_files, recreate_dataframes_parquet
        )
    print("Done")


if __name__ == "__main__":
    execute()
