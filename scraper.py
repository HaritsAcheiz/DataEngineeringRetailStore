import json
import httpx
from googleapiclient.errors import HttpError
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request


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

    def create_service(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        with open('products-spreadsheet-395219-554760172bff.json') as f:
            token = json.load(f)
        print(token)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(token,scopes=scopes)
        print(creds)
        service = build('sheets', 'v4', credentials=creds)

        return service

    def create_sheet(self, service, title):
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            spreadsheet = service.spreadsheets().create(body=spreadsheet,fields='spreadsheetId').execute()
            print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")

            return spreadsheet.get('spreadsheetId')

        except HttpError as error:
            print(f"An error occurred: {error}")

            return error

    def get_values(self, service, spreadsheet_id, range_name):
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name).execute()
            rows = result.get('values', [])
            print(f"{len(rows)} rows retrieved")

            return result

        except HttpError as error:
            print(f"An error occurred: {error}")

            return error

    def update_values(self,service, spreadsheet_id, range_name, ):

    def to_google_sheet(self):
        pass

    def run(self):
        service = self.create_service()
        # result = self.create_sheet(service, title='first_try')
        self.get_values(service, spreadsheet_id='13JjE2R_vvwrPiMapF1g2m0Whrkdeci_rI7Y-osqGqlY', range_name="A1:C2")
        # return self.get_products()


if __name__ == '__main__':
    scraper = InsightScraper()
    scraper.run()