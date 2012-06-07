CC=gcc
CFLAGS=-ftest-coverage -fprofile-arcs
LDFLAGS=-ftest-coverage -fprofile-arcs
TESTARGS=
HELLOARGS=

html: test.info
	genhtml --branch-coverage test.info -o html

test.info: test.gcda hello.gcda
	lcov -c -d . -o test.info

test.c.gcov: test.gcda
	gcov test.c

test.gcda: test 
	./test $(TESTARGS)

hello.gcda: hello
	./hello $(HELLOARGS)

test: test.o printStart.o
test.o: test.c

hello: hello.o printStart.o
hello.o: hello.c

printStart.o: printStart.c 
printStart.c: printStart.h

clean:
	rm -f test *.gcno *.gcda *.o *.info
	rm -rf html
