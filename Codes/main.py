#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 23:16:14 2022

@author: kurup
"""

from matplotlib import pyplot as plt
from scipy import optimize
from tabulate import tabulate
import numpy as np
import pre_process_mod

def eqn_(L,Z,w,df): return 1-np.exp(np.multiply(-1*L/Z[w-1],df))

def loss_func(Z,df):
    loss_val=0
    data_len=len(df)
    L=Z[10]
    for i in range(1,11):
        df_wick = df[df['Wickets.in.Hand']==i]
        overs_rem = 50-df_wick['Over']
        runs_rem = df_wick['Innings.Total.Runs']-df_wick['Total.Runs']
        runs_pred = Z[i-1]*eqn_(L,Z,i,overs_rem)
        loss_val+=np.sum(np.square(runs_rem-runs_pred))

    return loss_val/data_len



def disp(L,Z):
  for i in range(1,11):
      x = np.array(range(51))
      temp=[]
      for j in range(0,51):
        temp.append(Z[i-1]*(1-np.exp(-1*L*j/Z[i-1])))
      y = np.array([Z[i-1]*(1-np.exp(-1*L*o/Z[i-1])) for o in range(0,51)])
      plt.plot(x,y,label=str(i))
      plt.text(x[-1],y[-1],i)
  plt.show()

def duck_lew_mod(df):
    tmp = 300*np.ones(11)
    tmp[10]=0.1
    data_len=len(df)

    loss = np.zeros(10)
    res=optimize.minimize(fun=loss_func,x0=tmp,args=(df))
    Z = res.x[:10]
    L = res.x[10]
    for i in range(1,11):
        df_wick = df[df['Wickets.in.Hand']==i]
        overs_rem = 50-df_wick['Over']
        runs_rem  = df_wick['Innings.Total.Runs']-df_wick['Total.Runs']
        runs_pred = Z[i-1]*eqn_(L,Z,i,overs_rem)
        loss[i-1]=np.sum(np.square(runs_rem-runs_pred))/data_len
    
    
    #plots and table
    disp(L,Z)
    disp_list=[]
    for i in range(len(loss)):
        disp_list.append([loss[i],Z[i]])


    print(tabulate([[loss[i],Z[i],L] for i in range(len(loss))], headers=['loss', 'Z',"L"]))
    print(f"Total loss: {sum(loss):.3f}")
    
    return loss,Z,L



def main():  
    file_name='./files/04_cricket_1999to2011.csv'

    #preprocessing part
    data_post=pre_process_mod.pre_process(file_name)

    #learning part
    loss,Z,L = duck_lew_mod(data_post)

if __name__=="__main__":
    main()
