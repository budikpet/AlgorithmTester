import os
import click
import re
import shutil
from math import log, ceil
from typing import List
from algorithm_tester.solver_strategy import Strategies
from algorithm_tester.mydataclasses import AnalysisFile

class FilePair:
    def __init__(self, file1, file2):
        if "_sol" in file1:
            self.solutionFile, self.dataFile = file1, file2
        else:
            self.solutionFile, self.dataFile = file2, file1

@click.group()
def helpers():
    pass

def get_analysis_files(path: str):
    """ 
    Reads analysisOutput files in path.

    Returns a list of AnalysisFile objects

    """
    data = list()
    
    # r=root, d=directories, f = files
    for root, _, files in os.walk(path):
        for file in files:
            if "column" not in file:
                full_path = f'{root}/{file}'
                data.append(AnalysisFile(file, full_path))
    return data

def get_files_dict(path: str):
    data = dict()
    
    # r=root, d=directories, f = files
    for root, _, files in os.walk(path):
        for file in files:
            value = f'{root}/{file}'
            key = int(re.findall("[0-9]+", file)[0])

            if key in data.keys():
                data[key].append(value)
            else:
                data[key] = [value]
    return data

def getFiles(path: str):
    data = get_files_dict(path)
    
    result = list()
    for (key, pair) in data.items():
        value = FilePair(pair[0], pair[1])
        result.append((key, value))

    result.sort()
    result = [pair for (_, pair) in result]

    return result

inputModes = ["data", "solution"]

@helpers.command()
@click.option("--mode", type=click.Choice(inputModes), default=inputModes[0])
@click.argument("directory", required=True)
def get_test_files(mode, directory):
    filePairs = getFiles(path=directory)

    for pair in filePairs:
        if mode == "data":
            print(pair.dataFile)
        else:
            print(pair.solutionFile)

if __name__ == "__main__":
    helpers()   # pylint: disable=no-value-for-parameter