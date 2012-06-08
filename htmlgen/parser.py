import gcov
import os

class TracefileParser:
    def __init__(self, filename, basepath = None):
        self.filename = filename
        self.basepath = basepath or os.path.dirname(filename)
        self.basepath = os.path.abspath(self.basepath)
        self.sources = {}

    def _parse_once(self):
        if len(self.sources) == 0:
            self._parse()

    def _parse(self):
        funcname = ''
        funcline = 0
        source = None

        with open(self.filename) as f:
            for line in f:
                line = line.strip()

                if line == 'end_of_record':
                    if source is not None:
                        self.sources[source.filename] = source
                else:
                    key, argstr = tuple(line.split(':'))
                    args = argstr.split(',')

                    if key == 'SF':
                        fname = args[0]
                        if fname.startswith(self.basepath):
                            source = gcov.Source(args[0])
                        else:
                            source = None

                    elif source is not None:

                        if key == 'FN':
                            funcline = int(args[0])
                            funcname = args[1]

                        elif key == 'FNDA':
                            times = int(args[0])
                            func = gcov.Function(funcline, funcname, times)
                            source.add_function(func)

                        elif key == 'BRDA':
                            line = int(args[0])
                            path = int(args[2])
                            times = int(args[3])
                            source.add_branch(gcov.Branch(line, path, times))

                        elif key == 'DA':
                            line = int(args[0])
                            times = int(args[1])
                            source.add_line(gcov.Line(line, times))

    def list_sources(self):
        self._parse_once()
        return self.sources.keys()

    def get_source(self, name):
        self._parse_once()
        return self.sources[name]



