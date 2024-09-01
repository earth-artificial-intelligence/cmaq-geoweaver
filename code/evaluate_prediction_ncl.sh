#!/bin/bash
# Specify the name of the script you want to submit
pwd
SCRIPT_NAME="evaluate_prediction_ncl_slurm.sh"
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


# evaluate the prediction accuracy

cmaq_folder="/groups/ESS/zsun/cmaq"
permanent_eval_folder="/groups/ESS3/zsun/cmaq/ai_results/evaluation/"
mkdir -p $cmaq_folder/results/
mkdir -p $permanent_eval_folder
chmod +x $cmaq_folder/results/ -R
chmod +x $permanent_eval_folder -R

#export YYYYMMDD_POST='20220806'
#export stdate_file='20220806'
#export eddate_file='20220808'

#This needs to be auto date

export dx=12000

source /home/zsun/.bashrc
module load ncl

rm $cmaq_folder/geoweaver_eva_daily_O3.ncl

cat << 'INNER_EOF' >> $cmaq_folder/geoweaver_eva_daily_O3.ncl

load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "/opt/sw/spack/apps/linux-centos8-cascadelake/gcc-9.3.0-openmpi-4.0.4/ncl-6.6.2-fr/lib/ncarg/nclscripts/csm/contributed.ncl"

setvalues NhlGetWorkspaceObjectId()
"wsMaximumSize": 600000000
end setvalues

begin
sdate=getenv("YYYYMMDD_POST")
wfname=getenv("wfname")
obs_dir=getenv("obs_dir_NCL")
ofname=getenv("ofname")
mod_dir=getenv("postdata_dir")
mfname=getenv("mfname")
dkm=tofloat(getenv("dx"))
grid_fname=(getenv("grid_fname"))

maxdist=dkm/90000.0*1.414
;maxarea=0.25
;thd=70
;maxdist=0.13*1.414
maxarea=0.25
thd=35.0

;-----read model lat lon------
;read lat lon
f1 = addfile(grid_fname,"r")
mlat = f1->LAT(0,0,:,:)
mlon = f1->LON(0,0,:,:)
delete(f1)
mlat1d = ndtooned(mlat)
mlon1d = ndtooned(mlon)
delete([/mlat,mlon/])

;-----read cmaq results-----
f2 = addfile(mod_dir+mfname,"r")
mO3 = f2->O3(:,0,:,:) ;ppb


nt = dimsizes(mO3(:,0,0))
ny = dimsizes(mO3(0,:,0))
nx = dimsizes(mO3(0,0,:))

m8O3 = new((/17,ny,nx/),"double")
m8maxO3 = new((/ny,nx/),"double")

do ih=0,16
  m8O3(ih,:,:)=dim_avg_n(mO3(ih:ih+7,:,:),0)
end do
m8maxO3 = dim_max_n(m8O3,0) ;type double
mO31d_d=ndtooned(m8maxO3) ; type double
mO31d=tofloat(mO31d_d)

delete([/f2,mO3,m8O3,m8maxO3/])

;-----read obs-----
syyyy1=str_get_cols(sdate,0,3)
smm1=str_get_cols(sdate,4,5)
sdd1=str_get_cols(sdate,6,7)

ymd=jul2greg(greg2jul(tointeger(syyyy1),tointeger(smm1),tointeger(sdd1),-1)+1)
syyyy2=tostring_with_format(ymd(0),"%0.4i")
smm2=tostring_with_format(ymd(1),"%0.2i")
sdd2=tostring_with_format(ymd(2),"%0.2i")

tolat=(/-999.0/) ;set the first data to 0
tolon=tolat
toO3=tolat

