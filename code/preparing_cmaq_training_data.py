# Write first python in Geoweaver
# Write first python in Geoweaver
# Write first python in Geoweaver
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

sdate = date(2021, 4, 5)   # start date
edate = date(2021, 4, 6)   # end date

delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    list_day=day.strftime('%Y%m%d')
    days.append(list_day)
aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll,mm,nn,oo1,pp,qq,rr,ss=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
#ff=[]
# k = time dimension - start from 12 to match with data
t = [12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9,10,11]
for i in days:
  # read cmaq results
  # old files before 20210315 are not in diractory. must choose later date.
  if int(i)>=20210315 and int(i)<=20210902:
    files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/CCTMout/12km/POST/"+"COMBINE3D_ACONC_v531_gcc_AQF5X_"+i+"_extracted.nc")
  else:
    files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/CCTMout/12km/POST/"+"COMBINE3D_ACONC_v531_gcc_AQF5X_"+i+"_extracted.nc")
  for j in files:

    df = xr.open_dataset(j)
    for k in t:
  	# O3 variable
  	# O3 variable
      oo=df.variables['O3'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      aa.append(o3tp)
  	# NO2
      oo=df.variables['NO2'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      bb.append(o3tp)
      # CO
      oo=df.variables['CO'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      cc.append(o3tp)
       # PM25_EC
      oo=df.variables['PM25_EC'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      dd.append(o3tp)
      # PM25_CO
      oo=df.variables['PM25_OC'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      ee.append(o3tp)
      
      
  # read emission results
  # old files before 20210315 are not in diractory. must choose later date.
  if int(i)>=20191231 and int(i)<=20210902:
    files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/emis2021/12km/all/"+"emis_mole_all_"+i+"_AQF5X_nobeis_2016fh_16j.ncf")
  elif int(i)==20220303:
    files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/emis2021/12km/all/"+"emis_mole_all_"+i+"_AQF5X_cmaq_cb6ae7_2017gb_17j.ncf")

# set todays date if they don't change dataformate    
#  else if int(i)>=20220313 and int(i)<=int(today):
  elif int(i)>=20220313 and int(i)<=20220331:
    files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/emis2021/12km/all/"+"emis_mole_all_"+i+"_AQF5X_cmaq_cb6ae7_2017gb_17j.ncf")
  for j in files:

    df = xr.open_dataset(j)
    for k in t:
  	# CO variable
      oo=df.variables['CO'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      ff.append(o3tp)
  	# NO2
      oo=df.variables['NO2'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      gg.append(o3tp)
      # NO
      oo=df.variables['NO'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      hh.append(o3tp)  
      
# read mcip results 
# date must be later of 20210101
  files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/mcip/12km/"+"METCRO2D_"+i+".nc")
  for j in files:
    df = xr.open_dataset(j)
    for k in t:
  	# CO variable
      oo=df.variables['PRSFC'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      ii.append(o3tp)
  	# NO2
      oo=df.variables['PBL'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      jj.append(o3tp)
      # NO
      oo=df.variables['TEMP2'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      kk.append(o3tp)
            # NO
      oo=df.variables['WSPD10'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      ll.append(o3tp)
            # NO
      oo=df.variables['WDIR10'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      mm.append(o3tp)
            # NO
      oo=df.variables['WSTAR'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      nn.append(o3tp)
            # NO
      oo=df.variables['RGRND'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      oo1.append(o3tp)
            # NO
      oo=df.variables['RN'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      pp.append(o3tp)
        	# NO2
      oo=df.variables['RC'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      qq.append(o3tp)
        	# NO2
      oo=df.variables['CFRAC'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      rr.append(o3tp)
      
      
cmaq_O3=list(np.concatenate(aa).flat) 
cmaq_NO2=list(np.concatenate(bb).flat) 
cmaq_CO=list(np.concatenate(cc).flat) 
cmaq_PM25_EC=list(np.concatenate(dd).flat) 
cmaq_PM25_CO=list(np.concatenate(ee).flat)
CO_emi=list(np.concatenate(ff).flat) 
NO2_emi=list(np.concatenate(gg).flat) 
NO_emi=list(np.concatenate(hh).flat) 
PRSFC=list(np.concatenate(ii).flat) 
PBL=list(np.concatenate(jj).flat) 
TEMP2=list(np.concatenate(kk).flat) 
WSPD10=list(np.concatenate(ll).flat) 
WDIR10=list(np.concatenate(mm).flat) 
WSTAR=list(np.concatenate(nn).flat) 
RGRND=list(np.concatenate(oo1).flat) 
RN=list(np.concatenate(pp).flat)
RC=list(np.concatenate(qq).flat)
CFRAC=list(np.concatenate(rr).flat)

## selecting lat and long
df = xr.open_dataset('/home/yli74/scripts/plots/2020fire/GRIDCRO2D')
lat_1 = df.variables['LAT'][:].values[0,0]
lat_flt=np.ravel(lat_1)
# need to manipulate 48 values if the next day data is available
LAT=np.tile(lat_flt,48)
# long
lon_1 = df.variables['LON'][:].values[0,0]
lon_flt=np.ravel(lon_1)
# need to manipulate 48 values if the next day data is available
LON=np.tile(lon_flt,48)
# creating dataframe

## creatime date-time dimension
# date-time dimension for today
time0=[]
t = ['12','13','14','15','16','17','18','19','20','21','22','23','00','01','02','03','04','05','06','07','08','09','10','11']
for i in days:
  for j in t:
    time_0=np.full((265,442),i+j)
    time0.append(time_0)
YYMMDDHH=list(np.concatenate(time0).flat)  



# saving variables
dat=pd.DataFrame({'Latitude':LAT,'Longitude':LON,'YYYYMMDDHH':YYMMDDHH,'CMAQ12KM_O3(ppb)':cmaq_O3,'CMAQ12KM_NO2(ppb)':cmaq_NO2,'CMAQ12KM_CO(ppm)':cmaq_CO,'CMAQ_EC(ug/m3)':cmaq_PM25_EC,'CMAQ_OC(ug/m3)':cmaq_PM25_CO,'NO2(moles/s)':NO2_emi,'CO(moles/s)':CO_emi,'NO(moles/s)':NO_emi,'PRSFC(Pa)':PRSFC,'PBL(m)':PBL,'TEMP2(K)':TEMP2,'WSPD10(m/s)':WSPD10,'WDIR10(degree)':WDIR10,'WSTAR(m/s)':WSTAR,'RGRND(W/m2)':RGRND,'RN(cm)':RN,'RC(cm)':RC,'CFRAC':CFRAC})
print(dat.head())
dat.to_csv(home+'/cmaq/training_data.csv',index=False)

