Requirements:

Install requirements (pip install -r requirements.txt)

## Create a .env 

At the root folder, create a .env file and add your on a var named OPEN_AI_KEY 

## DB

Use your own db file or create one with inep educational data following the next steps. You can also download it from kaggle: https://www.kaggle.com/datasets/belisarenata/inep-educacional-surveys-database

## Recriating the db

well, if you insist... 

run data_collection/collect_data.py and be patient. Lots of downloads there. I highly suggest using a debugger to check if the progress is smooth. 

run dataframe_parsing/create_registration_data_dataframes.py to create your db file with the registration data

run dataframe_parsing/split_data_by_education_level.py to populate the db with actual data 

## Some comments about coding style

When choosing between concision or performance over readability, I always pick readability.

This is the first time I'm using polars, sqlite, langchain and basically every lib except for beautifulsoup4.

This code is far from optimal, especially data collection and data parsing. Coming from pandas, polars require a new way of thinking that I'm not used to (yet!). 

This code was written so anyone could understand it and/or what I could do in the moment :shrug:
