from train_model import get_model
from src.utils import get_root_dir
import os

def forecast(item: str = None,
             periods: int = 60,
             conf_int: bool = True,
             filepath: str = os.path.join(get_root_dir(), 'models')):

    return get_model(item, filepath).predict(n_periods=periods, return_conf_int=conf_int, alpha=0.5)

if __name__ == '__main__':

    pass