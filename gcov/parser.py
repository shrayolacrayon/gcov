from __future__ import division
from source import Source, Branch, Function, Line
import os
from collections import defaultdict, namedtuple

Coverage = namedtuple('Coverage', ['hits', 'total', 'percent'])
Summary = namedtuple('Summary', ['lines', 'functions', 'branches'])

def make_coverage(cov):
    perc = round(cov[0] / cov[1] * 100, 2)
    return Coverage(cov[0], cov[1], perc)

class TracefileParser:
    def __init__(self, filename, basepath = None):
        if not os.path.isfile(filename):
            raise IOError('No such file' + filename)
        self.filename = filename
        self.basepath = basepath or os.getcwd()
        self.basepath = os.path.abspath(self.basepath)
        self.sources = defaultdict(dict)

    def _parse_once(self):
        if len(self.sources) <= 0:
            self._parse()

    def _parse(self):
        funclines = {}
        source = None

        with open(self.filename) as f:
            for line in f:
                line = line.strip()

                if line == 'end_of_record':
                    if source is not None:
                        directory, filename = os.path.split(source.filename)
                        self.sources[directory][filename] = source
                        source = None
                else:
                    key, argstr = tuple(line.split(':'))
                    args = argstr.split(',')

                    if key == 'SF':
                        fname = args[0]
                        if fname.startswith(self.basepath):
                            source = Source(args[0])
                        else:
                            source = None

                    elif source is not None:

                        if key == 'FN':
                            name = args[1]
                            funclines[name] = int(args[0])

                        elif key == 'FNDA':
                            hits = int(args[0])
                            name = args[1]
                            func = Function(funclines[name], name, hits)
                            source.add_function(func)

                        elif key == 'BRDA':
                            line = int(args[0])
                            path = int(args[2])
                            hits = 0 if args[3] == '-' else int(args[3])
                            source.add_branch(Branch(line, path, hits))

                        elif key == 'DA':
                            line = int(args[0])
                            hits = int(args[1])
                            source.add_line(Line(line, hits))

    def list_dirs(self):
        self._parse_once()
        return self.sources.keys()

    def list_files(self, directory):
        self._parse_once()
        return self.sources[directory].keys()

    def get_source(self, directory, filename):
        self._parse_once()
        return self.sources[directory][filename]

    def get_source_abspath(self, abspath):
        return self.get_source(*os.path.split(abspath))

    def line_info(self, directory, filename):
        source = self.get_source(directory, filename)
        lineinfo = []
        lineno = 1
        with open(source.filename) as f:
            for line in f:
                if lineno in source.functions:
                    lineinfo.append({'type': 'function', 'function': source.functions[lineno]})
                elif lineno in source.branches:
                    lineinfo.append({'type': 'branch', 'branch': source.branches[lineno]})
                elif lineno in source.lines:
                    lineinfo.append({'type': 'line', 'line': source.lines[lineno]})
                else:
                    lineinfo.append({'type': 'blank'})
                lineno += 1

    def _generic_coverage(self, calc_coverage, directory=None, filename=None):
        self._parse_once()
        hits, total = 0, 0

        if directory and filename:
            source = self.get_source(directory, filename)
            return calc_coverage(source)
        elif directory:
            for filename in self.sources[directory]:
                source = self.get_source(directory, filename)
                fhits, ftotal = calc_coverage(source)
                hits += fhits
                total += ftotal
        else:
            for directory in self.list_dirs():
                dhits, dtotal = self._generic_coverage(calc_coverage, directory)
                hits += dhits
                total += dtotal
        
        return hits, total

    def _source_line_coverage(self, source):
        total = len(source.lines)
        hits = 0

        for line in source.lines.values():
            if line.hits > 0:
                hits += 1

        return hits, total

    def _source_function_coverage(self, source):
        total = len(source.functions)
        hits = 0

        for function in source.functions.values():
            if function.hits > 0:
                hits += 1

        return hits, total

    def _source_branch_coverage(self, source):
        total = len(source.branches) * 2
        hits = 0

        for brancha, branchb in source.branches.values():
            if brancha.hits > 0:
                hits += 1
            if branchb.hits > 0:
                hits += 1

        return hits, total

    def line_coverage(self, directory=None, filename=None):
        return self._generic_coverage(self._source_line_coverage, 
                                        directory, filename)

    def function_coverage(self, directory=None, filename=None):
        return self._generic_coverage(self._source_function_coverage,
                                        directory, filename)

    def branch_coverage(self, directory=None, filename=None):
        return self._generic_coverage(self._source_branch_coverage,
                                        directory, filename)

    def coverage_summary(self, directory=None, filename=None):
        lines = make_coverage(self.line_coverage(directory, filename))
        functions = make_coverage(self.function_coverage(directory, filename))
        branches = make_coverage(self.branch_coverage(directory, filename))

        return Summary(lines, functions, branches)
        
    def full_statistics(self, directory=None, filename=None):
        rows = [
            ('Line', self.line_coverage),
            ('Function', self.function_coverage),
            ('Branch', self.branch_coverage)
        ]

        if directory and filename:
            statstr = directory + '/' + filename + '\n'
        elif directory:
            statstr = directory + '\n'
        else:
            statstr = 'Total\n'

        for row in rows:
            hits, total = row[1](directory, filename)
            statstr += row[0] + ' Coverage: ' + str(hits) + '/' + str(total) + '\n'

        return statstr
