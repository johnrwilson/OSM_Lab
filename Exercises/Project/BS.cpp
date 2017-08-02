/* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
 * 
 * This file contains routines to serially compute the call and 
 * put price of an European option.
 * 
 * Simon Scheidegger -- 06/17.
 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/ 

#include <algorithm>    // Needed for the "max" function
#include <cmath>
#include <iostream>
#include <fstream>
#include <omp.h>



/* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 A simple implementation of the Box-Muller algorithm, used to 
generate gaussian random numbers; necessary for the Monte Carlo 
method below. */

double gaussian_box_muller() {
  double x = 0.0;
  double y = 0.0;
  double euclid_sq = 0.0;

  // Continue generating two uniform random variables
  // until the square of their "euclidean distance" 
  // is less than unity
  do {
    x = 2.0 * rand() / static_cast<double>(RAND_MAX)-1;
    y = 2.0 * rand() / static_cast<double>(RAND_MAX)-1;
    euclid_sq = x*x + y*y;
  } while (euclid_sq >= 1.0);

  return x*sqrt(-2*log(euclid_sq)/euclid_sq);
}

void initialize(double *v, int n){
  #pragma omp parallel for
  for(int i=0; i<n; i++)
    v[i] = gaussian_box_muller();
}
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing a European vanilla call option with a Monte Carlo method

double monte_carlo_call_price(double *EZs, const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T, const int& num_threads) {

  double S_adjust = S * exp(T*(r-0.5*v*v));
  double S_cur = 0.0;
  double payoff_sum = 0.0;

  #pragma omp parallel for reduction(+:payoff_sum)
  //omp_set_num_threads(num_threads);

  for (int i=0; i<num_sims; i++) {
    S_cur = S_adjust * exp(sqrt(v*v*T)*EZs[i]);
    payoff_sum += std::max(S_cur - K, 0.0);
  }
  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing a European vanilla put option with a Monte Carlo method

double monte_carlo_put_price(double *EZs, const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T, const int& num_threads) {

  double S_adjust = S * exp(T*(r-0.5*v*v));
  double S_cur = 0.0;
  double payoff_sum = 0.0;

  #pragma omp parallel for reduction(+:payoff_sum)
  //omp_set_num_threads(num_threads);
  for (int i=0; i<num_sims; i++) {
    S_cur = S_adjust * exp(sqrt(v*v*T)*EZs[i]);
    payoff_sum += std::max(K - S_cur, 0.0);
  }
  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing an Asian vanilla call option with a Monte Carlo method

double monte_carlo_call_asian(const int& num_sims, const int& num_periods, const double& S, const double& K, const double& r, const double& v, const double& T, const int& num_threads) {

  double payoff_sum = 0.0;
  double per_length = T / num_periods;

  #pragma omp parallel for reduction (+:payoff_sum)
  //omp_set_num_threads(num_threads);
  for (int i=0; i<num_sims; i++) { 
    double S_prev = S;
    double S_cur = 0.0;
    double *AZs = (double*)malloc(num_periods*sizeof(double));
    initialize(AZs, num_periods);
    double sbar = 0.0;
    for (int j=0; j<num_periods; j++) {
      S_cur = S_prev * exp(sqrt(v*v*per_length)*AZs[j]+(r - 0.5*v*v)*per_length);
      sbar += S_cur;
      S_prev = S_cur;
    };
    payoff_sum += std::max(sbar / num_periods - K, 0.0);
  };

  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing an Asian vanilla put option with a Monte Carlo method

double monte_carlo_put_asian(double *AZs, const int& num_sims, const int& num_periods, const double& S, const double& K, const double& r, const double& v, const double& T, const int& num_threads) {

  double payoff_sum = 0.0;
  double per_length = T / num_periods;

  #pragma omp parallel for reduction (+:payoff_sum)
  //omp_set_num_threads(num_threads);
  for (int i=0; i<num_sims; i++) {
    double S_cur = 0.0;
    double S_prev = S;
    double sbar = 0.0;
    for (int j=0; j<num_periods; j++) {
      S_cur = S_prev * exp(sqrt(v*v*per_length)*AZs[i*num_sims+j]+(r - 0.5*v*v)*per_length);
      sbar += S_cur;
      S_prev = S_cur;
    };
    payoff_sum += std::max((K -( sbar /(double) num_periods)), 0.0);
  };

  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


int main(int argc, char **argv) {

  // Parameters                                                                             
  int num_sims = 10000000;   // Number of simulated asset paths                                                       
  double S = 100.0;  // Option price 
  double K = 100.0;  // Strike price                                                                                  
  double r = 0.05;   // Risk-free rate (5%)                                                                           
  double v = 0.2;    // Volatility of the underlying (20%)                                                            
  double T = 1.0;    // One year until expiry                                                                         
  int m = 100;     // The number of time periods in T over which to average

  double *EZs = (double*)malloc(num_sims*sizeof(double));
  
  initialize(EZs, num_sims);

  

  
  
  // Then we calculate the call/put values via Monte Carlo                                                                          
  double call = monte_carlo_call_price(EZs, num_sims, S, K, r, v, T, 8);
  double put = monte_carlo_put_price(EZs, num_sims, S, K, r, v, T, 8);

  double call_A = monte_carlo_call_asian(num_sims, m, S, K, r, v, T, 8);
  //double put_A = monte_carlo_put_asian(AZs, num_sims, m, S, K, r, v, T, 8);

  // Finally we output the parameters and prices                                                                      
  std::cout << "Number of Paths:   " << num_sims << std::endl;
  std::cout << "Underlying:        " << S << std::endl;
  std::cout << "Strike:            " << K << std::endl;
  std::cout << "Risk-Free Rate:    " << r << std::endl;
  std::cout << "Volatility:        " << v << std::endl;
  std::cout << "Maturity:          " << T << std::endl;
  std::cout << "T Divisions:       " << m << std::endl;

  std::cout << "Call Price:        " << call << std::endl;
  std::cout << "Put Price:         " << put << std::endl;
  std::cout << "Asian Call Price:  " << call_A << std::endl;
  //std::cout << "Asian Put Price:   " << put_A << std::endl;




  return 0;
}