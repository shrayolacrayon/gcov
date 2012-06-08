#include "printStart.h"
#include <stdio.h>

void printStart(char* filename){
	char str[1024];
	FILE *f = fopen(filename, "r"); //opens up a file pointer for reading
	int nb = fread(str, 1,1023,f);
	str[nb] = 0;
	printf("%s \n ", str);
	fclose(f);
}