do ih=12,35
  if (ih.lt.24) then
    shh=tostring_with_format(ih,"%0.2i")
    syyyy=syyyy1
    smm=smm1
    sdd=sdd1
  else
    shh=tostring_with_format(ih-24,"%0.2i")
    syyyy=syyyy2
    smm=smm2
    sdd=sdd2
  end if
  data=asciiread(obs_dir+ofname+syyyy+smm+sdd+shh+".dat",-1,"string")
  xx=array_append_record(tolat,stringtofloat(str_get_field(data(1::), 2,",")),0)
  yy=array_append_record(tolon,stringtofloat(str_get_field(data(1::), 3,",")),0)
  zz=array_append_record(toO3,stringtofloat(str_get_field(data(1::), 4,",")),0)
  delete([/tolat,tolon,toO3/])
  tolat=xx
  tolon=yy
  toO3=zz
  delete([/xx,yy,zz/])
  delete(data)
end do

toO3@_FillValue = -999.0

;-----calculate max ave 8 hour o3-----
oflag=tolat*0+1
aa=ind((oflag.gt.0).and.(toO3.ge.0))
ii=0
print("8h start")
if (any(ismissing(aa))) then
  iflag=0
else
  iflag=1
  olat=(/tolat(aa(0))/)
  olon=(/tolon(aa(0))/)
  oO3=(/-999.0/)
  o8O3 = new(17,"float")
  o8O3 = -999.0
end if
delete(aa)
do while (iflag.gt.0)
  aa=ind((tolat.eq.olat(ii)).and.(tolon.eq.olon(ii)).and.(toO3.ge.0))
  oflag(aa)=0
  if (dimsizes(aa).eq.24) then  ; calculate 24 h, so calculate 8hr ozone here
    do ih = 0, 16
      o8O3(ih) = avg(toO3(aa(ih:ih+7)))
    end do
    oO3(ii)=max(o8O3)
  end if
  o8O3 = -999.0
  delete(aa)
  aa=ind((oflag.gt.0).and.(toO3.ge.0))
  if (any(ismissing(aa))) then
    iflag=0
  else
    xx=array_append_record(olat,(/tolat(aa(0))/),0)
    yy=array_append_record(olon,(/tolon(aa(0))/),0)
    zz=array_append_record(oO3,(/-999.0/),0)
    delete([/olat,olon,oO3/])
    olat=xx
    olon=yy
    oO3=zz
    delete([/xx,yy,zz/])
    ii=ii+1
  end if
  delete(aa)
end do
print("obs 8hour max end")
aa=ind(oO3.ge.0)
nobs=dimsizes(aa)
olat24=olat(aa)
olon24=olon(aa)
oO324=oO3(aa)
;print("oO324: "+oO324)
delete([/aa,olat,olon,oO3/])
mO324=oO324*0-999.0
;print("mO324: "+mO324)
;print("mO31d: "+mO31d)
areaa=oO324*0-999.0
areab=areaa
aread=areaa
;print("areaa: "+areaa)
;print("areab: "+areab)
;print("aread: "+aread)

;-----find model point-----
do in=0,nobs-1
  dis=sqrt((mlat1d-olat24(in))^2+(mlon1d-olon24(in))^2)
  aa=minind(dis)
  ;print(in+" "+aa)
  if (dis(aa).lt.maxdist) then
    mO324(in)=mO31d(aa)
    cc=ind((mlat1d.ge.(olat24(in)-maxarea)).and.(mlat1d.le.(olat24(in)+maxarea)).and.\
           (mlon1d.ge.(olon24(in)-maxarea)).and.(mlon1d.le.(olon24(in)+maxarea)))
    areaa(in)=0
    areab(in)=0
    if (oO324(in).ge.thd) then
      aread(in)=0
      if (max(mO31d(cc)).ge.thd) then
        areab(in)=1
      else
        aread(in)=1
      end if
    else
      bb=ind((olat24.ge.(olat24(in)-maxarea)).and.(olat24.le.(olat24(in)+maxarea)).and.\
             (olon24.ge.(olon24(in)-maxarea)).and.(olon24.le.(olon24(in)+maxarea)))
      if (max(mO31d(aa)).ge.thd) then
        if (max(oO324(bb)).ge.thd) then
          areaa(in)=0
        else
          areaa(in)=1
        end if
      else
        areaa(in)=0
      end if
      delete(bb)
    end if
    delete(cc)
  end if
  delete(aa)
