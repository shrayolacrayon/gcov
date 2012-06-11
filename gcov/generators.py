from jinja2 import Environment, PackageLoader
from collections import namedtuple

env = Environment(loader = PackageLoader('gcov'))

def front_page(tracefile):
    template = env.get_template('index.html')

    summary = tracefile.coverage_summary()
    
    directories = [(name, tracefile.coverage_summary(name)) \
                        for name in tracefile.list_dirs()]

    return template.render(basepath = tracefile.basepath,
                           directories = directories,
                           summary = summary)

def directory_page(tracefile, directory):
    template = env.get_template('directory.html')

    summary = tracefile.coverage_summary(directory)

    files = [(name, tracefile.coverage_summary(directory, name)) \
                    for name in tracefile.list_files(directory)]

    
