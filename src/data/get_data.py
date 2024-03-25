import pandas as pd
import os
import sys
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

def get_raw_data(url_current = None,
                 url_historical = None,
                 raw_loc = None):

    '''
    Retrieve the latest raw data files from given url
    '''
    
    # Load environment variables
    load_dotenv(find_dotenv())
    
    if url_current != None:
        url_current = os.environ.get("URL_CURRENT")

    if url_historical != None:
        url_historical = os.environ.get("URL_HISTORICAL")

    df_current = pd.read_csv(os.environ.get("URL_CURRENT"))
    df_historical = pd.read_csv(os.environ.get("URL_HISTORICAL"))
    
    if raw_loc != None:
        raw_loc = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'data/raw/'))

    df_current.to_csv(os.path.join(raw_loc, 'current.csv'))
    df_historical.to_csv(os.path.join(raw_loc, 'historical.csv'))

    return df_current, df_historical

if __name__ == '__main__':

    globals()[sys.argv[1]]()