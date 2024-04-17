import pandas as pd
from src.utils import get_root_dir
import os

def count_per_pop(df: pd.DataFrame = None,
                  pop_count: int = 1000,
                  count_col: str = 'Count',
                  pop_col: str = 'Population'
                  ) -> pd.DataFrame:

    df[f'Count_Per_{str(pop_count)}'] = df[count_col] / (df[pop_col] / pop_count)

    return df


if __name__ == '__main__':

    pass