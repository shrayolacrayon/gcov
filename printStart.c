#include "printStart.h"
void printStart(char* filename){
	char str;
	FILE *f = fopen(argv[1], "r"); //opens up a file pointer for reading
	int nb = fread(str, 1,1023,f);
	str[nb] = 0;
	printf("%s \n ", str);
	fclose(f);
}