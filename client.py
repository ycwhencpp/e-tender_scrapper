import logging
import os 

URL = os.environ.get('URL') or 'https://etenders.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct'
LOG_FILE = os.environ.get('LOG_FILE') or  'scraper.log'
FILE_PATH = os.environ.get('FILE_PATH') or 'e_tender_data.csv'
LOG_LEVEL = logging.INFO
