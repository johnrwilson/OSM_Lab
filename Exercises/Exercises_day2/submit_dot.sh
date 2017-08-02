#!/bin/bash -l

#SBATCH --ntasks=8

#SBATCH --time=00:01:00


#SBATCH --job-name=test_submission
#SBATCH --output=dot_test.out
#SBATCH --error=dot_test.err

export OMP_NUM_THREADS=$1


### openmp executable
./dot_prod.exec

