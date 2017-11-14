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
#from scipy.stats import genextreme as gev
import seaborn as sns
from netCDF4 import Dataset as netcdf_file 
from cdo import *
cdo = Cdo()
EU = os.path.expanduser
sys.path.append(EU("../"))
from return_time_plot import *

ddir="/gpfs/projects/cpdn/scratch/Khaled/"
bfolder="/region/"
output={"Precip":("item5216_daily_mean","(mm/day)"),"Tmax":("item3236_daily_maximum","(K)"),"Tmin":("item3236_daily_minimum","(K)")}

def read_data(batch,diag,os):
    files=glob.glob(ddir+"batch_"+str(batch)+bfolder+output[diag][0]+"/subset_*.nc")
    mean_vals=[]
    
    # Read the dictionary of the run OS
    run_os=read_os_run("/home/sarah.sparrow/batch_"+str(batch)+"_os_results.csv")
    
    for ifile in files:
	file_split=ifile.split("/")
	filename=file_split[-1]
	filename_split=filename.split("_")
	umid=filename_split[4]
	# Check the OS workunit was run on and reject if not windows
	if run_os[umid]==os:
    		# Compute the field mean value timeseries and return it as a numpy array
    		if diag=="Precip":
			vals=cdo.fldmean(input=ifile,returnCdf=True).variables[output[diag][0]][:] 
                	vals = vals.flatten()
                	vals=vals*86400
                	mean_val=np.sum(vals)
		else:
			vals=cdo.fldmean(input=ifile,returnCdf=True).variables[output[diag][0]][:] 	
			vals = vals.flatten()
			mean_val=np.mean(vals)
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

def plot_data(data,cols,plabel,ax):
    sns.distplot(data, color=cols[1],label=plabel)
    #numargs = gev.numargs
    #[ c ] = [0.9,] * numargs
    #gev_shape,gev_loc,gev_scale = gev.fit(data)
    #max_val=np.max(data)
    #min_val=np.min(data)
    #bins_hist=numpy.arange(min_val,max_val,(max_val-min_val)/25)
    #n, bins, patches = ax.hist(data,bins=bins_hist,normed=1,facecolor=cols[1],alpha=0.3,label=plabel)
    #gev_pdf = gev.pdf(numpy.arange(100),gev_shape,loc=gev_loc,scale=gev_scale)
    #plt.plot(numpy.arange(100),gev_pdf,color=cols[0])
    #print gev_pdf
 
def plot_distribution_data(diag): 

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
    batch_act=631
    batch_nat=632
    
    data_win=read_data(batch_act,diag,"Windows")
    data_lin=read_data(batch_act,diag,"Linux")
    data_mac=read_data(batch_act,diag,"Mac")
    #data_nat=read_data(batch_nat,diag,"Windows")
    
    plot_data(np.array(data_win),["MediumBlue","RoyalBlue"],"Windows",ax)
    plot_data(np.array(data_lin),["SeaGreen","SpringGreen"],"Linux",ax)
    plot_data(np.array(data_mac),["Orange","Gold"],"Mac",ax)

    ax.set_title(diag+" Distribution")

    ll=ax.legend(loc="upper right",prop={"size": 12},fancybox=True,numpoints=1)

    fig.savefig("distribution_"+diag+".png",dpi=28.75*2)

	
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="The diagnostic variable to look at Precip, Tmax or Tmin")
    args = parser.parse_args()
    plot_distribution_data(args.variable)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()




