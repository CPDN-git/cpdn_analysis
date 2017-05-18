
#!/bin/bash
#set -x

#------------------------------------------------------------------------------------------------------
# DOWNLOAD AND FILTERING SCRIPT FOR WAH BATCHES
#------------------------------------------------------------------------------------------------------

clim=1
batch=000
project="wwa"
domain="SAS50"
experiment="GHGONLYCLIM"
sampleclim=200
#lon1=-16 ; lon2=68  ; lat1=3   ; lat2=47  ; regdom=0 ; remapgrid="r1440x720" # DUB25
lon1=12  ; lon2=126 ; lat1=-22 ; lat2=53  ; regdom=1 ; remapgrid="r720x360"  # SAS50

#------------------------------------------------------------------------------------------------------

home="/ouce-home/projects/weather_attribution/batch"$batch

#------------------------------------------------------------------------------------------------------
# SELECT THE VARIABLES YOU WANT TO EXTRACT
#------------------------------------------------------------------------------------------------------

select=( "PRCP" "TPMN" "T850" "U200" "MSLP" "U10M" "V10M" ) # GLOBAL DOMAIN
#select=( "T850" ) # GLOBAL DOMAIN
for choice in "${select[@]}" ; do dir_out=$home"/"$choice"_GLOBL" ; mkdir $dir_out
rm $home"/check_download_b"$batch"_"$choice"_GLOBL.out" ; done

select_regional=( "PRCP" "TMAX" "TMIN" "MSLP" ) # REGIONAL DOMAIN
#select_regional=( "MSLP" ) # REGIONAL DOMAIN
for choice in "${select_regional[@]}" ; do dir_out=$home"/"$choice"_"$domain ; mkdir $dir_out
rm $home"/check_download_b"$batch"_"$choice"_"$domain".out" ; done

#------------------------------------------------------------------------------------------------------
# SELECT THE CORRECT DOWNLOAD URL
#------------------------------------------------------------------------------------------------------

#model="hadam3p_eu"
BATCH_LIST_URL="http://upload2.cpdn.org/project_results/"$project"/batch_"$batch"/batch_"$batch".txt.gz"
#BATCH_LIST_URL="http://upload2.cpdn.org/results/batch_"$batch"/batch_"$batch".txt.gz"
#BATCH_LIST_URL="http://upload2.cpdn.org/results/"$model"/batch"$batch"/batch"$batch".txt.gz"

rm "batch_"$batch".txt" ; wget $BATCH_LIST_URL ; gunzip "batch_"$batch".txt.gz"
mv "batch_"$batch".txt" "batch_"$batch"_new.txt"
#rm "batch_387.txt" ; cp "/gpfs/projects/cpdn/storage/boinc/upload/batch_387/batch_387.txt.gz" . ; gunzip "batch_387.txt.gz"
#sed -e "s/http:\/\/upload2.cpdn.org\/results/\/gpfs\/projects\/cpdn\/storage\/boinc\/upload/g" "batch_387.txt" > "batch_387_new.txt"
#rm "batch_387.txt" ; cp "/gpfs/projects/cpdn/storage/boinc/project_results/wwa/batch_387/batch_387.txt.gz" . ; gunzip "batch_387.txt.gz"
#sed -e "s/http:\/\/upload2.cpdn.org/\/gpfs\/projects\/cpdn\/storage\/boinc/g" "batch_387.txt" > "batch_387_new.txt"

#------------------------------------------------------------------------------------------------------
# LOOP OVER YEARS AND MONTHS
#------------------------------------------------------------------------------------------------------

YEAR0=1986
YEARE=2015

let YEAR1=$YEAR0 ; let scnt=$sampleclim+20
while [[ $YEAR0 -le $YEARE ]] ; do echo "YEAR " $YEAR0
let year=$YEAR0 ; year=`printf "%.4d" $year` ; let yyyy=$YEAR0-1

#------------------------------------------------------------------------------------------------------

MTH0=1
MTHE=12

let MTH1=$MTH0 ; mm1=`printf "%.2d" $MTH1`
let nne=($MTHE-$MTH1+1)*1 ; let mme=($MTHE-$MTH1+1)*30
let yye=($YEARE-$YEAR1+1)*1 ; let yyye=$nne*$yye
while [[ $MTH0 -le $MTHE ]] ; do echo "MONTH " $MTH0
let mm=$MTH0 ; mm=`printf "%.2d" $mm` ; let mth=$MTH0+1

#------------------------------------------------------------------------------------------------------

cd $home

grep "_"$mth".zip" "batch_"$batch"_new.txt" > "batch_"$batch"_"$mm".txt"
grep "_"$yyyy"12_" "batch_"$batch"_"$mm".txt" > "batch_"$batch"_"$year$mm".txt"
#sed -i '2100,10000d' "batch_"$batch"_"$year$mm".txt"

