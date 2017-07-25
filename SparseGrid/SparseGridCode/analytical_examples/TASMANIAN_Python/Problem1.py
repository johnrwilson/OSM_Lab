#!/usr/bin/python

##############################################################################################################################################################################
# Copyright (c) 2017, Miroslav Stoyanov
#
# This file is part of
# Toolkit for Adaptive Stochastic Modeling And Non-Intrusive ApproximatioN: TASMANIAN
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
#    and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse
#    or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# UT-BATTELLE, LLC AND THE UNITED STATES GOVERNMENT MAKE NO REPRESENTATIONS AND DISCLAIM ALL WARRANTIES, BOTH EXPRESSED AND IMPLIED.
# THERE ARE NO EXPRESS OR IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR THAT THE USE OF THE SOFTWARE WILL NOT INFRINGE ANY PATENT,
# COPYRIGHT, TRADEMARK, OR OTHER PROPRIETARY RIGHTS, OR THAT THE SOFTWARE WILL ACCOMPLISH THE INTENDED RESULTS OR THAT THE SOFTWARE OR ITS USE WILL NOT RESULT IN INJURY OR DAMAGE.
# THE USER ASSUMES RESPONSIBILITY FOR ALL LIABILITIES, PENALTIES, FINES, CLAIMS, CAUSES OF ACTION, AND COSTS AND EXPENSES, CAUSED BY, RESULTING FROM OR ARISING OUT OF,
# IN WHOLE OR IN PART THE USE, STORAGE OR DISPOSAL OF THE SOFTWARE.
##############################################################################################################################################################################
#
#
#  The examples below were adjusted for the OSM 17 lab at BFI Chicago.
#  Simon Scheidegger, 07/17
#
##############################################################################################################################################################################

# necessary import for every use of TASMANIAN
#
import TasmanianSG
import numpy as np

# imports specifically needed by the examples
import math
from random import uniform
from datetime import datetime
from matplotlib import pyplot as plt

print("TasmanianSG version: {0:s}".format(TasmanianSG.__version__))
print("TasmanianSG license: {0:s}".format(TasmanianSG.__license__))

grid1 = TasmanianSG.TasmanianSparseGrid()
grid2 = TasmanianSG.TasmanianSparseGrid()

## First function:
## interpolate: f(x,y) = cos( 2*pi*w + c1x + c2y)
## using refinement
aPnts = np.empty([1000, 2])
for iI in range(1000):
    for iJ in range(2):
        aPnts[iI][iJ] = uniform (-1.0, 1.0)

# Implement such that w = 1, c1 = 2, c2 = 2
aTres = np.empty([1000,])
for iI in range(1000):
    aTres[iI] = math.cos(2 * math.pi + 2 * aPnts[iI][0] + 2 * aPnts[iI][1])

# Adaptive Sparse Grid with dimension 2 and 1 output and maximum refinement level 5, refinement criterion.
iDim = 2
iOut = 1
iDepth = 1
fTol = 1.E-5
which_basis = 1 
refinement_level = 6

# level of grid before refinement
grid1.makeLocalPolynomialGrid(iDim, iOut, iDepth, which_basis, "localp")

aPoints = grid1.getPoints()
aVals = np.empty([aPoints.shape[0], 1])
for iI in range(aPoints.shape[0]):
    aVals[iI] = math.cos(2 * math.pi + 2 * aPoints[iI][0] + 2 * aPoints[iI][1])
grid1.loadNeededPoints(aVals)

print("\n-------------------------------------------------------------------------------------------------")
print("Example 1: interpolate f(x,y) = cos( 2*pi*w + c1x + c2y)")
print("   the error is estimated as the maximum from 1000 random points")
print("   tolerance is set at 1.E-5 and piecewise linear basis functions are used\n")

print("               Classic refinement ")
print(" refinement level         points     error   ")

#refinement level
err_vals = []
num_pts = []
for iK in range(refinement_level):
    grid1.setSurplusRefinement(fTol, 1, "fds")   #also use fds, or other rules
    aPoints = grid1.getNeededPoints()
    aVals = np.empty([aPoints.shape[0], 1])
    for iI in range(aPoints.shape[0]):
        aVals[iI] = math.cos(2 * math.pi + 2 * aPoints[iI][0] + 2 * aPoints[iI][1])
    grid1.loadNeededPoints(aVals)

    aRes = grid1.evaluateBatch(aPnts)
    fError1 = max(np.fabs(aRes[:,0] - aTres))

    num_pts.append(grid1.getNumPoints())
    err_vals.append(fError1)
    print(" {0:9d} {1:9d}  {2:1.2e}".format(iK+1, grid1.getNumPoints(), fError1))

