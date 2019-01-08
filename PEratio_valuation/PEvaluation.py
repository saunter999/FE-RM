#!/usr/bin/env python
import pandas as pd
from scipy import *
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.stats.mstats import gmean

def preview():
      plt.figure(1)
      df=pd.read_excel("data.xlsx",index_col='Date',parse_dates=True) 
      CPI_now=253.22
      fig, axes = plt.subplots(nrows=2, ncols=1)
      ##raw data
      df.plot(subplots=False,ax=axes[0])
#      print(df.index)
      print(df.columns)
#      print(df['S&P_Price'])
#      print(df['CPI'])

      realPrice= ( df['S&P_Price']/df['CPI']*CPI_now ).rename('realPrice')
      realPrice.plot(legend=True,ax=axes[1])
#      print(realPrice)
      plt.ylabel('realPrice')

      realEarning=( df['Earnings']/df['CPI']*CPI_now).rename('realEarning')
      realEarning.plot(legend=True,secondary_y=True,ax=axes[1])
#      print(realEarning)
      plt.ylim([0,450])
      plt.ylabel('realEarning')
      return df,realPrice,realEarning 

def obtainMonthly_price():
    plt.figure(2)
    df=pd.read_csv("GSPC.csv",index_col='Date',parse_dates=True)
    print(df.columns,df.index)
    Price=df['Close'].resample('1M').mean()
    Price.plot()

def PEratio(P,E,rp,re,ma,title):
    plt.figure(3)
    plt.title(title)
    prd=12 ##calculate unadjustated P/E in yearly basis 
    for shift in ma:
      if shift==0:
        dateindex=pd.date_range(start=P.index[prd],end='12/31/2000',freq='Y') 
        ratio=pd.Series(index=dateindex)
        for i in range(len(ratio)):
           # print(i,P.index[(1+i)*prd],P.iloc[(1+i)*prd])
           ratio.iloc[i]=P.iloc[(1+i)*prd]/E.iloc[(1+i)*prd-1]
        print("mean of P/E for ma="+str(shift)+':',mean(ratio))	
        plt.axhline(y=mean(ratio),c='b')
        ratio=ratio.rename('MA='+str(shift))
        ratio.plot(legend=True)

      else:
        st=shift*12
        dateindex=pd.date_range(start=rp.index[st],end='12/31/2000',freq='1Y') 
        ratio=pd.Series(index=dateindex)
        for i in range(len(ratio)):
           ratio.iloc[i]=rp.iloc[st+i*prd]/gmean(re.iloc[i*prd:st+i*prd])
        print("mean of P/E for ma="+str(shift)+':',mean(ratio))	
        plt.axhline(y=mean(ratio),c='orange')
        ratio=ratio.rename('MA='+str(shift))
        ratio.plot(legend=True)
	   

def EPratio(rp,re,ma,title,fut=-7):
    plt.figure(4)
    plt.title(title)
    CPI_now=210.036
    prd=12 ##calculate unadjustated E/P in yearly basis 
    for shift in ma:
      if shift==0:
        df=pd.read_excel("data.xlsx",index_col='Date',parse_dates=True,sheet_name=1) 
        E=df['Earnings']
        P=df['S&P_Price']
#        realPrice= ( P[::prd]/df['CPI'][::prd]*CPI_now ).rename('realPrice')
        realPrice= ( P[::prd]).rename('realPrice')
        yd=pd.Series(index=realPrice.index[1:])
        for i in range(1,len(realPrice)):
            yd.iloc[i-1]=(realPrice.iloc[i]/realPrice.iloc[i-1]-1)*100
        yd=yd.rename('yield+shift:'+str(fut))
        yd1=yd.rename('yield+unshift')
#        dateindex=pd.date_range(start=P.index[prd],end='12/31/2007',freq='Y') 
#        ratio=pd.Series(index=dateindex)
#        for i in range(len(ratio)):
#           ratio.iloc[i]=E.iloc[(1+i)*prd-1]/P.iloc[(1+i)*prd]
#        print("mean of E/P for ma="+str(shift)+':',mean(ratio))	
#        ratio=ratio.rename('MA='+str(shift))
      #  ratio.plot(legend=True,c='b')
        (yd.shift(fut)).plot(marker='o',legend=True,c='k',secondary_y=True)
        yd1.plot(c='y',ls='--',legend=True,secondary_y=True)

      else:
        st=shift*12
        dateindex=pd.date_range(start=rp.index[st],end='12/31/2000',freq='Y') 
        ratio=pd.Series(index=dateindex)
        for i in range(len(ratio)):
           ratio.iloc[i]=gmean(re.iloc[i*prd:st+i*prd])/rp.iloc[st+i*prd]
        print("mean of E/P for ma="+str(shift)+':',mean(ratio))	
        ratio=ratio.rename('MA='+str(shift))
        ratio.plot(legend=True)
	   
	   

if __name__=="__main__":
      df,rp,re=preview()
      print(df.columns)
#      obtainMonthly_price()
      PEratio(df['S&P_Price'],df['Earnings'],rp,re,ma=[0,10],title='P/E')
      EPratio(rp,re,ma=[0,10],title='E/P')
      plt.show()
