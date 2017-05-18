
#--------------------------------------------------------------------------------------------------------

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
# ANNUAL CYCLE MONTHLY
#--------------------------------------------------------------------------------------------------------

nc.file <- open.nc(paste(remote,"WAH_PRCP_a009_CLIM_ACT_Ethiopia_198701_200912_daily_120mem_276monthly_fldmean_monmean.nc",sep=""))
time0 <- var.get.nc(nc.file,"time")
outp0 <- var.get.nc(nc.file,"PRCP") * 86400
close.nc(nc.file)
year0 = as.numeric(substr(time0,1,4))
mth0 = (as.numeric(substr(time0,5,6)) - 1) / 12
month0 = as.numeric(substr(time0,5,6))
date0 = year0 + mth0
end = length(outp0[,1]) ; mean0 = 0 ; lower0 = 0 ; upper0 = 0 ; for ( a in 1:12 ) {
lower0[a] = quantile(outp0[1:end,(month0)==a], c(.05,.95))[[1]]
upper0[a] = quantile(outp0[1:end,(month0)==a], c(.05,.95))[[2]]
mean0[a] = mean(outp0[1:end,(month0)==a]) }
date00 = (1:12) ; date000 = t(replicate(end,date0))

#--------------------------------------------------------------------------------------------------------

nc.file <- open.nc(paste(remote,"CHIRPS_PRCP_Ethiopia_198701_200912_daily_fldmean_monmean.nc",sep=""))
time2 <- round(var.get.nc(nc.file,"time"),0)
outp2 <- round(var.get.nc(nc.file,"PRCP"),4) ; outp2[is.na(outp2)] <- 0 ; outp2 = as.numeric(outp2)
close.nc(nc.file)
year2 = as.numeric(substr(time2,1,4))
mth2 = (as.numeric(substr(time2,5,6)) - 1) / 12
month2 = as.numeric(substr(time2,5,6))
date2 = year2 + mth2
mean2 = 0 ; lower2 = 0 ; upper2 = 0 ; for ( a in 1:12 ) {
lower2[a] = quantile(outp2[(month2)==a], c(.05,.95))[[1]]
upper2[a] = quantile(outp2[(month2)==a], c(.05,.95))[[2]]
mean2[a] = mean(outp2[(month2)==a]) }
date22 = (1:12)

#--------------------------------------------------------------------------------------------------------
# PLOTTING
#--------------------------------------------------------------------------------------------------------

rr_min=0.0
rr_max=9.0
rtime1=1
rtime2=12

taxis1 <- c("1","2","3","4","5","6","7","8","9","10","11","12")
taxis2 <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
raxis <- c("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14")

png(filename="PRCP_Ethiopia_198701_200912_allmember_monthly.png",width = 1024, height = 768,bg = "white") ; par(mar=c(5,5,4,3))
plot(date00,mean0,type="n",cex=1.0,ylim=c(rr_min,rr_max),col="black",xlim=c(rtime1,rtime2),main="Monthly Precipitation Climatology (1987-2009) - Ethiopia"
,xlab="Month",ylab="Monthly precipitation [mm/day]",cex.lab=1.6,cex.axis=1.6,cex.main=2.2,xaxt="n",yaxt="n") ; par(new=T)
plot(date00,upper0,xlim=c(rtime1,rtime2),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("black",0.6),xaxt="n",yaxt="n",xlab="",ylab="") ; par(new=T)
plot(date00,lower0,xlim=c(rtime1,rtime2),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("black",0.6),xaxt="n",yaxt="n",xlab="",ylab="")
polygon(c(date00,rev(date00)),c(lower0,rev(upper0)),col=alpha("black",0.2),border=NA) ; par(new=T)
plot(date22,upper2,xlim=c(rtime1,rtime2),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("darkorchid",0.4),xaxt="n",yaxt="n",xlab="",ylab="") ; par(new=T)
plot(date22,lower2,xlim=c(rtime1,rtime2),ylim=c(rr_min,rr_max),type="l",lty=1,col=alpha("darkorchid",0.4),xaxt="n",yaxt="n",xlab="",ylab="")
polygon(c(date22,rev(date22)),c(lower2,rev(upper2)),col=alpha("darkorchid",0.1),border=NA) ; par(new=T)
par(new=T) ; plot(date00,mean0,type="l",lty=1,lwd=6.0,cex=1.4,ylim=c(rr_min,rr_max),col="black",xlim=c(rtime1,rtime2),xaxt="n",yaxt="n",xlab="",ylab="")
par(new=T) ; plot(date22,mean2,type="l",lty=1,lwd=4.0,cex=1.4,ylim=c(rr_min,rr_max),col="darkorchid",xlim=c(rtime1,rtime2),xaxt="n",yaxt="n",xlab="",ylab="")
abline(h=raxis,col="grey66",lty=2,lwd=0.5) ; abline(v=taxis1,col="grey66",lty=2,lwd=0.5)
axis(1,at=taxis1,labels=taxis2,tick=TRUE,cex.axis=1.8) ; axis(2,at=raxis,labels=raxis,tick=TRUE,cex.axis=1.8,las=2)
lego1 = c("HadRM3P AFR50 (120 member; 5-95% percentile)","CHIRPS Observations (5-95% percentile)")
legcol1 = c("black","darkorchid") ; legend("topleft",lwd=2,col=legcol1,bty="n",cex=1.8,lego1)
dev.off()

#--------------------------------------------------------------------------------------------------------
quit()
#--------------------------------------------------------------------------------------------------------

