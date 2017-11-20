### multi-panel plot of regional rotated regional grid data - precip
# Author : Sihan Li
import sys
import os
import numpy as np
import math
import datetime
import fnmatch
import matplotlib
import glob
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from scipy.io import netcdf
from netCDF4 import *
from datetime import date, timedelta
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import datetime, time
from mpl_toolkits.basemap import Basemap, shiftgrid
from netCDF4 import Dataset as NetCDFFile, date2index, num2date
import matplotlib.animation as animation
ddir='HAPPI/' 
def get_rot_global_coords(in_file):
    f=netcdf.netcdf_file(ddir+in_file,'r')
    glat=f.variables['global_latitude0']
    glon=f.variables['global_longitude0']
    f.close()
    return glat,glon   

def plot_chg(fig,Pr_data1_in,Pr_data2_in,Pr_data3_in,glon,glat,fname_out=False):
	fig = plt.figure(figsize=(7,6))
	print glon[-1,0]
	print glon[0,-1]
	month_list=['a)','b)','c)','d)','e)','f)','g)','h)','i)']
    	ax1 = fig.add_subplot(331)
    	ax1.set_title(month_list[0])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=(Pr_data2_in[0,:,:]-Pr_data1_in[0,:,:])/Pr_data1_in[0,:,:]*100
	CS4 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	
	ax2 = fig.add_subplot(332)
    	ax2.set_title(month_list[1])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=(Pr_data3_in[0,:,:]-Pr_data1_in[0,:,:])/Pr_data1_in[0,:,:]*100
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	

	
	ax3 = fig.add_subplot(333)
    	ax3.set_title(month_list[2])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=(Pr_data3_in[0,:,:]-Pr_data2_in[0,:,:])/Pr_data2_in[0,:,:]*100
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	
	ax4 = fig.add_subplot(334)
    	ax4.set_title(month_list[3])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=(Pr_data2_in[1,:,:]-Pr_data1_in[1,:,:])/Pr_data1_in[1,:,:]*100
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	
	ax6 = fig.add_subplot(335)
    	ax6.set_title(month_list[4])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=(Pr_data3_in[1,:,:]-Pr_data1_in[1,:,:])/Pr_data1_in[1,:,:]*100
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	
	ax6 = fig.add_subplot(336)
    	ax6.set_title(month_list[5])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=Pr_data3_in[1,:,:]-Pr_data2_in[1,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	
	ax7 = fig.add_subplot(337)
    	ax7.set_title(month_list[6])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=(Pr_data2_in[2,:,:]-Pr_data1_in[2,:,:])/Pr_data1_in[2,:,:]*100
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	
	ax9 = fig.add_subplot(338)
    	ax9.set_title(month_list[7])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=(Pr_data3_in[2,:,:]-Pr_data1_in[2,:,:])/Pr_data1_in[2,:,:]*100
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	
	ax9 = fig.add_subplot(339)
    	ax9.set_title(month_list[8])
	map = Basemap(llcrnrlon=255,llcrnrlat=glat[-1,0],urcrnrlon=325,urcrnrlat=glat[0,-1],\
                        resolution='l',area_thresh=1000.,projection='lcc',\
                        lat_1=(glat[-1,0]+glat[0,-1])/2,lon_0=(glon[-1,0]+glon[0,-1])/2)
    	for i in range(0,4):
    		if i==0:
	    		longitude=glon[0,:]
	    		latitude=glat[0,:]
    		elif i==1:
	    		longitude=glon[:,0]
            		latitude=glat[:,0]
    		elif i==2:
	    		longitude=glon[-1,:]
            		latitude=glat[-1,:]
    		elif i==3:
            		longitude=glon[:,-1]
            		latitude=glat[:,-1]
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(-50,50,5)
	Varin=(Pr_data3_in[2,:,:]-Pr_data2_in[2,:,:])/Pr_data2_in[2,:,:]*100
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.BrBG)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	fig.subplots_adjust(right=0.9)	
	fig.colorbar(CS2, cax=cbar_ax)
	plt.tight_layout()
	if fname_out:
    		fig.savefig(fname_out,dpi=300)
