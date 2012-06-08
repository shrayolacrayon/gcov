import os

env = Environment(
    ENV = os.environ,
    CFLAGS = '-ftest-coverage -fprofile-arcs',
    LIBS = ['gcov']
)

if os.uname()[0] == 'Darwin':
    env.Replace(CC = 'gcc-4.2')

EXECUTABLES=['test', 'hello']

for name in EXECUTABLES:
    env.Program(name, [name + '.c', 'printStart.c'])
    env.Command(name + '.gcda', [name], './' + name)

env.Command('test.info', 
            ['test.gcda', 'hello.gcda'], 
            'lcov -c -d . -o test.info')

env.Command('html', ['test.info'], 'genhtml test.info -o html')

