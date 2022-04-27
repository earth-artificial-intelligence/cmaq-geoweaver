
import xarray as xr
import pandas as pd
import glob, os
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
# home directory
home = str(Path.home())


days=[]
from datetime import date, timedelta

sdate = date(2021, 10, 30)   # start date
edate = date(2022, 1, 1)   # end date

delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    list_day=day.strftime('%Y%m%d')
    days.append(list_day)


time = ['12','13','14','15','16','17','18','19','20','21','22','23','00','01','02','03','04','05','06','07','08','09','10','11']
for i in days:
  for t in time:
    files = "/groups/ESS/share/projects/SWUS3km/data/OBS/AirNow/AQF5X/"+"AQF5X_Hourly_"+i+t+".dat"
    with open(files, 'r') as file:
      text = file.read()
    new_string = text.replace('"', '')

    outF = open("/home/mislam25/cmaq/observation/AQF5X_Hourly_"+i+t+".txt", "w")
    for line in new_string:
      # write line to output file
      outF.write(line)
    outF.close()
