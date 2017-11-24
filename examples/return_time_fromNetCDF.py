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

ddir="/group_workspaces/jasmin/cssp_china/users/ssparrow01/extracted/"
os_dir="/home/users/ssparrow01/os_split/"
bfolder="/region/"
output={"Precip":("item5216_daily_mean","(mm/day)"),"Tmax":("item3236_daily_maximum","(K)"),"Tmin":("item3236_daily_minimum","(K)"),"Tmean":("item3236_daily_mean","(K)")}
timeargs=["mean","max","min","sum"]
varname_dict={"Precip":("Pr","Prx","Prn","PrSum"),"Tmax":("Tmax","TXx","TXn","TmaxSum"),"Tmin":("Tmin","TNx","TNn","TminSum"), "Tmean":("T","Tx","Tn","Tsum")}

cols=[["MediumBlue","RoyalBlue"],["SeaGreen","SpringGreen"],["Orange","Gold"],["Indigo","MediumSlateBlue"]]

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
                        mean_val==np.min(vals)
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
		print "Skipping line"
    f.close()
    return run_os 

def plot_data(data,cols,plabel,ax,errb):
    y_data_all, x_data_all = calc_return_times(data,direction="descending",period=1)
    
    conf_all = calc_return_time_confidences(data,direction="descending",bsn=1000)
    conf_all_x = calc_return_time_confidences(x_data_all,direction="descending",bsn=1000)

    l1=ax.semilogx(x_data_all,y_data_all, marker='o',markersize=2,
                       linestyle='None',mec=cols[0],mfc=cols[0],
                       color=cols[0],fillstyle='full',
                       label=plabel,zorder=2)
    print x_data_all.shape
    conf_all_5=conf_all[0,:].squeeze()
    conf_all_95=conf_all[1,:].squeeze()

    conf_all_x_5=conf_all_x[0,:].squeeze()
    conf_all_x_95=conf_all_x[1,:].squeeze()

    if errb=="both":
    	cl0=ax.fill_between(x_data_all,conf_all_5,conf_all_95,color=cols[1],alpha=0.2,linewidth=1.,zorder=0)
    if errb=="magnitude" or errb=="both":
    	cl1=ax.semilogx([x_data_all,x_data_all],[conf_all_5,conf_all_95],color=cols[1],linewidth=1.,zorder=1)
    if errb=="return_time" or errb=="both":
	cl2=ax.semilogx([conf_all_x_5,conf_all_x_95],[y_data_all,y_data_all],color=cols[1],linewidth=1.,zorder=1)
 
def plot_return_time_data(diag,time_proc,batches,bnames,res,subr,errb): 

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
    batch_list = batches.split(",")
    batch_names = bnames.split(",")

    for ib, batch_no in enumerate(batch_list):
    	data_win=read_data(batch_no,diag,time_proc,["Windows"],res,subr)
    	plot_data(np.array(data_win),cols[ib],batch_names[ib],ax,errb)

    dtitle=varname_dict[diag][timeargs.index(time_proc)]
    ax.set_title(dtitle+" Return Times")

    ax.set_xlim(1.,1.e5)
    labels=['','1/1','1/10','1/100','1/1000','1/10000','']
    ax.set_xticklabels(labels)

    ll=ax.legend(loc="lower right",prop={"size": 12},fancybox=True,numpoints=1)

    fig.savefig("return_time_"+dtitle+".png",dpi=28.75*2)

	
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="The diagnostic variable: Precip, Tmean, Tmax or Tmin")
    parser.add_argument("time_process", help="The time processing required: mean, max, min or sum") 
    parser.add_argument("batch", help="The list of batch numbers to plot, entered as eg '507,508,509'")
    parser.add_argument("batch_name",help="The batch names to use entered as eg 'Actual,Natural,GHG only''")
    parser.add_argument("--region_resolution", default="", help="The regional model resolution: '50km' or '25km'")
    parser.add_argument("--subregion", default="", help="The sub region of interest as 'lon1,lon2,lat1,lat2'")
    parser.add_argument("--error_bar", default="both", help="Which error bars to display: 'return_time','magnitude','both'")
    args = parser.parse_args()
    plot_return_time_data(args.variable,args.time_process,args.batch,args.batch_name,args.region_resolution,args.subregion, args.error_bar)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()




