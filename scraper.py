import json
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import pandas as pd

@dataclass
class InsightScraper:
    base_url = 'https://www.insight.com'

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        }

        with httpx.Client(headers=headers) as client:
            response = client.get(url, follow_redirects=True)

        return response

    def parse(self, response):
        tree = HTMLParser(response.text)

        return tree

    def get_products(self):
        url = f'https://www.insight.com/api/product-search/search?country=US&q=*%3A*&instockOnly=false&start=0&salesOrg=2400&lang=en_US&category=hardware%2Fcomputer_components%2Fcomputer_accessories&rows=100000&userSegment=CES%2CCES%2CCES%2CCES&tabType=products&locale=en_US&userSegment=CES'
        response = self.fetch(url)
        products = json.dumps(response.json()['products'])
        df = pd.read_json(products)

        return df

    def run(self):
        return self.get_products()


if __name__ == '__main__':
    scraper = InsightScraper()
    scraper.run()