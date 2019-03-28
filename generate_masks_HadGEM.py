# script to take polygon(s) and turn into a mask on a particular lat-lon grid
# Modified from Peter Uhe's original script
# Sihan Li
# 27/07/2017
import math
import numpy as np
from matplotlib.path import Path
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap,cm
import os
import unicodedata

# Use osgeo (gdal library) to load shapefile
# Installed by '$conda install gdal'
from osgeo import ogr
########################################################################################
### Convert global coords to rotated (regional) coords

def glob2rot(lon, lat, pole_lon, pole_lat):

	# Make sure rotlon is between 0 and 360
	while (lon  >= 360.0):
		lon  -= 360.0
	while (lon  <    0.0):
		lon  += 360.0

    # Make sure pole_lon is between 0 and 360
	while (pole_lon >= 360.0):
		pole_lon -= 360.0
	while (pole_lon <    0.0):
		pole_lon += 360.0

	# Convert inputs to radians
	lon_r = math.radians(lon)
	lat_r = math.radians(lat)
	pole_lon_r = math.radians(pole_lon)
	pole_lat_r = math.radians(pole_lat)

	# Amount rotated about 180E meridian
	if (pole_lon_r == 0.0):
		sock = 0.0;
	else:
		sock = pole_lon_r - math.pi

	# Need to get the screw in range -pi to pi
	screw = lon_r - sock;
	while (screw < -1.0 * math.pi):
		screw += 2.0 * math.pi
	while (screw > math.pi):
		screw -= 2.0 * math.pi
	bpart = math.cos(screw) * math.cos(lat_r)

	x = (-1.0 * math.cos(pole_lat_r) * bpart) + (math.sin(pole_lat_r) * math.sin(lat_r))
	if (x >=  1.0):
		x =  1.0
	if (x <= -1.0):
		x = -1.0
	lat2 = math.asin(x)

	t1 = math.cos(pole_lat_r) * math.sin(lat_r)
	t2 = math.sin(pole_lat_r) * bpart

	x = (t1 + t2) / math.cos(lat2)

	if (x >=  1.0):
		x =  1.0
	if (x <= -1.0):
		x = -1.0
	lon2 = -1.0 * math.acos(x)

	if (screw >= 0.0 and screw <= math.pi):
		lon2 *= -1.0

	# Convert back to degrees
	lon = math.degrees(lon2)
	lat = math.degrees(lat2)

	return lon, lat

########################################################################################
### Convert rotated (regional) to global grid

def rot2glob(lon, lat, pole_lon, pole_lat):
	# Make sure rotlon is between 0 and 360
	while (lon >= 360.0):
		lon -= 360.0
	while (lon <    0.0):
		lon += 360.0
	# Make sure pole_lon is between 0 and 360
	while (pole_lon >= 360.0):
		pole_lon -= 360.0
	while (pole_lon < 0.0): 
		pole_lon += 360.0

	# Convert inputs to radians
	lon = math.radians(lon)
	lat = math.radians(lat)
	pole_lon = math.radians(pole_lon)
	pole_lat = math.radians(pole_lat)

	# Amount rotated about 180E meridian
	if (pole_lon == 0.0):
		sock = 0.0
	else:
		sock = pole_lon - math.pi

	cpart = math.cos(lon) * math.cos(lat)
	x = math.cos(pole_lat) * cpart + math.sin(pole_lat) * math.sin(lat)

	if (x >=  1.0):
		x =  1.0
	if (x <= -1.0):
		x = -1.0
	lat_out = math.asin(x)

	t1 = -1.0 * math.cos(pole_lat) * math.sin(lat)
	t2 = math.sin(pole_lat) * cpart

	x = (t1 + t2) / math.cos(lat_out)
	if (x >=  1.0):
		x =  1.0
	if (x <= -1.0):
		x = -1.0
	lon_out = -1.0 * math.acos(x)
 
    # Make sure rotlon is between -PI and PI    
	while (lon < -1*math.pi):
		lon += 2.0*math.pi
	while (lon > math.pi):
		lon -= 2.0*math.pi

	if (lon >= 0.0 and lon <= math.pi):
		lon_out *= -1.0
	lon_out += sock;
	# Convert back to degrees
	lon_out = math.degrees(lon_out)
	lat_out = math.degrees(lat_out)

	return lon_out, lat_out

########################################################################################

####################################################################################

# Load a text file containing lists of vertices (space separated, one vertex per line)
# Creates matplotlib.path.Path objects representing the polygons. 
# Lines starting with '#' are ignored
# A blank line indicates the end of a polygon, so multiple polygons can be defined with new lines in between
def load_polygons(fname):
	polygons=[]
	tmp=[]
	# Import Polygons of mask in fname (separate polygons are separated by a blank line)
	for line in open(fname,'r'):
		if line[0]=='#': 
			# skip commented lines
			continue
		elif line.strip()!='':
			# Add coordinates to list
			tuple=line.strip().split()
			tmp.append(tuple) # lon,lat
		else: # blank line
			# Finished reading data for this polygon
			# create polygon path out of list of vertices
			if tmp !=[]:
				polygons.append(Path(np.array(tmp)))
				tmp=[]
	# If the file didn't end in a blank line, add the final polygon
	if tmp !=[]:
		polygons.append(Path(np.array(tmp)))
	# print polygons
	# polygons=glob2rot(polygons[:,1], polygons[:,2], 236.68,79.95)
	return polygons

###################################################################################

