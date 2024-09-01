#!/bin/bash

days_back=90

permanent_location="/groups/ESS3/zsun/cmaq/ai_results/"
cmaq_gif_location="/groups/ESS/share/projects/SWUS3km/graph/12km/"

echo "start to traverse "${cmaq_gif_location}

for i in $(seq 0 $days_back)
do
  end_day=$i
  echo "$end_day days ago"
  begin_day=$((i))
  # Setting env variables
  YYYYMMDD_POST=$(date -d $begin_day' day ago' '+%Y%m%d')
  #/groups/ESS/share/projects/SWUS3km/graph/12km/20221108/FORECAST_O3_20221108.gif
  cp -u $cmaq_gif_location/$YYYYMMDD_POST/"FORECAST_O3_"$YYYYMMDD_POST.gif $permanent_location/gifs/ || true
  cp -u $cmaq_gif_location/$YYYYMMDD_POST/obsoverlay/gif/OBS-FORECAST_O3_$YYYYMMDD_POST.gif $permanent_location/gifs/ || true
  
done

