#!/usr/bin/env python
import pandas as pd
from scipy import *
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def computeYd(Price):
      Pny=Price.iloc[prd:]
      ##Method1:average yield rate over 12 months
      yd=pd.Series()
      averyd=pd.Series()
      for idx,item in enumerate(Pny):
          yd[Pny.index[idx]]=(Pny.iloc[idx]/Price.iloc[idx]-1.0)
      for idx,item in enumerate(yd):
          #if (idx+1)%12==0:
          if idx+1>12:
#             print (yd.index[idx],yd.iloc[idx-11:idx+1],mean(yd.iloc[idx-11:idx+1]))
             averyd[yd.index[idx]]=mean(yd.iloc[idx-11:idx+1])
#      print(averyd)
#      print(averyd.max(),averyd.min())
      yd=yd.rename('Monthly yd')
      averyd=averyd.rename("aver0_yearly yd")
      yd.plot(legend=True)
      averyd.plot(legend=True)




if __name__=="__main__":
      df=pd.read_excel("data.xlsx",index_col='Date')#parse_dates=True) 
      P=df['S&P_Price']
      CPI_now=df['CPI'].iloc[-1]
      realP=df['S&P_Price']/df['CPI']*CPI_now
      prd=12
#      computeYd(P)
      computeYd(realP)
      
      

      plt.show()
