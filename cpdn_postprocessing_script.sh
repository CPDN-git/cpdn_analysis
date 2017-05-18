
#!/bin/bash
#set -x

#------------------------------------------------------------------------------------------------------
# DOWNLOAD AND FILTERING SCRIPT FOR WAH BATCHES
#------------------------------------------------------------------------------------------------------

clim=1                     # 1 for climatology and 0 for standard output
batch=000                  # Batch number
project="wwa"              # Project name for extraction directory
domain="SAS50"             # Domain name of your choice
experiment="GHGONLYCLIM"   # Name of experiment
sampleclim=200             # Ensemble size for annual climatology output

#------------------------------------------------------------------------------------------------------
# SELECT REGIONAL DOMAIN AND CHOSE RESOLUTION THAT APPROXIMATELY FITS GRID SPACING
#------------------------------------------------------------------------------------------------------

#lon1=-16 ; lon2=68  ; lat1=3   ; lat2=47  ; regdom=0 ; remapgrid="r1440x720" # DUB25
lon1=12  ; lon2=126 ; lat1=-22 ; lat2=53  ; regdom=1 ; remapgrid="r720x360"  # SAS50

#------------------------------------------------------------------------------------------------------

home="/ouce-home/projects/weather_attribution/batch"$batch

#------------------------------------------------------------------------------------------------------
# SELECT THE VARIABLES YOU WANT TO PROCESS
# MAKE SURE THE ONES YOU HAVE EXTRACTED THEM BEFORE
#------------------------------------------------------------------------------------------------------

select=( "PRCP" "TPMN" "T850" "U200" "MSLP" "U10M" "V10M" ) # GLOBAL DOMAIN
#select=( "T850" ) # GLOBAL DOMAIN
for choice in "${select[@]}" ; do dir_out=$home"/"$choice"_GLOBL" ; done

select_regional=( "PRCP" "TMAX" "TMIN" "MSLP" ) # REGIONAL DOMAIN
#select_regional=( "MSLP" ) # REGIONAL DOMAIN
for choice in "${select_regional[@]}" ; do dir_out=$home"/"$choice"_"$domain ; done

#------------------------------------------------------------------------------------------------------
# LOOP OVER YEARS AND MONTHS
#------------------------------------------------------------------------------------------------------

YEAR0=1986 # Start year and end year as in the output (runs should start in December the year before)
YEARE=2015 # End year (in case of standard runs, end year equals start year)

let YEAR1=$YEAR0 ; let scnt=$sampleclim+20
while [[ $YEAR0 -le $YEARE ]] ; do echo "YEAR " $YEAR0
let year=$YEAR0 ; year=`printf "%.4d" $year` ; let yyyy=$YEAR0-1

#------------------------------------------------------------------------------------------------------

MTH0=1     # Start month which should be January in case of Climatology
MTHE=12    # End month which should be December in case of Climatology

let MTH1=$MTH0 ; mm1=`printf "%.2d" $MTH1`
let nne=($MTHE-$MTH1+1)*1 ; let mme=($MTHE-$MTH1+1)*30
let yye=($YEARE-$YEAR1+1)*1 ; let yyye=$nne*$yye
while [[ $MTH0 -le $MTHE ]] ; do echo "MONTH " $MTH0
let mm=$MTH0 ; mm=`printf "%.2d" $mm` ; let mth=$MTH0+1
cd $home ; let MTH0=$MTH0+1
done

#------------------------------------------------------------------------------------------------------
# MAKE ANNUAL GLOBAL FILE (SINGLE YEAR OR CLIMATOLOGY)
#------------------------------------------------------------------------------------------------------

for choice in "${select[@]}" ; do dir_out=$home"/"$choice"_GLOBL" ; cd $dir_out