#------------------------------------------------------------------------------------------------------
# DOWNLOAD
#------------------------------------------------------------------------------------------------------

while read inputfile ; do

wget $inputfile
name=`echo "$inputfile" | rev | cut -d \/ -f 1 | rev`
umid=`echo "$name" | cut -d \_ -f 3`

echo ' ' ; echo $name ; echo ' '
rm *".nc" ; rm *.day ; unzip $name
rm $name ; rm xa* ; rm $umid"ga.pe"*".nc"

#-----------------------------------------------------------------------------------------------------
for choice in "${select[@]}" ; do # GLOBAL DOMAIN
#-----------------------------------------------------------------------------------------------------

if [[ $choice == PRCP ]] ; then field="field90" ; fldnr=5216  ; tconv="mean" ; ts=30 ; qmax=2000   ; qmin=0     ; fr=86400 ; fi
if [[ $choice == TPMN ]] ; then field="field16" ; fldnr=3236  ; tconv="mean" ; ts=1  ; qmax=400    ; qmin=100   ; fr=1     ; fi
if [[ $choice == T850 ]] ; then field="field16" ; fldnr=16203 ; tconv="mean" ; ts=1  ; qmax=400    ; qmin=100   ; fr=1     ; level=850 ; fi
if [[ $choice == U200 ]] ; then field="field56" ; fldnr=15201 ; tconv="mean" ; ts=1  ; qmax=200    ; qmin=-150  ; fr=1     ; level=200 ; fi
if [[ $choice == MSLP ]] ; then field="field8"  ; fldnr=16222 ; tconv="mean" ; ts=30 ; qmax=120000 ; qmin=80000 ; fr=1     ; fi
if [[ $choice == U10M ]] ; then field="field56" ; fldnr=3225  ; tconv="mean" ; ts=1  ; qmax=100    ; qmin=-90   ; fr=1     ; fi
if [[ $choice == V10M ]] ; then field="field57" ; fldnr=3226  ; tconv="mean" ; ts=1  ; qmax=90     ; qmin=-80   ; fr=1     ; fi

if [[ $ts -eq 1 ]]  ; then tempres="mthly" ; nhours=720 ; elif [[ $ts -eq 30 ]] ; then tempres="daily" ; nhours=24 ; fi
dir_out=$home"/"$choice"_GLOBL" ; nr=0
file_out="WAH_"$choice"_b"$batch"_"$experiment"_global_"$umid"_"$year$mm"_"$tempres".nc" ; rm $dir_out/$file_out

#-----------------------------------------------------------------------------------------------------

name_item=$field":stash_item" ; name_section=$field":stash_section"
name_method=$field":cell_method" ; name_time=$field"("
item=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_item` | cut -d \" -f 2)
section=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_section` | cut -d \" -f 2)
method=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_method` | cut -d \" -f 2 | rev | cut -d' ' -f 2 | rev)
tstep=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 1 | rev | cut -d \( -f 1 | rev)
code=$section$item ; mn_period=$tstep":meaning_period"
tperiod=$(ncdump -h $umid"ma.pc"*".nc" |  grep `echo $mn_period` | cut -d \" -f 2 | cut -d' ' -f 1)
if [[ $code -eq $fldnr && $method == $tconv && $tperiod -eq $nhours ]] ; then echo "FILE OK"
timcode=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 1 | rev | cut -d \( -f 1 | rev)
levcode=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 2)
latcode=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 3)
loncode=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 4 | cut -d \) -f 1)
name_field=$field ; else echo "CONTINUE"
nr=1 ; while [[ $nr -lt 20 ]] ; do
name_item=$field"_"$nr":stash_item" ; name_section=$field"_"$nr":stash_section"
name_method=$field"_"$nr":cell_method" ; name_time=$field"_"$nr"("
item=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_item` | cut -d \" -f 2)
section=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_section` | cut -d \" -f 2)
method=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_method` | cut -d \" -f 2 | rev | cut -d' ' -f 2 | rev)
tstep=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 1 | rev | cut -d \( -f 1 | rev)
code=$section$item ; mn_period=$tstep":meaning_period"
tperiod=$(ncdump -h $umid"ma.pc"*".nc" |  grep `echo $mn_period` | cut -d \" -f 2 | cut -d' ' -f 1)
if [[ $code -eq $fldnr && $method == $tconv && $tperiod -eq $nhours ]] ; then echo "FILE OK"
timcode=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 1 | rev | cut -d \( -f 1 | rev)
levcode=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 2)
latcode=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 3)
loncode=$(ncdump -h $umid"ma.pc"*".nc" | grep `echo $name_time` | cut -d \, -f 4 | cut -d \) -f 1)
name_field=$field"_"$nr ; else echo "IGNORE" ; fi
let nr=nr+1 ; done ; fi

