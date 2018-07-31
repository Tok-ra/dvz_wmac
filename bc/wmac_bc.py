#!/share/apps/python/2.7.2/bin/python
import numpy as np
"""
    Purpose:
    1) Reads stomp model cell face coordinates and zonation info.
    2) Reads list of vertices defining polygons for different plan-view 
       portions of model domain. Rotates the coordinates.
    3) Loops through x-y locations for grid, determines the polygon each
       x-y point lies within, and creates linked lists of cell faces for BCs.

    Author: 
       Mark Rockhold, PNNL, 24-Feb-2015 

    Project:
       ASCEM, Site Applications, Hanford WMA-C 
"""
def point_in_poly(polyx,polyy,x,y):
    """ 
    Determines if a point (x,y) lies within a polygon defined by a list 
    of x-y data pairs (polyx,polyy). The polygon points should be listed 
    in clockwise order. Any holes in the polygon should be listed in 
    counterclockwise order. Returns True or False.
    """
    nvert = len(polyx)
    c = False
    i = 0
    j = nvert-1
    while i < nvert:
        if((polyy[i]>y) != (polyy[j]>y)) and (x<(polyx[j]-polyx[i])/(polyy[j]-polyy[i])*(y-polyy[i])+polyx[i]):
            c = not c
        j = i
        i += 1
    return c

def main():

    # stomp needs lower case
    # trying this in real002 scratchdir setup to test 
    #zonation_file = 'facies_real001_plustanks.ups'
    #zonation_file = 'facies_real002_plustanks.ups'
    #zonation_file = 'SGRfacies_renum_003_plustanks.ups'
    zonation_file = 'SGRfacies_renum_004_plustanks.ups'
    # These polygons are in true space coordinates  
    poly_file_list = 'poly.list'
    xcell_face_coords_file = 'cfxc.dat'
    ycell_face_coords_file = 'cfyc.dat'
    zcell_face_coords_file = 'cfzc.dat'
    ext = '.lnk'

    # load x-dir grid cell face coordinates
    print 'reading x cell face coordinates'
    fin = open(xcell_face_coords_file,'r')
    xcf = []
    i = 0
    while(1):
       end_of_xcell_face_coords_file = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_xcell_face_coords_file = 0
          xcf.append(i)
          xcf[i] = float(w[0])
          i += 1
       if end_of_xcell_face_coords_file == 1: break
    #print xcf
    fin.close()

    # y-dir
    print 'reading y cell face coordinates'
    fin = open(ycell_face_coords_file,'r')
    ycf = []
    j = 0
    while(2):
       end_of_ycell_face_coords_file = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_ycell_face_coords_file = 0
          ycf.append(j)
          ycf[j] = float(w[0])
          j += 1
       if end_of_ycell_face_coords_file == 1: break
    #print ycf   
    fin.close()

    # z-dir
    print 'reading z cell face coordinates'
    fin = open(zcell_face_coords_file,'r')
    zcf = []
    k = 0
    while(3):
       end_of_zcell_face_coords_file = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_zcell_face_coords_file = 0
          zcf.append(k)
          zcf[k] = float(w[0])
          k += 1
       if end_of_zcell_face_coords_file == 1: break
    #print zcf
    fin.close()

    # load zonation file
    print 'reading zonation file'
    fin = open(zonation_file,'r')
    zid = []
    n = 0
    while(4):
       end_of_zonation_file = 1
       s = fin.readline()
       w = s.split()
       if len(w) > 0:
          end_of_zonation_file = 0
          zid.append(n)
          zid[n] = int(w[0])
          n += 1
       if end_of_zonation_file == 1: break
    fin.close()

    nx = len(xcf) - 1
    ny = len(ycf) - 1
    nz = len(zcf) - 1
    nxyz = nx*ny*nz
    print 'nx=',nx,' ny=',ny,' nz=',nz
    print ' '

    print 'reading file list'
    fin = open(poly_file_list,'r')
    nfile = 0
    fnm = []
    while(16):
       end_of_poly_file_list = 1
       s = fin.readline()
       s = s.strip('\n\r')
       if len(s) > 0:
          end_of_poly_file_list = 0
          fnm.append(nfile)
          fnm[nfile] = s
          nfile += 1
       if end_of_poly_file_list == 1: break
    fin.close()   
