# NASA-GEOWEAVER: Environment setting

import os
import sys
import subprocess
import pkg_resources

with open('requirements.txt','w') as out:
  out.write('''
absl-py==1.0.0
affine==2.3.1
asttokens==2.0.5
astunparse==1.6.3
attrs==21.4.0
autokeras==1.0.18
backcall==0.2.0
cachetools==5.0.0
certifi==2021.10.8
cftime==1.6.0
charset-normalizer==2.0.12
click==8.1.3
click-plugins==1.1.1
cligj==0.7.2
cmaps==1.0.5
cycler==0.11.0
decorator==5.1.1
earthpy==0.9.4
executing==0.8.3
Fiona==1.8.21
flatbuffers==2.0
fonttools==4.29.1
gast==0.5.3
geopandas==0.10.2
glob2==0.7
google-auth==2.6.0
google-auth-oauthlib==0.4.6
google-pasta==0.2.0
grpcio==1.44.0
h5py==3.6.0
idna==3.3
imageio==2.19.0
imageio-ffmpeg==0.4.7
importlib-metadata==4.11.2
ipython==8.1.1
jedi==0.18.1
joblib==1.1.0
kaleido==0.2.1
keras==2.8.0
Keras-Preprocessing==1.1.2
keras-tuner==1.1.0
kiwisolver==1.3.2
kt-legacy==1.0.4
libclang==13.0.0
Markdown==3.3.6
matplotlib==3.5.1
matplotlib-inline==0.1.3
munch==2.5.0
netCDF4==1.5.8
networkx==2.8
numpy==1.22.2
oauthlib==3.2.0
opencv-python==4.5.5.64
opt-einsum==3.3.0
packaging==21.3
pandas==1.4.1
parso==0.8.3
pathlib==1.0.1
pathlib2==2.3.7.post1
pexpect==4.8.0
pickleshare==0.7.5
Pillow==9.0.1
plotly==5.7.0
prompt-toolkit==3.0.28
protobuf==3.19.4
ptyprocess==0.7.0
pure-eval==0.2.2
pyasn1==0.4.8
pyasn1-modules==0.2.8
Pygments==2.11.2
pyparsing==3.0.7
pyproj==3.3.1
python-dateutil==2.8.2
pytz==2021.3
PyWavelets==1.3.0
rasterio==1.2.10
requests==2.27.1
requests-oauthlib==1.3.1
rsa==4.8
scikit-image==0.19.2
scikit-learn==1.0.2
scipy==1.8.0
seaborn==0.11.2
Shapely==1.8.2
six==1.16.0
sklearn==0.0
snuggs==1.4.7
stack-data==0.2.0
tenacity==8.0.1
tensorboard==2.8.0
tensorboard-data-server==0.6.1
tensorboard-plugin-wit==1.8.1
tensorflow==2.8.0
tensorflow-gpu==2.8.0
tensorflow-io-gcs-filesystem==0.24.0
termcolor==1.1.0
tf-estimator-nightly==2.8.0.dev2021122109
threadpoolctl==3.1.0
tifffile==2022.5.4
traitlets==5.1.1
typing_extensions==4.1.1
urllib3==1.26.8
wcwidth==0.2.5
Werkzeug==2.0.3
wrapt==1.13.3
xarray==2022.3.0
xgboost==1.6.0
zipp==3.7.0''')
  
python = sys.executable
subprocess.check_call([python, '-m', 'pip', 'install', '-r', 'requirements.txt'], stdout=subprocess.DEVNULL)
    #subprocess.check_call(
        #[python, '-m', 'conda', 'install', '-c','conda-forge','xgboost'],
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
