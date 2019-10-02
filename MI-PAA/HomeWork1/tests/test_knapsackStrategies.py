import os
import re
from knapsackSolver import knapsackSolver
from solverStrategy import Strategies
from myDataClasses import Solution
from click.testing import CliRunner

class FilePair:
    def __init__(self, file1, file2):
        if "_sol" in file1:
            self.solutionFile, self.dataFile = file1, file2
        else:
            self.solutionFile, self.dataFile = file2, file1

def getFiles(path: str):
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
    
    result = list()
    for (key, pair) in data.items():
        value = FilePair(pair[0], pair[1])
        result.append((key, value))

    result.sort()
    result = [pair for (_, pair) in result]

    return result

def checkFile(cliRunner, filePair: FilePair, strategy):
    print(f"Testing file: {filePair.dataFile}")
    solutions = cliRunner.invoke(knapsackSolver, ["--dataFile", filePair.dataFile, "-s", strategy]).output.split("\n")

    # Check values
    with open(filePair.solutionFile, "r") as solutionFile:
        for solution in solutions:
            if solution == "":
                break
            line = solutionFile.readline().split(" ")
            assert line[2] == solution.split(" ")[3]

def test_bruteForce_NR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NR')[0:2]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.BruteForce.name)

def test_branchBorder_NR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NR')[0:2]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.BranchBorder.name)

def test_bruteForce_ZR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/ZR')[0:2]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.BruteForce.name)

def test_branchBorder_ZR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/ZR')[0:2]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.BranchBorder.name)