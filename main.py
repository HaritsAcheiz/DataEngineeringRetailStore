import pandas as pd

from scraper import InsightScraper

if __name__ == '__main__':
    # s = InsightScraper()
    # product_df = s.run()
    # product_df.to_csv('products.csv', index=False)
    product_df = pd.read_csv('products.csv')
    product_df.info()