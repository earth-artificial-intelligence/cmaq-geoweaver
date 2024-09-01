#!/bin/bash

echo "Converting netcdf to geotiff"

# geotif_dir="/groups/ESS3/zsun/cmaq/ai_results/geotiff"
# mkdir -p $geotif_dir

# prediction_netcdf_dir = ""
# grid_netcdf_dir = ""

# Specify the name of the script you want to submit
SCRIPT_NAME="convert_netcdf_to_geotiff_slurm.sh"
echo "write the slurm script into ${SCRIPT_NAME}"
cat > ${SCRIPT_NAME} << 'EOF'
#!/bin/bash
#SBATCH -J generate_images_ncl_slurm       # Job name
#SBATCH --output=/scratch/%u/%x-%N-%j.out  # Output file`
#SBATCH --error=/scratch/%u/%x-%N-%j.err   # Error file`
#SBATCH -n 1               # Number of tasks
#SBATCH -c 4               # Number of CPUs per task (threads)
#SBATCH --mem=20G          # Memory per node (use units like G for gigabytes) - this job must need 200GB lol
#SBATCH -t 0-03:00         # Runtime in D-HH:MM format

module load imagemagick
module load netcdf
module load gdal

# Activate your customized virtual environment
source /home/zsun/anaconda3/bin/activate

python -u << INNER_EOF

import xarray as xr
import traceback
import rasterio
from rasterio.transform import from_origin
import numpy as np
import os



def add_lat_lon_to_netcdf(predicted_netcdf_path, output_new_geolocated_netcdf_path, grid_netcdf_path):
    try:
        # Load the NetCDF files
        print(f"Opening grid netcdf {grid_netcdf_path}")
        print(f"Opening prediction netcdf {predicted_netcdf_path}")
        grid_ds = xr.open_dataset(grid_netcdf_path)
        o3_ds = xr.open_dataset(predicted_netcdf_path)
        # Extract LAT and LON variables, and remove the TSTEP and LAY dimensions
        lat = grid_ds['LAT'].squeeze(dim='TSTEP', drop=True).squeeze(dim='LAY', drop=True)
        lon = grid_ds['LON'].squeeze(dim='TSTEP', drop=True).squeeze(dim='LAY', drop=True)

        # Add the spatial grid to the O3 dataset
        print("Assign coords to predicted netcdf: ")
        o3_ds = o3_ds.assign_coords(
            LAT=(['ROW', 'COL'], lat.values), 
            LON=(['ROW', 'COL'], lon.values)
        )
        # Save the updated NetCDF with geospatial information
        print("Saving to file")
        o3_ds.to_netcdf(output_new_geolocated_netcdf_path)
        print(f"New geolocated netcdf is saved to {output_new_geolocated_netcdf_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def create_geotiff_from_netcdf(netcdf_path, geotiff_path):
    try:
        # Load the NetCDF file
        ds = xr.open_dataset(netcdf_path)

        # Extract variables
        o3 = ds['O3']
        lat = ds['LAT']
        lon = ds['LON']

        # Get dimensions
        n_bands = o3.sizes['TSTEP']
        rows = o3.sizes['ROW']
        cols = o3.sizes['COL']

        # Calculate the affine transform from the latitude and longitude
        transform = from_origin(
            lon.min().values,  # x-coordinate of the upper-left corner
            lat.max().values,  # y-coordinate of the upper-left corner
            (lon.max().values - lon.min().values) / cols,  # pixel width
            (lat.max().values - lat.min().values) / rows   # pixel height
        )

        # Define the CRS (Coordinate Reference System)
        crs = 'EPSG:4326'  # Assuming WGS84, adjust if needed

        # Create a GeoTIFF with all bands
        with rasterio.open(
            geotiff_path,
            'w',
            driver='GTiff',
            height=rows,
            width=cols,
            count=n_bands,  # Number of bands
            dtype=o3.dtype,
            crs=crs,
            transform=transform
        ) as dst:
            for t in range(n_bands):
                # Extract and reshape data for the current band
                band_data = o3.isel(TSTEP=t).squeeze().values
                if band_data.shape != (rows, cols):
                    raise ValueError(f"Unexpected shape for band {t}: {band_data.shape}")
                dst.write(band_data, t + 1)  # Write data to each band

        print(f"GeoTIFF has been created at {geotiff_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


def process_netcdf_files(predicted_netcdf_folder, predicted_geotiff_folder, grid_netcdf_path):
    for filename in os.listdir(predicted_netcdf_folder):
        if filename.endswith('.nc'):
            predicted_netcdf_path = os.path.join(predicted_netcdf_folder, filename)
            geotiff_filename = filename.replace('.nc', '_with_grid.tif')
            geotiff_path = os.path.join(predicted_geotiff_folder, geotiff_filename)
            
            geolocated_netcdf_path = predicted_netcdf_path.replace('.nc', '_with_grid.nc')
            
            # Check if the GeoTIFF already exists
            if not os.path.exists(geotiff_path):
                # Add latitude and longitude to the NetCDF
                add_lat_lon_to_netcdf(
                    predicted_netcdf_path=predicted_netcdf_path,
                    output_new_geolocated_netcdf_path=geolocated_netcdf_path,
                    grid_netcdf_path=grid_netcdf_path
                )
                
                # Create GeoTIFF from the geolocated NetCDF
                create_geotiff_from_netcdf(
                    netcdf_path=geolocated_netcdf_path,
                    geotiff_path=geotiff_path
                )
            else:
                print(f"GeoTIFF already exists: {geotiff_path}")


def do_all_conversion():
    try:
        # Example usage
        ai_results_folder = "/groups/ESS3/zsun/cmaq/ai_results/"
        predicted_netcdf_folder = f"{ai_results_folder}/netcdfs/"
        predicted_geotiff_folder = f"{ai_results_folder}/geotiffs/"
        grid_netcdf_path = "/groups/ESS3/zsun/cmaq/GRIDCRO2D_20200101.nc"

        process_netcdf_files(predicted_netcdf_folder, predicted_geotiff_folder, grid_netcdf_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    do_all_conversion()

INNER_EOF

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


