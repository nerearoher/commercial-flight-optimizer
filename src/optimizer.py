import warnings
warnings.simplefilter("ignore")

import sys
import pandas as pd
from collections import namedtuple
from pulp import *
from datetime import datetime
import numpy as np
import time

df_marzo15 = {}

bases = ["LPA", "TFN"]
Operator = ["ATB", "AC6"]
crewRoutes = { (i,j) : [] for i in Operator for j in bases}
print(crewRoutes)


def importDataSet(date):   
  df = pd.read_csv("./../data_sets/VUELOSREDUCIDOS.CSV", header=None)
  df = df.rename(columns={0:'Date', 1:'FlightID', 2:'Operator', 3:'Departure', 4:'Arrival', 5:'DepTime', 6:'ArrTime'})
  df.drop([7], axis=1, inplace=True)
  #df = df[:-1]
    
  selectedDate = df['Date'] == date
  df_final = df[selectedDate]
    
  df_final['DepTime'] = pd.to_timedelta(df_final['DepTime']+':00')
  df_final['ArrTime'] = pd.to_timedelta(df_final['ArrTime']+':00')
    
  df_final.sort_values(by=['DepTime'], inplace=True)
  df_final.index = range(len(df_final.index))
    
  FlightDur = ((df_final['ArrTime'] -df_final['DepTime']))
  for i in range(len(FlightDur)):
    FlightDur[i] = int((FlightDur[i].total_seconds())/60)
  df_final["FlightDuration"] = FlightDur
    
  delete = ["CMN","RAK","FNC","PXO","VGO","EUN","PNA","LIS","PMI"]
  df_final = df_final[~df_final['Departure'].isin(delete)]
  df_final = df_final[~df_final['Arrival'].isin(delete)]
  df_final.index = range(len(df_final.index))
    
  return df_final

df_marzo15 = importDataSet('15/03/20')
print(df_marzo15)