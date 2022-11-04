import json
import pandas as pd
import ee

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# identify a 500 meter buffer around our Point Of Interest (POI)
poi = ee.Geometry.Point(32.047501, -110.773903).buffer(500)

# Get TROPOMI NRTI Image Collection for GoogleEarth Engine
tropomiCollection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_O3").filterDate('2019-01-01','2019-02-28')

def poi_mean(img):
    # This function will reduce all the points in the area we specified in "poi" and average all the data into a single daily value
    mean = img.reduceRegion(reducer=ee.Reducer.mean(), 
    geometry=poi,scale=250).get('O3_column_number_density')
    return img.set('date', img.date().format()).set('mean',mean)
    
# Map function to our ImageCollection
poi_reduced_imgs = tropomiCollection.map(poi_mean)
nested_list = poi_reduced_imgs.reduceColumns(ee.Reducer.toList(2), ['date','mean']).values().get(0)

# we need to call the callback method "getInfo" to retrieve the data
df = pd.DataFrame(nested_list.getInfo(), columns=['Date','tropomi_O3_mean'])


# Convert Date column to DateTime
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
# convert tropomi_O3_mean to ppbV (parts-per-billion-volume)
df['tropomi_O3.ppbV'] = (df['tropomi_O3_mean']/3)*224

df.drop('tropomi_O3_mean', inplace=True, axis=1)
# Save data to CSV file
df.to_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/tropomi_O3.csv')

