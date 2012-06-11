from gcov.parser import TracefileParser
from gcov.generators import front_page, directory_page, file_page, stylesheet
import sys, os
import argparse

def genhtml(infofile, basepath, outdir):
    tracefile = TracefileParser(infofile, basepath)
    toplevel = os.path.join(outdir, 'index.html')

    with open(toplevel, 'w') as f:
        f.write(front_page(tracefile))

    with open(os.path.join(outdir, 'style.css'), 'w') as f:
        f.write(stylesheet())

    for directory in tracefile.list_dirs():
        dirname = os.path.join(outdir, directory[1:])
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        
        with open(os.path.join(dirname, 'index.html'), 'w') as f:
            f.write(directory_page(tracefile, toplevel, directory))

        with open(os.path.join(dirname, 'style.css'), 'w') as f:
            f.write(stylesheet())

        for filename in tracefile.list_files(directory):
            with open(os.path.join(dirname, filename + '.html'), 'w') as f:
                f.write(file_page(tracefile, toplevel, directory, filename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Generate html for tracefile')
    parser.add_argument('infofile')
    parser.add_argument('-b', '--basepath', 
                        default = os.getcwd())
    parser.add_argument('-o', '--outdir', 
                        default = os.path.join(os.getcwd(), 'html'))

    args = parser.parse_args(sys.argv[1:])

    genhtml(args.infofile, args.basepath, args.outdir)
    
