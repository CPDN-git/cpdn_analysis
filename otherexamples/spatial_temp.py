### multi-panel plot of regional rotated grid data-temperature
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
ddir='data/' 
def get_rot_global_coords(in_file):
    f=netcdf.netcdf_file(ddir+in_file,'r')
    glat=f.variables['global_latitude0']
    glon=f.variables['global_longitude0']
    f.close()
    return glat,glon   

def plot_chg(fig,T_data1_in,T_data2_in,T_data3_in,glon,glat,fname_out=False):
	fig = plt.figure(figsize=(6,6))
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
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data2_in[0,:,:]-T_data1_in[0,:,:]
	CS4 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
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
    		x, y = map(longitude, latitude)
	x1, y1=map(glon[:],glat[:])
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data3_in[0,:,:]-T_data1_in[0,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
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
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data3_in[0,:,:]-T_data2_in[0,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
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
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data2_in[1,:,:]-T_data1_in[1,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
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
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data3_in[1,:,:]-T_data1_in[1,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
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
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data3_in[1,:,:]-T_data2_in[1,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
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
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data2_in[2,:,:]-T_data1_in[2,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
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
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data3_in[2,:,:]-T_data1_in[2,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
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
	clevs = np.arange(0,2.1,0.1)
	Varin=T_data3_in[2,:,:]-T_data2_in[2,:,:]
	CS2 = map.contourf(x1,y1,Varin,clevs,cmap=plt.cm.YlOrRd)
	map.drawcoastlines(color = '0.15',linewidth=0.2)
	map.drawcountries(color = '0.15',linewidth=0.2)
	fig.subplots_adjust(right=0.9)
	cbar_ax = fig.add_axes([0.94, 0.15, 0.01, 0.7])
	fig.colorbar(CS2, cax=cbar_ax)
	plt.tight_layout()
	plt.show()
	if fname_out:
    		fig.savefig(fname_out,dpi=300)
def main():
	ddir='Data/'  
	in_file1='hist_temp_Annual.nc'
	in_file2='W15degree_temp_Annual.nc'
	in_file3='W2degree_temp_Annual.nc'
	glat,glon=get_rot_global_coords(in_file1)
	nc = Dataset(ddir+in_file1, mode='r')
	T_data1 = nc.variables['item3236_monthly_mean'][:]
	nc = Dataset(ddir+in_file2, mode='r')
	T_data2 = nc.variables['item3236_monthly_mean'][:]
	nc = Dataset(ddir+in_file3, mode='r')
	T_data3 = nc.variables['item3236_monthly_mean'][:]
	
	T_data1=np.squeeze(T_data1[:,0,:,:])-273.15
	T_data2=np.squeeze(T_data2[:,0,:,:])-273.15
	T_data3=np.squeeze(T_data3[:,0,:,:])-273.15

	T_data1_in=np.zeros((3,183,162))
	T_data2_in=np.zeros((3,183,162))
	T_data3_in=np.zeros((3,183,162))
	
	T_data1_in[0,:,:]=T_data1
	T_data2_in[0,:,:]=T_data2
	T_data3_in[0,:,:]=T_data3
	
	ddir='Data/'  
	in_file1='hist_temp_wet.nc'
	in_file2='W15degree_temp_wet.nc'
	in_file3='W2degree_temp_wet.nc'
	glat,glon=get_rot_global_coords(in_file1)
	nc = Dataset(ddir+in_file1, mode='r')
	T_data1 = nc.variables['item3236_monthly_mean'][:]
	nc = Dataset(ddir+in_file2, mode='r')
	T_data2 = nc.variables['item3236_monthly_mean'][:]
	nc = Dataset(ddir+in_file3, mode='r')
	T_data3 = nc.variables['item3236_monthly_mean'][:]
	
	T_data1=np.squeeze(T_data1[:,0,:,:])-273.15
	T_data2=np.squeeze(T_data2[:,0,:,:])-273.15
	T_data3=np.squeeze(T_data3[:,0,:,:])-273.15
	
	T_data1_in[1,:,:]=T_data1
	T_data2_in[1,:,:]=T_data2
	T_data3_in[1,:,:]=T_data3
	
	in_file1='hist_temp_dry.nc'
	in_file2='W15degree_temp_dry.nc'
	in_file3='W2degree_temp_dry.nc'
	glat,glon=get_rot_global_coords(in_file1)
	nc = Dataset(ddir+in_file1, mode='r')
	T_data1 = nc.variables['item3236_monthly_mean'][:]
	nc = Dataset(ddir+in_file2, mode='r')
	T_data2 = nc.variables['item3236_monthly_mean'][:]
	nc = Dataset(ddir+in_file3, mode='r')
	T_data3 = nc.variables['item3236_monthly_mean'][:]
	
	T_data1=np.squeeze(T_data1[:,0,:,:])-273.15
	T_data2=np.squeeze(T_data2[:,0,:,:])-273.15
	T_data3=np.squeeze(T_data3[:,0,:,:])-273.15
	
	T_data1_in[2,:,:]=T_data1
	T_data2_in[2,:,:]=T_data2
	T_data3_in[2,:,:]=T_data3

		
	fout='Figures/hist_15_2degree_temp'
	f_ext='.png'
	plot_chg(plt.figure(),T_data1_in,T_data2_in,T_data3_in,glon,glat,fname_out=fout+f_ext)
	print "saved as",fout+f_ext
		
	print 'Finished!'
	
#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()
