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
from scipy import stats
from netCDF4 import Dataset as netcdf_file 
from cdo import *
cdo = Cdo()
EU = os.path.expanduser
sys.path.append(EU("../"))
from return_time_plot import *

ddir="/group_workspaces/jasmin2/cpdn_rapidwatch/joe_scratch/extracted/"
bfolder="/region/"
output={"Precip":("item5216_daily_maximum","(mm/day)"),"Tmax":("item3236_daily_maximum","(K)"),"Tmin":("item3236_daily_minimum","(K)"),"Tmean":("item3236_daily_mean","(K)")}


def read_data(batch,diag,time_proc, os_run,resolution,subregion,umid_limits):
    files=glob.glob(ddir+"batch_"+str(batch)+bfolder+output[diag][0]+"/"+output[diag][0]+"*.nc")
    mean_vals=[]
    # Work out the input string for cdo
    if resolution == '50km':
        remap=' -remapbil,r720x360'
    elif resolution == '25km':
        remap=' -remapbil,r1440x720'
    else:
        remap=''

    if subregion != '':
        subreg=' -sellonlatbox,'+subregion
    else:
        subreg=''

    inputstr=subreg+remap

    
    #pool = multiprocessing.Pool(processes=10)

    for ifile in files:
        file_split=ifile.split("/")
        filename=file_split[-1]
        filename_split=filename.split("_")
        umid=filename_split[3]
        print umid
	if (umid>umid_limits[0]) and (umid<umid_limits[1]):
                # Compute the field mean value timeseries and return it as a numpy array
		vals=cdo.selmon('7/9', input=' -fldmean '+inputstr+" "+ifile,returnCdf=True).variables[output[diag][0]][:]
		vals = vals.flatten()
		
		# Convert to mm/day for Precip
                if diag=="Precip":
                	vals=vals*86400

		# Perform the required time processing on the data
        	if time_proc =="mean":
                	mean_val=np.mean(vals)
        	elif time_proc =="max":
                	mean_val=np.max(vals)
        	elif time_proc =="min":
                	mean_val==np.min(vals)
        	elif time_proc =="sum":
                	mean_val=np.sum(vals)
        	elif time_proc =="all":
                	mean_val=vals

        	mean_vals.append(mean_val)

    #pool.close()
    #pool.join()

    return mean_vals


def plot_figure(diag,time_proc,res,subr,errb,restore):
    # Set up the plot
    font = {'family' : 'sans-serif',
            'size'   : 20}

    matplotlib.rc('font', **font)
    fig = plt.figure()
    fig.set_size_inches(16,8)
    
    # Read or restore the data
    if restore==False:
	dataHist=read_data("646",diag,time_proc,res,subr,("0000","zzzz"))
        data15=read_data("647",diag,time_proc,res,subr,("0000","zzzz"))
        data2=read_data("648",diag,time_proc,res,subr,("0000","zzzz"))
	np.save('batch_646_data.npy',np.array(dataHist))
        np.save('batch_647_data.npy',np.array(data15))
	np.save('batch_648_data.npy',np.array(data2))
    else:
        dataHist=np.load('batch_646_data.npy')
        data15=np.load('batch_647_data.npy')
	data2=np.load('batch_648_data.npy')

    plot_distribution_data(dataHist,data15,data2,diag,fig)
    plot_return_time_data(dataHist,data15,data2,errb,diag,fig)
    plt.tight_layout()
    fig.savefig("combined_figure_"+str(diag)+"_joe.png",dpi=28.75*2)

def plot_distribution_data(dataHist,data15,data2,diag,fig): 
    ax = fig.add_subplot(1,2,1)
    plt.setp(ax.get_xticklabels(),fontsize=16)
    plt.setp(ax.get_yticklabels(),fontsize=16)

    # PLot the data
    sns.distplot(np.array(data15), kde=False,fit=stats.genextreme, color="gold",label="1.5 degree",fit_kws={"linewidth":2.5,"color":"gold"})
    sns.distplot(np.array(data2), kde=False,fit=stats.genextreme, color="red",label="2 degree",fit_kws={"linewidth":2.5,"color":"red"})
    sns.distplot(np.array(dataHist), kde=False,fit=stats.genextreme, color="MediumBlue",label="Historical",fit_kws={"linewidth":2.5,"color":"MediumBlue"})
   
    ax.set_ylabel("Percentage (%)",fontsize=16)
    ax.set_xlabel(diag+" "+output[diag][1],fontsize=16)

    #ll=ax.legend(loc="upper right",prop={"size": 12},fancybox=True,numpoints=1,framealpha=1)
    ax.text(0.93,0.99,"(a)",transform=ax.transAxes,fontsize=20,verticalalignment='top')

def risk_ratio(dataHist,dataNat,year,threshold,label):
    HistCount=sum(np.array(dataHist)>threshold)
    NatCount=sum(np.array(dataNat)>threshold)
    P_hist=float(HistCount)/float(len(dataHist))
    P_nat=float(NatCount)/float(len(dataNat))
    RiskRatio=P_hist/P_nat
    if label:
	print year+" Risk ratio ",RiskRatio
    return RiskRatio

