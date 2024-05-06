import pandas as pd
from src.data.make_dataset import main
from src.utils import get_root_dir
import pmdarima as pm
import pickle
import os

def build_arima(df: pd.DataFrame = None,
                field: str | list[str] = 'Major',
                values: str | list[str] = None,
                output_filepath: str = os.path.join(get_root_dir(), 'models'),
                trace: bool = True):
    
    if df.empty:
        df = main()

    if values == None:
        values = df[field].unique()

    for item in values:

        print(item, '...')

        trend = df[df[field]==item].groupby('Date').sum(numeric_only=True)['Count']
        # train = trend.iloc[:-12]
        # test = trend.iloc[-12:]

        model = pm.auto_arima(trend, 
                              m=12,                 # frequency of series                      
                              seasonal=True,        # TRUE if seasonal series
                              d=None,               # let model determine 'd'
                              test='adf',           # use adftest to find optimal 'd'
                              start_p=0, start_q=0, # minimum p and q
                              max_p=12, max_q=12,   # maximum p and q
                              D=None,               # let model determine 'D'
                              trace=trace,
                              error_action='ignore',  
                              suppress_warnings=True, 
                              stepwise=True)
        
        with open(os.path.join(output_filepath, f'{item}.pkl'), 'wb') as file:  
            pickle.dump(model, file)

        

def build_all_models(df: pd.DataFrame = None,
                     build_borough: bool = True,
                     build_major: bool = True,
                     output_filepath: str = os.path.join(get_root_dir(), 'models')) -> None:

    print('Building models...')

    if df == None:
        df = main()

    if build_borough:
        build_arima(df, field='Borough')

    if build_major:
        build_arima(df, field='Major')


if __name__ == '__main__':

    print('Running train_models')
    build_all_models()