plt.plot(num_pts, err_vals, 'o')
plt.xlabel("Number of points in grid")
plt.ylabel("Error of interpolation")
plt.title("f(x,y) = cos( 2*pi + 2x + 2y)")
plt.savefig("Errorvpoints1.png")
# write coordinates of grid to a text file
f2=open("Adaptive_sparse_grid1.txt", 'w')
np.savetxt(f2, aPoints, fmt='% 2.16f')
f2.close()
 
grid2 = TasmanianSG.TasmanianSparseGrid()
grid2.makeLocalPolynomialGrid(iDim, iOut, refinement_level+iDepth, which_basis, "localp")
a = grid2.getNumPoints()
 
print("\n-------------------------------------------------------------------------------------------------")
print "   a fix sparse grid of level ", refinement_level+iDepth, " would consist of " ,a, " points"
print("\n-------------------------------------------------------------------------------------------------\n")    

## First function:
## interpolate: f(x,y) = exp( -c1*abs(x1 -w1) - c2*abs(x2 -w2) )
## using refinement
aPnts = np.empty([1000, 2])
for iI in range(1000):
    for iJ in range(2):
        aPnts[iI][iJ] = uniform (-1.0, 1.0)

# Implement such that w1 = 1, w2 = 5, c1 = 2, c2 = 3
w1 = 1
w2 = 5
c1 = 2
c2 = 3
aTres = np.empty([1000,])
for iI in range(1000):
    aTres[iI] = math.exp( -c1*np.abs(aPnts[iI][0] -w1) - c2*np.abs(aPnts[iI][1] -w2) )


# Adaptive Sparse Grid with dimension 2 and 1 output and maximum refinement level 5, refinement criterion.
iDim = 2
iOut = 1
iDepth = 1
fTol = 1.E-5
which_basis = 1 
refinement_level = 6

# level of grid before refinement
grid1.makeLocalPolynomialGrid(iDim, iOut, iDepth, which_basis, "localp")

aPoints = grid1.getPoints()
aVals = np.empty([aPoints.shape[0], 1])
for iI in range(aPoints.shape[0]):
    aVals[iI] = math.exp( -c1*np.abs(aPoints[iI][0] -w1) - c2*np.abs(aPoints[iI][1] -w2) )
grid1.loadNeededPoints(aVals)

print("\n-------------------------------------------------------------------------------------------------")
print("Example 1: interpolate f(x,y) = exp( -c1*abs(x1 -w1) - c2*abs(x2 -w2) )")
print("   the error is estimated as the maximum from 1000 random points")
print("   tolerance is set at 1.E-5 and piecewise linear basis functions are used\n")

print("               Classic refinement ")
print(" refinement level         points     error   ")

#refinement level
err_vals = []
num_pts = []
for iK in range(refinement_level):
    grid1.setSurplusRefinement(fTol, 1, "fds")   #also use fds, or other rules
    aPoints = grid1.getNeededPoints()
    aVals = np.empty([aPoints.shape[0], 1])
    for iI in range(aPoints.shape[0]):
        aVals[iI] = math.exp( -c1*np.abs(aPoints[iI][0] -w1) - c2*np.abs(aPoints[iI][1] -w2) )
    grid1.loadNeededPoints(aVals)

    aRes = grid1.evaluateBatch(aPnts)
    fError1 = max(np.fabs(aRes[:,0] - aTres))

    num_pts.append(grid1.getNumPoints())
    err_vals.append(fError1)
    print(" {0:9d} {1:9d}  {2:1.2e}".format(iK+1, grid1.getNumPoints(), fError1))

plt.plot(num_pts, err_vals, 'o')
plt.xlabel("Number of points in grid")
plt.ylabel("Error of interpolation")
plt.title("f(x,y) = exp( -c1*abs(x1 -w1))")
plt.savefig('Errorvpoints2.png')
# write coordinates of grid to a text file
f2=open("Adaptive_sparse_grid2.txt", 'w')
np.savetxt(f2, aPoints, fmt='% 2.16f')
f2.close()
 
grid2 = TasmanianSG.TasmanianSparseGrid()
grid2.makeLocalPolynomialGrid(iDim, iOut, refinement_level+iDepth, which_basis, "localp")
a = grid2.getNumPoints()
 
print("\n-------------------------------------------------------------------------------------------------")
print "   a fix sparse grid of level ", refinement_level+iDepth, " would consist of " ,a, " points"
print("\n-------------------------------------------------------------------------------------------------\n")    


    
