#!/usr/bin/env python 
from scipy import *
from pylab import *
from numpy import random
from scipy import stats
import numpy as np


n=20
p=0.1
times=random.binomial(n,p)
print times

tms=range(n+1)
prb=stats.binom(n,p)
print prb.pmf(tms)
print sum(prb.pmf(tms))


a=[2,10]
b=[-1,1]
print np.dot(a,b) 
