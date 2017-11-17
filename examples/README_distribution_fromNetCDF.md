To use distribuion_fromNetCDF.py you will need certain python packages installed.  

In the directory above there is a pyenv.yml file that is a miniconda environment that has all the necessary installed packages in it.  To use this download miniconda (as per instructions on the cpdn_extract_scripts git repsitory up to the point that you create the environment) if you don’t have it already. Then your can import the environment by using:

conda env create -f pyenv.yml
source activate pyenv

You will need to update the file paths in the script and also download the OS split csv file and put it somewhere that the script points to. This can be downloaded from (change the batch number as appropriate):
http://sepia.oerc.ox.ac.uk/cpdnboinc/batch_os_breakdown.php?batchid=518

You run as follows:

./distribution_fromNetCDF.py Tmax max 507 50km ‘110,117,25,35’

Input 1: The variable  (options are Tmax, Tmin, Tmean, Precip) 
Input 2: The time processing (options are mean, max, min, sum)
Input 3: The batch number to look at
Input 4: The region resolution (if you want to regrid the data, otherwise just enter as "")
Input 5: The subregion boundaries as ‘lon1,lon2,lat1,lat2’ if you don’t want a subregion just enter ""

There is also a return_time_fromNetCDF.py that works in a similar way but take in a list of up to 4 batch numbers (entered as "1,2,3,4") and batch_names (entered as "'Actual','Natural','GHG Only','Climatology'")
