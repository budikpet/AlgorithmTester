from knapsackSolver import knapsackSolver
from solverStrategy import Strategies
from myDataClasses import Solution
from helpers import FilePair, getFiles
from click.testing import CliRunner

def checkFile(cliRunner, filePair: FilePair, strategy, exact: bool = False):
    print(f"Testing file: {filePair.dataFile}")
    solutions = cliRunner.invoke(knapsackSolver, ["--dataFile", filePair.dataFile, "-t", False, "-s", strategy.name, "-e", 10]).output.split("\n")

    # Check values
    with open(filePair.solutionFile, "r") as solutionFile:
        for solution in solutions:
            if solution == "":
                break
            line = solutionFile.readline().split(" ")
            solution = solution.split(" ")

            if len(line) == 1:
                return

            if exact:
                # Check if found value matches exactly
                assert int(line[2]) == int(solution[2])
            else:
                # Check if the found value is at most the best value
                assert int(line[2]) >= int(solution[2])
            print

def test_constructive_DP_Weight_NK():
    path = './data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NK')[0:2]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.DPWeight, exact=True)

def test_constructive_DP_NK():
    path = './data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NK')[0:2]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.DP, exact=True)

def test_constructive_Greedy_NK():
    path = './data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NK')[0:5]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.Greedy)

def test_constructive_GreedyOne_NK():
    path = './data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NK')[0:5]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.GreedyOne)

def test_constructive_FPTAS_NK():
    path = './data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NK')[0:2]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.FPTAS)