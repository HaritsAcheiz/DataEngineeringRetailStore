import json
import time
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
        url = f'https://www.insight.com/api/product-search/search?country=US&q=*%3A*&instockOnly=false&start=0&salesOrg=2400&lang=en_US&category=hardware%2Fcomputer_components%2Fcomputer_accessories&rows=200&userSegment=CES%2CCES%2CCES%2CCES&tabType=products&locale=en_US&userSegment=CES'
        response = self.fetch(url)
        products = json.dumps(response.json()['products'])
        df = pd.read_json(products)
        print(df)

        # tree = self.parse(response)
        # title = tree.css_first('title').text(strip=True)
        # print(title)
        # print(tree.html)

    # def webdriver_setup(self):
    #     PROXY = '202.134.19.50:3128'
    #     opt = uc.ChromeOptions()
    #     # opt.add_argument(f'--proxy-server={PROXY}')
    #     driver = uc.Chrome(options=opt)
    #
    #     return driver
    #
    # def get_product_links2(self, driver):
    #     special_url = urljoin(self.base_url, 'specials?p=1')
    #     driver.get(special_url)
    #     wait = WebDriverWait(driver, 10)
    #     # wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR)))
    #     input('Press Any Key...')
    #
    #     print(driver.title)
    #
    # def run2(self):
    #     driver = self.webdriver_setup()
    #     self.get_product_links2(driver)
    #
    # def get_product_links(self, url):
    #     response = self.fetch(url)
    #     print(response)
    #     tree = self.parse(response)
    #     link_elements = tree.css('div.product-inner.product-inner-wide > div.absolute-link-wrapper > a')
    #     product_links = [link_element.attributes.get('href', None) for link_element in link_elements]
    #     return product_links
    #
    #
    #
    # def get_special_offer(self):
    #     special_url = urljoin(self.base_url, 'specials?p=1')
    #     product_links = self.get_product_links(self.base_url)


    def run(self):
        self.get_products()


if __name__ == '__main__':
    scraper = InsightScraper()
    scraper.run()
