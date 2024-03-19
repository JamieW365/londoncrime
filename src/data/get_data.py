import pandas as pd
import os
import sys
from pathlib import Path
from dotenv import find_dotenv, load_dotenv



def get_raw_data():

    load_dotenv(find_dotenv())
    
    df_current = pd.read_csv(os.environ.get("URL_CURRENT"))
    df_historical = pd.read_csv(os.environ.get("URL_HISTORICAL"))
    
    raw_loc = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'data/raw/'))

    df_current.to_csv(os.path.join(raw_loc, 'current.csv'))
    df_historical.to_csv(os.path.join(raw_loc, 'historical.csv'))

if __name__ == '__main__':
    globals()[sys.argv[1]]()