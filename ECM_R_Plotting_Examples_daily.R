
#--------------------------------------------------------------------------------------------------------

#install.packages("ncdf4")

library("stringr")
library("caTools")
library("plotrix")
library("scales")
library("RNetCDF")
library("ncdf4")
library("forecast")
library("grDevices")
library("ggplot2")
library("ismev")
library("vioplot")
library("base")

#--------------------------------------------------------------------------------------------------------

remote="/ouce-home/projects/weather_attribution/batchA09/subregion/"

#--------------------------------------------------------------------------------------------------------
# ANNUAL CYCLE DAILY
#--------------------------------------------------------------------------------------------------------

# read in file for model data
# you may want to check the dimension size by typing dim(time0) or dim(outp0)
# the first file is a vector and the second file a matrix with dimensions for ensemble member and time
nc.file <- open.nc(paste(remote,"WAH_PRCP_a009_CLIM_ACT_Ethiopia_198701_200912_daily_120mem_276monthly_fldmean.nc",sep=""))
time0 <- var.get.nc(nc.file,"time")
outp0 <- var.get.nc(nc.file,"PRCP") * 86400
close.nc(nc.file)
# date conversion for model data
year0 = as.numeric(substr(time0,1,4))
mth0 = (as.numeric(substr(time0,5,6)) - 1) / 12
month0 = as.numeric(substr(time0,5,6))
day0 = (as.numeric(substr(time0,7,8)) -1) / 30 * (1/12)
dayth0 = as.numeric(substr(time0,7,8)) + (( month0 - 1 ) * 30 )
date0 = year0 + mth0 + day0
# make mean and percentiles for model data
end = length(outp0[,1]) ; mean0 = 0 ; lower0 = 0 ; upper0 = 0 ; for ( a in 1:360 ) {
lower0[a] = quantile(outp0[1:end,(dayth0)==a], c(.10,.90))[[1]]
upper0[a] = quantile(outp0[1:end,(dayth0)==a], c(.10,.90))[[2]]
mean0[a] = mean(outp0[1:end,(dayth0)==a]) }
# generate time matrix equivalent to model data matrix
date00 = (1:360) ; date000 = t(replicate(end,date0))

#--------------------------------------------------------------------------------------------------------

# read in file for observational data
nc.file <- open.nc(paste(remote,"CHIRPS_PRCP_Ethiopia_198701_200912_daily_fldmean.nc",sep=""))
time2 <- round(var.get.nc(nc.file,"time"),0)
outp2 <- round(var.get.nc(nc.file,"PRCP"),4) ; outp2[is.na(outp2)] <- 0 ; outp2 = as.numeric(outp2)
close.nc(nc.file)
# kick out Februray 29 in observational data
yy2 = as.numeric(substr(time2,1,4)) ; mm2 = as.numeric(substr(time2,5,6)) ; dd2 = as.numeric(substr(time2,7,8))
time22 = time2[!mm2==2|!dd2==29]
# date conversion for observational data
year2 = as.numeric(substr(time22,1,4))
mth2 = (as.numeric(substr(time22,5,6)) - 1) / 12
month2 = as.numeric(substr(time22,5,6))
day2 = (as.numeric(substr(time22,7,8)) -1) / 31 * (1/12)
ddd = (1:365) ; dayth2 = as.vector(replicate(23,ddd))
date2 = year2 + mth2 + day2
# make mean and percentiles for observational data
mean2 = 0 ; lower2 = 0 ; upper2 = 0 ; for ( a in 1:365 ) {
lower2[a] = quantile(outp2[(dayth2)==a], c(.10,.90))[[1]]
upper2[a] = quantile(outp2[(dayth2)==a], c(.10,.90))[[2]]
mean2[a] = mean(outp2[(dayth2)==a]) }
# generate time values that match 360 day calendar
date22 = (1:365) * 360/365

#--------------------------------------------------------------------------------------------------------
# PLOTTING OF ANNUAL PRECIPITATION CYCLE
#--------------------------------------------------------------------------------------------------------

