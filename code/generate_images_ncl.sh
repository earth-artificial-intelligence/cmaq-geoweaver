#!/bin/bash
# generate images and gif from the NetCDF files

cmaq_folder="/groups/ESS/aalnaim/cmaq"
mkdir $cmaq_folder"/plots"
rm $cmaq_folder"/plots/*" # clean everything first

echo $(date -d '2 day ago' '+%Y%m%d')
# Setting env variables
#export YYYYMMDD_POST=$(date -d '2 day ago' '+%Y%m%d') #This needs to be auto date `date -d "-2 day ${1}" +%Y%m%d`
export YYYYMMDD_POST='20220701'
#export stdate_post=$(date -d '2 day ago' '+%Y-%m-%d') #This needs to be auto date
export stdate_post='2022-07-01'
#export eddate_post=$(date -d '1 day ago' '+%Y-%m-%d') #This needs to be auto date
export eddate_post='2022-07-02'

#export stdate_file=$(date -d '2 day ago' '+%Y%m%d') #This needs to be auto date
export stdate_file='20220701'
#export eddate_file=$(date -d '1 day ago' '+%Y%m%d') #This needs to be auto date
export eddate_file='20220702'


export postdata_dir=$cmaq_folder"/prediction_nc_files"
export mcip_dir="/groups/ESS/share/projects/SWUS3km/data/cmaqdata/mcip/12km"
export dir_graph=$cmaq_folder"/plots"

module load ncl

rm $cmaq_folder/geoweaver_plot_daily_O3.ncl
cat <<EOF >> $cmaq_folder/geoweaver_plot_daily_O3.ncl
load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/contributed.ncl"

setvalues NhlGetWorkspaceObjectId()
"wsMaximumSize": 600000000
end setvalues

begin

date = getenv("YYYYMMDD_POST")
d1 = getenv("stdate_post")
d2 = getenv("eddate_post")

dFile1 = getenv("stdate_file")
dFile2 = getenv("eddate_file")

;print("Passed Date: "+date)

aconc_dir = getenv("postdata_dir")
grid_dir = getenv("mcip_dir")
plot_dir = getenv("dir_graph")

print(aconc_dir+"/COMBINE3D_ACONC_v531_gcc_AQF5X_"+dFile1+"_"+dFile2+"_ML_extracted.nc")
cdf_file1 = addfile(aconc_dir+"/COMBINE3D_ACONC_v531_gcc_AQF5X_"+dFile1+"_"+dFile2+"_ML_extracted.nc","r")
cdf_file= addfile(grid_dir+"/GRIDCRO2D_"+date+".nc","r")

ptime = (/"12","13","14","15","16","17","18","19","20","21","22","23","00","01","02","03","04","05","06","07","08","09","10","11"/)

time = cdf_file1->TFLAG(:,0,:)
o3 = cdf_file1->O3(:,:,:) ;ppb
;pm25 = cdf_file1->PM25_TOT(:,0,:,:)


nt = dimsizes(o3(:,0,0))
ny = dimsizes(o3(0,:,0))
nx = dimsizes(o3(0,0,:))

print(nt+" "+ny+" "+nx)
print(max(o3))
print(min(o3))
print(avg(o3))

;print(max(pm25))
;print(min(pm25))
;print(avg(pm25))

;print(time)

lat = cdf_file->LAT(0,0,:,:)
lon = cdf_file->LON(0,0,:,:)

o3@lat2d = lat
o3@lon2d = lon

res = True
res@gsnMaximize = True                ; maximize pot in frame
res@gsnFrame = False               ; don't advance frame
res@gsnDraw = False
;res@gsnSpreadColors = True
res@lbLabelAutoStride = True
;res@lbBoxLinesOn = False
res@pmLabelBarHeightF = 0.1
res@pmLabelBarWidthF = 0.5
res@cnFillOn=True
;res@cnMonoFillPattern=True
;res@cnMonoLineColor=True
res@cnLinesOn=False
;res@pmLabelBarDisplayMode="never"
res@gsnLeftString  = "";
res@gsnRightString = ""

res@mpLimitMode = "LatLon"
res@mpMinLonF = -120 ;min(lon)+0.2
res@mpMaxLonF = -70 ;max(lon)-0.2
res@mpMinLatF = 25 ;min(lat)+0.05
res@mpMaxLatF = 50 ;max(lat)-0.05
res@mpDataBaseVersion = "MediumRes"
;res@tiMainString = times(it)
res@mpDataBaseVersion       = "MediumRes"
res@mpDataSetName           = "Earth..4"
res@mpAreaMaskingOn         = True
res@mpOutlineBoundarySets = "GeophysicalAndUSStates"
res@mpOutlineSpecifiers="United States : States"
res@mpLandFillColor         = "white"
res@mpInlandWaterFillColor  = "white"
res@mpOceanFillColor        = "white"
res@mpGeophysicalLineColor    = "Black"
res@mpGeophysicalLineThicknessF = 1.5

;res@gsnSpreadColors         = True
res@lbLabelAutoStride       = True
res@lbLabelFont             = 25
res@tiXAxisFont             = 25
res@pmTickMarkDisplayMode   = "Always"
res@tmXBLabelFont           = 25
res@tmXBLabelFontHeightF    = 0.013
res@tmXBLabelDeltaF         = -0.5
res@tmYLLabelFont           = 25
res@tmYLLabelFontHeightF    = 0.013
res@tmXBLabelDeltaF         = -0.5
res@tmXTLabelsOn            = False
res@tmXTLabelFont           = 25
res@tmXTLabelFontHeightF    = 0.013
res@tmYRLabelsOn            = False
res@tmYRLabelFont           = 25
res@tmYRLabelFontHeightF    = 0.013


res@mpProjection           = "LambertConformal" ;"CylindricalEquidistant"
res@mpLambertParallel1F    = 33.
res@mpLambertParallel2F    = 45.
res@mpLambertMeridianF     = -98.

res@cnLevelSelectionMode = "ManualLevels"
res@cnMinLevelValF          = 0.
res@cnMaxLevelValF          = 80
res@cnLevelSpacingF         = 4

res@txFont   = "times-roman"
res@tiMainFont   = "times-roman"

do it = 0, nt-1
  if (it .lt. 12) then
    pdate=d1
  else
    pdate=d2
  end if

  pname=plot_dir+"/testPlot_"+pdate+"_"+ptime(it)
  wks = gsn_open_wks("png",pname)
  gsn_define_colormap(wks, "WhiteBlueGreenYellowRed")

  res@tiMainString = pdate+" "+ptime(it)+" UTC O~B~3~N~ Forecast (ppbV)"
  plot = gsn_csm_contour_map(wks,o3(it,:,:),res)
  draw(plot)
  frame(wks)
  delete(wks)
  system("composite -geometry 100x70+900+900 /groups/ESS/aalnaim/cmaq/mason-logo-green.png "+pname+".png "+pname+".png")
end do
delete(res)

end
EOF


ncl $cmaq_folder/geoweaver_plot_daily_O3.ncl

# convert -delay 100 *.png 20220613_20220614.gif
convert -delay 100 $cmaq_folder/plots/testPlot*.png $cmaq_folder/plots/"Map_"$YYYYMMDD_POST.gif

if [ $? -eq 0 ]; then
    echo "Generating images/gif Completed Successfully"
else
    echo "Generating images/gif Failed!"
fi