def plot_data(data,cols,plabel,ax,errb,diag):
    y_data_all, x_data_all = calc_return_times(data,direction="descending",period=1)
    
    conf_all = calc_return_time_confidences(data,direction="descending",bsn=10000)
    conf_all_x = calc_return_time_confidences(x_data_all,direction="descending",bsn=10000)

    boot_all = calc_bootstrap_ensemble(data,direction="descending",bsn=10000)
    boot_all_x = calc_bootstrap_ensemble(x_data_all,direction="descending",bsn=10000)

    l1=ax.semilogx(x_data_all,y_data_all, marker='o',markersize=4,
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

    return boot_all, boot_all_x


def find_nearest(array,value):
    idx=(np.abs(array-value)).argmin()
    return idx 

def calc_bootstrap_ensemble(em, direction="ascending", bsn=1e4):
        # bsn = boot strap number, number of times to resample the distribution
        ey_data = em.flatten()
        # create the store
        sample_store = numpy.zeros((int(bsn), ey_data.shape[0]), 'f')
        # do the resampling
        for s in range(0, int(bsn)):
                t_data = numpy.zeros((ey_data.shape[0]), 'f')
                for y in range(0, ey_data.shape[0]):
                        x = random.uniform(0, ey_data.shape[0])
                        t_data[y] = ey_data[int(x)]
                t_data.sort()
                # reverse if necessary
                if direction == "descending":
                        t_data = t_data[::-1]
                sample_store[s] = t_data
	return sample_store


def plot_return_time_data(dataHist,data15,data2,errb,diag,fig): 
    ax = fig.add_subplot(1,2,2)
    ax.set_ylabel(diag+" "+output[diag][1],fontsize=16)
    ax.set_xlabel("Return time",fontsize=16)
    plt.setp(ax.get_xticklabels(),fontsize=16)
    plt.setp(ax.get_yticklabels(),fontsize=16)
    ax.set_xlim(1,1e4)

    actBoot,actBootx=plot_data(np.array(dataHist),["MediumBlue","MediumBlue"],"Historical",ax,errb,diag)
    15Boot,15Bootx=plot_data(np.array(data15),["Gold","Gold"],"1.5 degree",ax,errb,diag)
    2Boot,2Bootx=plot_data(np.array(data2),["Red","Red"],"2 degree",ax,errb,diag)
    #[RR_5,RR_50,RR_95]=calc_RR_conf(actBoot,natBoot,[5,50,95],threshold)
    rp_threshold=10
    [RR_5,RR_50,RR_95]=calc_RR_conf(2Bootx,histBootx,[5,50,95],rp_threshold)
    print "2 degree RR:",RR_50,RR_5,RR_95
    [RR_5,RR_50,RR_95]=calc_RR_conf(15Bootx,histBootx,[5,50,95],rp_threshold)
    print "1.5 degree RR:",RR_50,RR_5,RR_95

    labels=['','1/1','1/10','1/100','1/1000','1/10000']
    ax.set_xticklabels(labels)

    ll=ax.legend(loc="lower right",prop={"size": 14},fancybox=True,numpoints=1)
    ax.text(0.93,0.99,"(b)",transform=ax.transAxes,fontsize=20,verticalalignment='top')

def calc_RR_conf(actBoot,natBoot,percentile,threshold,bsn=1000):
    RR=[]
    for ib in range(0,bsn):
	RR.append(risk_ratio(actBoot[ib,:].flatten(),natBoot[ib,:].flatten(),"",threshold,False))
    RR_5=get_val_percentile(RR,percentile[0])
    RR_50=get_val_percentile(RR,percentile[1])
    RR_95=get_val_percentile(RR,percentile[2])
    return [RR_5,RR_50,RR_95]

def get_val_percentile(data, percentile):
    if len(data) < 1:
        value = None
    elif (percentile >= 100):
        sys.stderr.write('ERROR: percentile must be < 100.  you supplied: %s\n'%
 percentile)
        value = None
    else:
        element_idx = int(len(data) * (percentile / 100.0))
        data.sort()
        value = data[element_idx]
    return value

	
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="The diagnostic variable to look at Precip, Tmean, Tmax or Tmin")
    parser.add_argument("time_process", help="The time processing required: mean, max, min or sum")
    parser.add_argument("--region_resolution", default="", help="The regional model resolution, 50km or 25km")
    parser.add_argument("--subregion", default="", help="The sub region of interest as lon1,lon2,lat1,lat2")
    parser.add_argument("--error_bar", default="both", help="Which error bars to display: 'return_time','magnitude','both'")
    parser.add_argument("--restore", action="store_true", help="Restore the data")

    args = parser.parse_args()
    plot_figure(args.variable,args.time_process,args.region_resolution,args.subregion, args.error_bar,args.restore)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()




