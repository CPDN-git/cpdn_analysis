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
from netCDF4 import Dataset as netcdf_file 
from cdo import *
cdo = Cdo()
EU = os.path.expanduser
sys.path.append(EU("../"))
from return_time_plot import *

ddir="/gpfs/projects/cpdn/scratch/Khaled/"
bfolder="/region/"
output={"Precip":("item5216_daily_mean","(mm/day)"),"Tmax":("item3236_daily_maximum","(K)"),"Tmin":("item3236_daily_minimum","(K)")}

def read_data(batch,diag):
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
	if run_os[umid]=="Windows":
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
    y_data_all, x_data_all = calc_return_times(data,direction="descending",period=1)
    
    conf_all = calc_return_time_confidences(data,direction="descending",bsn=1000)
    
    l1=ax.semilogx(x_data_all,y_data_all, marker='o',markersize=7,
                       linestyle='None',mec=cols[0],mfc=cols[0],
                       color=cols[0],fillstyle='full',
                       label=plabel,zorder=2)
    print x_data_all.shape
    conf_all_5=conf_all[0,:].squeeze()
    conf_all_95=conf_all[1,:].squeeze()
    cl1=ax.fill_between(x_data_all,conf_all_5,conf_all_95,facecolor=cols[1],edgecolor=cols[1],alpha=0.3,linewidth=1.5,zorder=4)

 
def plot_return_time_data(diag): 

    # Set up the plot
    font = {'family' : 'sans-serif',
            'size'   : 20}

    matplotlib.rc('font', **font)
    fig = plt.figure()
    fig.set_size_inches(8,8)
    ax = fig.add_subplot(1,1,1)
    fig.subplots_adjust(bottom=0.15)
    ax.set_ylabel("Yearly JAS "+diag+" exceeding this amount "+output[diag][1],fontsize=16)
    ax.set_xlabel("Chance of event occurring in a given year",fontsize=16)
    plt.setp(ax.get_xticklabels(),fontsize=12)
    plt.setp(ax.get_yticklabels(),fontsize=12)

    # Read in the data
    batch_act=631
    batch_nat=632
    
    data_act=read_data(batch_act,diag)
    data_nat=read_data(batch_nat,diag)
    
    plot_data(np.array(data_act),["MediumBlue","RoyalBlue"],"Actual",ax)

    plot_data(np.array(data_nat),["SeaGreen","SpringGreen"],"Natural",ax)

    ax.set_title(diag+" Return Times")

    #ax.set_ylim(200,400)
    ax.set_xlim(1.,1.e4)
    labels=['','1/1','1/10','1/100','1/1000','']
    ax.set_xticklabels(labels)

    ll=ax.legend(loc="lower right",prop={"size": 12},fancybox=True,numpoints=1)

    fig.savefig("return_time_"+diag+".png",dpi=28.75*2)

	
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="The diagnostic variable to look at Precip, Tmax or Tmin")
    args = parser.parse_args()
    plot_return_time_data(args.variable)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()




