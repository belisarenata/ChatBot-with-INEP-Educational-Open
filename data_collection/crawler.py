from collections import defaultdict
import pickle
import re
from bs4 import BeautifulSoup
import requests


def indicators_crawler():
    # This is a roughly constructed crawler for the page on september-2024;
    # Changes on the page can create the need for updating this code.

    base_url = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais"
    requested_page = requests.get(base_url, timeout=30)
    content = requested_page.text
    soup = BeautifulSoup(content, features="html.parser")

    # Find all the divs with class "card great-cards"
    cards = soup.find_all("div", class_="card great-cards")

    # Ignore cards that are not under "Educação Básica" manually
    # This is a far from ideal approach.
    # A better approach to this is getting only the cards under "Educação Básica",
    # but due to the way page is constructed, this would add some complexity.
    cards = cards[:-3]

    indicators = defaultdict()
    for card in cards:
        name = card.text.strip("\n")
        link = card.contents[1].attrs["href"]
        indicators[name] = link

    return indicators


def year_crawler(indicators: dict):
    # TODO: Add parametrization to crawl page on different filters and parse downloaded data accordingly

    file_download_link_by_indicator_by_year = defaultdict(lambda: defaultdict())
    for indicator, link in indicators.items():
        requested_page = requests.get(link, timeout=30)
        if requested_page.status_code == 200:
            content = requested_page.text
            soup = BeautifulSoup(content, features="html.parser")

            # Now, we figure what years are available to each indicator
            # This check has the side effect to ignore multiple-years indicators (Ex: "Taxas de Transição")

            # Find all tabs with yearly info
            yearly_tabs = soup.find_all("div", class_="tab")

            # Get only tabs text, a.k.a. the year, that are an actual year.
            # Aditional check is necessary to avoid ignoring badly formated years (Ex: 2023. on "Taxas de Não-resposta")
            actual_years = [
                x
                for tab in yearly_tabs
                if (x := tab.text.strip("\n")) and x.isnumeric() or x[:-1].isnumeric()
            ]

        for year in actual_years:
            # Again, due to the way the page is build, it's simpler, thought time-consuming, to request yearly pages
            requested_year_page = requests.get(url=f"{link}/{year}", timeout=30)
            if requested_year_page.status_code == 200:
                content = requested_year_page.text
                soup = BeautifulSoup(content, features="html.parser")

                # Get the tag that has the word "Escolas" in the tag's text.
                # This is done because in some pages, tags have extra info (Ex: "updated at...") or extra blank spaces
                download_info = soup.find("a", string=re.compile(r"\.*Escolas\.*"))
                if download_info:
                    file_download_link_by_indicator_by_year[indicator][year] = (
                        download_info.attrs["href"]
                    )

    return file_download_link_by_indicator_by_year


def technical_note_crawler(indicators: dict):
    # TODO: CREATE CRAWLER FOR TECHNICAL NOTES
    return


def execute(
    re_request_pages: bool | None = False,
    redownload_technical_notes: bool | None = False,
):
    indicators = indicators_crawler()
    if re_request_pages:
        file_download_link_by_indicator_by_year = year_crawler(indicators)
        serializable_dict = {
            k: v
            for k, v in file_download_link_by_indicator_by_year.items()
            if not callable(v)
        }
        with open("./data_collection/file_download_link_by_indicator_by_year", "wb") as file:
            pickle.dump(serializable_dict, file)
        return file_download_link_by_indicator_by_year
    try:
        with open("./data_collection/file_download_link_by_indicator_by_year", "rb") as file:
            file_download_link_by_indicator_by_year = pickle.load(file)
        return file_download_link_by_indicator_by_year
    except Exception:
        print("No dict found. Run again with 're_request_pages = True'")

    if redownload_technical_notes:
        indicators = technical_note_crawler()


if __name__ == "__main__":
    execute()
