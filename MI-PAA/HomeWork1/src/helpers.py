import os
import click
import re
import shutil
from math import log, ceil
from solverStrategy import Strategies
from myDataClasses import Modes

class FilePair:
    def __init__(self, file1, file2):
        if "_sol" in file1:
            self.solutionFile, self.dataFile = file1, file2
        else:
            self.solutionFile, self.dataFile = file2, file1

@click.group()
def helpers():
    pass

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

def to_csv(output_folder, input_folder, file_name: str):
    with open(f'{input_folder}/{file_name}', "r") as inF:
        with open(f'{output_folder}/{file_name.replace(".dat", ".csv")}', "w") as outF:
            line = inF.readline()
            while line:
                split = line.split("|")

                if len(split) < 2:
                    line = inF.readline()
                    continue

                data = split[0].strip().replace(" ", ";")
                bag = split[1].strip().replace(" ", "")

                outF.write(f'{data};{bag}\n')

                line = inF.readline()

@helpers.command()
@click.option("--dir_name", "--output_folder_name", type=str, default="result_csv")
@click.argument("input_dir", required=True)
@click.argument("output_dir", required=True)
def output_to_csv(dir_name, input_dir, output_dir):
    output_folder = f'{output_dir}/{dir_name}'

    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    for root, _, files in os.walk(input_dir):
        for file_name in files:
            to_csv(output_folder, root, file_name)
    print

def get_sums_dict(filepath, strategy, sums_dict, item_num):
    lines = list()
    with open(filepath, "r") as input_file:
        lines = input_file.readlines()
        currSum = 0
        for line in lines:
            currSum += int(line.split(" ")[1])

        if item_num not in sums_dict:
            sums_dict[item_num] = dict()

        if strategy not in sums_dict[item_num]:
            sums_dict[item_num][strategy] = currSum
        else:
            sums_dict[item_num][strategy] += currSum

    return lines

0, 1, 2,   3,  4,  5,  6,  7,  8,  9        
4, 7, 10, 13, 16, 19, 22, 25, 28, 31
def write_hist(output_folder, strategy, hist_dict, lines, startExp, endExp, step):
    if strategy not in hist_dict:
        hist_dict[strategy] = [0 for exp in range(startExp, endExp, step)]
    
    for line in lines:
        split = line.split(" ")
        if len(split) < 2:
            continue

        numOfConfigs = int(split[1])
        index = max(ceil(log(numOfConfigs + 1, 2)), startExp)
        index = min(index, endExp)
        index -= startExp
        index = ceil(index/step)
        hist_dict[strategy][index] += 1

def agregate(sorted_files, histogram_for_value: int, output_folder):
    step = 2
    startExp = 4
    endExp = 32

    sums_dict = dict()
    hist_dict = dict()
    for item_num in sorted(sorted_files):
        for filepath in sorted_files[item_num]:
            filename = filepath.split("/")[-1]
            strategy = filename.split("_inst_")[1].replace(".dat", "")
            lines = get_sums_dict(filepath, strategy, sums_dict, item_num)
            if item_num == histogram_for_value:
                # Create histogram file for current file
                write_hist(output_folder, strategy, hist_dict, lines, startExp, endExp, step)
    
    with open(f'{output_folder}/sums.csv', "w") as sums_file:
        sums_file.write(f"file;Sum_{Strategies.BruteForce.name};Sum_{Strategies.BranchBound.name}\n")
        for (item_num, sums_by_methods) in sums_dict.items():
            bf_sum = sums_by_methods[Strategies.BruteForce.name]
            bb_sum = sums_by_methods[Strategies.BranchBound.name]
            sums_file.write(f'{item_num};{ceil(bf_sum/500)};{ceil(bb_sum/500)}\n')

    with open(f'{output_folder}/hist.csv', "w") as hist_file:
        hist_file.write(f"maximum_num;Count_{Strategies.BruteForce.name};Count_{Strategies.BranchBound.name}\n")
        count_tuples = list(zip(hist_dict[Strategies.BruteForce.name], hist_dict[Strategies.BranchBound.name]))
        for i, (brute_count, branch_count) in enumerate(count_tuples):
            if i != 0:
                hist_file.write(f'(2^{(i - 1)*step + startExp}, 2^{i*step + startExp}>;{brute_count};{branch_count}\n')
            else:
                hist_file.write(f'(0, 2^{i*step + startExp}>;{brute_count};{branch_count}\n')
            
    print

def create_clean_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)

@helpers.command()
@click.option("--value", type=int, default=4, help="File for which to get histogram values for.")
@click.option("--dir_name", "--output_folder_name", type=str, default="agregatedResults")
@click.argument("input_dir", required=True)
@click.argument("output_dir", required=True)
def agregated_results(dir_name, value, input_dir, output_dir):
    output_folder = f'{output_dir}/{dir_name}'

    create_clean_folder(output_folder)

    sorted_files = get_files_dict(input_dir)
    agregate(sorted_files, value, output_folder)
            
    print

@helpers.command()
@click.option("--stop", type=int, default=1000)
def test(stop):
    from time import sleep
    for i in range(1, stop):
        sleep(1)
        print(f'Test: {i}')

if __name__ == "__main__":
    helpers()   # pylint: disable=no-value-for-parameter