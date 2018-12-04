#!/usr/bin/env python
from scipy import *
from pylab import *
from numpy import random


def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")



if __name__=="__main__":
     ts=0;te=2
     N=1000
     tseries=linspace(ts,te,N)
     x0=100
     mu=0.1
     sigma=0.25
     #standard brownian motion wt
     Nit=5
     for j in range(Nit):
             print "Nit=",j+1
	     wt=zeros(N)
	     for i in range(N-1):
#		 print i,sqrt(tseries[i+1]-tseries[i])
		 wt[i+1]=wt[i]+sqrt(tseries[i+1]-tseries[i])*random.normal(0.0,1.0)
	     fig1=figure(1)
	     ax1=axes()
	#     plot(tseries,wt,'s-',markersize=2)
	     plot(tseries,wt)
	     if j==Nit-1:
                title('Standard brownian motion')
                xlim([ts,te])
                axhline(y=0,c='k')
		xlabel('Times/year')

	     figure(2)
	     ax2=axes()
	     xt=[]
	     for i in range(N):
		 xt.append(x0+mu*tseries[i]+sigma*wt[i])
	     plot(tseries,xt)
	     if j==Nit-1:
                title('Brownian motion with drift mu='+str(mu)+'and sigma='+str(sigma))
                xlim([ts,te])
                axhline(y=x0,c='k')
		xlabel('Times/year')

	     figure(3)
	     ax2=axes()
	     xt=[]
	     for i in range(N):
		 xt.append(x0*exp( (mu-sigma**2/2)*tseries[i]+sigma*wt[i]))
	     plot(tseries,xt)
	     if j==Nit-1:
                title('Geometric brownian motion with drift mu='+str(mu)+'and sigma='+str(sigma))
                xlim([ts,te])
                axhline(y=x0,c='k')
	     pause()

     show()
     
