from gcov.parser import TracefileParser
from gcov.generators import front_page
import sys

if __name__ == '__main__':
    tp = TracefileParser(sys.argv[1])
 
    print front_page(tp)
