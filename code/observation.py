# get all the airnow station data and save to csvs as well
import glob, os
import numpy as np
from cmaq_ai_utils import *

sdate = date(2022, 8, 1)   # start date
edate = date(2022, 8, 2)   # end date
days = get_days_list(sdate, edate)

observation_folder = f"{cmaq_folder}/observation/"
create_and_clean_folder(observation_folder)

time = ['12','13','14','15','16','17','18','19','20','21','22','23','00','01','02','03','04','05','06','07','08','09','10','11']
for i in range(len(days)-1):
  current_day = days[i]
  next_day = days[i+1]
  for x in range(len(time)):
    if x >= 12:
      i = next_day
    else:
      i = current_day
    t = time[x]
    files = "/groups/ESS/share/projects/SWUS3km/data/OBS/AirNow/AQF5X/"+"AQF5X_Hourly_"+i+t+".dat"
    
    with open(files, 'r') as file:
      text = file.read()
      new_string = text.replace('"', '')
      out_file = f"{observation_folder}/AQF5X_Hourly_{i}{t}.txt"
      print("Saving to :", out_file)
      outF = open(out_file, "w")
      for line in new_string:
        outF.write(line)
      
      outF.close()
