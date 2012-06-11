from jinja2 import Environment, PackageLoader
from collections import namedtuple

env = Environment(loader = PackageLoader('gcov'))

def front_page(tracefile):
    template = env.get_template('index.html')

    summary = tracefile.coverage_summary()
    
    directories = [(name, tracefile.coverage_summary(name)) \
                        for name in tracefile.list_dirs()]

    return template.render(directories = tracefile.list_dirs(), 
                           basepath = tracefile.basepath,
                           directories = directories,
                           summary = summary)
