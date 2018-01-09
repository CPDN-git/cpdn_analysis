#!/usr/bin/env python2.7
#############################################################################
# Program : return_time_fromNetCDF.py
# Author  : Sarah Sparrow
# Date    : 03/08/2017
# Purpose : Plot distribution for Lotus workshop data
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

ddir="/gpfs/projects/CPDN-lotus-guests/LOTUS_WORKSHOP_DATA/SummerSchoolData/newData/"
bfolder="tasmax/day"
output={"Tmax":("tasmax","(K)"),"Tmin":("tasmin","(K)"),"Tmean":("tas","(K)")}
timeargs=["mean","max","min","sum"]
varname_dict={"Tmax":("Tmax","TXx","TXn","TmaxSum"),"Tmin":("Tmin","TNx","TNn","TminSum"), "Tmean":("T","Tx","Tn","Tsum")}

def read_data(batch,diag,time_proc,subregion):
    files=glob.glob(ddir+str(batch)+"/"+bfolder+"/*201706-201708.nc")
    mean_vals=[]
    
    if subregion != '':
        subreg=' -sellonlatbox,'+subregion
    else:
        subreg=''

    inputstr=subreg

    for ifile in files:
	print ifile
        # Compute the field mean value timeseries and return it as a numpy array
        vals=cdo.fldmean(options = "-f nc",input=inputstr+" "+ifile,returnCdf=True).variables[output[diag][0]][:]

        vals = vals.flatten()
	

        # Perform the required time processing on the data
        if time_proc =="mean":
                mean_val=np.mean(vals)
        elif time_proc =="max":
                mean_val=np.max(vals)
        elif time_proc =="min":
                mean_val==np.min(vals)
        elif time_proc =="sum":
                mean_val=np.sum(vals)

        mean_vals.append(mean_val)
    return mean_vals


def plot_distribution_data(diag,time_proc,subr): 

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
    dataHist=read_data("historicalExt",diag,time_proc,subr)
    dataNat=read_data("historicalNatExt",diag,time_proc,subr)
    # PLot the data
    sns.kdeplot(np.array(dataNat), shade=True, color="SeaGreen",label="HistoricalNatExt")
    sns.kdeplot(np.array(dataHist), shade=True, color="Orange",label="HistoricalExt")
    
    dtitle=varname_dict[diag][timeargs.index(time_proc)]

    ax.set_title(dtitle+" Distribution")
    ax.set_ylabel("Occurrence",fontsize=16)
    if time_proc=="sum":
    	ax_set_xlabel(dtitle,fontsize=16)
    else:
    	ax.set_xlabel(dtitle+" "+output[diag][1],fontsize=16)

    ll=ax.legend(loc="upper right",prop={"size": 12},fancybox=True,numpoints=1)

    fig.savefig("distribution_"+dtitle+".png",dpi=28.75*2)

	
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="The diagnostic variable to look at Precip, Tmean, Tmax or Tmin")
    parser.add_argument("time_process", help="The time processing required: mean, max, min or sum")
    parser.add_argument("--subregion", default="", help="The sub region of interest as lon1,lon2,lat1,lat2")
    args = parser.parse_args()
    plot_distribution_data(args.variable,args.time_process,args.subregion)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()