#-----------------------------------------------------------------------------------------------------

ncrename -d $timcode,time -v $timcode,time -d $latcode,lat -v $latcode,lat -d $loncode,lon -v $loncode,lon $umid"ma.pc"*".nc" tmp1.nc
ncks -v $name_field tmp1.nc tmp2.nc ; if [[ $choice == T850 || $choice == U200 ]] ; then
cdo -setvrange,$qmin,$qmax -mulc,$fr -chname,$name_field,$choice -sellevel,$level -selvar,$name_field tmp2.nc tmp3.nc ; else
cdo -setvrange,$qmin,$qmax -mulc,$fr -chname,$name_field,$choice -selvar,$name_field tmp2.nc tmp3.nc ; fi
ncwa -a $levcode tmp3.nc tmp4.nc ; name_var=$choice
cdo -timmax -fldmax -gtc,$qmax tmp4.nc tmp5.nc ; cdo -timmax -fldmax -ltc,$qmin tmp4.nc tmp6.nc
FAIL1=$(ncdump tmp5.nc | grep -A 1 `echo $name_var` | tail -n 1 | cut -d \; -f 1 | sed -e 's/[eE]+*/\*10\^/' )
FAIL2=$(ncdump tmp6.nc | grep -A 1 `echo $name_var` | tail -n 1 | cut -d \; -f 1 | sed -e 's/[eE]+*/\*10\^/' )
TIME0=$(cdo -sinfo tmp4.nc | grep "Time coordinate" | rev | cut -d \: -f 1 | rev | cut -b 3-5 | cut -d' ' -f 1 )

if [[ $FAIL1 -eq 1 || $FAIL2 -eq 1 || $TIME0 -ne $ts ]] ; then echo "FAIL: "$umid"ma.pc"*".nc"
echo "FILE: $umid"ma.pc"*".nc" FAILED" >> $home"/check_download_b"$batch"_"$choice"_GLOBL.out" ; else
cdo -a -seldate,$year"-"$mm"-01",$year"-"$mm"-30" tmp4.nc $dir_out/$file_out

if [[ $ts -eq 30 ]] ; then NAME=`echo "$file_out" | cut -d \_ -f 1-7` # MAKE MONTHLY
rm $NAME"_mthly.nc" ; cdo -monmean $dir_out/$file_out $dir_out/$NAME"_mthly.nc" ; fi

fi ; rm "tmp"?".nc"

#-----------------------------------------------------------------------------------------------------
done ; rm $umid"ma.pc"*".nc" # END GLOBAL DOMAIN
#-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
for choice in "${select_regional[@]}" ; do # REGIONAL DOMAIN
#-----------------------------------------------------------------------------------------------------

if [[ $choice == PRCP ]] ; then field="field90" ; fldnr=5216  ; tconv="mean"    ; ts=30 ; qmax=2000   ; qmin=0     ; fr=86400 ; fi
if [[ $choice == TMAX ]] ; then field="field16" ; fldnr=3236  ; tconv="maximum" ; ts=30 ; qmax=400    ; qmin=100   ; fr=1     ; fi
if [[ $choice == TMIN ]] ; then field="field16" ; fldnr=3236  ; tconv="minimum" ; ts=30 ; qmax=400    ; qmin=100   ; fr=1     ; fi
if [[ $choice == MSLP ]] ; then field="field8"  ; fldnr=16222 ; tconv="mean"    ; ts=30 ; qmax=120000 ; qmin=80000 ; fr=1     ; fi

if [[ $ts -eq 1 ]]  ; then tempres="mthly" ; nhours=720 ; elif [[ $ts -eq 30 ]] ; then tempres="daily" ; nhours=24 ; fi
dir_out=$home"/"$choice"_"$domain ; nr=0
file_out="WAH_"$choice"_b"$batch"_"$experiment"_"$domain"_"$umid"_"$year$mm"_"$tempres".nc" ; rm $dir_out/$file_out

#-----------------------------------------------------------------------------------------------------

