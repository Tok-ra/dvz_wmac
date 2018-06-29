#!/share/apps/python/2.7.2/bin/python
from __future__ import division
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.spatial import cKDTree as KDTree
"""

   Uses similar media scaling to estimate hydraulic parameters from 
   field-measured volumetric water content using an assumed mean tension
   and reference Ks and water retention function.

   Written by ML Rockhold, 14-Sept-2015.
   Project WMA C Alternative Conceptual Models, client WRPS.

"""
class Invdisttree:
    """
    Inverse-distance-weighted interpolation using KDTree:
    """
    def __init__( self, X, z, leafsize, stat=0 ):
        assert len(X) == len(z), "len(X) %d != len(z) %d" % (len(X), len(z))
        self.tree = KDTree( X, leafsize=leafsize )  # build the tree
        self.z = z
        self.stat = stat
        self.wn = 0
        self.wsum = None;

    def __call__( self, q, nnear, eps, p, weights=None ):
        q = np.asarray(q)
        qdim = q.ndim
        if qdim == 1:
            q = np.array([q])
        if self.wsum is None:
            self.wsum = np.zeros(nnear)

        self.distances, self.ix = self.tree.query( q, k=nnear, eps=eps )
        interpol = np.zeros( (len(self.distances),) + np.shape(self.z[0]) )
        jinterpol = 0
        for dist, ix in zip( self.distances, self.ix ):
            if nnear == 1:
                wz = self.z[ix]
            elif dist[0] < 1e-10:
                wz = self.z[ix[0]]
            else:  # weight z s by 1/dist --
                w = 1 / dist**p
                if weights is not None:
                    w *= weights[ix]  # >= 0
                w /= np.sum(w)
                wz = np.dot( w, self.z[ix] )
                if self.stat:
                    self.wn += 1
                    self.wsum += w
            interpol[jinterpol] = wz
            jinterpol += 1
        return interpol if qdim > 1  else interpol[0]

# example useage: Kh.append(MualemVG_Kh(p,h[nf]))
def MualemVG_Kh(p,h):
    vga,vgn,ks,ell = p
    vgm = 1.0 - 1.0/vgn
    den = (1.0 + (vga*h)**vgn)**(vgm*ell)
    num = (1.0 - (vga*h)**(vgn-1.0)*(1.0+(vga*h)**vgn)**(-vgm))**2
    return ks*num/den

def VG_htheta(p,w,zon):
    vga,vgn,ts,tr = p
    sub = 5.e-3 
    add = 1.5e-2
    if w <= tr: 
       #wold = w
       w = tr + add 
       #print 'resetting w from',wold,' to ',w 
    if w >= ts:
       #wold = w
       w = ts - sub
       #print 'resetting w from',wold,' to ',w 
    se = (w-tr)/(ts-tr)
    vgm = 1.0 - 1.0/vgn
    #print 'w, tr, ts, se, vgm ',w, tr, ts, se,vgm
    h = 1.0/vga*(se**(-1.0/vgm)-1.0)**(1.0/vgn)
    return h

