#!/usr/bin/env python
from scipy import *
from pylab import *
from scipy import stats
import numpy as np

class Europeanoption:
      def __init__(self,optprds,assetprds,q,payoff,T,r):
         self.optprds=optprds
         self.assetprds=assetprds
	 self.q=q
	 self.payoff=payoff
	 self.T=T
	 self.r=r
	 self.Rn=exp(self.r*self.T/self.assetprds)
	 self.n=len(self.payoff)-1
#	 print self.n
	 self.Q=(stats.binom(self.n,1.0-q)).pmf(range(self.n+1))
#	 print len(self.Q)

      def pricing(self):
          self.c0=np.dot(self.payoff,self.Q)
	  self.c0/=self.Rn**self.optprds
	  print 'c0=',self.c0
         
          


if __name__=="__main__":
     case='chooser'
#     case=''
     if case=="chooser":
        print "--------pricing european chooser option-------"
        payoff=[47.34341647,36.37349148,26.22121698,16.95336542,9.118798113,3.666775793,8.308878289,14.37058761,20.63493313,26.53804768,32.00116975] ##European chooser option
        assetprds=15 
        optprds=10    ##for chooser option
     else:
        print "-------pricing european call/put option-------"
        payoff=[78.77315076,65.44817785,53.11639045,41.70376083,31.14177898,21.3670413,12.32087004,3.94896104,0,0,0,0,0,0,0,0] ##European call option
#     ppayoff=[0,0,0,0,0,0,0,0,3.798942289,10.9693506,17.60530789,23.74664979,29.43024277,34.69020547,39.55811342,44.0631887]  ##European put option
        assetprds=len(payoff)-1   
        optprds=15
     q=0.4925
     T=0.25
     r=0.02
     my_eurocallopt=Europeanoption(optprds,assetprds,q,payoff,T,r)
     my_eurocallopt.pricing()
