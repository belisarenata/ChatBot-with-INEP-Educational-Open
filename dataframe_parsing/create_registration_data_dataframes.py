import os
import sqlite3
import polars as pl
from enums import FKs
from helpers import ignore_rows_without_pk, recriate_header
import mappers


def create_and_concat_registration_data():
    files_path = "files/dataframe_parquet/Adequação da Formação Docente"
    years = os.listdir(files_path)
    registration_dataframe = pl.DataFrame()

    # Import a list with registration data fields and universal pk (school code)
    registration_fields = mappers.REGISTRATION_FIELDS
    school_fk = FKs.SCHOOL_CODE
    year_fk = FKs.YEAR
    
    fk_columns = [school_fk.name, year_fk.name]

    for year in years:
        df = pl.read_parquet(f"{files_path}/{year}")
        df = recriate_header(df)

        # Rename columns and drop row used as header
        df = df.rename(registration_fields)

        # Filter out registration fields and pk to a new df and drop null rows
        partial_registration_dataframe = df.select(fk_columns + list(registration_fields.values()))

        # Remove any row where pk is not convertible to number
        partial_registration_dataframe = ignore_rows_without_pk(partial_registration_dataframe, school_fk.name)

        if registration_dataframe.is_empty():
            registration_dataframe = partial_registration_dataframe

        else:
            registration_dataframe = pl.concat(
                [registration_dataframe, partial_registration_dataframe]
            ).unique(keep="last", subset=school_fk.name)

    #registration_dataframe.write_parquet("./data/registration.parquet")
    con = sqlite3.connect('database.db')

    registration_dataframe.write_database(
        table_name='registration',
        connection="sqlite:///database.db",
        engine="sqlalchemy",
        if_table_exists="replace"
    )


if __name__ == "__main__":
    create_and_concat_registration_data()
