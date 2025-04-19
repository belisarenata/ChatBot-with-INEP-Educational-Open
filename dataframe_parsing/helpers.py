import polars as pl
from thefuzz import fuzz
from enums import FKs


def recriate_header(df, n_rows: int | None = 3):
    # Every file comes with a standardized header that will be ignored.
    # This probably should be done on data_collection, but hey, better late than never, right?
    
    school_fk = FKs.SCHOOL_CODE
    year_fk = FKs.YEAR
    
    # New header values
    for _ in range(5):
        new_header = df.row(n_rows)
        if school_fk.value not in new_header:
            n_rows += 1
    else:
        if school_fk.value not in new_header:
            print("Check ths mf file")        

    # Rename columns and drop row used as header
    df = df.rename({old: new for old, new in zip(df.columns, new_header) if new})
    df = df.filter(pl.arange(0, df.height) >= n_rows)

    # Set fk names 
    df = df.rename({school_fk.value: school_fk.name, year_fk.value: year_fk.name})


    return df


def find_starting_position_by_value(df, string_or_enum, indicator_name):
    # I'm 100% sure there's a better way to do this
    # What is done here is:
    # We iterate over all values in the 10 first lines of the dataframe and try to find a fuzzy match with the given str
    # The given string should be an educational level, ideally the first one (Educação Infantil) in the usual order on sheets
    # Why fuzzy? Because names can change from year to year for the same indicator
    # I.e. "Educação Infatil" can become "Educacao infatil" or even "Educacao infatil anos inicias" in a given year
    # Another possibility is the name of a given educational level be followed "wrapped" around other info". 
    # I.e. "10 Hora-aula diária média - Educação Infantil", or "'Taxa de Distorção Idade-Série - Ensino Fundamental de 8 e 9 anos'"
    # So there's another check for that. This is tricky can lead to mistakes, since one educacional levels can be present in other string. I.E. EJA - Ensino Médio
    # Why? If you find out, please tell me. This entire multi-level indexing is annoying a.f. Just create separate sheets, you know?
    # So, if a fuzzy match is good enough, we early return the index of the line with the value.
    # Since iter_rows doesn't provide a counter, I added it by hand
    # If nothing is found, return None

    df_to_iter = df.head(10)
    index = 0
    str_value = string_or_enum if isinstance(string_or_enum, str) else string_or_enum.value
    if '(' in indicator_name: 
        #remove everything after opening parenthesis + empty space before it 
        indicator_name = indicator_name.split('(')[0][:-1]
    for row in df_to_iter.iter_rows(named=True):
        for column_name, value in row.items():
            if value:
                if str_value in value:
                    return column_name
                
                ratio = fuzz.ratio(value.removeprefix(indicator_name), str_value)   
                if ratio > 75:
                    print(value, column_name)  # Manually checking if something is off
                    return column_name
                
        index += 1
    return None


# Function to iterate over each line and each column of the reduced dataframe to find new index values
# Since I'm 100% noobie with polars (I miss you, pandas!, but also not), this is chatGpt code :shrug: 
# I'm also 100% sure there's a better way to do this
def find_new_header_index_by_value(df, str_value): 
    registration_fields_line_index = None

    # Iterar pelas linhas do dataframe
    for i in range(df.shape[0]):  # range baseado no número de linhas
        if registration_fields_line_index: 
            break
        line = df[i].to_dict(as_series=False)  # Obtemos os dados da linha como dicionário
        for value in line.values():  # Itera sobre os valores da linha
            if str_value in str(value):  # Verifica se o valor procurado está presente
                registration_fields_line_index = i  # Se encontrado, armazena o índice da linha
                break  # Paramos a busca na linha atual após encontrar o valor

    return registration_fields_line_index


def ignore_rows_without_pk(df, pk):
    df = df.filter(pl.col(pk).cast(pl.Int32, strict=False).is_not_null())
    return df