def main():
	ddir='Data/'  
	in_file1='pr_hist_prec_Annual.nc'
	in_file2='pr_15degree_prec_Annual.nc'
	in_file3='pr_2degree_prec_Annual.nc'
	glat,glon=get_rot_global_coords(in_file1)
	nc = Dataset(ddir+in_file1, mode='r')
	Pr_data1 = nc.variables['item5216_monthly_mean'][:]
	nc = Dataset(ddir+in_file2, mode='r')
	Pr_data2 = nc.variables['item5216_monthly_mean'][:]
	nc = Dataset(ddir+in_file3, mode='r')
	Pr_data3 = nc.variables['item5216_monthly_mean'][:]
	
	Pr_data1=np.squeeze(Pr_data1[:,0,:,:])*86400
	Pr_data2=np.squeeze(Pr_data2[:,0,:,:])*86400
	Pr_data3=np.squeeze(Pr_data3[:,0,:,:])*86400

	Pr_data1_in=np.zeros((3,183,162))
	Pr_data2_in=np.zeros((3,183,162))
	Pr_data3_in=np.zeros((3,183,162))
	
	Pr_data1_in[0,:,:]=Pr_data1
	Pr_data2_in[0,:,:]=Pr_data2
	Pr_data3_in[0,:,:]=Pr_data3
	
	in_file1='pr_hist_prec_wet.nc'
	in_file2='pr_15degree_prec_wet.nc'
	in_file3='pr_2degree_prec_wet.nc'
	glat,glon=get_rot_global_coords(in_file1)
	nc = Dataset(ddir+in_file1, mode='r')
	Pr_data1 = nc.variables['item5216_monthly_mean'][:]
	nc = Dataset(ddir+in_file2, mode='r')
	Pr_data2 = nc.variables['item5216_monthly_mean'][:]
	nc = Dataset(ddir+in_file3, mode='r')
	Pr_data3 = nc.variables['item5216_monthly_mean'][:]
	
	Pr_data1=np.squeeze(Pr_data1[:,0,:,:])*86400
	Pr_data2=np.squeeze(Pr_data2[:,0,:,:])*86400
	Pr_data3=np.squeeze(Pr_data3[:,0,:,:])*86400
	
	Pr_data1_in[1,:,:]=Pr_data1
	Pr_data2_in[1,:,:]=Pr_data2
	Pr_data3_in[1,:,:]=Pr_data3
	
	in_file1='pr_hist_prec_dry.nc'
	in_file2='pr_15degree_prec_dry.nc'
	in_file3='pr_2degree_prec_dry.nc'
	glat,glon=get_rot_global_coords(in_file1)
	nc = Dataset(ddir+in_file1, mode='r')
	Pr_data1 = nc.variables['item5216_monthly_mean'][:]
	nc = Dataset(ddir+in_file2, mode='r')
	Pr_data2 = nc.variables['item5216_monthly_mean'][:]
	nc = Dataset(ddir+in_file3, mode='r')
	Pr_data3 = nc.variables['item5216_monthly_mean'][:]
	
	Pr_data1=np.squeeze(Pr_data1[:,0,:,:])*86400
	Pr_data2=np.squeeze(Pr_data2[:,0,:,:])*86400
	Pr_data3=np.squeeze(Pr_data3[:,0,:,:])*86400
	
	Pr_data1_in[2,:,:]=Pr_data1
	Pr_data2_in[2,:,:]=Pr_data2
	Pr_data3_in[2,:,:]=Pr_data3

	fout='Figures/hist_15_2degree_prec_inPercent'
	f_ext='.png'
	plot_chg(plt.figure(),Pr_data1_in,Pr_data2_in,Pr_data3_in,glon,glat,fname_out=fout+f_ext)
	print "saved as",fout+f_ext
		
	print 'Finished!'
	
#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()
