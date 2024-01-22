import os
import urllib.parse
import httpx
from dataclasses import dataclass
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
@dataclass
class InsightScraper:
    base_url = 'https://www.insight.com'

    def fetch(self, url):
        print('Fetching data...')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        }

        with httpx.Client(headers=headers) as client:
            response = client.get(url, follow_redirects=True, timeout=10.0)

        if response.status_code != 200:
            response.raise_for_status()
        print('Data Collected!')
        return response

    def parse(self, response):
        print('Parsing product information...')
        json_data = response.json()
        products = json_data['products']
        print('Product information parsed!')
        return products

    def get_products(self):
        print('Get product information...')
        endpoint = '/gapi/product-search/search?country=US&q=*:*&instockOnly=false&start=0&salesOrg=2400&lang=en_US&category=hardware/computer_components&rows=20000&tabType=products&locale=en_US&userSegment=CES'
        url = urllib.parse.urljoin(self.base_url, endpoint)
        response = self.fetch(url)
        result = self.parse(response)
        print('Product information collected!')
        return result

    def to_database(self, products):
        print('Importing data into database...')
        df = pd.DataFrame.from_dict(products)
        df = pd.concat([df.drop(columns=['price', 'listPrice'], axis=1), df['price'].apply(pd.Series)], axis=1)
        DATABASE_USER = os.getenv('DATABASE_USER')
        DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
        DATABASE_HOST = os.getenv('DATABASE_HOST')
        DATABASE_PORT = os.getenv('DATABASE_PORT')
        DATABASE = os.getenv('DATABASE')
        engine = create_engine(f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE}')
        with engine.begin() as conn:
            conn.exec_driver_sql("""
            DROP TABLE IF EXISTS "public"."products"
            """)

            conn.exec_driver_sql("""CREATE TABLE "public"."products" (
            "searchProductId" VARCHAR(100) NOT NULL PRIMARY KEY,
            "alternateImage" TEXT,
            "availability" VARCHAR(20),
            "availabilityMessage" VARCHAR(50),
            "averageRating" FLOAT4,
            "description" TEXT,
            "image" TEXT,
            "manufacturerImage" TEXT,
            "insightPrice" FLOAT4,
            "listPrice" FLOAT4,
            "longDescription" TEXT,
            "manufacturerName" VARCHAR (100),
            "manufacturerPartNumber" VARCHAR (100),
            "materialId" VARCHAR (100),
            "reviewCount" INT4,
            "sku" VARCHAR (100),
            "callForPrice" bool,
            "bullet1" TEXT,
            "bullet2" TEXT,
            "bullet3" TEXT,
            "bullet4" TEXT,
            "bullet5" TEXT,
            "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            "modified_by" VARCHAR(20) DEFAULT CURRENT_USER,
            "webPrice" FLOAT4)
            """
            )

            conn.exec_driver_sql("""
            CREATE TEMPORARY TABLE temp_table AS SELECT * FROM "public"."products" WHERE false
            """
            )

            df.to_sql("temp_table", conn, index=False, if_exists="append")

            conn.exec_driver_sql("""
            INSERT INTO "public"."products" ("searchProductId", "alternateImage", "availability", "availabilityMessage",
            "averageRating", "description", "image", "manufacturerImage", "insightPrice", "listPrice", "longDescription",
            "manufacturerName", "manufacturerPartNumber", "materialId", "reviewCount", "sku", "callForPrice", "bullet1",
            "bullet2", "bullet3", "bullet4", "bullet5", "webPrice") SELECT "searchProductId", "alternateImage",
            "availability", "availabilityMessage", "averageRating", "description", "image", "manufacturerImage",
            "insightPrice", "listPrice", "longDescription", "manufacturerName", "manufacturerPartNumber", "materialId",
            "reviewCount", "sku", "callForPrice", "bullet1", "bullet2", "bullet3", "bullet4", "bullet5", "webPrice"
            FROM "temp_table"
            ON CONFLICT ("searchProductId")
            DO UPDATE SET
            "alternateImage" = EXCLUDED."alternateImage",
            "availability" = EXCLUDED."availability",
            "availabilityMessage" = EXCLUDED."availabilityMessage",
            "averageRating" = EXCLUDED."averageRating",
            "description" = EXCLUDED."description",
            "image" = EXCLUDED."image",
            "manufacturerImage" = EXCLUDED."manufacturerImage",
            "insightPrice" = EXCLUDED."insightPrice",
            "listPrice" = EXCLUDED."listPrice",
            "longDescription" = EXCLUDED."longDescription",
            "manufacturerName" = EXCLUDED."manufacturerName",
            "manufacturerPartNumber" = EXCLUDED."manufacturerPartNumber",
            "materialId" = EXCLUDED."materialId", 
            "reviewCount" = EXCLUDED."reviewCount",
            "sku" = EXCLUDED."sku",
            "callForPrice" = EXCLUDED."callForPrice",
            "bullet1" = EXCLUDED."bullet1",
            "bullet2" = EXCLUDED."bullet2",
            "bullet3" = EXCLUDED."bullet3",
            "bullet4" = EXCLUDED."bullet4",
            "bullet5" = EXCLUDED."bullet5",
            "webPrice" = EXCLUDED."webPrice"
            """
            )

        print('Data imported successfully!')

    def run(self):
        print('Program is running...')
        products = self.get_products()
        self.to_database(products)
        print('Task Completed!')

if __name__ == '__main__':
    scraper = InsightScraper()
    scraper.run()