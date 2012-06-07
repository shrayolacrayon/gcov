//test file for gcov
int gcd (int a, int b);
int main (){
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
	
	return 0;
}

int gcd(int a, int b){
	if (b == 0)
		return a;
	else
		return gcd(b, (a % b));
}
