import unittest
import os
import requests
from bs4 import BeautifulSoup
from main import Scraper
import csv

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.url = 'https://etenders.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct'
        self.scraper = Scraper(self.url)

    def test_get_data(self):
        self.scraper.get_data()
        self.assertEqual(self.scraper.row_count, 1)

        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'lxml')
        tender_table = soup.find('table', attrs={'class': 'list_table'})
        rows = tender_table.find_all('tr')
        self.assertEqual(len(rows), self.scraper.row_count-1)

    def test_write_csv(self):
        file_path = os.environ.get('FILE_PATH') or 'e_tender_data.csv'
        self.scraper.write_csv({'test_key': 'test_value'})

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            row = next(reader)
            self.assertIn('test_key', row)
            self.assertEqual(row['test_key'], 'test_value')

if __name__ == '__main__':
    unittest.main()
