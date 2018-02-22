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
timeargs=["mean","max","min","sum"]
varname_dict={"Precip":("Pr","Prx","Prn","PrSum"),"Tmax":("Tmax","TXx","TXn","TmaxSum"),"Tmin":("Tmin","TNx","TNn","TminSum"), "Tmean":("T","Tx","Tn","Tsum")}

def read_data(batch,diag,time_proc, os_run,resolution,subregion):
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
        if run_os[umid] in os_run:
                print run_os[umid]
                # Compute the field mean value timeseries and return it as a numpy array
                vals=cdo.fldmean(input=inputstr+" "+ifile,returnCdf=True).variables[output[diag][0]][:]

                # Convert to mm/day for Precip
                if diag=="Precip":
                        vals=vals*86400

                vals = vals.flatten()
                # Perform the required time processing on the data
                if time_proc =="mean":
                        mean_val=np.mean(vals)
                elif time_proc =="max":
                        mean_val=np.max(vals)
                elif time_proc =="min":
                        mean_val=np.min(vals)
                elif time_proc =="sum":
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
		print "Read "+filename
    f.close()
    return run_os 

def plot_distribution_data(diag,time_proc,batch_no,res,subr): 

    # Set up the plot
    font = {'family' : 'sans-serif',
            'size'   : 20}

    matplotlib.rc('font', **font)
    fig = plt.figure()
    fig.set_size_inches(8,8)
    ax = fig.add_subplot(1,1,1)
    fig.subplots_adjust(bottom=0.15)
    plt.setp(ax.get_xticklabels(),fontsize=12)
    plt.setp(ax.get_yticklabels(),fontsize=12)

    # Read in the data
    data_win=read_data(batch_no,diag,time_proc,["Windows"],res,subr)
    data_lin=read_data(batch_no,diag,time_proc,["Linux"],res,subr)
    data_mac=read_data(batch_no,diag,time_proc,["Mac"],res,subr)
    
    # PLot the data
    sns.kdeplot(np.array(data_win), shade=True, color="MediumBlue",label="Windows")
    sns.kdeplot(np.array(data_lin), shade=True, color="SeaGreen",label="Linux")
    sns.kdeplot(np.array(data_mac), shade=True, color="Orange",label="Mac")
    
    dtitle=varname_dict[diag][timeargs.index(time_proc)]

    ax.set_title("Batch "+str(batch_no)+" "+dtitle+" Distribution")
    ax.set_ylabel("Occurrence",fontsize=16)
    if time_proc=="sum":
    	ax_set_xlabel(dtitle,fontsize=16)
    else:
    	ax.set_xlabel(dtitle+" "+output[diag][1],fontsize=16)

    ll=ax.legend(loc="upper right",prop={"size": 12},fancybox=True,numpoints=1)

    fig.savefig("Batch_"+str(batch_no)+"_distribution_"+dtitle+".png",dpi=28.75*2)

	
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="The diagnostic variable to look at Precip, Tmean, Tmax or Tmin")
    parser.add_argument("time_process", help="The time processing required: mean, max, min or sum")
    parser.add_argument("batch", help="The batch number")
    parser.add_argument("--region_resolution", default="", help="The regional model resolution, 50km or 25km")
    parser.add_argument("--subregion", default="", help="The sub region of interest as lon1,lon2,lat1,lat2")
    args = parser.parse_args()
    plot_distribution_data(args.variable,args.time_process,args.batch,args.region_resolution,args.subregion)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()




