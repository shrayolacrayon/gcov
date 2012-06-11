from __future__ import division
from jinja2 import Environment, PackageLoader

env = Environment(loader = PackageLoader('gcov'))

def front_page(tracefile):
    template = env.get_template('index.html')
    fhits, ftotal = tracefile.function_coverage()
    bhits, btotal = tracefile.branch_coverage()
    lhits, ltotal = tracefile.line_coverage()

    fperc = fhits / ftotal * 100
    bperc = bhits / btotal * 100
    lperc = lhits / ltotal * 100

    return template.render(directories = tracefile.list_dirs(), 
                           basepath = tracefile.basepath,
                           fhits = fhits, ftotal = ftotal, fperc = fperc,
                           bhits = bhits, btotal = btotal, bperc = bperc,
                           lhits = lhits, ltotal = ltotal, lperc = lperc)