def main():
    print 'running...'

    # ksx[cm/s],ksy,ksz,thetas,thetar,alpha[1/cm],n,ellx,elly,ellz,href
    # h1 and h3 are the same here

    bf_params = [5.07e-3,5.07e-3,5.07e-3,0.293,0.027,0.114,1.74,0.1,0.1,0.5,180.0]
    h1_params = [4.79e-3,4.79e-3,1.60e-3,0.200,0.025,0.120,1.60,-1.2,-1.2,-1.2,446.0]
    h2_params = [9.40e-3,9.40e-3,9.40e-3,0.367,0.025,0.140,1.80,-1.0,-1.0,-0.2,245.0]
    h3_params = [4.79e-3,4.79e-3,1.60e-3,0.200,0.025,0.120,1.60,-1.2,-1.2,-1.2,446.0]

    water_content_data_file = 'sgsim1.ups'

    xcell_face_coords_file = 'cfxc.dat'
    ycell_face_coords_file = 'cfyc.dat'
    zcell_face_coords_file = 'cfzc.dat'

    surf_file1 = 'top_H3.srf'
    surf_file2 = 'top_H2.srf'
    surf_file3 = 'top_H1.srf'
    surf_file4 = 'backfill_landsurf.srf'

    # Specify output files
    test_output = 'wmac_param_step1.out'

    # Read x-dir cell face file
    print ' reading x cell face coordinates'
    fin = open(xcell_face_coords_file,'r')
    xcf = []
    i = 0
    while(1):
       end_of_xcell_face_coords_file = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_xcell_face_coords_file = 0
          xcf.append(float(w[0]))
          i += 1
       if end_of_xcell_face_coords_file == 1: break
    fin.close()

    # Read y-dir cell face coordinates
    print ' reading y cell face coordinates'
    fin = open(ycell_face_coords_file,'r')
    ycf = []
    j = 0
    while(2):
       end_of_ycell_face_coords_file = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_ycell_face_coords_file = 0
          ycf.append(float(w[0]))
          j += 1
       if end_of_ycell_face_coords_file == 1: break
    fin.close()

    # Read z-dir cell face coordinates
    print ' reading z cell face coordinates'
    fin = open(zcell_face_coords_file,'r')
    zcf = []
    k = 0
    while(3):
       end_of_zcell_face_coords_file = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_zcell_face_coords_file = 0
          zcf.append(float(w[0]))
          k += 1
       if end_of_zcell_face_coords_file == 1: break
    fin.close()

    # Read water contents
    print ' reading water contents'
    fin = open(water_content_data_file,'r')
    wc = []
    while(4):
       end_of_water_content_data_file = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_water_content_data_file = 0
          wc.append(float(w[0])/100.0)
       if end_of_water_content_data_file == 1: break
    fin.close()

    # Generate global cell faces
    cfxg = []
    cfyg = []
    cfzg = []
    ntot = 0
    for kc in range(len(zcf)):
       for jc in range(len(ycf)):
          for ic in range(len(xcf)):
             cfxg.append(xcf[ic])
             cfyg.append(ycf[jc])
             cfzg.append(zcf[kc])
             ntot += 1

    # Generate grid centroid coordinates
    xc = []
    yc = []
    zc = []
    nc = 0
    for kc in range(len(zcf)-1):
       for jc in range(len(ycf)-1):
          for ic in range(len(xcf)-1):
             xc.append((xcf[ic+1]+xcf[ic])*0.5)
             yc.append((ycf[jc+1]+ycf[jc])*0.5)
             zc.append((zcf[kc+1]+zcf[kc])*0.5)
             nc += 1

    x2d = []
    y2d = []
    for jc in range(len(ycf)-1):
       for ic in range(len(xcf)-1):
          x2d.append((xcf[ic+1]+xcf[ic])*0.5)
          y2d.append((ycf[jc+1]+ycf[jc])*0.5)


    print ' reading surface files'
    fin = open(surf_file1,'r')
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    east1 = []
    north1 = []
    elev1 = []
    while(5):
       end_of_surf_file1 = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_surf_file1 = 0
          east1.append(float(w[0]))
          north1.append(float(w[1]))
          elev1.append(float(w[2]))
       if end_of_surf_file1 == 1: break
    fin.close()

    fin = open(surf_file2,'r')
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    east2 = []
    north2 = []
    elev2 = []
    while(5):
       end_of_surf_file2 = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_surf_file2 = 0
          east2.append(float(w[0]))
          north2.append(float(w[1]))
          elev2.append(float(w[2]))
       if end_of_surf_file2 == 1: break
    fin.close()

    fin = open(surf_file3,'r')
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    east3 = []
    north3 = []
    elev3 = []
    while(5):
       end_of_surf_file3 = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_surf_file3 = 0
          east3.append(float(w[0]))
          north3.append(float(w[1]))
          elev3.append(float(w[2]))
       if end_of_surf_file3 == 1: break
    fin.close()

    fin = open(surf_file4,'r')
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    s = fin.readline()
    east4 = []
    north4 = []
    elev4 = []
    while(5):
       end_of_surf_file4 = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_surf_file4 = 0
          east4.append(float(w[0]))
          north4.append(float(w[1]))
          elev4.append(float(w[2]))
       if end_of_surf_file4 == 1: break
    fin.close()

    print '***************'

    # --- Delaunay interpolation
    fill = 0.0
    #east = np.array(east)
    #north = np.array(north)
    #elev = np.array(elev)
    #wc = np.array(wc)

    #wcp = griddata((east,north,elev),wc,(xc,yc,zc),method='linear',fill_value=fill)
    #zsrf= griddata((east,north),elev,(xc,yc),method='linear',fill_value=fill)

    p = 1
    Nnear = 3
    ndim = 2
    eps = 0
    leafsize = 10

    a = np.array([east1,north1])
    pin = np.transpose(a)
    b = np.array([x2d,y2d])
    pout = np.transpose(b)
    vin = np.array(elev1)
    invdisttree = Invdisttree(pin,vin,leafsize,stat=1)
    zsrf1 = invdisttree(pout,nnear=Nnear,eps=eps,p=p)

    a = np.array([east2,north2])
    pin = np.transpose(a)
    b = np.array([x2d,y2d])
    pout = np.transpose(b)
    vin = np.array(elev2)
    invdisttree = Invdisttree(pin,vin,leafsize,stat=1)
    zsrf2 = invdisttree(pout,nnear=Nnear,eps=eps,p=p)

    a = np.array([east3,north3])
    pin = np.transpose(a)
    b = np.array([x2d,y2d])
    pout = np.transpose(b)
    vin = np.array(elev3)
    invdisttree = Invdisttree(pin,vin,leafsize,stat=1)
    zsrf3 = invdisttree(pout,nnear=Nnear,eps=eps,p=p)

    a = np.array([east4,north4])
    pin = np.transpose(a)
    b = np.array([x2d,y2d])
    pout = np.transpose(b)
    vin = np.array(elev4)
    invdisttree = Invdisttree(pin,vin,leafsize,stat=1)
    zsrf4 = invdisttree(pout,nnear=Nnear,eps=eps,p=p)

    fou = open(test_output,'w')  
    nc = 0
    while nc < len(wc):

       #zsrf1= griddata((east1,north1),elev1,(xc[nc],yc[nc]),method='linear',fill_value=fill)
       #zsrf2= griddata((east2,north2),elev2,(xc[nc],yc[nc]),method='linear',fill_value=fill)
       #zsrf3= griddata((east3,north3),elev3,(xc[nc],yc[nc]),method='linear',fill_value=fill)
       #zsrf4= griddata((east4,north4),elev4,(xc[nc],yc[nc]),method='linear',fill_value=fill)

       n2 = 0
       while n2 < len(x2d):
          zon = 'none'
          if xc[nc] == x2d[n2] and yc[nc] == y2d[n2]:
             if zc[nc] <= zsrf1[n2]:
                zon = 'h3'
                ksx = h3_params[0]
                ksy = h3_params[1]
                ksz = h3_params[2]
                ts = h3_params[3]
                tr = h3_params[4]
                vga = h3_params[5]
                vgn = h3_params[6]
                ellx = h3_params[7]
                elly = h3_params[8]
                ellz = h3_params[9]
                href = h3_params[10]
             elif zc[nc] > zsrf1[n2] and zc[nc] <= zsrf2[n2]:
                zon = 'h2'
                ksx = h2_params[0]
                ksy = h2_params[1]
                ksz = h2_params[2]
                ts = h2_params[3]
                tr = h2_params[4]
                vga = h2_params[5]
                vgn = h2_params[6]
                ellx = h2_params[7]
                elly = h2_params[8]
                ellz = h2_params[9]
                href = h2_params[10]
             elif zc[nc] > zsrf2[n2] and zc[nc] <= zsrf3[n2]:
                zon = 'h1'
                ksx = h1_params[0]
                ksy = h1_params[1]
                ksz = h1_params[2]
                ts = h1_params[3]
                tr = h1_params[4]
                vga = h1_params[5]
                vgn = h1_params[6]
                ellx = h1_params[7]
                elly = h1_params[8]
                ellz = h1_params[9]
                href = h1_params[10]
             #elif zc[nc] > zsrf3[n2] and zc[nc] <= zsrf4[n2]:
             elif zc[nc] > zsrf3[n2]:
                zon = 'bf'
                ksx = bf_params[0]
                ksy = bf_params[1]
                ksz = bf_params[2]
                ts = bf_params[3]
                tr = bf_params[4]
                vga = bf_params[5]
                vgn = bf_params[6]
                ellx = bf_params[7]
                elly = bf_params[8]
                ellz = bf_params[9]
                href = bf_params[10]
             if zon <> 'none':
                p = [vga,vgn,ts,tr]
                h = VG_htheta(p,wc[nc],zon)       
                sfh = h/href
                sfk = sfh
                hb = 1.0/vga/sfh 
                vga_new = 1.0/hb
                ksz_new = ksz*sfk**2
                ksx_new = ksz_new*(ksx/ksz)
                ksy_new = ksz_new*(ksy/ksz)
                l2p = [zon,wc[nc],ksx_new,ksy_new,ksz_new,ts,tr,vga_new,vgn,ellx,elly,ellz]
                print>>fou,','.join(map(str,l2p))
                break
          n2 += 1
       nc += 1 
    fou.close()

if __name__ == '__main__':
    main()

