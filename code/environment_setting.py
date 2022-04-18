# NASA-GEOWEAVER: Environment setting

import os
import sys
import subprocess
import pkg_resources

# Required packages to run this process.
required = {'pandas','pathlib','sklearn','numpy','keras','tensorflow','tensorflow-gpu','autokeras','kaleido','glob2','scipy','netCDF4','xarray','geopandas','Shapely','rasterio','earthpy'}
#required = {'GDAL'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Packages missing and will be installed: ", missing)
    python = sys.executable
    subprocess.check_call(
        [python, '-m', 'pip', 'install', *missing],
      stdout=subprocess.DEVNULL)
    #subprocess.check_call(
        #[python, '-m', 'conda', 'install', '-c','conda-forge','gdal', *missing],
      #stdout=subprocess.DEVNULL)


################################
#  END OF PACKAGES Installation  #


# Creating directoris 
from pathlib import Path
home = str(Path.home())
folders = ['cmaq/exploratory_analysis', 'cmaq/prediction_maps', 'cmaq/prediction_files','cmaq/models','cmaq/observation']
for folder in folders:
  paths=Path(home+'/'+folder)
  paths.mkdir(parents=True,exist_ok=True)
  
  ###############################
  # END OF DIRECTORY CREATION #