name_item=$field":stash_item" ; name_section=$field":stash_section"
name_method=$field":cell_method" ; name_time=$field"("
item=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_item` | cut -d \" -f 2)
section=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_section` | cut -d \" -f 2)
method=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_method` | cut -d \" -f 2 | rev | cut -d' ' -f 2 | rev)
tstep=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 1 | rev | cut -d \( -f 1 | rev)
code=$section$item ; mn_period=$tstep":meaning_period"
tperiod=$(ncdump -h $umid"ga.pd"*".nc" |  grep `echo $mn_period` | cut -d \" -f 2 | cut -d' ' -f 1)
if [[ $code -eq $fldnr && $method == $tconv && $tperiod -eq $nhours ]] ; then echo "FILE OK"
timcode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 1 | rev | cut -d \( -f 1 | rev)
levcode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 2)
latcode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 3)
loncode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 4 | cut -d \) -f 1)
name_field=$field ; else echo "CONTINUE"
nr=1 ; while [[ $nr -lt 2 ]] ; do
name_item=$field"_"$nr":stash_item" ; name_section=$field"_"$nr":stash_section"
name_method=$field"_"$nr":cell_method" ; name_time=$field"_"$nr"("
item=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_item` | cut -d \" -f 2)
section=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_section` | cut -d \" -f 2)
method=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_method` | cut -d \" -f 2 | rev | cut -d' ' -f 2 | rev)
tstep=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 1 | rev | cut -d \( -f 1 | rev)
code=$section$item ; mn_period=$tstep":meaning_period"
tperiod=$(ncdump -h $umid"ga.pd"*".nc" |  grep `echo $mn_period` | cut -d \" -f 2 | cut -d' ' -f 1)
if [[ $code -eq $fldnr && $method == $tconv && $tperiod -eq $nhours ]] ; then echo "FILE OK"
timcode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 1 | rev | cut -d \( -f 1 | rev)
levcode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 2)
latcode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 3)
loncode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_time` | cut -d \, -f 4 | cut -d \) -f 1)
name_field=$field"_"$nr ; else echo "IGNORE" ; fi
let nr=nr+1 ; done ; fi

name_grid=$name_field":grid_mapping" ; name_rot=$name_field":coordinates"
rotcode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_grid` | cut -d \" -f 2)
glatcode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_rot` | cut -d \" -f 2 | cut -d' ' -f 1)
gloncode=$(ncdump -h $umid"ga.pd"*".nc" | grep `echo $name_rot` | cut -d \" -f 2 | rev | cut -d' ' -f 1 | rev)

#-----------------------------------------------------------------------------------------------------

ncrename -d $timcode,time -v $timcode,time -d $latcode,lat -v $latcode,lat -d $loncode,lon -v $loncode,lon $umid"ga.pd"*".nc" tmp1.nc
if [[ $regdom -eq 1 ]] ; then ncks -C -v time,$name_field,lat,lon,$glatcode,$gloncode,$rotcode tmp1.nc tmp2.nc ; fi
if [[ $regdom -eq 0 ]] ; then ncks -C -v time,$name_field,lat,lon tmp1.nc tmp2.nc ; fi ; if [[ $choice == PRCP ]] ; then
cdo -setmisstoc,0 -setvrange,$qmin,$qmax -mulc,$fr -chname,$name_field,$choice -selvar,$name_field tmp2.nc tmp4.nc ; else
cdo -setvrange,$qmin,$qmax -mulc,$fr -chname,$name_field,$choice -selvar,$name_field tmp2.nc tmp4.nc ; fi ; name_var=$choice
cdo -timmax -fldmax -gtc,$qmax tmp4.nc tmp5.nc ; cdo -timmax -fldmax -ltc,$qmin tmp4.nc tmp6.nc
FAIL1=$(ncdump tmp5.nc | grep -A 1 `echo $name_var` | tail -n 1 | cut -d \; -f 1 | sed -e 's/[eE]+*/\*10\^/' )
FAIL2=$(ncdump tmp6.nc | grep -A 1 `echo $name_var` | tail -n 1 | cut -d \; -f 1 | sed -e 's/[eE]+*/\*10\^/' )
TIME0=$(cdo -sinfo tmp4.nc | grep "Time coordinate" | rev | cut -d \: -f 1 | rev | cut -b 3-5 | cut -d' ' -f 1 )

if [[ $FAIL1 -eq 1 || $FAIL2 -eq 1 || $TIME0 -ne $ts ]] ; then echo "FAIL: "$umid"ga.pd"*".nc"
echo "FILE: $umid"ga.pd"*".nc" FAILED" >> $home"/check_download_b"$batch"_"$choice"_"$domain".out" ; else
cdo -a -sellonlatbox,$lon1,$lon2,$lat1,$lat2 -remapbil,$remapgrid -seldate,$year"-"$mm"-01",$year"-"$mm"-30" tmp4.nc $dir_out/$file_out
fi ; rm "tmp"?".nc"

#-----------------------------------------------------------------------------------------------------
done ; rm $umid"ga.pd"*".nc" # END REGIONAL DOMAIN
#-----------------------------------------------------------------------------------------------------

done < "batch_"$batch"_"$year$mm".txt"

#------------------------------------------------------------------------------------------------------

let MTH0=$MTH0+1
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