#
# loop over the surface polygons
#
    for nf in range(len(fnm)):
       print ' '
       print 'nf=',nf
       poly_file_in = fnm[nf]
       fin1 = open(poly_file_in,'r')
       print 'reading',poly_file_in
       name_parts = poly_file_in.split('.')
       fname2 = name_parts[0] + ext
       fou1 = open(fname2,'w')

       # rotation specifications 
       xpiv = 574667.0
       ypiv = 136453.0
       deg = -45.0
       xoffset = 0.0
       yoffset = 0.0
       pi = 3.14159265358979
       rot = deg*pi/180.0

       xp = []
       yp = []
       npt = 0
       while(18):
          end_of_poly_file_in = 1
          s4 = fin1.readline().strip('\n\r')
          w4 = s4.split(',')
          if len(w4) > 1:
             end_of_poly_file_in = 0
             easting = float(w4[0])
             northing = float(w4[1])
             xdis = easting - xpiv
             ydis = northing - ypiv 
             xr = xdis*np.cos(rot) + ydis*np.sin(rot) + xpiv - xoffset
             yr = -xdis*np.sin(rot) + ydis*np.cos(rot) + ypiv - yoffset
             xp.append(xr)
             yp.append(yr)
             npt += 1
          if end_of_poly_file_in == 1: break 
       fin1.close()
       
       # generate linked lists for upper BCs
       fid = 3
       for j in range(len(ycf)-1):
          j1 = j + 1
          yn = (ycf[j1] + ycf[j])*0.5
          for i in range(len(xcf)-1):
             i1 = i + 1
             xn = (xcf[i1] + xcf[i])*0.5
             inside = point_in_poly(xp,yp,xn,yn)
             if inside:
#original logic only worked if there were no inactive cells on bottom of domain
#so now need to modify to account for this with basalt set to inactive.
                #for k in range(len(zcf)-1):
                for k in range(len(zcf)-1,1,-1):
                   #print 'k=',k 
                   #k1 = k + 1
                   k1 = k
                   nloc = (k1-1)*nx*ny + (j1-1)*nx + i1
                   if zid[nloc-1] > 0:
                      line = [i1,j1,k1,fid] 
                      print>>fou1,' '.join(map(str,line)) 
                      break
                      #if k1 < nz:
                      #   kt = k1 + 1
                      #   nt = (kt-1)*nx*ny + (j1-1)*nx + i1
                      #   if zid[nt-1] == 0:
                      #      line = [i1,j1,k1,fid]
                      #      print>>fou1,' '.join(map(str,line)) 
                      #      break
                      ## MLR added this 26-Feb-2015 to correct problem with logic 
                      #else:
                      #   line = [i1,j1,k1,fid]
                      #   print>>fou1,' '.join(map(str,line)) 
                      #   break

       fou1.close()      

       # generate linked list for south boundary         
       fname = 'wmac_south_boundary.lnk' 
       fou1 = open(fname,'w') 
       j1 = 1
       fid = -2
       for i in range(len(xcf)-1):
          i1 = i + 1
          for k in range(len(zcf)-1):
             k1 = k + 1
             nloc = (k1-1)*nx*ny + (j1-1)*nx + i1
             if zid[nloc-1] != 0:
                line = [i1,j1,k1,fid]
                print>>fou1,' '.join(map(str,line)) 
       fou1.close()

       # generate linked list for north boundary         
       fname = 'wmac_north_boundary.lnk'
       fou1 = open(fname,'w')
       j1 = ny 
       fid = 2
       for i in range(len(xcf)-1):
          i1 = i + 1
          for k in range(len(zcf)-1):
             k1 = k + 1
             nloc = (k1-1)*nx*ny + (j1-1)*nx + i1
             if zid[nloc-1] != 0:
                line = [i1,j1,k1,fid]
                print>>fou1,' '.join(map(str,line)) 
       fou1.close()

       # generate linked list for west boundary         
       fname = 'wmac_west_boundary.lnk'
       fou1 = open(fname,'w')
       i1 = 1 
       fid = -1 
       for j in range(len(ycf)-1):
          j1 = j + 1
          for k in range(len(zcf)-1):
             k1 = k + 1
             nloc = (k1-1)*nx*ny + (j1-1)*nx + i1
             if zid[nloc-1] != 0:
                line = [i1,j1,k1,fid]
                print>>fou1,' '.join(map(str,line)) 
       fou1.close()

       # generate linked list for east boundary         
       fname = 'wmac_east_boundary.lnk'
       fou1 = open(fname,'w')
       i1 = nx 
       fid = 1 
       for j in range(len(ycf)-1):
          j1 = j + 1
          for k in range(len(zcf)-1):
             k1 = k + 1
             nloc = (k1-1)*nx*ny + (j1-1)*nx + i1
             if zid[nloc-1] != 0:
                line = [i1,j1,k1,fid]
                print>>fou1,' '.join(map(str,line)) 
       fou1.close()

if __name__ == '__main__':
    main()

