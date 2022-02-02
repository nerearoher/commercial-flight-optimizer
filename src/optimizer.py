import warnings
warnings.simplefilter('ignore')

import sys
import pandas as pd
from collections import namedtuple
from pulp import *
from datetime import datetime
import numpy as np
import time

data_frame_march15 = {}

air_bases = ['LPA', 'TFN']
flight_operators = ['ATB', 'AC6']
crewRoutes = { (i,j) : [] for i in flight_operators for j in air_bases}
print(crewRoutes)

def importDataSet(date):   
  data_frame = pd.read_csv('data_sets/VUELOSMAR2020.CSV', header=None)
  # data_frame = pd.read_csv('data_sets/VUELOSREDUCIDOS.CSV', header=None)
  data_frame = data_frame.rename(columns={0:'Date', 1:'FlightID', 2:'Flight Operators', 3:'Departure', 4:'Arrival', 5:'DepTime', 6:'ArrTime'})
  data_frame.drop([7], axis=1, inplace=True)
   
  selectedDate = data_frame['Date'] == date
  data_frame_final = data_frame[selectedDate]
    
  data_frame_final['DepTime'] = pd.to_timedelta(data_frame_final['DepTime']+':00')
  data_frame_final['ArrTime'] = pd.to_timedelta(data_frame_final['ArrTime']+':00')
    
  data_frame_final.sort_values(by=['DepTime'], inplace=True)
  data_frame_final.index = range(len(data_frame_final.index))
    
  FlightDur = ((data_frame_final['ArrTime'] - data_frame_final['DepTime']))
  for i in range(len(FlightDur)):
    FlightDur[i] = int((FlightDur[i].total_seconds())/60)
  data_frame_final['FlightDuration'] = FlightDur
    
  delete = ['CMN','RAK','FNC','PXO','VGO','EUN','PNA','LIS','PMI']
  data_frame_final = data_frame_final[~data_frame_final['Departure'].isin(delete)]
  data_frame_final = data_frame_final[~data_frame_final['Arrival'].isin(delete)]
  data_frame_final.index = range(len(data_frame_final.index))
    
  return data_frame_final

data_frame_march15 = importDataSet('15/03/20')
print('Data Frame')
print(data_frame_march15)

flights_id = data_frame_march15['FlightID'].tolist()
print('ID fligths')
print(flights_id)
flights_id_copy = flights_id.copy()

for i in air_bases:
  flights_id_copy.append(i)

flights_id_list = list(flights_id)
flights_id_copy = list(flights_id_copy)

flight_operators_len = len(flight_operators)
air_bases_len = len(air_bases)
flights_id_len = len(flights_id_list)
flights_id_copy_len = len(flights_id_copy)
flight_operators_len_range = range(len(flight_operators))
air_bases_len_range = range(len(air_bases))
flights_id_list_len_range = range(len(flights_id_list))
flights_id_copy_len_range = range(len(flights_id_copy))

min_connect_time = 20
max_connect_time = 180
short_connect_time = 30

connection_graph = {}
connection_sgraph = {}
not_connection_graph = {}
flights_id_graph = {}

def build_graph(data_frame):
  for i in range(len(data_frame)):
    for j in range(len(data_frame)):
      if(data_frame.loc[i, 'Arrival'] == data_frame.loc[j, 'Departure']):
        time_i = (data_frame.loc[i,"ArrTime"].total_seconds())/60
        time_j = (data_frame.loc[j,"DepTime"].total_seconds())/60
        connection_time = time_j - time_i
        flight_id_i = data_frame.loc[i, 'FlightID']
        flight_id_j = data_frame.loc[j, 'FlightID']
        if (connection_time >= min_connect_time):
          if (connection_time <= max_connect_time):
            connection_graph[(flight_id_i, flight_id_j)] = connection_time
            if((connection_time >= min_connect_time) and (connection_time < short_connect_time)):
              connection_sgraph[(flight_id_i, flight_id_j)] = connection_time
            else:
              not_connection_graph[(flight_id_i, flight_id_j)] = connection_time
          flights_id_graph[(flight_id_i, flight_id_j)] = connection_time
    for f in flights_id:
        dep = (data_frame.loc[data_frame_march15['FlightID'] == f, 'Departure']).values[0]
        arr = (data_frame.loc[data_frame_march15['FlightID'] == f, 'Arrival']).values[0]
        if(dep in air_bases):
            not_connection_graph[(dep,f)] = -1
            connection_graph[(dep,f)] = -1
            flights_id_graph[(dep,f)] = -1
        if(arr in air_bases):
            flights_id_graph[(f,arr)] = -1
            not_connection_graph[(f,arr)] = -1
            connection_graph[(f,arr)] = -1
  # print(flights_id_graph)

build_graph(data_frame_march15)