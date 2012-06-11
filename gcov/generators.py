from jinja2 import Environment, PackageLoader
from collections import namedtuple
import os

env = Environment(loader = PackageLoader('gcov'))

def front_page(tracefile):
    template = env.get_template('index.html')

    summary = tracefile.coverage_summary()
    
    directories = [(name, tracefile.coverage_summary(name)) \
                        for name in tracefile.list_dirs()]

    return template.render(basepath = tracefile.basepath,
                           directories = directories,
                           summary = summary,
                           tracefile = os.path.basename(tracefile.filename))

def directory_page(tracefile, toplevel, directory):
    template = env.get_template('directory.html')

    summary = tracefile.coverage_summary(directory)

    files = [(name, tracefile.coverage_summary(directory, name)) \
                    for name in tracefile.list_files(directory)]

    return template.render(directory = directory,
                           files = files,
                           summary = summary,
                           toplevel = toplevel,
                           tracefile = os.path.basename(tracefile.filename))


def file_page(tracefile, toplevel, directory, filename):
    template = env.get_template('file.html')

    summary = tracefile.coverage_summary(directory, filename)

    lineinfo = tracefile.line_info(directory, filename)

    return template.render(directory = directory, filename = filename,
                           lineinfo = lineinfo,  summary = summary,
                           toplevel = toplevel,
                           tracefile = os.path.basename(tracefile.filename))

    
