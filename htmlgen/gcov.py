from collections import defaultdict
from collections import namedtuple

Branch = namedtuple('Branch', ['lineno', 'path', 'times'])
Function = namedtuple('Function', ['name', 'lineno', 'times'])
Line = namedtuple('Line', ['lineno', 'times'])

def pair():
    return [None, None]

class Source:
    def __init__(self, filename):
        self.filename = filename
        self.branches = defaultdict(pair)
        self.functions = {}
        self.lines = {}

    def add_branch(self, branch):
        self.branches[branch.lineno][branch.path] = branch

    def add_function(self, func):
        self.functions[func.lineno] = func

    def add_line(self, line):
        self.lines[line.lineno] = line
