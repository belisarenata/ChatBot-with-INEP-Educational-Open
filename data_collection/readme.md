# Data Collection

## Crawler

First, we access INEP's page with all available researches.
Then, each one of them is crawled to get the download link to a specific research for the specif year.
Since download links are (hopefully) immutable, a binary folder is created with a dict of strings with following this format: 
{
    indicator:
    {
        year: link,
        year2: link2, 
    },
    indicator2: ... 
}

This crawler should only be rerun if something crashes on the following step. 

## Download data

Now, with a specific link for each research data, we actually download the data.
Once again, since this data is (hopefully) mostly immutable, do not run this step again unless strictly necessary. 

## Data Reformating

Files are download either in a zip file containing .xlsx, .ods and some metadata in a .txt or are downloaded directly as .xlxs
We either extract or simply copy the file to a new location where every file is a .xlxs
Then, optionally, parse it to csv and/or polars dataframe.  
You might be wondering why all this files are necessary. They are not.
But considering I don't want to handle ~180 files every time I have a new idea, it takes me 3 lines to export files in a format using polars and I wanted to learn how to use git LFS, :shrug: 