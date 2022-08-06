#!/bin/bash
# generate images and gif from the prediction NetCDF files and overlay the AirNow station observation on the top

# Setting env variables
export YYYYMMDD_POST=$(date -d '3 day ago' '+%Y%m%d')
export stdate_post=$(date -d '3 day ago' '+%Y-%m-%d')
export eddate_post=$(date -d '2 day ago' '+%Y-%m-%d')

export stdate_file=$(date -d '3 day ago' '+%Y%m%d')
export eddate_file=$(date -d '2 day ago' '+%Y%m%d')


export postdata_dir="/groups/ESS/aalnaim/cmaq/prediction_nc_files"
export mcip_dir="/groups/ESS/share/projects/SWUS3km/data/cmaqdata/mcip/12km"
export graph_dir="/groups/ESS/aalnaim/cmaq/plots"

export obs_dir_NCL="/groups/ESS/share/projects/SWUS3km/data/OBS/AirNow/AQF5X"

module load ncl

cat <<EOF >>/groups/ESS/aalnaim/cmaq/geoweaver_plot_daily_O3_Airnow.ncl
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

obs_dir = getenv("obs_dir_NCL")
plot_dir = getenv("graph_dir")

hr=new(24,"string")
hr=(/"00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"/)

print(plot_dir)
aconc_dir = getenv("postdata_dir")
grid_dir = getenv("mcip_dir")

cdf_file1 = addfile(aconc_dir+"/COMBINE3D_ACONC_v531_gcc_AQF5X_"+dFile1+"_"+dFile2+"_ML_extracted.nc","r")
cdf_file= addfile(grid_dir+"/GRIDCRO2D_"+date+".nc","r")
cdf_file2= addfile(grid_dir+"/METCRO2D_"+date+".nc","r")

time = cdf_file1->TFLAG(:,0,:)
o3 = cdf_file1->O3(:,:,:) ;ppb
wspd10=cdf_file2->WSPD10(:,0,:,:)
wdir10=cdf_file2->WDIR10(:,0,:,:)

temp = cdf_file2->TEMP2

nt = dimsizes(o3(:,0,0))
ny = dimsizes(o3(0,:,0))
nx = dimsizes(o3(0,0,:))

print(max(temp))
print(min(temp))
print(avg(temp))



print(nt+" "+ny+" "+nx)
print(max(o3))
print(min(o3))
print(avg(o3))

lat = cdf_file->LAT(0,0,:,:)
lon = cdf_file->LON(0,0,:,:)

o3@lat2d = lat
o3@lon2d = lon
o3@unit = "ppbv"

UV10=wind_component(wspd10,wdir10,0)
UV10@lat2d = lat
UV10@lon2d = lon


res = True
res@gsnMaximize = True                ; maximize pot in frame
res@gsnFrame = False               ; dont advance frame
res@gsnDraw = False
res@gsnLeftString  = ""
res@gsnRightString = ""
res@txFont   = "times-roman"
res@tiMainFont   = "times-roman"
;res@tiMainFontHeightF = 0.02
;res@vpWidthF        = 0.7
;res@vpHeightF       = 0.7

;;set map;;
mpres                             = res
mpres@mpLimitMode = "LatLon"
mpres@mpDataSetName               = "Earth..4"
mpres@mpDataBaseVersion           = "MediumRes"
mpres@mpOutlineOn                 = True
mpres@mpGeophysicalLineThicknessF = 1.5
mpres@mpFillDrawOrder             = "PostDraw"
mpres@mpFillOn                    = False
mpres@mpAreaMaskingOn         = True
mpres@mpOutlineBoundarySets = "GeophysicalAndUSStates"
mpres@mpOutlineSpecifiers         = "United States:States"
mpres@mpProjection           = "LambertConformal"
mpres@mpLambertParallel1F    = 33.
mpres@mpLambertParallel2F    = 45.
mpres@mpLambertMeridianF     = -98.
mpres@mpMinLonF = -120 ;min(lon)+0.2
mpres@mpMaxLonF = -70 ;max(lon)-0.2
mpres@mpMinLatF = 25 ;min(lat)+0.05
mpres@mpMaxLatF = 50 ;max(lat)-0.05
mpres@pmTickMarkDisplayMode   = "Always"
mpres@mpLandFillColor         = "white"
mpres@mpInlandWaterFillColor  = "white"
mpres@mpOceanFillColor        = "white"
mpres@mpGeophysicalLineColor    = "Black"

