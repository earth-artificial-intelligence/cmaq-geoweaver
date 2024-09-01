#!/bin/bash
# Specify the name of the script you want to submit
SCRIPT_NAME="generate_images_ncl_slurm.sh"
echo "write the slurm script into ${SCRIPT_NAME}"
cat > ${SCRIPT_NAME} << 'EOF'
#!/bin/bash
#SBATCH -J generate_images_ncl_slurm       # Job name
#SBATCH --output=/scratch/%u/%x-%N-%j.out  # Output file`
#SBATCH --error=/scratch/%u/%x-%N-%j.err   # Error file`
#SBATCH -n 1               # Number of tasks
#SBATCH -c 4               # Number of CPUs per task (threads)
#SBATCH --mem=20G          # Memory per node (use units like G for gigabytes) - this job must need 200GB lol
#SBATCH -t 0-01:00         # Runtime in D-HH:MM format

module load imagemagick

if command -v convert >/dev/null 2>&1; then
    echo "Command exists."
else
    echo "Command does not exist."
fi

cmaq_folder="/groups/ESS/zsun/cmaq"

# generate images and gif from the NetCDF files

echo "cmaq_folder="${cmaq_folder}
permanent_location="/groups/ESS3/zsun/cmaq/ai_results/"
mkdir -p "${cmaq_folder}/raw_ai_plots/"


export postdata_dir="${cmaq_folder}/prediction_nc_files"
export mcip_dir="/scratch/sma8/forecast/mcip/12km"
export dir_graph="${cmaq_folder}/raw_ai_plots"

echo "Loading NCL"
source /home/zsun/.bashrc
module load ncl
echo "Loaded NCL"

rm ${cmaq_folder}/geoweaver_plot_daily_O3.ncl

echo "Drafting "${cmaq_folder}/geoweaver_plot_daily_O3.ncl
cat <<INNER_EOF >> ${cmaq_folder}/geoweaver_plot_daily_O3.ncl
load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/contributed.ncl"

setvalues NhlGetWorkspaceObjectId()
"wsMaximumSize": 600000000
end setvalues

begin

print("NCL script successfully begin: ")

date = getenv("YYYYMMDD_POST")
d1 = getenv("stdate_post")
d2 = getenv("eddate_post")

dFile1 = getenv("stdate_file")
dFile2 = getenv("eddate_file")

;print("Passed Date: "+date)

;aconc_dir = getenv("postdata_dir")
grid_dir = getenv("mcip_dir")
plot_dir = getenv("dir_graph")

print("/groups/ESS/zsun/cmaq/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_"+dFile1+"_ML_extracted.nc")
cdf_file1 = addfile("/groups/ESS/zsun/cmaq/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_"+dFile1+"_ML_extracted.nc","r")
print(grid_dir+"/GRIDCRO2D_"+date+".nc")
cdf_file= addfile(grid_dir+"/GRIDCRO2D_"+date+".nc","r")

ptime = (/"12","13","14","15","16","17","18","19","20","21","22","23","00","01","02","03","04","05","06","07","08","09","10","11"/)

time = cdf_file1->TFLAG(:,0,:)
o3 = cdf_file1->O3(:,0,:,:) ;ppb
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
res@gsnFrame = False               ; dont advance frame
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

  pname=plot_dir+"/"+date+"/testPlot_"+pdate+"_"+ptime(it)
  wks = gsn_open_wks("png",pname)
  gsn_define_colormap(wks, "WhiteBlueGreenYellowRed")

  res@tiMainString = pdate+" "+ptime(it)+" UTC O~B~3~N~ Forecast (ppbV)"
  plot = gsn_csm_contour_map(wks,o3(it,:,:),res)
  draw(plot)
  frame(wks)
  delete(wks)
  system("composite -geometry 100x70+900+900 /groups/ESS/zsun/cmaq/mason-logo-green.png "+pname+".png "+pname+".png")
end do
delete(res)

end
exit
INNER_EOF

echo "Start to run the NCL script: "$cmaq_folder"/geoweaver_plot_daily_O3.ncl"

echo "ncl "$cmaq_folder"/geoweaver_plot_daily_O3.ncl"

echo $(date -d '1 day ago' '+%Y%m%d')

days_back=90

force=false

