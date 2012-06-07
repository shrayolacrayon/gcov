CC=gcc
LDFLAGS=-ftest-coverage -fprofile-arcs -lgcov

%: %.c
