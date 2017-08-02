#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>

using namespace std;

int in_circle(double x, double y)
{
	double hypoten = sqrt(pow(x, 2) + pow(y, 2));
	if (hypoten <= 1)
	{
		return 1;
	}
	else
	{
		return 0;
	};
}


int main()
{
	srand(time(0));
	const int dim = 2;
	const double R = 1.0; //The radius of the desired circle
	const double xmax = R;
	const double xmin = -R;
	const double ymax = R;
	const double ymin = -R;
	double vol = (xmax - xmin) * (ymax - ymin);
	long num_sims = 10000;
	double sum = 0.0;
	for (int i = 0; i < num_sims; i++)
	{
		double x = (rand() * 1.0 / RAND_MAX) * 2 * R - R;
		double y = (rand() * 1.0 / RAND_MAX) * 2 * R - R;
		sum += in_circle(x, y);
	};
	double PI = vol * sum / (double) num_sims;
	cout << "PI estimated at " << PI << " in " << num_sims << " simulations" << endl;
	return 0;
}
