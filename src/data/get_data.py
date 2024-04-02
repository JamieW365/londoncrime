import pandas as pd
from os.path import join
from os import environ
import sys
import pandas as pd
import requests
from src.utils import get_root_dir
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

def get_raw_data(local: bool = True,
                 raw_loc: str = join(get_root_dir(), 'data/raw'), 
                 url_current: str = None,
                 url_historical: str = None,
                 url_population: str = None,
                 overwrite: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:

    '''
    Retrieve the latest raw data files from given url or local directory.

        Parameters :
            local : boolean, default True
                When True this will retrieve raw data files from given local directory (see raw_loc).
                When False this will retrieve raw data files from given urls (see url_current, url_historical).

            raw_loc : str, optional
                The directory path that should hold raw, untouched data files. If not provided then this will
                default to the original project data structures file path.
            
            url_current : string, optional
                If local is False then current data will be loaded from the string provided in url_current. If
                not provided then this will default to the URL_CURRENT environment variable set in the project
                .env file.

            url_historical : string, optional
                If local is False then historical data will be loaded from the string provided in url_current. If
                not provided then this will default to the URL_HISTORICAL environment variable set in the project
                .env file.

            overwrite : boolean, default True
                When True this will overwrite any existing data files when loading raw data from url. When False
                then existing raw data files will remain in place.

        Returns :
            DataFrame, DataFrame
                Returns two separate DataFrames, the first containing current crime records, and the second containing
                historical crime records.
    '''
    
    # Load environment variables
    load_dotenv(find_dotenv())

    # Retrieve raw data from local directory
    if local:
        df_current = pd.read_csv(join(raw_loc, 'current.csv'))
        df_historical = pd.read_csv(join(raw_loc, 'historical.csv'))
        df_population = pd.read_csv(join(raw_loc, 'population.csv'))
    # Reload fresh raw data from government website
    else:
        if url_current == None:
            url_current = environ.get("URL_CURRENT")

        if url_historical == None:
            url_historical = environ.get("URL_HISTORICAL")

        if url_population == None:
            url_population = environ.get("URL_POP_BOROUGH")

        df_current = pd.read_csv(url_current)
        df_historical = pd.read_csv(url_historical)
        df_population = pd.read_csv(url_population)
        
        # Save raw data to local directory
        if overwrite:
            df_current.to_csv(join(raw_loc, 'current.csv'), index=False)
            df_historical.to_csv(join(raw_loc, 'historical.csv'), index=False)
            df_population.to_csv(join(raw_loc, 'population.csv'), index=False)

    return df_current, df_historical, df_population

if __name__ == '__main__':

    globals()[sys.argv[1]]()