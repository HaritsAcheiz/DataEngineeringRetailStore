import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from urllib.parse import urljoin

@dataclass
class IherbScraper:
    base_url = 'https://www.iherb.com'

    def fetch(self, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
        }

        with httpx.Client(headers=headers, follow_redirects=True) as client:
            response = client.get(url)

        return response

    def parse(self, response):
        tree = HTMLParser(response.text)

        return tree

    def get_product_links(self, url):
        response = self.fetch(url)
        tree = self.parse(response)
        link_elements = tree.css('div.product-inner.product-inner-wide > div.absolute-link-wrapper > a')
        product_links = [link_element.attributes.get('href', None) for link_element in link_elements]
        return product_links



    def get_special_offer(self):
        special_url = urljoin(self.base_url, 'specials?p=1')
        product_links = self.get_links(special_url)


    def run(self):
        self.get_special_offer()

if __name__ == '__main__':
    scraper = IherbScraper()
    scraper.run()
