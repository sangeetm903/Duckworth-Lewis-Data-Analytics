#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:40:20 2022
file_name="/home/kurup/Desktop/Data/Assignment 1/Codes/files/04_cricket_1999to2011.csv"
data_inn_1=pd.read_csv(file_name)
@author: kurup
"""

import pandas as pd
import re
from tqdm import tqdm

def convert_date(date_old):
    get_months={
        'Jan':"1",
        'Feb':"2",
        'Mar':"3",
        'Apr':"4",
        'May':"5",
        'Jun':"6",
        'Jul':"7",
        'Aug':"8",
        'Sep':"9",
        'Oct':"10",
        'Nov':"11",
        'Dec':"12"
    }

    month,day,year=date_old.split(" ")
    month=get_months[month]

    day=day.split("-")[0] # comment this line to get the xx-xx form for date
    #here the first number before the hyphen is only considered
    return day+'/'+month+'/'+year

def remo_not_50(data_inn_1):
  for i in data_inn_1.Match.unique():
      if len(data_inn_1[data_inn_1['Match']==i])<50:
          temp=data_inn_1[data_inn_1['Match']==i]
          if min(temp["Wickets.in.Hand"])>0:
              data_inn_1=data_inn_1[data_inn_1["Match"]!=i]
  return data_inn_1

def pre_process(file_name):

    read_data_csv = pd.read_csv(file_name)
    data_inn_1=read_data_csv[read_data_csv["Innings"]==1]

    ################################################################################
    # un-comment the following lines to remove data of matches with incomplete data
    data_inn_1=remo_not_50(data_inn_1)           #<------------------
    ################################################################################

    data_inn_1=data_inn_1.sort_values(by=["Match",'Over']) #sorting based on match number and overs
    len_data=len(data_inn_1)
    data_inn_1.iloc[0]['Total.Runs'] = data_inn_1.iloc[0]['Runs'] #for edge case error avoidance

    try:

        for i in tqdm(range(1,len_data)):
            if (re.search("[0-9]+/[0-9]+/[0-9]+",data_inn_1['Date'].iloc[i]))==None:
                data_inn_1['Date'].iloc[i] = convert_date(data_inn_1.iloc[i]['Date']) #Date correction

            present_match=data_inn_1.iloc[i]["Match"]
            pre_match=data_inn_1.iloc[i-1]['Match']



            if (data_inn_1.iloc[i]['Over']!=1):
                data_inn_1.iloc[i]['Total.Runs'] = data_inn_1.iloc[i]['Runs'] + data_inn_1.iloc[i-1]['Total.Runs']

            else :
                match_id = data_inn_1['Match'].iloc[i-1]
                data_inn_1[data_inn_1['Match']==match_id]['Innings.Total.Runs'] = data_inn_1['Total.Runs'].iloc[i-1]
                data_inn_1.iloc[i]['Total.Runs'] = data_inn_1.iloc[i]['Runs']


        data_inn_1['Runs.Remaining'] = data_inn_1['Innings.Total.Runs'] - data_inn_1['Total.Runs']
        ret_data = data_inn_1.filter(items=['Over','Innings.Total.Runs','Total.Runs',"Runs.Remaining",'Wickets.in.Hand'])


    except:
        print("Error occured in preprocessing!")
        exit()


    return ret_data