if [[ $clim -eq 0 ]] ; then
for file in `ls "WAH_"$choice"_b"$batch"_"$experiment"_global_"????"_"$year$mm1"_mthly.nc" ` ; do
UMID=`echo "$file" | cut -d \_ -f 6` ; rm "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$year"_"$mm"monthly.nc"
cdo -mergetime "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$year??"_mthly.nc" "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$year"_"$mm"monthly.nc"
filter=$(cdo -info "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$year"_"$mm"monthly.nc" | tail -n 1 | cut -d \: -f 1 | cut -b 4-6)
if [[ $filter -ne $nne ]] ; then rm "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$year"_"$mm"monthly.nc" ; fi ; done

rm $home"/WAH_"$choice"_b"$batch"_"$experiment"_global_"$year$mm1"_"$year$mm"_mthly_all_"$mm"monthly.nc"
ncecat `ls "WAH_"$choice"_b"$batch"_"$experiment"_global_"????"_"$year"_"$mm"monthly.nc"` tmp1.nc ; ncpdq -a time,record tmp1.nc tmp2.nc
cdo -a -seldate,$year"-"$mm1"-01",$year"-"$mm"-31" tmp2.nc $home"/WAH_"$choice"_b"$batch"_"$experiment"_global_"$year$mm1"_"$year$mm"_mthly_all_"$mm"monthly.nc"
chmod 755 $home"/WAH_"$choice"_b"$batch"_"$experiment"_global_"$year$mm1"_"$year$mm"_mthly_all_"$mm"monthly.nc" ; rm "tmp"?".nc"
fi

#------------------------------------------------------------------------------------------------------

if [[ $clim -eq 1 ]] ; then count=0
for file in `ls "WAH_"$choice"_b"$batch"_"$experiment"_global_"????"_"$year$mm1"_mthly.nc" | sort -R | head -"$scnt"` ; do
UMID=`echo "$file" | cut -d \_ -f 6` ; let count=$count+1 ; MEM=`printf "%.3d" $count`
cdo -mergetime "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$year??"_mthly.nc" "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$MEM"_"$year"_"$mm"monthly.nc"
filter=$(cdo -info "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$MEM"_"$year"_"$mm"monthly.nc" | tail -n 1 | cut -d \: -f 1 | cut -b 4-6)
if [[ $filter -ne $nne ]] ; then rm "WAH_"$choice"_b"$batch"_"$experiment"_global_"$UMID"_"$MEM"_"$year"_"$mm"monthly.nc" ; let count=$count-1 ; fi
done ; fi

done

#------------------------------------------------------------------------------------------------------
# MAKE ANNUAL REGIONAL FILE (SINGLE YEAR OR CLIMATOLOGY)
#------------------------------------------------------------------------------------------------------

for choice in "${select_regional[@]}" ; do dir_out=$home"/"$choice"_"$domain ; cd $dir_out

for file in `ls "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"????"_"$year$mm1"_daily.nc" ` ; do
UMID=`echo "$file" | cut -d \_ -f 6` ; rm "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"$UMID"_"$year"_daily_"$mm"monthly.nc"
cdo -mergetime "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"$UMID"_"$year??"_daily.nc" "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"$UMID"_"$year"_daily_"$mm"monthly.nc"
filter=$(cdo -info "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"$UMID"_"$year"_daily_"$mm"monthly.nc" | tail -n 1 | cut -d \: -f 1 | cut -b 4-6)
if [[ $filter -ne $mme ]] ; then rm "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"$UMID"_"$year"_daily_"$mm"monthly.nc" ; fi ; done

filenumber=`ls "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"????"_"$year"_daily_"$mm"monthly.nc" | wc -l`

if [[ $clim -eq 0 ]] ; then sample=250 ; let samplecount=$filenumber/$sample ; cnt=0
for ((n=1; n<=$samplecount; n++)) ; do nr=`printf "%.2d" $n` ; let cnt=$cnt+$sample
file_out=$home"/WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"$year$mm1"_"$year$mm"_daily_"$sample"mem_"$nr"_"$mm"monthly.nc"
rm $file_out ; ncecat `ls "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"????"_"$year"_daily_"$mm"monthly.nc" | head -"$cnt" | tail -"$sample"` tmp1.nc
ncpdq -a time,record tmp1.nc tmp2.nc ; cdo -a -seldate,$year"-"$mm1"-01",$year"-"$mm"-31" tmp2.nc $file_out ; rm "tmp"?".nc"
done ; fi

#------------------------------------------------------------------------------------------------------

if [[ $clim -eq 1 ]] ; then sample=$sampleclim ; sample=`printf "%.3d" $sample`
file_out=$home"/WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"$year$mm1"_"$year$mm"_daily_"$sample"mem_"$mm"monthly.nc"
rm $file_out ; ncecat `ls "WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"????"_"$year"_daily_"$mm"monthly.nc" | tail -"$sample"` tmp1.nc
ncpdq -a time,record tmp1.nc tmp2.nc ; cdo -a -seldate,$year"-"$mm1"-01",$year"-"$mm"-31" tmp2.nc $file_out ; rm "tmp"?".nc"
fi

done

#------------------------------------------------------------------------------------------------------

let YEAR0=$YEAR0+1
done

#------------------------------------------------------------------------------------------------------
# FINALIZE ANNUAL GLOBAL CLIMATOLOGY FILE
#------------------------------------------------------------------------------------------------------

if [[ $clim -eq 1 ]] ; then
for choice in "${select[@]}" ; do dir_out=$home"/"$choice"_GLOBL" ; cd $dir_out

count=$sampleclim ; let countmore=$count+10 ; ensmem=`printf "%.3d" $count`
for ((n=1; n<=$countmore; n++)) ; do MEM=`printf "%.3d" $n` ; rm $choice"_"$MEM"_allmonth_allyear.nc"
cdo -mergetime "WAH_"$choice"_b"$batch"_"$experiment"_global_"????"_"$MEM"_"????"_"$mm"monthly.nc" $choice"_"$MEM"_allmonth_allyear.nc"
filter=$(cdo -info $choice"_"$MEM"_allmonth_allyear.nc" | tail -n 1 | cut -d \: -f 1 | cut -b 4-6)
if [[ $filter -ne $yyye ]] ; then rm $choice"_"$MEM"_allmonth_allyear.nc" ; fi ; done

rm $home"/WAH_"$choice"_b"$batch"_"$experiment"_global_"$YEAR1"01_"$YEARE"12_mthly_"$ensmem"mem_"$yyye"monthly.nc"
ncecat `ls $choice"_"???"_allmonth_allyear.nc" | head -$count` tmp1.nc ; ncpdq -a time,record tmp1.nc tmp2.nc
cdo -a -seldate,$YEAR1"-"$mm1"-01",$YEARE"-"$mm"-31" tmp2.nc $home"/WAH_"$choice"_b"$batch"_"$experiment"_global_"$YEAR1$mm1"_"$YEARE$mm"_mthly_"$ensmem"mem_"$yyye"monthly.nc"
rm $choice"_"???"_allmonth_allyear.nc" ; rm "tmp"?".nc"
done ; fi

#------------------------------------------------------------------------------------------------------
exit
#------------------------------------------------------------------------------------------------------

