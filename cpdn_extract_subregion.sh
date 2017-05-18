
#!/bin/bash

#----------------------------------------------------------

home="/ouce-home/projects/weather_attribution/batchA09/subregion"

#----------------------------------------------------------
# MAKE ONE FILE
#----------------------------------------------------------

cd $home

for FILE in `ls "WAH_PRCP_a009_CLIM_ACT_AFR50_"????"01_"????"12_daily_120mem_12monthly.nc"` ; do
date=`echo "$FILE" | cut -d \_ -f 7 | cut -b 1-4` ; newname="WAH_"$date"_tmp.nc"
cdo -fldmean -sellonlatbox,38,43,8,13 $FILE $newname ; done

FILEOUT=$home"/WAH_PRCP_a009_CLIM_ACT_Ethiopia_198701_200912_daily_120mem_276monthly_fldmean.nc"
rm $FILEOUT ; cdo -mergetime "WAH_"????"_tmp.nc" tmp.nc
cdo -settaxis,1987-01-01,00:00,1day tmp.nc $FILEOUT ; rm "WAH_"????"_tmp.nc" ; rm tmp.nc

#----------------------------------------------------------
# EXTRACT ENSO YEARS
#----------------------------------------------------------

cd $home

FILEIN="WAH_PRCP_a009_CLIM_ACT_Ethiopia_198701_200912_daily_120mem_276monthly_fldmean.nc"
rm "WAH_PRCP_a009_CLIM_ACT_Ethiopia_198701_200912_daily_120mem_276monthly_fldmean_ElNino.nc"
cdo -seldate,1994-09-01,1995-08-31 $FILEIN en1.nc
cdo -seldate,1997-09-01,1998-08-31 $FILEIN en2.nc
cdo -seldate,2002-09-01,2003-08-31 $FILEIN en3.nc
#cdo -seldate,2009-09-01,2010-08-31 $FILEIN en4.nc
cdo -mergetime "en"?".nc" "WAH_PRCP_a009_CLIM_ACT_Ethiopia_198701_200912_daily_120mem_276monthly_fldmean_ElNino.nc"
rm "WAH_PRCP_a009_CLIM_ACT_Ethiopia_198701_200912_daily_120mem_276monthly_fldmean_LaNina.nc"
cdo -seldate,1988-09-01,1989-08-31 $FILEIN la1.nc
cdo -seldate,1998-09-01,1999-08-31 $FILEIN la2.nc
cdo -seldate,2007-09-01,2008-08-31 $FILEIN la3.nc
#cdo -seldate,2010-09-01,2011-08-31 $FILEIN la4.nc
cdo -mergetime "la"?".nc" "WAH_PRCP_a009_CLIM_ACT_Ethiopia_198701_200912_daily_120mem_276monthly_fldmean_LaNina.nc"
rm "en"?".nc" ; rm "la"?".nc"

#----------------------------------------------------------
exit
#----------------------------------------------------------

