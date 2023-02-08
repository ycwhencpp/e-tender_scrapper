import csv
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import client

class Scraper:
    def __init__(self, url, log_level=logging.INFO):


        self.url = url
        self.row_count = 1

        # fetching the filepath from the os 
        self.file_path = client.FILE_PATH


        # create a FileHandler and set a log file
        self.log_file = client.LOG_FILE 

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.log_level = log_level

        self._setup_logging()
        self.metadata = self._get_meta_data()
        self.fieldnames=self._get_field_names()

    def _setup_logging(self):

        # create a FileHandler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.log_level)

        # create a formatter and set it to the file handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # add the file handler to the logger
        self.logger.addHandler(file_handler)

        

    # returns the metadata
    def _get_meta_data(self):
        return {
            'S.no': 0,
            'data_source': 'Central Public Procurement portal',
            'data_collection_date': datetime.now().strftime("%Y-%m-%d"),
            'url': self.url,
            'other_metadata': 'Any additional information about the data'
        }

    # return fieldnames
    def _get_field_names(self):
        return [
                'S.no','data_source', 'data_collection_date', 'url', 'other_metadata',
                'tender_published_Date','tender_closing_date' , 
                'tender_opening_date','tender_tile_and_id',
                'tender_origanisation'
        ]


    # scrapes the url for relevant data
    def get_data(self):

        self.logger.info("Starting the data collection")

        # getting whole html content 
        try:
            page = requests.get(self.url)
            soup = BeautifulSoup(page.text, 'lxml')
            tender_table = soup.find('table', attrs={'class': 'list_table'})
        
        except Exception as e:
            self.logger.error("Error in fetching the data from the URL. %s", e)
            return

        if tender_table:  # if data is availaible writing it to the file 
        
            rows = tender_table.find_all('tr')

            for row in rows:

                cells = row.find_all('td')
                if cells:
                    self.metadata['S.no'] = self.row_count
                    tender = {
                        'tender_published_Date': cells[1].text.strip(),
                        'tender_closing_date': cells[2].text.strip(),
                        'tender_opening_date': cells[3].text.strip(),
                        'tender_tile_and_id': cells[4].text.strip(),
                        'tender_origanisation': cells[5].text.strip(),
                    }
                    self.write_csv({**self.metadata, **tender})
                    self.row_count += 1

        else:
            self.logger.error("Unable to find the tenders table")
            return


    # writing tender data into the csv file
    def write_csv(self, tender_info):


        # write_header flag is only set to True if the file doesn't already exist and the row_count is 1
        write_header = False 
        if self.row_count == 1:
            write_header = True 

        with open(self.file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(tender_info)

        
        self.logger.info(f"Scraped data has been written to {self.file_path}")




def main():

    start_time = datetime.now()

    scraper = Scraper(client.URL, log_level=client.LOG_LEVEL)
    scraper.get_data()

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    scraper.logger.info(f"Elapsed time: {elapsed_time}")


if __name__ == "__main__":
    
    main()





    
