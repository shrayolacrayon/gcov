import sys, os

sys.path.append(os.getcwd())

from gcov.parser import TracefileParser
from gcov.generators import front_page

if __name__ == '__main__':
    tp = TracefileParser(sys.argv[1])
 
    print front_page(tp)
