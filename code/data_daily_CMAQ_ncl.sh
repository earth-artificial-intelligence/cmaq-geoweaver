module load ncl


dateYesterday=$(date -d "2 day ago" '+%-d')
dateMonth=$(date -d "yesterday" '+%-m')
cd
ncl dateMonth=$dateMonth dateYesterday=$dateYesterday /groups/ESS/aalnaim/cmaq12_airnow_O3.ncl

