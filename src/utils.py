import os
from pathlib import Path

'''
Utility functions ot be used throughout project modules
'''

def get_root_dir() -> str:
    '''
    Returns the absolute path of the project root directory.
    '''

    return str(Path(os.path.abspath(__file__)).parents[1])
