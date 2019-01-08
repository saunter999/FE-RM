#!/usr/bin/env python
from scipy import *

def levelpayment(n,c,M0):
    return (1.0+c)**n*M0*c/( (1.0+c)**n-1.0)


if __name__=="__main__":
     n=30*12;M0=400000;c=0.05/12
     print levelpayment(n,c,M0)
 
