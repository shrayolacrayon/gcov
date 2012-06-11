from gcov.parser import TracefileParser
import sys

if __name__ == '__main__':
    tp = TracefileParser(sys.argv[1])
    
    
    print tp.full_statistics()
    
    for directory in tp.list_dirs():
        print tp.full_statistics(directory)
        for filename in tp.list_files(directory):
            print tp.full_statistics(directory, filename)

