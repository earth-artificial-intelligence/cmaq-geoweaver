import pandas as pd

# Read Airnow data extract from AirnowAPI and saved to system
airnow = pd.read_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/airnow_data.csv', parse_dates=["Date"])

# Scale data to match predictors scale
airnow.AirNow_O3 = airnow.AirNow_O3 * 1000
airnow.AirNow_CO = airnow.AirNow_CO * 10
# Reformat date string
airnow["Date"] = airnow["Date"].dt.strftime('%Y%m%d')


# Read Tropomi extracted from Google Earth Engine and saved to system
tropomi = pd.read_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/tropomi_O3.csv', parse_dates=["Date"])
tropomi["Date"] = tropomi["Date"].dt.strftime('%Y%m%d')
tropomiDaily = tropomi.groupby("Date").max()
# Make date match CMAQ and Airnow retrieved data. This is done only becuase TROPOMI doesn't have data before 2018, so making the data the same as the other source for merging later.
# If the data retrieved for CMAQ and Airnow is after 2018, then this below line can be deleted.
tropomiDaily["Date"] = pd.date_range("20170101", "20170227").strftime('%Y%m%d')
tropomiDaily.reset_index(drop=True, inplace=True)

# Read downloaded CMAQ data.
cmaq = pd.read_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/cmaq_2017_Jan_Feb.csv', parse_dates=["date"])
# Drop unnecessary columns
cmaq.drop(["column", "row", "Lambert_X", "LAMBERT_Y", "Unnamed: 0"], axis=1, inplace=True)
# Reformat date string
cmaq['Date'] = cmaq["date"].dt.strftime('%Y%m%d')

# Merge all data frames together
final = airnow.merge(tropomiDaily, on="Date").merge(cmaq, on="Date")
# Drop any duplicated rows
final = final.drop_duplicates("Date")

final.to_csv("/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/final.csv", index=False)