for i in $(seq 1 $days_back)
do
  end_day=$i
  echo "$end_day days ago"
  begin_day=$((i+1))
  # Setting env variables
  export YYYYMMDD_POST=$(date -d $begin_day' day ago' '+%Y%m%d') #This needs to be auto date `date -d "-2 day ${1}" +%Y%m%d`
  #export YYYYMMDD_POST='20220806'
  export stdate_post=$(date -d $begin_day' day ago' '+%Y-%m-%d') #This needs to be auto date
  #export stdate_post='2022-08-06'
  export eddate_post=$(date -d $end_day' day ago' '+%Y-%m-%d') #This needs to be auto date
  #export eddate_post='2022-08-08'

  export stdate_file=$(date -d $begin_day' day ago' '+%Y%m%d') #This needs to be auto date
  #export stdate_file='20220806'
  export eddate_file=$(date -d $end_day' day ago' '+%Y%m%d') #This needs to be auto date
  #export eddate_file='20220808'
  stdate_file=$(date -d $begin_day' day ago' '+%Y%m%d')
  echo "stdate_file="$stdate_file
  # determine if the prediction netcdf is there
  predict_nc_file=$cmaq_folder"/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_"$stdate_file"_ML_extracted.nc"
  if [ -f "$predict_nc_file" ]; then
    echo "$predict_nc_file exists."
  else
    echo "$predict_nc_file doesn't exist. Skipping..."
    continue
  fi
  
  predict_gif_file=$permanent_location/gifs/Map_$YYYYMMDD_POST.gif
  if [ "$force" != true ] ; then
    if [ -f "$predict_gif_file" ]; then
      echo "$predict_gif_file exists. Skipping..."
      continue
    else
      echo "$predict_gif_file doesn't exist. Generating..."
    fi
  else
    echo "force to regenerate $predict_gif_file.."
  fi

  mkdir -p $cmaq_folder/raw_ai_plots/$YYYYMMDD_POST/
  
  # rm -rf $cmaq_folder/raw_ai_plots/$YYYYMMDD_POST/* # clean everything in the folder first

  ncl $cmaq_folder/geoweaver_plot_daily_O3.ncl

  echo "Finished "$cmaq_folder"/geoweaver_plot_daily_O3.ncl"

  # convert -delay 100 *.png 20220613_20220614.gif

  echo "Converted images to gif"
  echo "convert -delay 100 $cmaq_folder/raw_ai_plots/$YYYYMMDD_POST/testPlot*.png $cmaq_folder/raw_ai_plots/$YYYYMMDD_POST/Map_$YYYYMMDD_POST.gif"
  convert -delay 100 $cmaq_folder/raw_ai_plots/$YYYYMMDD_POST/testPlot*.png $cmaq_folder/raw_ai_plots/$YYYYMMDD_POST/Map_$YYYYMMDD_POST.gif

  # cp the results to permanent location
  echo "cp $predict_nc_file $permanent_location/netcdfs/"
  cp $predict_nc_file $permanent_location/netcdfs/
  echo "cp $cmaq_folder/raw_ai_plots/$YYYYMMDD_POST/Map_$YYYYMMDD_POST.gif $permanent_location/gifs/"
  cp $cmaq_folder/raw_ai_plots/$YYYYMMDD_POST/Map_$YYYYMMDD_POST.gif $permanent_location/gifs/
  echo "Moved the generated netcdfs and gifs to permanent locations"
  
done



if [ $? -eq 0 ]; then
    echo "Generating images/gif Completed Successfully"
else
    echo "Generating images/gif Failed!"
fi


EOF

# Submit the Slurm job and wait for it to finish
echo "sbatch ${SCRIPT_NAME}"

# Submit the Slurm job
job_id=$(sbatch ${SCRIPT_NAME} | awk '{print $4}')
echo "job_id="${job_id}

if [ -z "${job_id}" ]; then
    echo "job id is empty. something wrong with the slurm job submission."
    exit 1
fi

# Wait for the Slurm job to finish
file_name=$(find /scratch/zsun -name '*'${job_id}'.out' -print -quit)
previous_content=$(cat file_name)
exit_code=0
while true; do
    # Capture the current content
    file_name=$(find /scratch/zsun -name '*'${job_id}'.out' -print -quit)
    current_content=$(<"${file_name}")

    # Compare current content with previous content
    diff_result=$(diff <(echo "$previous_content") <(echo "$current_content"))
    # Check if there is new content
    if [ -n "$diff_result" ]; then
        # Print the newly added content
        echo "$diff_result"
    fi
    # Update previous content
    previous_content="$current_content"


    job_status=$(scontrol show job ${job_id} | awk '/JobState=/{print $1}')
    #echo "job_status "$job_status
    #if [[ $job_status == "JobState=COMPLETED" ]]; then
    #    break
    #fi
    if [[ $job_status == *"COMPLETED"* ]]; then
        echo "Job $job_id has finished with state: $job_status"
        break;
    elif [[ $job_status == *"CANCELLED"* || $job_status == *"FAILED"* || $job_status == *"TIMEOUT"* || $job_status == *"NODE_FAIL"* || $job_status == *"PREEMPTED"* || $job_status == *"OUT_OF_MEMORY"* ]]; then
        echo "Job $job_id has finished with state: $job_status"
        exit_code=1
        break;
    fi
    sleep 10  # Adjust the sleep interval as needed
done

echo "Slurm job ($job_id) has finished."

echo "Print the job's output logs"
sacct --format=JobID,JobName,State,ExitCode,MaxRSS,Start,End -j $job_id
find /scratch/zsun/ -type f -name "*${job_id}.out" -exec cat {} \;
cat /scratch/zsun/test_data_slurm-*-$job_id.out

echo "All slurm job for ${SCRIPT_NAME} finishes."

exit $exit_code

