import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

import lxml


class Scraper:
    def __init__(self, url):
        self.url = url

        self.metadata = {
            'S.no':0,
            'data_source': 'Central Public Procurement portal',
            'data_collection_date': datetime.now().strftime("%Y-%m-%d"),
            'url': url,
            'other_metadata': 'Any additional information about the data'
        }
        self.row_count = 1
        
    def get_data(self):

        # getting whole html content 
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'lxml') # Use 'lxml' library instead of 'html.parser'
        
        tender_table=soup.find('table',attrs={'class':'list_table'}) # scraping and storing tables whose class name is"list_table"

        if tender_table:
            
            rows=tender_table.find_all('tr') # fetching the rows from the table
            for row in rows:
                

                cells = row.find_all('td') #fetching the table data



                if cells:
                    self.metadata['S.no'] = self.row_count

                    #storing the relevant info in tender dict
                    tender = {
                        'tender_published_Date': cells[1].text.strip(),
                        'tender_closing_date': cells[2].text.strip(),
                        'tender_opening_date': cells[3].text.strip(),
                        'tender_tile_and_id': cells[4].text.strip(),
                        'tender_origanisation':cells[5].text.strip(),
                    }
                    self.write_csv({**self.metadata, **tender})
                    self.row_count += 1
                
        else:
            print("unable to find the tenders table")
            return
    
    # to write the fetched data into csv file
    def write_csv(self, tender_info):
        fieldnames = ['S.no','data_source', 'data_collection_date', 'url', 'other_metadata',
                    'tender_published_Date','tender_closing_date' , 
                    'tender_opening_date','tender_tile_and_id',
                    'tender_origanisation']
        with open('e_tender_data.csv','a',newline='') as file:
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            if self.row_count == 1:
                writer.writeheader()
            writer.writerow(tender_info)


if __name__ == "__main__":
    # start = datetime.now()
    url = 'https://etenders.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct'
    scraper = Scraper(url)
    scraper.get_data()
    # end = datetime.now()
    # td = (end - start).total_seconds() * 10**3
    # print(f"The time of execution of above program is : {td:.03f}ms")
