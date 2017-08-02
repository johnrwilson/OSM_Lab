#!/bin/bash -l

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8

#SBATCH --time=00:10:00


#SBATCH --job-name=Black-S
#SBATCH --output=BS.out
#SBATCH --error=BS.err

export OMP_NUM_THREADS=$1


### openmp executable
./BS.cpp.exec