# dimensions of x (time) and y (precip data) axis 
tt_min=1
tt_max=360 
rr_min=0.0
rr_max=15.0
# labelling of x and y axis
taxis1 <- c("15","45","75","105","135","165","195","225","255","285","315","345")
taxis2 <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
raxis <- c("0","2","4","6","8","10","12","14","16","18","20","22","24","26")

# plot name and size
png(filename="PRCP_Ethiopia_198701_200912_allmember_daily.png",width = 1024, height = 768,bg = "white") ; par(mar=c(5,5,4,3))
# data plotting ("black" is model and "darkorchid" is observations)
plot(date00,mean0,type="n",cex=1.0,ylim=c(rr_min,rr_max),col="black",xlim=c(tt_min,tt_max),main="Daily Precipitation Climatology (1987-2009) - Ethiopia"
,xlab="Month",ylab="Daily precipitation [mm/day]",cex.lab=1.6,cex.axis=1.6,cex.main=2.2,xaxt="n",yaxt="n") ; par(new=T)
plot(date00,upper0,xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("black",0.6),xaxt="n",yaxt="n",xlab="",ylab="") ; par(new=T)
plot(date00,lower0,xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("black",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
polygon(c(date00,rev(date00)),c(lower0,rev(upper0)),col=alpha("black",0.2),border=NA) ; par(new=T)
plot(date22,upper2,xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("darkorchid",0.4),xaxt="n",yaxt="n",xlab="",ylab="") ; par(new=T)
plot(date22,lower2,xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("darkorchid",0.4),xaxt="n",yaxt="n",xlab="",ylab="")
polygon(c(date22,rev(date22)),c(lower2,rev(upper2)),col=alpha("darkorchid",0.1),border=NA) ; par(new=T)
par(new=T) ; plot(date00,mean0,type="l",lty=1,lwd=6.0,cex=1.4,ylim=c(rr_min,rr_max),col="black",xlim=c(tt_min,tt_max),xaxt="n",yaxt="n",xlab="",ylab="")
par(new=T) ; plot(date22,mean2,type="l",lty=1,lwd=4.0,cex=1.4,ylim=c(rr_min,rr_max),col="darkorchid",xlim=c(tt_min,tt_max),xaxt="n",yaxt="n",xlab="",ylab="")
# some dashed lines for better readibility and axis labelling
abline(h=raxis,col="grey66",lty=2,lwd=0.5) ; abline(v=taxis1,col="grey66",lty=2,lwd=0.5)
axis(1,at=taxis1,labels=taxis2,tick=TRUE,cex.axis=1.8) ; axis(2,at=raxis,labels=raxis,tick=TRUE,cex.axis=1.8,las=2)
# adding legend
lego1 = c("HadRM3P AFR50 (120 member; 10-90% percentile)","CHIRPS Observations (10-90% percentile)")
legcol1 = c("black","darkorchid") ; legend("topleft",lwd=2,col=legcol1,bty="n",cex=1.8,lego1)
# finish plotting (close plotting device)
dev.off()

#--------------------------------------------------------------------------------------------------------
# BOXPLOT (SEASONAL MAXIMUM OF PRECIPITATION)
#--------------------------------------------------------------------------------------------------------

# this is a bit more complicated than desirable, hence using CDO instead might be the better option
# seasonal max or mean for model and observational data (spring = MAM)
time1MAM = matrix(data=0,nrow=end,ncol=23) ; for ( i in 1:end) { for ( j in 1:23) { 
time1MAM[i,j] = mean(date000[i,(month0==3|month0==4|month0==5)&year0==(1986+j)]) }}
outp1MAM = matrix(data=0,nrow=end,ncol=23) ; for ( i in 1:end) { for ( j in 1:23) {
outp1MAM[i,j] = max(outp0[i,(month0==3|month0==4|month0==5)&year0==(1986+j)]) }}
time2MAM = 0 ; for ( j in 1:23) { time2MAM[j] = mean(date2[(month2==3|month2==4|month2==5)&year2==(1986+j)]) }
outp2MAM = 0 ; for ( j in 1:23) { outp2MAM[j] = max(outp2[(month2==3|month2==4|month2==5)&year2==(1986+j)]) }
time1MAM = floor(time1MAM) ; time2MAM = floor(time2MAM)

#--------------------------------------------------------------------------------------------------------

# seasonal max or mean for model and observational data (summer = JJA)
time1JJA = matrix(data=0,nrow=end,ncol=23) ; for ( i in 1:end) { for ( j in 1:23) {
time1JJA[i,j] = mean(date000[i,(month0==6|month0==7|month0==8)&year0==(1986+j)]) }}
outp1JJA = matrix(data=0,nrow=end,ncol=23) ; for ( i in 1:end) { for ( j in 1:23) {
outp1JJA[i,j] = max(outp0[i,(month0==6|month0==7|month0==8)&year0==(1986+j)]) }}
time2JJA = 0 ; for ( j in 1:23) { time2JJA[j] = mean(date2[(month2==6|month2==7|month2==8)&year2==(1986+j)]) }
outp2JJA = 0 ; for ( j in 1:23) { outp2JJA[j] = max(outp2[(month2==6|month2==7|month2==8)&year2==(1986+j)]) }
time1JJA = floor(time1JJA) ; time2JJA = floor(time2JJA)

#--------------------------------------------------------------------------------------------------------
# MAKE BOXPLOT FOR MAX OR MEAN SEASONAL PRECIPITATION
#--------------------------------------------------------------------------------------------------------

# labelling of x and y axis
taxis <- c("1986","1988","1990","1992","1994","1996","1998","2000","2002","2004","2006","2008","2010","2012","2014")
raxis <- c("0","2","4","6","8","10","12","14","16","18","20","22","24","26","28","30","32","34","36","38","40")

# dimensions of x (time) axis
tt_min=1986.5
tt_max=2009.5
# dimensions of y (precip data) axis for MAM case
rr_min=0
rr_max=24 # 6
# plotting of MAM data
png(filename="PRCP_Ethiopia_198701_200912_boxplot_MAM_daily_max.png",width = 1024, height = 768,bg = "white") ; par(mar=c(5,5,4,3))
boxplot(outp1MAM~time1MAM,ylim=c(rr_min,rr_max),col="grey77",axes=FALSE)
par(new=T) ; plot(time2MAM,outp2MAM,type="l",lty=1,lwd=3,cex=1.4,col="darkorange",ylim=c(rr_min,rr_max),xlim=c(tt_min,tt_max)
,xaxt="n",yaxt="n",xlab="",ylab="",main="Seasonal maximum of daily Precipitation: MAM - Ethiopia",cex.main=2.1)
axis(1,at=taxis,labels=taxis,tick=TRUE,cex.axis=1.8) ; axis(2,at=raxis,labels=raxis,tick=TRUE,cex.axis=1.8,las=2)
lego1 = c("HadRM3P (120 member)","CHIRPS (Observations)")
legcol1 = c("grey22","darkorange") ; legend("bottomright",lwd=2,col=legcol1,bty="n",cex=1.8,lego1)
dev.off()
# dimensions of y (precip data) axis for JJA case

#--------------------------------------------------------------------------------------------------------

rr_min=4  # 1
rr_max=28 # 7
# plotting of JJA data
png(filename="PRCP_Ethiopia_198701_200912_boxplot_JJA_daily_max.png",width = 1024, height = 768,bg = "white") ; par(mar=c(5,5,4,3))
boxplot(outp1JJA~time1JJA,ylim=c(rr_min,rr_max),col="grey77",axes=FALSE)
par(new=T) ; plot(time2JJA,outp2JJA,type="l",lty=1,lwd=3,cex=1.4,col="red",ylim=c(rr_min,rr_max),xlim=c(tt_min,tt_max)
,xaxt="n",yaxt="n",xlab="",ylab="",main="Seasonal maximum of daily Precipitation: JJA - Ethiopia",cex.main=2.1)
axis(1,at=taxis,labels=taxis,tick=TRUE,cex.axis=1.8) ; axis(2,at=raxis,labels=raxis,tick=TRUE,cex.axis=1.8,las=2)
lego1 = c("HadRM3P (120 member)","CHIRPS (Observations)")
legcol1 = c("grey22","red") ; legend("bottomright",lwd=2,col=legcol1,bty="n",cex=1.8,lego1)
dev.off()

#--------------------------------------------------------------------------------------------------------
# CALCULATION OF SEASONAL RETURN TIMES
#--------------------------------------------------------------------------------------------------------

# number of bootstraps
R = 1000
# convert matrix of seasonal maxima into vector
rr0_MAM = as.vector(outp1MAM) ; rr2_MAM = as.vector(outp2MAM)
rr0_JJA = as.vector(outp1JJA) ; rr2_JJA = as.vector(outp2JJA)

# sorting of model data MAM
xx0 <- length(rr0_MAM) ; rr_ranked0_MAM = 0 ; rr_time0_MAM = vector(mode='numeric',length=xx0)
for (kk in 1:xx0) { rr_time0_MAM[kk] <- xx0/(xx0-(kk-1)) } ; rr_ranked0_MAM <- sort(rr0_MAM)
# bootstrapping of model data MAM
boot.retrn <- array(dim=c(xx0,R)) ; outp = as.numeric(rr0_MAM[1:xx0])
for (i in 1:R) { boot.sample = as.numeric(sample(outp,xx0,replace=T))
boot.rank <- order(boot.sample) ; boot.retrn[,i] = as.numeric(boot.sample[boot.rank]) }
lower0_MAM = 0 ; upper0_MAM = 0 ; for (j in 1:xx0) {
lower0_MAM[j] = quantile(boot.retrn[j,], c(.05,.95))[[1]]
upper0_MAM[j] = quantile(boot.retrn[j,], c(.05,.95))[[2]] }

# sorting of observational data MAM
xx2 <- length(rr2_MAM) ; rr_ranked2_MAM = 0 ; rr_time2_MAM = vector(mode='numeric',length=xx2)
for (kk in 1:xx2) { rr_time2_MAM[kk] <- xx2/(xx2-(kk-1)) } ; rr_ranked2_MAM <- sort(rr2_MAM)
# bootstrapping of observational data MAM
boot.retrn <- array(dim=c(xx2,R)) ; outp = as.numeric(rr2_MAM[1:xx2])
for (i in 1:R) { boot.sample = as.numeric(sample(outp,xx2,replace=T))
boot.rank <- order(boot.sample) ; boot.retrn[,i] = as.numeric(boot.sample[boot.rank]) }
lower2_MAM = 0 ; upper2_MAM = 0 ; for (j in 1:xx2) {
lower2_MAM[j] = quantile(boot.retrn[j,], c(.05,.95))[[1]]
upper2_MAM[j] = quantile(boot.retrn[j,], c(.05,.95))[[2]] }

#--------------------------------------------------------------------------------------------------------

# sorting of model data JJA
xx0 <- length(rr0_JJA) ; rr_ranked0_JJA = 0 ; rr_time0_JJA = vector(mode='numeric',length=xx0)
for (kk in 1:xx0) { rr_time0_JJA[kk] <- xx0/(xx0-(kk-1)) } ; rr_ranked0_JJA <- sort(rr0_JJA)
# bootstrapping of model data JJA
boot.retrn <- array(dim=c(xx0,R)) ; outp = as.numeric(rr0_JJA[1:xx0])
for (i in 1:R) { boot.sample = as.numeric(sample(outp,xx0,replace=T))
boot.rank <- order(boot.sample) ; boot.retrn[,i] = as.numeric(boot.sample[boot.rank]) }
lower0_JJA = 0 ; upper0_JJA = 0 ; for (j in 1:xx0) {
lower0_JJA[j] = quantile(boot.retrn[j,], c(.05,.95))[[1]]
upper0_JJA[j] = quantile(boot.retrn[j,], c(.05,.95))[[2]] }

# sorting of observational data JJA
xx2 <- length(rr2_JJA) ; rr_ranked2_JJA = 0 ; rr_time2_JJA = vector(mode='numeric',length=xx2)
for (kk in 1:xx2) { rr_time2_JJA[kk] <- xx2/(xx2-(kk-1)) } ; rr_ranked2_JJA <- sort(rr2_JJA)
# bootstrapping of observational data JJA
boot.retrn <- array(dim=c(xx2,R)) ; outp = as.numeric(rr2_JJA[1:xx2])
for (i in 1:R) { boot.sample = as.numeric(sample(outp,xx2,replace=T))
boot.rank <- order(boot.sample) ; boot.retrn[,i] = as.numeric(boot.sample[boot.rank]) }
lower2_JJA = 0 ; upper2_JJA = 0 ; for (j in 1:xx2) {
lower2_JJA[j] = quantile(boot.retrn[j,], c(.05,.95))[[1]]
upper2_JJA[j] = quantile(boot.retrn[j,], c(.05,.95))[[2]] }

#--------------------------------------------------------------------------------------------------------
# PLOTTING OF SEASONAL RETURN TIMES
#--------------------------------------------------------------------------------------------------------

# labelling of x and y axis
taxis <- c("0.1","0.3","1","3","10","30","100","300","1000","3000")
raxis <- c("0","4","8","12","16","20","24","28","32","36","40")

# dimensions of x (time) axis
tt_min=3
tt_max=1000
# dimensions of y (precip data) axis for MAM case
rr_min=8
rr_max=36
# plot name and size
png(filename=paste("PRCP_Ethiopia_198701_200912_ReturnTimes_MAM_daily_max.png", sep=""),width = 1000, height = 800,bg = "white") ; par(mar=c(5,5,4,3))
# return time plotting ("black" is model and "red" is observations)
plot(rr_time0_MAM,rr_ranked0_MAM,type="l", pch=19,cex=0.2,ylim=c(rr_min,rr_max),log="x",col="grey85",xlim=c(tt_min,tt_max)
,main=paste("HadRM3P: Maximum seasonal MAM Rainfall Ethiopia",sep=""),xaxt="n",yaxt="n"
,xlab="Return period [years]",ylab="Maximum of Precipitation [mm/day]",cex.lab=1.8,cex.axis=1.8,cex.main=2.2)
par(new=T) ; plot(rr_time0_MAM,upper0_MAM,log="x",xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("black",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
par(new=T) ; plot(rr_time0_MAM,lower0_MAM,log="x",xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("black",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
polygon(c(rr_time0_MAM,rev(rr_time0_MAM)),c(lower0_MAM,rev(upper0_MAM)),col=alpha("black",0.2),border=NA)
par(new=T) ; plot(rr_time2_MAM,upper2_MAM,log="x",xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("red",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
par(new=T) ; plot(rr_time2_MAM,lower2_MAM,log="x",xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("red",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
polygon(c(rr_time2_MAM,rev(rr_time2_MAM)),c(lower2_MAM,rev(upper2_MAM)),col=alpha("red",0.2),border=NA)
par(new=T) ; plot(rr_time0_MAM,rr_ranked0_MAM,type="p",pch=19,cex=0.8,ylim=c(rr_min,rr_max),log="x",col="black",xlim=c(tt_min,tt_max),xaxt="n",yaxt="n",xlab="",ylab="")
par(new=T) ; plot(rr_time2_MAM,rr_ranked2_MAM,type="p",pch=19,cex=0.8,ylim=c(rr_min,rr_max),log="x",col="red",xlim=c(tt_min,tt_max),xaxt="n",yaxt="n",xlab="",ylab="")
# some dashed lines for better readibility and axis labelling
abline(h=raxis,col="grey55",lty=2,lwd=0.6) ; abline(v=taxis,col="grey55",lty=2,lwd=0.6) ; abline(h=c("0.0"),col="grey11",lty=1,lwd=0.6)
axis(1,at=taxis,labels=taxis,tick=TRUE,cex.axis=1.8) ; axis(2,at=raxis,labels=raxis,tick=TRUE,cex.axis=1.8,las=2)
# adding legend
lego1 = c("HadRM3P AFR50 Climatology (5-95% percentile)","CHIRPS Observations (5-95% percentile)")
legcol1 = c("black","red") ; legend("bottomright",lwd=2,col=legcol1,bty="n",cex=1.8,lego1)
# finish plotting (close plotting device)
dev.off()

#--------------------------------------------------------------------------------------------------------

# dimensions of y (precip data) axis for JJA case
rr_min=8
rr_max=36
# plot name and size
png(filename=paste("PRCP_Ethiopia_198701_200912_ReturnTimes_JJA_daily_max.png", sep=""),width = 1000, height = 800,bg = "white") ; par(mar=c(5,5,4,3))
# return time plotting ("black" is model and "red" is observations)
plot(rr_time0_JJA,rr_ranked0_JJA,type="l", pch=19,cex=0.2,ylim=c(rr_min,rr_max),log="x",col="grey85",xlim=c(tt_min,tt_max)
,main=paste("HadRM3P: Maximum seasonal JJA Rainfall Ethiopia",sep=""),xaxt="n",yaxt="n"
,xlab="Return period [years]",ylab="Maximum of Precipitation [mm/day]",cex.lab=1.8,cex.axis=1.8,cex.main=2.2)
par(new=T) ; plot(rr_time0_JJA,upper0_JJA,log="x",xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("black",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
par(new=T) ; plot(rr_time0_JJA,lower0_JJA,log="x",xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("black",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
polygon(c(rr_time0_JJA,rev(rr_time0_JJA)),c(lower0_JJA,rev(upper0_JJA)),col=alpha("black",0.2),border=NA)
par(new=T) ; plot(rr_time2_JJA,upper2_JJA,log="x",xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("red",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
par(new=T) ; plot(rr_time2_JJA,lower2_JJA,log="x",xlim=c(tt_min,tt_max),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("red",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
polygon(c(rr_time2_JJA,rev(rr_time2_JJA)),c(lower2_JJA,rev(upper2_JJA)),col=alpha("red",0.2),border=NA)
par(new=T) ; plot(rr_time0_JJA,rr_ranked0_JJA,type="p",pch=19,cex=0.8,ylim=c(rr_min,rr_max),log="x",col="black",xlim=c(tt_min,tt_max),xaxt="n",yaxt="n",xlab="",ylab="")
par(new=T) ; plot(rr_time2_JJA,rr_ranked2_JJA,type="p",pch=19,cex=0.8,ylim=c(rr_min,rr_max),log="x",col="red",xlim=c(tt_min,tt_max),xaxt="n",yaxt="n",xlab="",ylab="")
# some dashed lines for better readibility and axis labelling
abline(h=raxis,col="grey55",lty=2,lwd=0.6) ; abline(v=taxis,col="grey55",lty=2,lwd=0.6) ; abline(h=c("0.0"),col="grey11",lty=1,lwd=0.6)
axis(1,at=taxis,labels=taxis,tick=TRUE,cex.axis=1.8) ; axis(2,at=raxis,labels=raxis,tick=TRUE,cex.axis=1.8,las=2)
# adding legend
lego1 = c("HadRM3P AFR50 Climatology (5-95% percentile)","CHIRPS Observations (5-95% percentile)")
legcol1 = c("black","red") ; legend("bottomright",lwd=2,col=legcol1,bty="n",cex=1.8,lego1)
# finish plotting (close plotting device)
dev.off()

#--------------------------------------------------------------------------------------------------------
quit()
#--------------------------------------------------------------------------------------------------------







