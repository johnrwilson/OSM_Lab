#include <iostream>
#include <cmath>
#include <complex>

using namespace std;

int main()
{
	double a;
	double b;
	double c;
	cout << "Enter the coefficients for the polynomial ax^2+bx+c.\n";
	cout << "a = ";
	cin >> a;
	cout << "b = ";
	cin >> b;
	cout << "c = ";
	cin >> c;
	complex<double> inside = pow(b, 2) - 4 * a * c;
	complex<double> root1 = (-b + sqrt(inside)) / (2 * a);
	complex<double> root2 = (-b - sqrt(inside)) / (2 * a);
	cout << "The first root is " << root1 << ".\n";
	cout << "The second root is " << root2 << ".\n";
	return 0;
}
