import pandas as pd
import sys
from os.path import join, abspath, dirname
from src.utils import get_root_dir

def combine_data(df_current: pd.DataFrame,
                 df_historical: pd.DataFrame,
                 output_filepath: str = join(get_root_dir(), 'data/interim'),
                 overwrite: bool = True) -> pd.DataFrame:

    '''
    Combine current and historical crime data into a single interim data set
    '''

    # Rename columns to something more workable
    df_current.rename(columns={'MajorText': 'Major',
                               'MinorText': 'Minor',
                               'LookUp_BoroughName': 'Borough'},
                      inplace=True)
    
    df_historical.rename(columns={'MajorText': 'Major',
                               'MinorText': 'Minor',
                               'LookUp_BoroughName': 'Borough'},
                         inplace=True)

    # Drop Historical Fraud and Forgery from the data
    df_current.drop(df_current[df_current['Minor']=='Historical Fraud and Forgery'].index, inplace=True)
    df_historical.drop(df_historical[df_historical['Minor']=='Historical Fraud and Forgery'].index, inplace=True)

    df_total = df_historical.merge(df_current, how='outer', on=('Major', 'Minor', 'Borough')).fillna(0)

    if overwrite:
        df_total.to_csv(join(output_filepath, 'total_crime.csv'), index=False)

    return df_total

def restructure_data(df_crime: pd.DataFrame,
                     df_population: pd.DataFrame) -> pd.DataFrame:

    '''
    Transform data into time-series
    '''

    # By stacking the data we can merge all date columns into a single column which can be used for time-series analysis
    df_reshaped = df_crime.set_index(['Major', 'Minor', 'Borough']).stack().reset_index().rename(columns={'level_3': 'Date',
                                                                                                          0: 'Count'})
    
    # Convert year month filed from integer to type date-time
    df_reshaped['Date'] = pd.to_datetime(df_reshaped['Date'], format='%Y%m')

    # Save year for population merging
    df_reshaped['Year'] = df_reshaped['Date'].dt.year

    # Merge yearly population
    df_reshaped = df_reshaped.merge(df_population[['Name', 'Population', 'Year']], 
                                    how='inner', 
                                    left_on=['Borough', 'Year'], 
                                    right_on=['Name', 'Year']) \
                             .drop(['Name', 'Year'], axis=1)

    return df_reshaped

if __name__ == '__main__':

    globals()[sys.argv[1]]()