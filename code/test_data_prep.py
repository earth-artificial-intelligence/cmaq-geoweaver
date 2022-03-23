# Write first python in Geoweaver
import xarray as xr
import pandas as pd
import glob, os
import datetime
import numpy as np
from pathlib import Path

# home directory
home = str(Path.home())
today=datetime.datetime.today().strftime('%Y%m%d')
pday_= datetime.datetime.today() - datetime.timedelta(days=1)
pday=pday_.strftime('%Y%m%d')
fday_= datetime.datetime.today() + datetime.timedelta(days=1)
fday=fday_.strftime('%Y%m%d')
days=[pday,today]

aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll,mm,nn,oo1,pp,qq,rr,ss=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

#ff=[]
for i in days:
  files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/CCTMout/12km/POST/"+"COMBINE3D_ACONC_v531_gcc_AQF5X_"+i+"_extracted.nc")
  for j in files:
    df = xr.open_dataset(j)
    for k in range(24):
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
        # NO
#      oo=df.variables['NO'][:].values[k,0]
#      oo3=np.ravel(oo)
#     o3tp=np.transpose(oo3)
#      ff.append(o3tp)
  files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/emis2021/12km/all/"+"emis_mole_all_"+i+"_AQF5X_cmaq_cb6ae7_2017gb_17j.ncf")
  for j in files:
    df = xr.open_dataset(j)
    for k in range(24):
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
      
  files = glob.glob("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/mcip/12km/"+"METCRO2D_"+i+".nc")
  for j in files:
    df = xr.open_dataset(j)
    for k in range(24):
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
for i in t:
    time_0=np.full((265,442),today+i)
    time0.append(time_0)
t_today=list(np.concatenate(time0).flat)  

# date time dimension for yesterday
time1=[]
for i in t:
    time_1=np.full((265,442),pday+i)
    time1.append(time_1)
t_pday=list(np.concatenate(time1).flat)

# stacking 2 days values
time_var=np.vstack((t_pday,t_today))
YYMMDDHH=list(np.concatenate(time_var).flat)

# saving variables
dat=pd.DataFrame({'Latitude':LAT,'Longitude':LON,'YYYYMMDDHH':YYMMDDHH,'CMAQ12KM_O3(ppb)':cmaq_O3,'CMAQ12KM_NO2(ppb)':cmaq_NO2,'CMAQ12KM_CO(ppm)':cmaq_CO,'CMAQ_EC(ug/m3)':cmaq_PM25_EC,'CMAQ_OC(ug/m3)':cmaq_PM25_CO,'NO2(moles/s)':NO2_emi,'CO(moles/s)':CO_emi,'NO(moles/s)':NO_emi,'PRSFC(Pa)':PRSFC,'PBL(m)':PBL,'TEMP2(K)':TEMP2,'WSPD10(m/s)':WSPD10,'WDIR10(degree)':WDIR10,'WSTAR(m/s)':WSTAR,'RGRND(W/m2)':RGRND,'RN(cm)':RN,'RC(cm)':RC,'CFRAC':CFRAC})
dat.to_csv(home+'/cmaq/test_data.csv',index=False)

