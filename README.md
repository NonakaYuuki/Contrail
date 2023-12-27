# contrail

## Visualization Method of Contrail Formation Areas
### 1. Downloading Meteorological Data
Download MSM data using the following command:\
$ ```python data/MSM_download.py```

Download ClimCORE data from the following URL into ```./data/ClimCORE```:\
http://www.atmos.rcast.u-tokyo.ac.jp/miyasaka/data/eriitoh_20230927.jBPbpdXGdUjQ/

### 2. Visualization of Contrail Formation Areas
$ ```python3 src/main.py ```

### ※ Troubleshooting xesmf Installation & Import
Create a virtual environment named xesmf_env using conda:\
$ ```conda create -n xesmf_env```

Activate the xesmf_env virtual environment:\
$ ```conda activate xesmf_env```

Install xesmf:\
$ ```conda install -c conda-forge xesmf```\
$ ```conda install -c conda-forge dask netCDF4```

<br>
------------------------- Description of Each File -------------------------

## ./src/main.py
Using flight data (CARATS open data or OpenSky data) and meteorological data (MSM data or ClimCORE data), calculate the number of flights generating contrails and visualize the potential contrail formation areas.

Input for the ```Contrail_in_Japan``` class includes the date and latitude-longitude range for analysis.

### ```vis_contrail_MSM()```
Visualize areas where contrails can form using MSM data.

### ```vis_contrail_ClimCORE()```
Visualize areas where contrails can form using ClimCORE data.

### ```count_flight()```
Count the number of flights that can potentially generate contrails.

<br>

## ./src/ClimCORE.py
Input the year, month, day, hour, latitude (degrees), longitude (degrees), and pressure altitude (feet) into the ClimCORE class. Execute the functions below to obtain meteorological data for the specified date, time, and location. The output is in the form of xarray.dataset.

### ```Pressure()```
Function to output pressure (hPa).

### ```RHi()```
Function to output relative humidity to ice (%).

### ```Temperature()```
Function to output temperature (K).

### ```U_Wind()```
Function to output east-west wind speed. Westerly wind is positive (m/s).

### ```V_Wind()```
Function to output north-south wind speed. Southerly wind is positive (m/s).

<br>

## ./src/CARATS.py
Input the path to CARATS open data (CSV file) into the ```path```.
### ```cover_path()```
Function to interpolate flight routes between two points. Interpolation is done to achieve approximately 0.1 degrees between points.

### ```rmk_flight_data()```
Return flight data interpolated by the above function.

### ```vis_path()```
Visualize flight data from CARATS open data.

<br>

## ./src/vapor_pressure_graph.py
Graphs of the proposed saturation vapor pressure curves for water and ice in previous papers. These formulas are used to convert relative humidity from water to relative humidity to ice.

<br>

## ./src/vertical_profile.py
The function ```vis_profile(date, hour, lat, lon)``` visualizes vertical profiles of temperature and relative humidity to ice at a given date and location.

The above is an explanation of the files in Japanese. Please let me know if you have any questions or need further clarification.