end do

;-----cal rmse corr nme nmb me mb-----
tt=ind((mO324.ge.0).and.(oO324.ge.0))

if (any(ismissing(tt))) then
  rmse=-999.0
  corr=-999.0
  nmb=-999.0
  nme=-999.0
  me=-999.0
  mb=-999.0
else
  rmse=dim_rmsd_n(oO324(tt),mO324(tt),0)
  corr=esccr(oO324(tt),mO324(tt),0)
  nmb=sum((mO324(tt)-oO324(tt)))/sum(oO324(tt))
  nme=sum(abs(oO324(tt)-mO324(tt)))/sum(oO324(tt))
  me=avg(abs(oO324(tt)-mO324(tt)))
  mb=avg((mO324(tt)-oO324(tt)))
end if
;-----cal ah afar-----
;print("areaa: "+areaa)
;print("areab: "+areab)
aa=ind((areaa+areab).gt.0)
bb=ind((aread+areab).gt.0)
;print("aa: "+aa)
;print("bb: "+bb)
if (any(ismissing(aa))) then
  afar=0.
else
  afar=tofloat(sum(areaa(aa)))/tofloat(sum(areab(aa))+sum(areaa(aa)))*100
end if
delete(aa)
if (any(ismissing(bb))) then
  ah=-999.0
else
  ah=tofloat(sum(areab(bb)))/tofloat(sum(areab(bb))+sum(aread(bb)))*100
end if
delete(bb)
write_table(wfname,"a",[/sdate,dimsizes(tt),avg(oO324(tt)),avg(mO324(tt)),rmse,corr,nmb,nme,mb,me,ah,afar/],\
            "%s,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f")
delete(tt)
end

exit
INNER_EOF

days_back=30
force=true
for i in $(seq 1 $days_back)
do
  end_day=$i
  echo "$end_day days ago"
  begin_day=$((i+1))
  # Setting env variables
  export YYYYMMDD_POST=$(date -d $begin_day' day ago' '+%Y%m%d')
  export stdate_file=$(date -d $begin_day' day ago' '+%Y%m%d') #This needs to be auto date
  export eddate_file=$(date -d $end_day' day ago' '+%Y%m%d') #This needs to be auto date
  export wfname=$cmaq_folder"/results/geoweaver_evalution_"$YYYYMMDD_POST"_results.txt"

  export obs_dir_NCL="/scratch/sma8/forecast/OBS/AirNow/AQF5X/"
  export ofname="/AQF5X_Hourly_"

  export postdata_dir=$cmaq_folder"/prediction_nc_files/"

  export mfname="COMBINE3D_ACONC_v531_gcc_AQF5X_"$stdate_file"_ML_extracted.nc"

  export grid_fname="/scratch/sma8/forecast/mcip/12km/GRIDCRO2D_"$YYYYMMDD_POST".nc" 
  echo "Current Day: "$stdate_file
  # determine if the prediction netcdf is there
  predict_nc_file=$cmaq_folder"/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_"$stdate_file"_ML_extracted.nc"
  if [ -f "$predict_nc_file" ]; then
    echo "$predict_nc_file exists."
  else
    echo "$predict_nc_file doesn't exist. Skipping..."
    continue
  fi
  
  predict_eval_file=$permanent_eval_folder"eval_"$stdate_file".txt"
  
  if [ "$force" != true ] ; then
    if [ -f "$predict_eval_file" ]; then
      echo "$predict_eval_file exists. Skipping..."
      continue
    else
      echo "$predict_eval_file doesn't exist. Generating..."
    fi
  fi
  
  rm -rf $cmaq_folder/results/* # clean everything first
  ncl $cmaq_folder/geoweaver_eva_daily_O3.ncl
  
  if [ $? -eq 0 ]; then
    echo "Evaluation Completed Successfully"
    cat $wfname
    cp $wfname $predict_eval_file
  else
    echo "Evaluation Failed!"
  fi
  
done



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


