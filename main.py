import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

class scraper:
    def __init__(self, url):
        self.url = url
        self.tenders = []
        self.metadata = {
            'data_source': 'Central Public Procurement portal',
            'data_collection_date': datetime.now().strftime("%Y-%m-%d"),
            'url': url,
            'other_metadata': 'Any additional information about the data'
        }
        
    def get_data(self):

        # getting whole html content 
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content,'html.parser')


        tender_table=soup.find('table',attrs={'class':'list_table'}) # scraping and storing tables whose class name is"list_table"

        if tender_table:

            rows=tender_table.find_all('tr') # fetching the rows from the table

            for row in rows:

                if 'list_header' in row['class']: # if it is the header row just skip it 
                    continue

                cells = row.find_all('td') #fetching the table data

                if len(cells) > 0:

                    #storing the relevant info in tender dict
                    tender = {
                        'S.no': cells[0].text.strip(),
                        'tender_published_Date': cells[1].text.strip(),
                        'tender_closing_date': cells[2].text.strip(),
                        'tender_opening_date': cells[3].text.strip(),
                        'tender_tile_and_id': cells[4].text.strip(),
                        'tender_origanisation':cells[5].text.strip(),
                }
                self.tenders.append(tender)
        else:
            print("unable to find the tenders table")
            return
    
    # to write the fetched data into csv file
    def write_csv(self):

        with open('check.csv','w',newline='') as file:

            # intailising the field names
            fieldnames = ['data_source', 'data_collection_date', 'url', 'other_metadata',
                          'S.no','tender_published_Date','tender_closing_date' , 
                          'tender_opening_date','tender_tile_and_id',
                          'tender_origanisation']

            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for tender in self.tenders:
                tender.update(self.metadata)
                writer.writerow(tender)

if __name__ == '__main__':
    scraper = scraper('https://etenders.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct')
    scraper.get_data()
    scraper.write_csv()




