import os
from pathlib import Path

'''
Utility functions ot be used throughout project modules
'''

def get_root_dir() -> str:
    '''
    Returns the absolute path of the project root directory.
    '''
    
    file_dir = str(Path(os.path.abspath(__file__)))
    target_dir = 'londoncrime'
    project_dir = file_dir[:file_dir.index(target_dir) + len(target_dir)]
    print(project_dir)
    pass

if __name__ == '__main__':

    breakpoint()