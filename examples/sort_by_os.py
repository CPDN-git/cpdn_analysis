# sort extracted data by os systems to do other analysis
import sys
import os, glob
import csv
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_file 
import os, shutil
path="/gpfs/projects/cpdn/scratch/cenv0628/screen_os/batch_608/region/item5216_daily_mean/"
moveto="/gpfs/projects/cpdn/scratch/cenv0628/screen_os/batch_608/region/item5216_daily_mean/Windows/"
movetoto="/gpfs/projects/cpdn/scratch/cenv0628/screen_os/batch_608/region/item5216_daily_mean/MacLinux/"
def read_os_run(filename):
    run_os = {}
    f=open(filename)
    for row in csv.reader(f):
	try:
		key=row[0]
		val=row[-1]
		run_os[key]=val
	except:
		print "Skipping line"
    f.close()
    return run_os 

def read_data(batch):
    files=glob.glob("item*.nc")
    # Read the dictionary of the run OS
    run_os=read_os_run("/home/meredith.li/batch_"+str(batch)+"_os_results.csv")
    
    for ifile in files:
	file_split=ifile.split("/")
	filename=file_split[-1]
	filename_split=filename.split("_")
	umid=filename_split[3]
	# Check the OS workunit was run on and reject if not windows
	if run_os[umid]=="Windows":
		src = path+ifile
		dst = moveto+ifile
		shutil.move(src,dst)	
	else:
		src = path+ifile
		dst = movetoto+ifile
		shutil.move(src,dst)

#Main controling function
def main():
    batch=608
    read_data(batch)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()


