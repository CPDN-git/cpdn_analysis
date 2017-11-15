#!/usr/bin/env python2.7
#############################################################################
# Program : return_time_fromNetCDF.py
# Author  : Sarah Sparrow
# Date    : 03/08/2017
# Purpose : Plot return time periods and errors for 2014 Tmax
#############################################################################

import sys
import os, glob
import csv
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from netCDF4 import Dataset as netcdf_file 
from cdo import *
cdo = Cdo()

ddir="/group_workspaces/jasmin/cssp_china/users/ssparrow01/extracted/"
os_dir="/home/users/ssparrow01/os_split/"
bfolder="/region/"
output={"Precip":("item5216_daily_mean","(mm/day)"),"Tmax":("item3236_daily_maximum","(K)"),"Tmin":("item3236_daily_minimum","(K)"),"Tmean":("item3236_daily_mean","(K)")}

def read_data(batch,diag,os,resolution,subregion):
    files=glob.glob(ddir+"batch_"+str(batch)+bfolder+output[diag][0]+"/*.nc")
    mean_vals=[]
    # Read the dictionary of the run OS
    run_os=read_os_run(os_dir+"batch_"+str(batch)+"_os_results.csv")
    
    # Work out the input string for cdo
    if resolution == '50km':
	remap=' -remapbil,r720x360'
    elif resolution == '25km':
	remap=' -remapbil,r1440x730'
    else:
	remap=''

    if subregion != '':
	subreg=' -sellonlatbox,'+subregion
    else:
	subreg=''

    inputstr=subreg+remap

    for ifile in files:
	file_split=ifile.split("/")
	filename=file_split[-1]
	filename_split=filename.split("_")
	umid=filename_split[3]
	print umid
	# Check the OS workunit was run on and reject if not windows
	if run_os[umid]==os:
    		# Compute the field mean value timeseries and return it as a numpy array
    		if diag=="Precip":
			vals=cdo.fldmean(input=inputstr+" "+ifile,returnCdf=True).variables[output[diag][0]][:] 
                	vals = vals.flatten()
                	vals=vals*86400
                	mean_val=np.sum(vals)
		else:
			vals=cdo.fldmean(input=inputstr+" "+ifile,returnCdf=True).variables[output[diag][0]][:] 	
			vals = vals.flatten()
			mean_val=np.sum(vals)
		mean_vals.append(mean_val)
    return mean_vals

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

def plot_distribution_data(diag,batch_no,res,subr): 

    # Set up the plot
    font = {'family' : 'sans-serif',
            'size'   : 20}

    matplotlib.rc('font', **font)
    fig = plt.figure()
    fig.set_size_inches(8,8)
    ax = fig.add_subplot(1,1,1)
    fig.subplots_adjust(bottom=0.15)
    ax.set_ylabel("Occurrence",fontsize=16)
    ax.set_xlabel(diag,fontsize=16)
    plt.setp(ax.get_xticklabels(),fontsize=12)
    plt.setp(ax.get_yticklabels(),fontsize=12)

    # Read in the data
    data_win=read_data(batch_no,diag,"Windows",res,subr)
    data_lin=read_data(batch_no,diag,"Linux",res,subr)
    data_mac=read_data(batch_no,diag,"Mac",res,subr)
    
    # PLot the data
    sns.kdeplot(np.array(data_win), shade=True, color="MediumBlue",label="Windows")
    sns.kdeplot(np.array(data_lin), shade=True, color="SeaGreen",label="Linux")
    sns.kdeplot(np.array(data_mac), shade=True, color="Orange",label="Mac")

    ax.set_title("Batch "+str(batch_no)+" "+diag+" Distribution")

    ll=ax.legend(loc="upper right",prop={"size": 12},fancybox=True,numpoints=1)

    fig.savefig("Batch_"+str(batch_no)+"_distribution_"+diag+".png",dpi=28.75*2)

	
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="The diagnostic variable to look at Precip, Tmean, Tmax or Tmin")
    parser.add_argument("batch", help="The batch number")
    parser.add_argument("region_resolution", default="", help="The regional model resolution, 50km or 25km")
    parser.add_argument("subregion", default="", help="The sub region of interest as lon1,lon2,lat1,lat2")
    args = parser.parse_args()
    plot_distribution_data(args.variable,args.batch,args.region_resolution,args.subregion)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()




