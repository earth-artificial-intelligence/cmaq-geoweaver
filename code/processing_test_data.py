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
date_list = [base - timedelta(days=x) for x in range(2)]
days = [date.strftime('%Y%m%d') for date in date_list]

aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll,mm,nn,oo1,pp,qq,rr,ss=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
#ff=[]
# k = time dimension - start from 12 to match with data
t = [12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9,10,11]
for i in days:
  print(i)
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
      o3tp=np.round(o3tp)      
      aa.append(o3tp)
  	# NO2
      oo=df.variables['NO2'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
      bb.append(o3tp)
      # CO
      oo=df.variables['CO'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
      cc.append(o3tp)

      # PM25_CO
      oo=df.variables['PM25_OC'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
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
      o3tp=np.round(o3tp)
      ff.append(o3tp)

      # NO
#      oo=df.variables['NO'][:].values[k,0]
#      oo3=np.ravel(oo)
#      o3tp=np.transpose(oo3)
#      o3tp=np.round(o3tp)
#      hh.append(o3tp)  
      
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
      o3tp=np.round(o3tp)
      ii.append(o3tp)
  	# NO2
      oo=df.variables['PBL'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
      jj.append(o3tp)
      # NO
      oo=df.variables['TEMP2'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
      kk.append(o3tp)
            # NO
      oo=df.variables['WSPD10'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
      ll.append(o3tp)
            # NO
      oo=df.variables['WDIR10'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
      mm.append(o3tp)

            # NO
      oo=df.variables['RGRND'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
      oo1.append(o3tp)

        	# NO2
      oo=df.variables['CFRAC'][:].values[k,0]
      oo3=np.ravel(oo)
      o3tp=np.transpose(oo3)
      o3tp=np.round(o3tp)
      rr.append(o3tp)
      
      
cmaq_O3=list(np.concatenate(aa).flat) 
print(len(cmaq_O3))
del aa
cmaq_NO2=list(np.concatenate(bb).flat) 
print(len(cmaq_NO2))
del bb
cmaq_CO=list(np.concatenate(cc).flat) 
print(len(cmaq_CO))
del cc

cmaq_PM25_CO=list(np.concatenate(ee).flat)

del ee
CO_emi=list(np.concatenate(ff).flat) 
print(len(CO_emi))
del ff

#NO_emi=list(np.concatenate(hh).flat) 
#del hh
PRSFC=list(np.concatenate(ii).flat) 
del ii
PBL=list(np.concatenate(jj).flat) 
del jj
TEMP2=list(np.concatenate(kk).flat) 
del kk
WSPD10=list(np.concatenate(ll).flat) 
del ll
WDIR10=list(np.concatenate(mm).flat)
del mm

RGRND=list(np.concatenate(oo1).flat) 
del oo1
#RN=list(np.concatenate(pp).flat)
#del pp
#RC=list(np.concatenate(qq).flat)
#del qq
CFRAC=list(np.concatenate(rr).flat)
print(len(CFRAC))
del rr

## selecting lat and long
df = xr.open_dataset('/home/yli74/scripts/plots/2020fire/GRIDCRO2D')
lat_1 = df.variables['LAT'][:].values[0,0]
lat_flt=np.ravel(lat_1)
# need to manipulate 48 values if the next day data is available
LAT=np.tile(lat_flt,len(days)*24)
print(len(LAT))
# long
lon_1 = df.variables['LON'][:].values[0,0]
lon_flt=np.ravel(lon_1)
# need to manipulate 48 values if the next day data is available
LON=np.tile(lon_flt,len(days)*24)
print(len(LON))
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
print(len(YYMMDDHH))


# saving variables
dat=pd.DataFrame({'Latitude':LAT,'Longitude':LON,'YYYYMMDDHH':YYMMDDHH,'CMAQ12KM_O3(ppb)':cmaq_O3,'CMAQ12KM_NO2(ppb)':cmaq_NO2,'CMAQ12KM_CO(ppm)':cmaq_CO,'CMAQ_OC(ug/m3)':cmaq_PM25_CO,'CO(moles/s)':CO_emi,'PRSFC(Pa)':PRSFC,'PBL(m)':PBL,'TEMP2(K)':TEMP2,'WSPD10(m/s)':WSPD10,'WDIR10(degree)':WDIR10,'RGRND(W/m2)':RGRND,'CFRAC':CFRAC})
print(dat.head())
dat.to_csv('/groups/ESS/aalnaim/cmaq/test_data.csv',index=False)



