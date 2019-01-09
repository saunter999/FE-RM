#!/usr/bin/env python
import pandas as pd
from scipy import *
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.stats.mstats import gmean
import numpy as np

def convertdate(df):
    cvtdate=[]
    for i in range(df.shape[0]):
        date=df.index[i]
#        print(date,(date-int(date))*100/12-1.0/24.0+int(date))
        cvtdate.append( (date-int(date))*100/12.-1.0/24.0+int(date) )
    df.index=cvtdate
    return df

def preview():
      plt.figure(1)
      df=pd.read_excel("data.xlsx",index_col='Date') 
      df=convertdate(df)
      CPI_now=253.22
      fig, axes = plt.subplots(nrows=2, ncols=1)
      ##raw data
      df.plot(subplots=False,ax=axes[0])
      print(df.columns)

      realPrice= ( df['S&P_Price']/df['CPI']*CPI_now ).rename('realPrice')
      realPrice.plot(legend=True,ax=axes[1])
      plt.ylabel('realPrice')

      realEarning=( df['Earnings']/df['CPI']*CPI_now).rename('realEarning')
      realEarning.plot(legend=True,secondary_y=True,ax=axes[1])
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
    prd=12 
    for shift in ma:
      if shift==0:
         ratio=pd.Series()
         for idx,item in enumerate(P):
            #if idx%prd==0 and idx!=0:
            if idx+1>prd:
                #print(idx,P.index[idx])
                ratio[P.index[idx]]=P.iloc[idx]/E.iloc[idx-1]
         print("mean of P/E for ma="+str(shift)+':',mean(ratio))	
         plt.axhline(y=mean(ratio),c='b')
         ratio=ratio.rename('MA='+str(shift))
         ratio.plot(legend=True)

      else:
        st=shift*12-1
        ratio=pd.Series()
        for idx,item in enumerate(rp): 
            #if idx%prd==0 and idx>st:
            if idx>st:
              # print(idx,rp.index[idx])
              ratio[rp.index[idx]]=rp.iloc[idx]/gmean(re.iloc[idx-st:idx])
        print("mean of P/E for ma="+str(shift)+':',mean(ratio))	
        plt.axhline(y=mean(ratio),c='orange')
        ratio=ratio.rename('MA='+str(shift))
        ratio.plot(legend=True)
	   
def computeYd(Price,prd):
      Pny=Price.iloc[prd:]
      yd=pd.Series()
      averyd=pd.Series()
      for idx,item in enumerate(Pny):
          yd[Pny.index[idx]]=(Pny.iloc[idx]/Price.iloc[idx]-1.0)
      for idx,item in enumerate(yd):
          if idx+1>prd:
          #if (idx+1)%12==0:
             averyd[yd.index[idx]]=mean(yd.iloc[idx-prd+1:idx+1])
      averyd=averyd.rename("yearly yd")
      return averyd

def EPratio(rp,re,ma,title,fut=-7):
    plt.figure(4)
    plt.title(title)
    CPI_now=210.036
    prd=12  
    for shift in ma:
      if shift==0:
        ##evaluating real yield rate
        df=pd.read_excel("data.xlsx",index_col='Date',sheet_name=1) 
        df=convertdate(df)
        P=df['S&P_Price']
        E=df['Earnings']
        realPrice= ( P/df['CPI']*CPI_now ).rename('realPrice')
        yd=computeYd(realPrice,prd)
        yd.plot(c='y',legend=True,secondary_y=True)

      else:
        st=shift*12-1
        ratio=pd.Series()
        for idx,item in enumerate(rp): 
            if idx>st:
            #if idx%prd==0 and idx>st:
              # print(idx,rp.index[idx])
              ratio[rp.index[idx]]=( rp.iloc[idx]/gmean(re.iloc[idx-st:idx]) )**-1
        print("mean of E/P for ma="+str(shift)+':',mean(ratio))	
        ratio=ratio.rename('MA='+str(shift))
        ratio.plot(legend=True)
	
    ##studying correlation between yd and EP_ratio
    futls=range(-12,1)
    cor=[]
    for fut in futls:
        ydshift=yd.shift(fut*prd)
        cor.append( corr(ydshift,ratio) )
    print("corr_coef:",cor)
    cor=array(cor)
    fut=futls[cor.argmax()]
    ydshift=(yd.shift(fut*prd)).rename("shifted yearly yd with shift="+str(fut))
    plt.axhline(y=0,c='k',ls='--')
    (ydshift).plot(legend=True,c='k',secondary_y=True)
	   
def corr(x,y):
    merged=pd.concat([x,y],axis=1).dropna()
    x=merged.iloc[:,0]
    y=merged.iloc[:,1]
    return np.corrcoef(x,y)[0,1]
	   

if __name__=="__main__":
      df,rp,re=preview()
#      obtainMonthly_price()
      PEratio(df['S&P_Price'],df['Earnings'],rp,re,ma=[0,10],title='P/E')
      EPratio(rp,re,ma=[0,10],title='E/P')
      plt.show()
