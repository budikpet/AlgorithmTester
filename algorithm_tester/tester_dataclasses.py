from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum
import re
import numpy as np

class AnalysisFile:

    def __init__(self, filename: str, full_path: str):
        parts = filename.replace(".dat", "").split("_")
        # self.num_of_items = int(re.findall("[0-9]+", parts[0])[0])
        self.dataset = parts[0]
        self.instance_info = parts[1]
        self.algorithm = parts[3]
        
        if len(parts) > 4:
            self.relative_mistake = float(parts[3].replace(",", "."))
        else:
            self.relative_mistake = float(-1)

        self.full_path = full_path