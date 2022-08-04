import xarray as xr
import pandas as pd
import glob, os
import numpy as np
from pathlib import Path
import datetime
from datetime import timedelta
# home directory
home = str(Path.home())

base = datetime.datetime.today() - timedelta(days=2)
date_list = [base + timedelta(days=x) for x in range(2)]
days = [date.strftime('%Y%m%d') for date in date_list]


# k = time dimension - start from 12 to match with data
t = [12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9,10,11]


for day in days:
	print("Getting data for: "+day)
    
	# read cmaq results
	df_cmaq = xr.open_dataset("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/CCTMout/12km/POST/COMBINE3D_ACONC_v531_gcc_AQF5X_"+day+"_extracted.nc")
    
	# read mcip results 
	df_mcip = xr.open_dataset("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/mcip/12km/METCRO2D_"+day+".nc")
        
	# read emissions results 
	df_emis = xr.open_dataset("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/emis2021/12km/all/emis_mole_all_"+day+"_AQF5X_cmaq_cb6ae7_2017gb_17j.ncf")
        
	for k in t:
            
            
		df_hourly = pd.DataFrame()
            
		# CMAQ data
            
		# O3 variable
		o3=df_cmaq.variables['O3'][:].values[k,0]
		cmaq_O3=list(np.ravel(o3).transpose().round())  
            
		# NO2
		no2=df_cmaq.variables['NO2'][:].values[k,0]
		cmaq_NO2=list(np.ravel(no2).transpose().round())
      
		# CO
		co=df_cmaq.variables['CO'][:].values[k,0]
		cmaq_CO=list(np.ravel(co).transpose().round())

		# PM25_CO
		pm25=df_cmaq.variables['PM25_OC'][:].values[k,0]
		cmaq_PM25_CO=list(np.ravel(pm25).transpose().round())
            
                              
                              
		# EMIS data
                              
		co_emis=df_emis.variables['CO'][:].values[k,0]
		CO_emi=list(np.ravel(co_emis).transpose().round())    
                
                              
                              
		# MCIP data
            
		# CO variable
		prsfc=df_mcip.variables['PRSFC'][:].values[k,0]
		PRSFC=list(np.ravel(prsfc).transpose().round())
            
		# NO2
		pbl=df_mcip.variables['PBL'][:].values[k,0]
		PBL=list(np.ravel(pbl).transpose().round())
            
		# TEMP2
		temp2=df_mcip.variables['TEMP2'][:].values[k,0]
		TEMP2=list(np.ravel(temp2).transpose().round())
            
		# WSPD10
		wspd10=df_mcip.variables['WSPD10'][:].values[k,0]
		WSPD10=list(np.ravel(wspd10).transpose().round())
            
		# WDIR10
		wdir10=df_mcip.variables['WDIR10'][:].values[k,0]
		WDIR10=list(np.ravel(wdir10).transpose().round())

		# RGRND
		rgrnd=df_mcip.variables['RGRND'][:].values[k,0]
		RGRND=list(np.ravel(rgrnd).transpose().round())

		# CFRAC
		cfrac=df_mcip.variables['CFRAC'][:].values[k,0]
		CFRAC=list(np.ravel(cfrac).transpose().round())

            
		## LAT/LON data
		df_coords = xr.open_dataset('/home/yli74/scripts/plots/2020fire/GRIDCRO2D')
            
		lat = df_coords.variables['LAT'][:].values[0,0]
		lat_flt=np.ravel(lat)
		LAT=np.tile(lat_flt,1)

		lon = df_coords.variables['LON'][:].values[0,0]
		lon_flt=np.ravel(lon)
		LON=np.tile(lon_flt,1)
            
		df_hourly['Latitude'] = LAT
		df_hourly['Longitude'] = LON
		df_hourly['YYYYMMDDHH'] = day+' '+str(k)
		df_hourly['CMAQ12KM_O3(ppb)'] = cmaq_O3
		df_hourly['CMAQ12KM_NO2(ppb)'] = cmaq_NO2
		df_hourly['CMAQ12KM_CO(ppm)'] = cmaq_CO
		df_hourly['CMAQ_OC(ug/m3)'] = cmaq_PM25_CO
		df_hourly['CO(moles/s)'] = CO_emi
		df_hourly['PRSFC(Pa)'] = PRSFC
		df_hourly['PBL(m)'] = PBL
		df_hourly['TEMP2(K)'] = TEMP2
		df_hourly['WSPD10(m/s)'] = WSPD10
		df_hourly['WDIR10(degree)'] = WDIR10
		df_hourly['RGRND(W/m2)'] = RGRND
		df_hourly['CFRAC'] = CFRAC
		df_hourly['month'] = df_hourly['YYYYMMDDHH'].str[4:6]
		df_hourly['day'] = df_hourly['YYYYMMDDHH'].str[6:8]
		df_hourly['hours'] = df_hourly['YYYYMMDDHH'].str[8:10]
            
            
		print('Saving file: test_data_'+day+'_'+str(k)+'.csv')
		df_hourly.to_csv('/groups/ESS/aalnaim/cmaq/input_hourly/test_data_'+day+'_'+str(k)+'.csv',index=False)

print('Done!')
