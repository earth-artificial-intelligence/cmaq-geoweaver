# All the utility functions that most steps in CMAQ-AI need
# this file should not contain any direct call of function
# it should be dedicated to define functions or variables

import xarray as xr
import pandas as pd
import glob, os
import numpy as np
from pathlib import Path
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt

# home directory
home = str(Path.home())
# cmaq_folder = "/groups/ESS3/aalnaim/cmaq/" # change if you want to use your own folder
cmaq_folder = "/Users/uhhmed/localCMAQ" # change if you want to use your own folder

def get_days_list(sdate, edate):
  days=[]
  
  delta = edate - sdate       # as timedelta

  for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    list_day=day.strftime('%Y%m%d')
    days.append(list_day)
  # add one more day
  one_more_day = sdate + timedelta(days=delta.days + 1)
  list_day=one_more_day.strftime('%Y%m%d')
  days.append(list_day)
  
  return days

def create_and_clean_folder(folder_path):
  os.makedirs(folder_path, exist_ok=True)
  # clean all files inside the folder
  for f in os.listdir(folder_path):
    os.remove(os.path.join(folder_path, f))

def remove_file(file_path):
  print(f'remove old files{file_path}')
  if os.path.exists(file_path):
    os.remove(file_path)
    
def turn_2_digits(a):
  return f"{a:02}"
