import os
import unittest
import requests_mock
from main import Scraper

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.url = 'https://etenders.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct'
        self.scraper = Scraper(self.url)
        self.File_path=os.environ.get('FILE_PATH') or 'e_tender_data.csv'
    @requests_mock.Mocker()
    def test_get_data(self, mock_request):
        # prepare the mock response
        mock_html = """
        <table class='list_table'>
            <tr>
                <td>1</td>
                <td>01-01-2021</td>
                <td>01-01-2022</td>
                <td>01-01-2023</td>
                <td>Tender 1</td>
                <td>Organization A</td>
            </tr>
            <tr>
                <td>2</td>
                <td>02-01-2021</td>
                <td>02-01-2022</td>
                <td>02-01-2023</td>
                <td>Tender 2</td>
                <td>Organization B</td>
            </tr>
        </table>
        """
        mock_request.get(self.url, text=mock_html)

        # run the method
        self.scraper.get_data()

        # check if the data has been written to the file
        file_path = self.File_path
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 3)  # 2 tenders + header
            self.assertEqual(lines[0].strip(), 'S.no,data_source,data_collection_date,url,other_metadata,tender_published_Date,tender_closing_date,tender_opening_date,tender_tile_and_id,tender_origanisation')
            self.assertEqual(lines[1].strip(), '1,Central Public Procurement portal,2023-02-08,https://etenders.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct,Any additional information about the data,01-01-2021,01-01-2022,01-01-2023,Tender 1,Organization A')
            self.assertEqual(lines[2].strip(), '2,Central Public Procurement portal,2023-02-08,https://etenders.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct,Any additional information about the data,02-01-2021,02-01-2022,02-01-2023,Tender 2,Organization B')

if __name__ == '__main__':
    unittest.main()
