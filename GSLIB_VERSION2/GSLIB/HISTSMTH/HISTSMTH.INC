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
c The following Parameters control static dimensioning for USMOOTH:
c
c   MAXDAT    maximum number of original data
c   MAXSMT    maximum number of histogram classes
c   MAXCLS    maximum number of classes for output cdf
c   MAXSTA    maximum number of statistics (quantiles, modes,...)
c
c-----------------------------------------------------------------------
c
c User Adjustable Parameters:
c
      parameter(MAXDAT =500000, 
     +          MAXSMT =   100,
     +          MAXCLS =  1000,
     +          MAXSTA =   100)
c
c Fixed Parameters:
c
      parameter(EPSLON=1.0e-10,NUMSCL=100,VERSION=2.000)
c
c Variable Declaration:
c
      real      utpar,ltpar,zmin,zmax,rcdf(MAXDAT),rvr(MAXDAT),
     +          val(1-MAXSMT:MAXCLS+MAXSMT),
     +          sval(MAXCLS),smthfac(MAXCLS),
     +          svali(-MAXSMT:MAXSMT),svalj(-MAXSMT:MAXSMT),
     +          mean,variance,qval(MAXSTA),qact(MAXSTA),qtry(MAXSTA),
     +          mode(MAXSTA),valley(MAXSTA),zinc,omin,psmax,
     +          objmean,objvari,objsmth,objquan,
     +          obtmean,obtvari,obtsmth,obtquan

      real      zz(MAXCLS),zzs(MAXCLS),rmean,rvar,tmean,tvar

      integer   ltail,utail,lin,lout,lps,ldbg,nd,nclass,ncut,nhist,
     +          nsmooth,nuq,uqind(MAXSTA),nmode,maxpert,report

      logical   lmean,lvari,lsmth,lquan,psign(MAXCLS)
c
c Common Blocks:
c
      common /datafd/ nd,rcdf,rvr,utpar,ltpar,ltail,utail,zmin,zmax

      common /genral/ lin,lout,ldbg,lps,nclass,ncut,nhist,nsmooth,
     +                smthfac,val,sval,svali,svalj,ilog,
     +                maxpert,report,omin,psmax

      common /smtpar/ mean,variance,nuq,qval,uqind,qact,qtry,nmode,
     +                mode,valley,zinc

      common /smtdpp/ zz,zzs,rmean,rvar,tmean,tvar

      common /smtspp/ objmean,objvari,objsmth,objquan,
     +                obtmean,obtvari,obtsmth,obtquan,
     +                sclmean,sclvari,sclsmth,sclquan

      common /logcha/ lmean,lvari,lsmth,lquan,psign
