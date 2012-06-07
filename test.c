//test file for gcov
#include <stdio.h>
int gcd (int a, int b);
int unused (int x);
int main (int argc, char *argv[]){
	char str[1024];
	FILE* f;
	int nb;
	int sum = 0;
	int evens = 0;
	int i;
	for ( i = 0; i < 10000; i++)
	{
	sum += i;
	if (sum % 2 == 0)
	{
		evens += i;
	}
	}
	gcd(3502, 42);
	if (argc > 1)
	{
		f = fopen(argv[1], "r"); //opens up a file pointer for reading
		nb = fread(str, 1,1023,f);
		str[nb] = 0;
		printf("%s \n ", str);
	}
	return 0;
	
}
//gcd recursive
int gcd(int a, int b){
	if (b == 0)
		return a;
	else
		return gcd(b, (a % b));
}

//unused method used for testing coverage
int unused (int x){
	if (x > 5)
		return x + 3;
	else
		return x;
}