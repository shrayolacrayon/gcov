CC=gcc

test: test.c
	$(CC) -ftest-coverage -fprofile-arcs test.c -o test
