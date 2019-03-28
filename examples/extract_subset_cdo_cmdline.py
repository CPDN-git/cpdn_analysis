#!/usr/bin/env python2.7
#############################################################################
# Program : extract_subset.py
# Author  : Sarah Sparrow
# Date    : 01/02/2019
# Purpose : Extract subset from HadGEM3-N216 data
#############################################################################

import sys
import os, glob
import argparse
import numpy as np
import seaborn as sns
from netCDF4 import Dataset as netcdf_file 
from cdo import *
cdo = Cdo()
EU = os.path.expanduser
sys.path.append(EU("../"))

expts=["historical","historicalNat","historicalExt","historicalNatExt"]

def process_data(args, expt):
  files=glob.glob(args.ddir+expt+"/"+args.var+"/"+args.freq+"/*.nc")
  for ifile in files:    
        fname=ifile.split("/")[-1]
        if args.subregion != '':
                subreg=' -sellonlatbox,'+args.subregion+' '
                tag_name="subset_"+(args.subregion).replace(",","_")
        else:
                subreg=''
        
        if args.mask != '':
                mask_reg=' -mul,'+args.mask+' '
                tag_name="mask_"+args.mask.split(".")[0]
        else:
                mask_reg=''

	opath=args.odir+expt+"/"+args.var+"/"
	if not os.path.exists(opath):
    		os.makedirs(opath)
        ofile=opath+tag_name+"_"+fname
        print subreg+mask_reg+ifile, ofile
        os.system('cdo -f nc selname,'+args.var+subreg+mask_reg+ifile+' '+ofile)
        #cdo.selname(args.var, options = "-f nc",input=subreg+mask_reg+ifile,output=ofile)
        
#Main controling function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("var", help="The diagnostic variable to look at as named in HadGEM3-N216 directory structure")
    parser.add_argument("freq", help="The data frequency to extract from monthly (Amon) or daily (day)")
    parser.add_argument("--subregion", default="", help="The sub region of interest as lon1,lon2,lat1,lat2")
    parser.add_argument("--mask", default="", help="Mask data to the specified shapefile")
    parser.add_argument("--ddir", default="/group_workspaces/jasmin4/cssp_china/wp1/HadGEM3-A-N216/", help="The full path to the top level HadGEM3-N216 data directory")
    parser.add_argument("--odir", default="", help="The directory to store the output files in")
    
    args = parser.parse_args()
    for expt in expts:
	print expt
        process_data(args,expt)
   
    print "Finished!"

#Washerboard function that allows main() to run on running this file
if __name__=="__main__":
  main()
