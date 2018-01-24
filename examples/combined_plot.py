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

ddir="/gpfs/projects/CPDN-lotus-guests/LOTUS_WORKSHOP_DATA/SummerSchoolData/newData/"
bfolder="tasmax/day"
output={"Tmax":("tasmax","(K)"),"Tmin":("tasmin","(K)"),"Tmean":("tas","(K)")}
timeargs=["mean","max","min","sum"]
varname_dict={"Tmax":("Tmax","TXx","TXn","TmaxSum"),"Tmin":("Tmin","TNx","TNn","TminSum"), "Tmean":("T","Tx","Tn","Tsum")}

cols=[["#00b478","#00b478"],["#c80000","#c80000"],["MediumBlue","RoyalBlue"],["Indigo","MediumSlateBlue"]]

def read_data(batch,diag,time_proc,subregion):
    files=glob.glob(ddir+str(batch)+"/"+bfolder+"/*201706-201708.nc")
    mean_vals=[]
    
    if subregion != '':
        subreg=' -sellonlatbox,'+subregion
    else:
        subreg=''

    for ifile in files:
	print ifile
        inputstr=' -selmon,7 -fldmean'+subreg+' -sub '+ifile+' '+ddir+'historical/tasmax/day/tasmax_1961-1990_max_07_ensmean_timmean.nc'
        # Compute the field mean value timeseries and return it as a numpy array
        vals=cdo.runmean(5,options = "-f nc",input=inputstr,returnCdf=True).variables[output[diag][0]][:]

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
        elif time_proc =="all":
		mean_val=vals
	
        mean_vals.append(mean_val)
    return mean_vals

def plot_figure(diag,time_proc,subr,errb,restore):
    # Set up the plot
    font = {'family' : 'sans-serif',
            'size'   : 20}

    matplotlib.rc('font', **font)
    fig = plt.figure()
    fig.set_size_inches(16,8)
    
    # Read or restore the data
    if restore==False:
        dataHist=read_data("historicalExt",diag,time_proc,subr)
        dataNat=read_data("historicalNatExt",diag,time_proc,subr)
        np.save('dataHist_'+str(diag)+'.npy',np.array(dataHist))
        np.save('dataNat_'+str(diag)+'.npy',np.array(dataNat))
    else:
        dataHist=np.load('dataHist_'+diag+'.npy')
        dataNat=np.load('dataNat_'+diag+'.npy')


    plot_distribution_data(dataHist,dataNat,fig)
    plot_return_time_data(dataHist,dataNat,errb,fig)
    plt.tight_layout()
    fig.savefig("combined_figure.png",dpi=28.75*2)

def plot_distribution_data(dataHist,dataNat,fig): 
    ax = fig.add_subplot(1,2,1)
    plt.setp(ax.get_xticklabels(),fontsize=16)
    plt.setp(ax.get_yticklabels(),fontsize=16)

    # PLot the data
    print "Maximum value Natural",max(dataNat)
    sns.distplot(np.array(dataNat), kde=False,fit=stats.genextreme, color="#00b478",label="HistoricalNat",fit_kws={"linewidth":2.5,"color":"#00b478"})
    sns.distplot(np.array(dataHist), kde=False,fit=stats.genextreme, color="#c80000",label="Historical",fit_kws={"linewidth":2.5,"color":"#c80000"})
    
    ax.plot([1.9,1.9],[0,0.35],'k--',linewidth=2.5,zorder=3,label="Warmest event pre 2010")
    ax.plot([2.3,2.3],[0,0.35],'k:',linewidth=2.5,zorder=3,label="2017 event")
   
    HistCount=sum(np.array(dataHist)>1.9)
    NatCount=sum(np.array(dataNat)>1.9)

    RiskRatio=float(HistCount)/float(NatCount)
    
    #ax.text(0.05,0.95,"Risk ratio for warmest event pre 2010 = "+str(round(RiskRatio,2)),transform=ax.transAxes,fontsize=12,verticalalignment='top')
    ax.set_ylim(0,0.35)
    ax.set_xlim(-6,8)
    #ax.set_title("July Distribution")
    ax.set_ylabel("Percentage (%)",fontsize=16)
    ax.set_xlabel("Max Overlapping Pentad Anomaly ($^{o}C$)",fontsize=16)

    #ll=ax.legend(loc="upper right",prop={"size": 12},fancybox=True,numpoints=1,framealpha=1)
    ax.text(0.93,0.99,"(a)",transform=ax.transAxes,fontsize=20,verticalalignment='top')

def plot_data(data,cols,plabel,ax,errb,lab):
    y_data_all, x_data_all = calc_return_times(data,direction="descending",period=1)
    
    conf_all = calc_return_time_confidences(data,direction="descending",bsn=1000
)
    conf_all_x = calc_return_time_confidences(x_data_all,direction="descending",
bsn=1000)

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

    ax.semilogx([min(x_data_all),max(x_data_all)],[1.9,1.9],'k--',linewidth=2.5,label=lab[0],zorder=2)
    ax.semilogx([min(x_data_all),max(x_data_all)],[2.3,2.3],'k:',linewidth=2.5,label=lab[1],zorder=2)
    
    nidx=find_nearest(y_data_all,1.9)
    
    ax.axvspan(conf_all_x_5[nidx],conf_all_x_95[nidx],ymin=0,ymax=(1.9+6)/(6+6),facecolor='silver',alpha=0.5,zorder=0)
    ax.set_ylim(-6,6)

def find_nearest(array,value):
    idx=(np.abs(array-value)).argmin()
    return idx 

def plot_return_time_data(dataHist,dataNat,errb,fig): 
    ax = fig.add_subplot(1,2,2)
    ax.set_ylabel("Max overlapping pentad anomaly ($^{o}C$)",fontsize=16)
    ax.set_xlabel("Chance of event occurring in a given year",fontsize=16)
    plt.setp(ax.get_xticklabels(),fontsize=16)
    plt.setp(ax.get_yticklabels(),fontsize=16)
    ax.set_xlim(1,1e3)

    plot_data(np.array(dataHist),cols[1],"Historical",ax,errb,[None,None])
    plot_data(np.array(dataNat),cols[0],"HistoricalNat",ax,errb,["Warmest event pre 2010","2017 event"])


#    ax.set_title("July Return Times")

    labels=['','1/1','1/10','1/100','1/1000']
    ax.set_xticklabels(labels)

    ll=ax.legend(loc="upper left",prop={"size": 14},fancybox=True,numpoints=1)
    ax.text(0.93,0.99,"(b)",transform=ax.transAxes,fontsize=20,verticalalignment='top')

	
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="The diagnostic variable to look at Precip, Tmean, Tmax or Tmin")
    parser.add_argument("time_process", help="The time processing required: mean, max, min or sum")
    parser.add_argument("--subregion", default="", help="The sub region of interest as lon1,lon2,lat1,lat2")
    parser.add_argument("--error_bar", default="both", help="Which error bars to display: 'return_time','magnitude','both'")
    parser.add_argument("--restore", action="store_true", help="Restore the data")

    args = parser.parse_args()
    plot_figure(args.variable,args.time_process,args.subregion, args.error_bar,args.restore)
    print 'Finished!'

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()




