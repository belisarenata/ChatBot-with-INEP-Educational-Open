# Before running this file, tun create_registration_data_dataframes.py to create the db

import os
import polars as pl
from enums import Indicator, FKs
from helpers import (
    find_starting_position_by_value,
    recriate_header,
    ignore_rows_without_pk,
)
import mappers


def create_and_concat_registration_data():
    school_fk = FKs.SCHOOL_CODE
    year_fk = FKs.YEAR
    
    fk_columns = [school_fk.name, year_fk.name]
    #original_fk_columns = [school_fk.value, year_fk.value]
    
    indicator_dicts = mappers.INDICATOR_DICTS
    categorical_indicators_n_by_name = mappers.NO_CATEGORICAL_INDICATORS
    non_leveled_indicator = mappers.SINGLE_VALUE_INDICATOR

    root_files_path = "./files/dataframe_parquet"
    sub_folders = os.listdir(root_files_path)

    # TODO: Figure out what to do with this.
    sub_folders.remove(Indicator.INSE.value)
    
    # List all files inside folders, indexed by indicator
    files_by_indicators = {
        folder: os.listdir(f"{root_files_path}/{folder}") for folder in sub_folders
    }

    for indicator, file_names in files_by_indicators.items():
        table_name = indicator.replace(" ", "_").removesuffix("parquet")
        indicator_dataframe = pl.DataFrame()
        indicator_dict = indicator_dicts.get(Indicator(indicator))

        categorical_values_df = True if indicator in categorical_indicators_n_by_name.keys() else False

        for file_name in file_names:
            df = pl.read_parquet(f"{root_files_path}/{indicator}/{file_name}")

            # Remove registration fields
            df = recriate_header(df)

            # Drop entirely empty rows
            df.filter(~pl.all_horizontal(pl.all().is_null()))

            # Some research use single vars for each school, some are divided by education levels. Single values are straight forward to handle:
            if indicator in non_leveled_indicator:
                df = ignore_rows_without_pk(df, school_fk.name)
                df = df.select(fk_columns,
                               value=df.columns[-1])

                indicator_dataframe = pl.concat([indicator_dataframe, df])

                indicator_dataframe.write_database(
                            table_name = table_name,
                            connection="sqlite:///database.db",
                            engine="sqlalchemy",
                            if_table_exists="append"
                        )
                continue

            # Try to find the row where the name of the first educational level of this indicator is
            # Trigger warning: bad coding. 
            column_name = find_starting_position_by_value(
                df, x:=next(iter(indicator_dict[next(iter(indicator_dict.keys()))].keys())), indicator_name=indicator
            )

            if not column_name:
                print(file_name, indicator, x)
                import warnings
                warnings.warn("Failed to gather data from: {file_name}, {indicator}, {x}")
                continue

            start_column_position = df.columns.index(column_name)

            for indicator_field_name in indicator_dict:
                indicator_items = indicator_dict[indicator_field_name]

                for educacional_level, sub_levels in indicator_items.items():
                    number_of_sub_levels = len(sub_levels) if sub_levels else 1
                    for sub_level_n in range(number_of_sub_levels):   

                        number_of_categories = categorical_indicators_n_by_name.get(indicator, 1)
                        data_fields = [indicator_field_name] if number_of_categories == 1 else [f"Categoria{n+1}" for n in range(number_of_categories)]

                        data_field_indicator = pl.DataFrame() 
                        for field_name in data_fields:
                            field = field_name.replace(" ", "_")
                            # Gather fks and value
                            categorical_df = df.select(
                                fk_columns,
                                value = df.columns[start_column_position],
                            )

                            # Rename value column
                            categorical_df = categorical_df.rename(
                                {categorical_df.columns[-1]: field}
                            )

                            # Add level fk
                            categorical_df = categorical_df.with_columns(
                                etapa=pl.lit(educacional_level.value),
                                classe=pl.lit(sub_levels[sub_level_n] if sub_levels else None)
                            ).cast(pl.Utf8)

                            categorical_df = ignore_rows_without_pk(categorical_df, school_fk.name)

                            categorical_df = categorical_df.filter(pl.col(field) != '--')
                            categorical_df = categorical_df.drop_nulls(subset=field)
                            categorical_df = categorical_df.with_columns(categorical_df.select(pl.col(field).cast(pl.Float32)))

                            data_field_indicator = pl.concat([data_field_indicator, categorical_df], how="diagonal")
                            start_column_position += 1
                
                        if categorical_values_df: 
                            indicator_categories = [indicator_field_name] if number_of_categories == 1 else [f"Categoria{n+1}" for n in range(number_of_categories)]
                           
                            data_field_indicator = data_field_indicator.group_by(["SCHOOL_CODE", "YEAR", "etapa", "classe"]).agg([
                                pl.col(category).sum() for category in indicator_categories
                            ])

                        
                        if indicator != Indicator.REND.value:
                            print(indicator, file_name, educacional_level, sub_level_n)
                            data_field_indicator.write_database(
                                table_name = table_name,
                                connection="sqlite:///database.db",
                                engine="sqlalchemy",
                                if_table_exists="append"
                            )

                        indicator_dataframe = pl.concat([indicator_dataframe, data_field_indicator], how="diagonal")
                        
        # This dataframe is harder to write step by step due to file format. Each "category" (i.e. reproval, approval or dropout) is sequentially listed.
        # My computer has no RAM to handle parsing 12kk lines to database 
        # That's why I'm "gambiarrando" this ):) 
        if indicator == Indicator.REND.value:
            indicator_categories = indicator_dict.keys()
                            
            indicator_dataframe = indicator_dataframe.group_by(["SCHOOL_CODE", "YEAR", "etapa", "classe"]).agg([
                pl.col(category).sum() for category in indicator_categories
            ])

            print(indicator)
            indicator_dataframe = indicator_dataframe.rechunk()

            yearly_dataframes = indicator_dataframe.partition_by("YEAR")
            for data_frame in yearly_dataframes:
                data_frame.write_database(
                    table_name = table_name,
                    connection="sqlite:///database.db",
                    engine="sqlalchemy",
                    if_table_exists="append"
                )


if __name__ == "__main__":
    create_and_concat_registration_data()
