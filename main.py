import os
import requests
import csv
from bs4 import BeautifulSoup
import logging
import logging.config

class scraper:
    def __init__(self, url):
        self.url = url
        self.tenders = []
        
    def get_data(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content,'html.parser')
        tender_table=soup.find('table',attrs={'class':'list_table'})
        print(tender_table)
        if tender_table:
            rows=tender_table.find_all('tr')
            for row in rows:
                # if 'list_header' in row['class']:
                #     continue
                cols = row.find_all('td')
                cols =[col.text.strip() for col in cols]
                self.tenders.append(cols)
        else:
            print("unable to find the tenders table")

    def write_csv(self):
        with open('etenders.csv','w',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['S.no','E-published Date','Closing Date' , 'Opening Date','Title and Ref.No./Tender ID','Organisation Chain'])
            writer.writerows(self.tenders)

if __name__ == '__main__':
    scraper = scraper('https://etenders.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct')
    scraper.get_data()
    scraper.write_csv()




