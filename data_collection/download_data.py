import os
import requests
import crawler

# TODO: FIX extract zipped files. Rebase at 3a.m. is not always a good ideia, who could imagine?
# TODO: add parametrization by year

downloaded_files_path = "./files/downloaded_data"


def download_data(indicators_name: str | None = None):
    file_download_link_by_indicator_by_year = crawler.execute()
    for indicator, info in file_download_link_by_indicator_by_year.items():
        if indicators_name and indicator not in indicators_name:
            continue

        # If destiny folder doesn't exists, creates it
        os.makedirs(f"{downloaded_files_path}/{indicator}", exist_ok=True)

        for year, download_link in info.items():
            # Download file with data and store it
            try:
                response = requests.get(download_link)
                filename = f"{downloaded_files_path}/{indicator}/{download_link.split('/')[-1]}"
                open(filename, "wb").write(response.content)

            except Exception as e:
                print(indicator, year, e)


def execute(
    redownload_data: bool | None = False,
    indicators_names: str | None = None,
):
    if redownload_data:
        download_data(indicators_names)

    print(f"Downloaded files at {downloaded_files_path}")


if __name__ == "__main__":
    execute()
