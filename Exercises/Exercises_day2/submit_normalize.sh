#!/bin/bash -l

#SBATCH --ntasks=8

#SBATCH --time=00:01:00


#SBATCH --job-name=test_submission
#SBATCH --output=openmp_test.out
#SBATCH --error=openmp_test.err

export OMP_NUM_THREADS=8


### openmp executable
./normalize_vec.cpp.exec