;mpres@lbLabelAutoStride       = True
mpres@tiXAxisFont             = 25
mpres@pmTickMarkDisplayMode   = "Always"
mpres@tmXBLabelFont           = 25
mpres@tmXBLabelFontHeightF    = 0.013
mpres@tmXBLabelDeltaF         = -0.5
mpres@tmYLLabelFont           = 25
mpres@tmYLLabelFontHeightF    = 0.013
mpres@tmXBLabelDeltaF         = -0.5
mpres@tmXTLabelsOn            = False
mpres@tmXTLabelFont           = 25
mpres@tmXTLabelFontHeightF    = 0.013
mpres@tmYRLabelsOn            = False
mpres@tmYRLabelFont           = 25
mpres@tmYRLabelFontHeightF    = 0.013

;;set contour;;
cnres                         = res
cnres@cnFillDrawOrder         = "PreDraw"
cnres@cnFillOn                = True
cnres@cnLinesOn               = False
cnres@cnLineLabelsOn          = False
cnres@lbLabelFont             = 25
cnres@lbLabelFontHeightF      = 0.013
cnres@tiXAxisFont             = 25
cnres@pmLabelBarWidthF        = 0.5
cnres@pmLabelBarHeightF       = 0.1
;cnres@pmLabelBarOrthogonalPosF = -0.02
cnres@lbLabelAutoStride       = True

;set vector;;
res_vc                        = res
res_vc@vcGlyphStyle           = "LineArrow"
res_vc@vcLineArrowThicknessF  = 3
res_vc@vcMinDistanceF         = 0.03
res_vc@vcRefLengthF           = 0.03
res_vc@vcRefAnnoOn            = True
res_vc@vcRefMagnitudeF           = 16
res_vc@vcRefAnnoString1          = "16m/s"
res_vc@vcRefAnnoSide             = "Top"
res_vc@vcRefAnnoString2On        = False
res_vc@vcRefAnnoPerimOn          = False
res_vc@vcRefAnnoOrthogonalPosF   = -0.02
res_vc@vcRefAnnoParallelPosF     = 0.999
;res_vc@vcRefAnnoBackgroundColor = "White"
res_vc@vcVectorDrawOrder         = "PostDraw"

do it = 0, nt-1
  if (it .lt. 12) then
    pdate=d1
  else
    pdate=d2
  end if

  ;print(time(it,0)+" "+time(it,1))
  rundate = yyyyddd_to_yyyymmdd( time(it,0) )
  runtime = hr( tointeger(time(it,1)/10000) )

  site = readAsciiTable(obs_dir+"/AQF5X_Hourly_"+rundate+runtime+".dat",1,"string",1)
  nrows = dimsizes(site)
  sitename = str_get_field(site,1,",")
  sitelat = stringtofloat(str_get_field(site,2,","))
  sitelon = stringtofloat(str_get_field(site,3,","))
  O3_obs = stringtofloat(str_get_field(site,4,","))

  obslon = sitelon(:,0)
  obslat = sitelat(:,0)
  obsO3 = O3_obs(:,0)

  npts = nrows(0)

  obsO3@_FillValue = -999.

;--- levels for dividing
  levels_O3  = ispan(0,80,4)

  nlevels = dimsizes(levels_O3)

  colors  = span_color_rgba("WhiteBlueGreenYellowRed",nlevels+1)

  num_distinct_markers = nlevels+1        ; number of distinct markers
  lat_O3 = new((/num_distinct_markers,npts/),float)
  lon_O3 = new((/num_distinct_markers,npts/),float)
  lat_O3 = -999
  lon_O3 = -999


;
; Group the points according to which range they fall in. At the
; same time, create the label that we will use later in the labelbar
;
  do i = 0, num_distinct_markers-1
    if (i.eq.0) then
      indexes_O3 = ind(obsO3(:).lt.levels_O3(0))
    end if
    if (i.eq.num_distinct_markers-1) then
      indexes_O3 = ind(obsO3(:).ge.max(levels_O3))
    end if
    if (i.gt.0.and.i.lt.num_distinct_markers-1) then
      indexes_O3 = ind(obsO3(:).ge.levels_O3(i-1).and.obsO3(:).lt.levels_O3(i))
    end if