def load_grid(fname,latname='gloabl_latitude0',lonname='global_longitude0'):
	# load region grid and returns list of points (lon,lat)
	with Dataset(fname,'r') as f:
		# Load 1d arrays of lon and lat
		lat=f.variables[latname][:]
		lon=f.variables[lonname][:]
		
		if len(lat.shape)==2:
			# 2D lat and lon:
			lonxx=lon
			latyy=lat
		else:
			# Create 2D arrays of lon and lat
			lonxx,latyy=np.meshgrid(lon,lat)
	#print lonxx
	#print latyy
	return lonxx,latyy

##################################################################################

# Function to create mask given polygons object and points array
def create_mask(polygons,points,nlat,nlon):
	# Convert polygons to mask (true if inside the polygon region)
	# add the masks for multiple polygons together
	for i,polygon in enumerate(polygons):
		# Determine if  points inside polygon
		tmp_mask = polygon.contains_points(points)
		# Reshape mask to dimensions of the grid
		tmp_mask=np.reshape(tmp_mask,[nlat,nlon])
		try:
			mask=tmp_mask | mask
		except:
			mask=tmp_mask
			
	return ~mask # Invert the mask so true is outside the region

#################################################################################

# Wrapper function to return the mask given the polygons file and grid file
def load_and_create_mask(f_polygons,f_grid,latname='global_latitude0',lonname='global_longitude0'):
	# Load inputs and create mask
	polygons=load_polygons(f_polygons)
	# Load 2D lon and lat arrays for grid
	lonxx,latyy=load_grid(f_grid,latname,lonname)
	nlat,nlon=lonxx.shape
	# Stack points into a N x 2 array (where N = nlat x nlon)
	points = np.vstack((lonxx.flatten(),latyy.flatten())).T
	# Call create_mask function for polygons and grid points
	return create_mask(polygons,points,nlat,nlon)

#################################################################################

def add_to_text(fileh,polygon):
	for coord in polygon.vertices:
		fileh.write(str(coord[0])+' '+str(coord[1])+'\n')
	fileh.write('\n')

#################################################################################
def get_rotated_pole(nc_in_file,in_var):
	# get the rotated pole longitude / latitude (for calculating weights)
	try:
		grid_map_name = getattr(nc_in_var,"grid_mapping")
		grid_map_var = nc_in_file.variables[grid_map_name]	
		plon = getattr(grid_map_var,"grid_north_pole_longitude")
		plat = getattr(grid_map_var,"grid_north_pole_latitude")
	except:
		plon = 0.0
		plat = 90.0
	return plon, plat


##############################################################################
def create_netcdf(template,data,outname,template_var='field16'):
	# create outfile object
	outfile=Dataset(outname,'w')

	# Create dimensions copied from template file
	temp=template.variables[template_var]
	for dim in temp.dimensions:
		if dim[:3]=='lat' or dim[:3] =='lon':
			leng=len(template.dimensions[dim])
		
			outfile.createDimension(dim[:3],leng)
			outfile.createVariable(dim[:3],'f',(dim[:3],))
			outfile.variables[dim[:3]][:]=template.variables[dim][:]
			print template.variables[dim].__dict__
			for att in template.variables[dim].ncattrs():
				outfile.variables[dim[:3]].__setattr__(att,template.variables[dim].__getattribute__(att))

	# Create data variable (named region_mask)
	outfile.createVariable('region_mask','f',['lat','lon'])
	outfile.variables['region_mask'][:]=(data-1)*-1

	outfile.close()

#############################################################################

# Create a mask, from textfile for a specific grid
# f_grid: (filename of netcdf file contatining grid information)
# latname, lonname: name of latitude and longitude variables in netcdf file
# 
def create_mask_fromtext(f_grid,textfile,region_name='region',latname='latitude0',lonname='longitude0',plot=False,template_var='field16'):

	# first create folders (if needed)
	if plot and not os.path.exists('plots'):
		os.mkdir('plots')
	#if not os.path.exists('masks_netcdf'):
	#	os.mkdir('masks_netcdf')
	#if not os.path.exists('masks_text'):
	#	os.mkdir('masks_text')

	# Load Shape file
	polygons=load_polygons(textfile)

	# Load lat lon grid (for mask)
	lonxx,latyy=load_grid(f_grid,latname=latname,lonname=lonname)
	nlat,nlon=lonxx.shape
	# Update lon to be from -180 to 180 
	# NOTE: (this is only if the shapefile uses lat coordinates from -180-180 )
	# Comment out otherwise
	#lonxx[lonxx>180]=lonxx[lonxx>180]-360
	# Turn lat and lon into a list of coordinates
	points = np.vstack((lonxx.flatten(),latyy.flatten())).T
	print points
	if plot:
		# Set up Basemap projection (may need fine tuning)
		m = Basemap(projection='robin',lon_0=180)
		xx,yy=m(lonxx,latyy) # basemap coordinates
		plot_mask = np.zeros([nlat,nlon])

	# Create mask out of polygon, matching points from grid
	
	mask = create_mask(polygons,points,nlat,nlon)
	#print mask 
	# Create netcdf for combined mask
	create_netcdf(Dataset(f_grid,'r'),mask,'region_mask/masks_netcdf/mask_'+region_name+'.nc',template_var='field16')

	if plot:
		plt.clf()
		m.contourf(xx,yy,mask)
		plt.colorbar()
		m.drawcoastlines(linewidth=0.2)
		m.drawcountries(linewidth=0.2)
		plt.title('Mask: '+region_name)
		plt.savefig('plots/mask_'+region_name+'.png')

#################################################################################

if __name__=='__main__':
	# Set up input files


	# Template grid for output mask
	f_grid='region_mask/region_template/HadGEM3-N216/HadGEM3-A-N216_template.nc'

	# Text file with region boundaries
	f_text = 'region_mask/source_file/Madeira.shp'

	create_mask_fromtext(f_grid,f_text, region_name = 'Madeira',latname='latitude',lonname='longitude', plot=False,template_var='pr')

