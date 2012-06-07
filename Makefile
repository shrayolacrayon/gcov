CC=gcc
CFLAGS=-ftest-coverage -fprofile-arcs
LDFLAGS=-ftest-coverage -fprofile-arcs

html: test.info
	genhtml --branch-coverage test.info -o html

test.info: test.c.gcov 
	lcov -c -d . -o test.info

test.c.gcov: test.gcda
	gcov test.c

test.gcda: test 
	./test

test: test.o

test.o: test.c

clean:
	rm -f test *.gcno *.gcda *.o *.info
	rm -rf html