;
; Now that we have the set of indexes whose values fall within
; the given range, take the corresponding lat/lon values and store
; them, so later we can color this set of markers with the appropriate
; color.
;
    if (.not.any(ismissing(indexes_O3))) then
      npts_range_O3 = dimsizes(indexes_O3)   ; # of points in this range.

      lat_O3(i,0:npts_range_O3-1) = obslat(indexes_O3)
      lon_O3(i,0:npts_range_O3-1) = obslon(indexes_O3)
  ;print("O3: "+npts_range_O3)
    end if


    delete(indexes_O3)            ; Necessary b/c "indexes" may be a different
  end do

  lat_O3@_FillValue = -999
  lon_O3@_FillValue = -999

  gsres               = True
  gsres@gsMarkerIndex = 16          ; Use filled dots for markers.

  hollowres           = True
  hollowres@gsMarkerIndex    = 4
  hollowres@gsMarkerColor    = "black"
  hollowres@gsMarkerSizeF    = 0.008

;;;;;;;;;   Plot Ozone
  pname=plot_dir+"/OBS-FORECAST_O3_"+rundate+runtime
  wks = gsn_open_wks("png",pname)
  gsn_define_colormap(wks, "WhiteBlueGreenYellowRed")

  pmid_O3 = new(num_distinct_markers,graphic)
  hollow_O3 = new(num_distinct_markers,graphic)

  cnres@tiMainString =  pdate+" "+runtime+" UTC O~B~3~N~ (ppbV)"
  cnres@cnLevelSelectionMode = "ManualLevels"
  cnres@cnMinLevelValF          = 0.
  cnres@cnMaxLevelValF          = 80
  cnres@cnLevelSpacingF         = 4

  ;plot = gsn_csm_contour_map(wks,o3(it,:,:),res)
  map = gsn_csm_map(wks,mpres)
  contour = gsn_csm_contour(wks,o3(it,:,:),cnres)
  vector  = gsn_csm_vector(wks,UV10(0,it,:,:),UV10(1,it,:,:),res_vc)
  overlay(map,contour)
  overlay(map,vector)

  pmid = new(num_distinct_markers,graphic)
  hollow = new(num_distinct_markers,graphic)
  do i = 0, num_distinct_markers-1
    if (.not.ismissing(lat_O3(i,0)))
      gsres@gsMarkerColor      = colors(i,:)
      gsres@gsMarkerSizeF      = 0.008
      gsres@gsMarkerThicknessF = 1
       pmid(i) = gsn_add_polymarker(wks,vector,lon_O3(i,:),lat_O3(i,:),gsres)
       hollow(i) = gsn_add_polymarker(wks,vector,lon_O3(i,:),lat_O3(i,:),hollowres)
    end if
  end do

  draw(map)
  frame(wks)
  delete(wks)
  delete(pmid_O3)
  delete(hollow_O3)
  system("composite -geometry 100x70+900+900 /groups/ESS/aalnaim/cmaq/mason-logo-green.png "+pname+".png "+pname+".png")


  delete(pmid)
  delete(hollow)
  delete(site)
  delete(sitename)
  delete(sitelat)
  delete(sitelon)
  delete(O3_obs)
  delete(obslon)
  delete(obslat)
  delete(obsO3)
  delete([/lon_O3,lat_O3/])

end do
delete(res)

;/

end
EOF


ncl /groups/ESS/aalnaim/cmaq/geoweaver_plot_daily_O3_Airnow.ncl

convert -delay 100 /groups/ESS/aalnaim/cmaq/plots/OBS*.png /groups/ESS/aalnaim/cmaq/plots/"Airnow_"$YYYYMMDD_POST.gif

if [ $? -eq 0 ]; then
    echo "Generating AirNow images/gif Completed Successfully"
	echo "Removing ncl file: geoweaver_plot_daily_O3_Airnow.ncl..."
	rm /groups/ESS/aalnaim/cmaq/geoweaver_plot_daily_O3_Airnow.ncl
else
    echo "Generating AirNow images/gif Failed!"
    echo "Removing ncl file: geoweaver_plot_daily_O3_Airnow.ncl..."
	rm /groups/ESS/aalnaim/cmaq/geoweaver_plot_daily_O3_Airnow.ncl
fi
