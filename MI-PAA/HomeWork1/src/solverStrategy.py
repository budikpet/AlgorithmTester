from myDataClasses import Task, Solution

class SolverStrategy(object):
    
    def solve(self, task: Task):
        pass


class BruteForce(SolverStrategy):
    
    def solve(self, task: Task):
        print(f"BruteForce#{task.id} solving.")

class BranchBorder(SolverStrategy):
    
    def solve(self, task: Task):
        print(f"BranchBorder#{task.id} solving.")