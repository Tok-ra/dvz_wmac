C%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
C                                                                      %
C Copyright (C) 1996, The Board of Trustees of the Leland Stanford     %
C Junior University.  All rights reserved.                             %
C                                                                      %
C The programs in GSLIB are distributed in the hope that they will be  %
C useful, but WITHOUT ANY WARRANTY.  No author or distributor accepts  %
C responsibility to anyone for the consequences of using them or for   %
C whether they serve any particular purpose or work at all, unless he  %
C says so in writing.  Everyone is granted permission to copy, modify  %
C and redistribute the programs in GSLIB, but only under the condition %
C that this notice and the above copyright notice remain intact.       %
C                                                                      %
C%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
c-----------------------------------------------------------------------
c
c The following Parameters control static dimensioning for BSMOOTH:
c
c   MAXDAT    maximum number of original data
c   MAXSMT    maximum size of smoothing template
c   MAXCLS    maximum classes for each input smoothed histogram
c   MAXQUA    maximum number of quantiles/cutoffs for bivariate histogr.
c   MAXLIM    maximum number of limits for envelope of non-zero p's
c
c-----------------------------------------------------------------------
c
c User Adjustable Parameters:
c
      parameter(MAXDAT = 10000, 
     +          MAXSMT =  1000, MAXSML = 10,
     +          MAXCLS =  1000,
     +          MAXQUA =    50,
     +          MAXLIM =    50)
c
c Fixed Parameters:
c
      parameter(EPSLON=1.0e-10,NUMSCL=100,VERSION=2.000)
c
c Variable Declaration:
c
      real      xmin,xinc,ymin,yinc,xval(MAXDAT),yval(MAXDAT),
     +          pval(MAXDAT),xuni(MAXCLS),yuni(MAXCLS),
     +          xunir(MAXCLS),yunir(MAXCLS),
     +          qvalx(0:MAXQUA),qvaly(0:MAXQUA),qtry(MAXQUA,MAXQUA),
     +          qval(MAXQUA,MAXQUA),qact(MAXQUA,MAXQUA),
     +          val(1-MAXSML:MAXCLS+MAXSML,1-MAXSML:MAXCLS+MAXSML),
     +          sval(MAXCLS,MAXCLS),svali(MAXSMT),
     +          sclmarg,sclcorr,sclsmth,sclquan,sclbhst,
     +          objmarg,objcorr,objsmth,objquan,objbhst,
     +          obtmarg,obtcorr,obtsmth,obtquan,obtbhst,omin,sfac

      real*8    asumx,asumy,asumxx,asumyy,asumxy,
     +          tsumx,tsumy,tsumxx,tsumyy,tsumxy,
     +          corract,corrtry,corr

      integer   lin,lout,ldbg,nlim,nd,nclsx,nclsy,nsmooth,nqx,nqy,
     +          indqx(0:MAXQUA),indqy(0:MAXQUA),maxpert,report,
     +          ixs(MAXSMT),iys(MAXSMT)

      logical   lmarg,lcorr,lsmth,lquan,lbhst

      character xoutfl*80,youtfl*80
c
c Common Blocks:
c
      common /datafd/ nd,xmin,xinc,ymin,yinc,xval,yval,pval

      common /genral/ lin,lout,ldbg,nlim,nclsx,nclsy,nsmooth,
     +                indqx,indqy,maxpert,report,xuni,yuni,
     +                xunir,yunir,val,sval,svali,sfac,omin,xint,xslp,
     +                ilogx,ilogy

      common /smtpar/ nqx,nqy,qvalx,qvaly,qtry,qval,qact,ixs,iys,
     +                sclmarg,sclcorr,sclsmth,sclquan,sclbhst,
     +                objmarg,objcorr,objsmth,objquan,objbhst,
     +                obtmarg,obtcorr,obtsmth,obtquan,obtbhst

      common /smtdbl/ asumx,asumy,asumxx,asumyy,asumxy,
     +                tsumx,tsumy,tsumxx,tsumyy,tsumxy,
     +                corract,corrtry,corr

      common /logcha/ lmarg,lcorr,lsmth,lquan,lbhst

      common /charac/ xoutfl,youtfl
