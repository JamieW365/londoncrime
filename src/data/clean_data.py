import pandas as pd
import os

def combine_data(df_current: pd.DataFrame,
                 df_historical: pd.DataFrame) -> pd.DataFrame:

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

    df_total.to_csv(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'data/interim/total_crime.csv')), index=False)

    return df_total

def restructure_data(df: pd.DataFrame) -> pd.DataFrame:

    '''
    Transform data into time-series
    '''

    # By stacking the data we can merge all date columns into a single column which can be used for time-series analysis
    df_reshaped = df.set_index(['Major', 'Minor', 'Borough']).stack().reset_index().rename(columns={'level_3': 'Date',
                                                                                                     0: 'Count'})
    
    # Convert year month filed from integer to type date-time
    df_reshaped['Date'] = pd.to_datetime(df_reshaped['Date'], format='%Y%m')

    return df_reshaped

if __name__ == '__main__':

    globals()[sys.argv[1]]()