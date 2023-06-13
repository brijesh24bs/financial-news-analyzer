import requests as req
from bs4 import BeautifulSoup as BS
import pandas as pd
from src.FNAnalyzer.logging import logger
import os

url = [
    "https://www.businesstoday.in/latest/economy",
    "https://www.reuters.com/world/india/",
    "https://www.livemint.com/news"
]


class Extract:
    def __init__(self, url:list):
        self.url = url
        self.newsList = []
        self.file_path = 'artifacts/data.csv'

    def extract(self):
        for url in self.url:
            try:
                logger.info(f"Extracting news headlines from url: {url}.....")
                webpage = req.get(url)
                trav = BS(webpage.content, "html.parser")
                for link in trav.find_all('a'):
                    if (str(type(link.string)) == "<class 'bs4.element.NavigableString'>"
                            and len(link.string.strip()) > 35):
                        self.newsList.append(link.string.strip())
                logger.info("Extracting completed....")
            except Exception as e:
                logger.error(e)

    def save_data(self):
        try:
            df = pd.DataFrame(self.newsList, columns=['headline'])
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            df.to_csv(self.file_path)
        except Exception as e:
            logger.error(e)


obj = Extract(url)
obj.extract()
obj.save_data()