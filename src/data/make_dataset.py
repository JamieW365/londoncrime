# -*- coding: utf-8 -*-
# import click
import logging
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from src.data.get_data import get_raw_data
from src.data.clean_data import combine_data, restructure_data

def main(input_filepath: str = None, 
         output_filepath: str = None):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    if input_filepath == None:
        input_filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'data/raw/'))

    if output_filepath == None:
        output_filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'data/processed/'))

    # Get current and historical raw data
    df_current, df_historical = get_raw_data(raw_loc=input_filepath)

    # Generate merged interim data, combining current and historical data
    df_total = combine_data(df_current, df_historical)

    # Restructure total data set to time-series
    df_reshaped = restructure_data(df_total)

    df_reshaped.to_csv(os.path.join(output_filepath, 'final.csv'), index=False)
    
    return df_reshaped

if __name__ == '__main__':

    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
