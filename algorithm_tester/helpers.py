import os

class FilePair:
    def __init__(self, file1, file2):
        if "_sol" in file1:
            self.solutionFile, self.dataFile = file1, file2
        else:
            self.solutionFile, self.dataFile = file2, file1

def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def get_files_dict(path: str):
    data = dict()
    
    # r=root, d=directories, f = files
    for root, _, files in os.walk(path):
        for file in files:
            parts = file.split("_")
            value = f'{root}/{file}'
            key: str = parts[1]

            if key.isnumeric():
                key = int(key)

            if key in data.keys():
                data[key].append(value)
            else:
                data[key] = [value]
    return data

def get_input_files(path: str):
    output = list()

    for root, _, files in os.walk(path):
        for file in files:
            output.append(file)

    return output