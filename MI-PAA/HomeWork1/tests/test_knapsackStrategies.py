from knapsackSolver import knapsackSolver
from solverStrategy import Strategies, Modes
from myDataClasses import Solution
from helpers import FilePair, getFiles
from click.testing import CliRunner

def checkFile(cliRunner, filePair: FilePair, strategy, mode):
    print(f"Testing file: {filePair.dataFile}")
    solutions = cliRunner.invoke(knapsackSolver, ["--dataFile", filePair.dataFile, "-s", strategy.name, "--mode", mode.name]).output.split("\n")

    # Check values
    with open(filePair.solutionFile, "r") as solutionFile:
        for solution in solutions:
            if solution == "":
                break
            line = solutionFile.readline().split(" ")
            solution = solution.split(" ")
            if mode == Modes.Constructive:
                assert int(line[2]) == int(solution[3])
            else:
                assert int(solution[3]) >= int(solution[4]) or int(line[2]) == int(solution[3])
            print

def test_constructive_bruteForce_NR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NR')[0:3]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.BruteForce, Modes.Constructive)

def test_constructive_branchBound_NR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NR')[0:3]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.BranchBound, Modes.Constructive)

def test_constructive_unsortedBranchBound_NR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NR')[0:3]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.UnsortedBranchBound, Modes.Constructive)

def test_decision_bruteForce_NR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NR')[0:3]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.BruteForce, Modes.Decision)

def test_decision_branchBound_NR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NR')[0:3]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.BranchBound, Modes.Decision)

def test_decision_unsortedBranchBound_NR():
    path = './HomeWork1/data'
    cliRunner = CliRunner()

    dataFiles = getFiles(f'{path}/NR')[0:3]
    
    for filePair in dataFiles:
        checkFile(cliRunner, filePair, Strategies.UnsortedBranchBound, Modes.Decision)

# def test_constructive_bruteForce_ZR():
#     path = './HomeWork1/data'
#     cliRunner = CliRunner()

#     dataFiles = getFiles(f'{path}/ZR')[0:2]
    
#     for filePair in dataFiles:
#         checkFile(cliRunner, filePair, Strategies.BruteForce, Modes.Constructive)

# def test_constructive_branchBound_ZR():
#     path = './HomeWork1/data'
#     cliRunner = CliRunner()

#     dataFiles = getFiles(f'{path}/ZR')[0:3]
    
#     for filePair in dataFiles:
#         checkFile(cliRunner, filePair, Strategies.BranchBound, Modes.Constructive)