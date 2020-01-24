import os
from typing import List
import time

def create_path(path: str):
    """
    Creates a required directory path if it does not exist.
    
    Arguments:
        path {str} -- Directory path.
    """
    if not os.path.isdir(path):
        os.makedirs(path)

def get_input_files(path: str) -> List[str]:
    """
    Gets all files from the path.
    
    Arguments:
        path {str} -- Directory to get files from.
    
    Returns:
        List[str] -- List of filenames.
    """
    output = list()

    for root, _, files in os.walk(path):
        for file in files:
            output.append(file)

    return output

def curr_time_millis():
    return round(time.time(), 3)