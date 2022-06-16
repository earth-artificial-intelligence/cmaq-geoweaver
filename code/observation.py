
import xarray as xr
import pandas as pd
import glob, os
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta, date
# home directory
home = str(Path.home())


days=[]

base = datetime.today() - timedelta(days=2)
date_list = [base - timedelta(days=x) for x in range(3)]
days = [date.strftime('%Y%m%d') for date in date_list]


time = ['12','13','14','15','16','17','18','19','20','21','22','23','00','01','02','03','04','05','06','07','08','09','10','11']
for i in days:
  for t in time:
    files = "/groups/ESS/share/projects/SWUS3km/data/OBS/AirNow/AQF5X/"+"AQF5X_Hourly_"+i+t+".dat"
    with open(files, 'r') as file:
      text = file.read()
    new_string = text.replace('"', '')

    outF = open("/groups/ESS/aalnaim/cmaq/observation/AQF5X_Hourly_"+i+t+".txt", "w")
    for line in new_string:
      # write line to output file
      outF.write(line)
    outF.close()
