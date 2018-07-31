# SUMMARY:      upper_lst.py
# USAGE:        generate lst files surface recharge boundary
# ORG:          Pacific Northwest National Laboratory
# AUTHOR:       Xuehang Song
# E-MAIL:       xuehang.song@pnnl.gov
# ORIG-DATE:    Jun-2018
# DESCRIPTION:  This scripts is revised based on Mark Rockhold's (MLR) work
# DESCRIPTION:  The main reason is 1) convert it to python3,
# DESCRIPTION:  2) learn how MLR create the boundary
# DESCRIP-END.  3) use different way to implement the setup to compare with MLR's setup
# COMMENTS:     only deal cartesian sturtured grids
#
# Last Change: 2018-07-29

## below is MLR's original description
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

import numpy as np
import re
import sys
import math
import glob
from shapely.geometry import Point
from shapely.geometry import MultiPoint
from matplotlib import pyplot as plt

# convert length units to m
def length_conversion(x):
    return {
        'a': 1e-10,
        'ang': 1e-10,
        'angstrom': 1e-10,
        'ao': 1e-10,
        'cm': 0.01,
        'ffl': 109.728,
        'ft': 0.3048,
        'furlong': 201.168,
        'm': 1,
        'mi': 1609.344,
        'mile': 1609.344,
        "mm": 0.001,
        'rod': 5.0292,
        'yd': 0.9144
    }.get(x, 1)


# read grid information from eSTOMP input
def retrieve_grids(grid_card):
    # read raw input deck
    input_file = open(grid_card, "r")
    estomp_input = input_file.readlines()
    input_file.close()

    # remove comments and blank lines in input deck
    estomp_input = [re.split('[#!\n]', x)[0] for x in estomp_input]
    estomp_input = [x for x in estomp_input if x]

    # locate start of grid card
    grid_line = [i for i, s in enumerate(estomp_input) if "~Grid" in s][0]

    if "cartesian" in estomp_input[grid_line + 1].lower():
        print("Cartesian grids")
    else:
        sys.exit("Unfortunately, this scripts only can deal with cartesian grids")
        
    # read nx, ny, nz
    nx, ny, nz = map(int, re.split('[,]', estomp_input[grid_line + 2])[0:3])
    grid_value = []
    iline = 3
    d_flag = 0
    # loop lines of etomp inputs until have enough entry for grids
    # while estomp_input[grid_line + iline][0] != "~":    
    while len(grid_value) < (1 + nx + 1 + ny + 1 + nz):
        line_data = estomp_input[grid_line + iline].split(",")
        ndata = int(math.floor(len(line_data) / 2))
        for idata in range(ndata):
            if ("@" in line_data[idata * 2]):
                d_flag = 1
                temp_n, temp_d = line_data[idata * 2].split("@")
                grid_value += [float(temp_d) *
                               length_conversion(line_data[idata * 2 + 1])] * int(temp_n)
            else:
                grid_value += [float(line_data[idata * 2]) *
                               length_conversion(line_data[idata * 2 + 1])]
        iline += 1

    # assign flatten grids values to x, y, z        
    if d_flag == 1:
        xo = grid_value[0]
        dx = np.asarray(grid_value[1:1 + nx])
        yo = grid_value[1 + nx]
        dy = np.asarray(grid_value[1 + nx + 1:1 + nx + 1 + ny])
        zo = grid_value[1 + nx + 1 + ny]
        dz = np.asarray(
            grid_value[1 + nx + 1 + ny + 1:1 + nx + 1 + ny + 1 + nz])
        x = xo + np.cumsum(dx) - 0.5 * dx
        y = yo + np.cumsum(dy) - 0.5 * dy
        z = zo + np.cumsum(dz) - 0.5 * dz
        xe = xo + sum(dx)
        ye = yo + sum(dy)
        ze = zo + sum(dz)
    else:
        xo = grid_value[0]
        xe = grid_value[nx]
        dx = np.diff(grid_value[0:(nx+1)])
        yo = grid_value[nx+1]
        ye = grid_value[nx+1+ny]
        dy = np.diff(grid_value[nx+1:(nx+1+ny+1)])        
        zo = grid_value[nx+1+ny+1]
        ze = grid_value[nx+1+ny+1+nz]
        dz = np.diff(grid_value[nx+1+ny+1:(nx+1+ny+1+nz+1)])
        x = xo + np.cumsum(dx) - 0.5 * dx
        y = yo + np.cumsum(dy) - 0.5 * dy
        z = zo + np.cumsum(dz) - 0.5 * dz
    print("Grid retrived from eSTOMP input")
    return xo, yo, zo, xe, ye, ze, dx, dy, dz, nx, ny, nz, x, y, z

if __name__ == '__main__':
    grid_card = "/people/song884/wmac/fy18/fine_model/model_setup/grids/fine_grid_card"
    zonation = "/people/song884/wmac/fy18/fine_model/model_setup/ehm/wma_c_pre_hanford_ehm_89x93x330.zon"
    poly_dir = "/people/song884/wmac/fy18/fine_model/model_setup/polygons/"

    # boundary type
    fid = 3
        
    # model_origin: the 'real' coordinate of model (0,0,0)
    origin_x = 574656.09 + 10 
    origin_y = 136454.41 + 10
    origin_z = 0
    
    # rotation specifications
    xpiv = 574667.0
    ypiv = 136453.0
    deg = -45.0
    xoffset = 0.0
    yoffset = 0.0
    pi = 3.14159265358979
    rot = deg*pi/180.0
    
    # read x, y, z coordinates
    xo, yo, zo, xe, ye, ze, dx, dy, dz, nx, ny, nz, x, y, z = retrieve_grids(
        grid_card)
    xcf = np.append(x-0.5*dx,xe)+origin_x
    ycf = np.append(y-0.5*dy,ye)+origin_y
    zcf = np.append(z-0.5*dz,ze)+origin_z        
    x = x+origin_x
    y = y+origin_y
    z = z+origin_z
    xo = xo+origin_x
    yo = yo+origin_y
    zo = zo+origin_z
    xe = xe+origin_x
    ye = ye+origin_y
    ze = ze+origin_z

    
    # read zonation file
    zid = np.genfromtxt(zonation).flatten(order="C").astype(int)
    zid_array = zid.reshape((nx, ny, nz), order="F")
    
    # read polygon
    all_poly = np.sort(glob.glob(poly_dir + "*csv"))


    # build polygons
    poly_shapes = {}    
    for ipoly in all_poly:
        print(ipoly)
        # read data and do rotation
        poly_data = np.genfromtxt(ipoly,delimiter=",")
        easting = poly_data[:, 0]
        northing = poly_data[:, 1]
        xdis = easting - xpiv
        ydis = northing - ypiv 
        xp = xdis*np.cos(rot) + ydis*np.sin(rot) + xpiv - xoffset
        yp = -xdis*np.sin(rot) + ydis*np.cos(rot) + ypiv - yoffset
        # use multipoint to build polygon
        poly_shapes[ipoly] = MultiPoint([(xp[i], yp[i]) for i in range(len(xp))]).convex_hull


    # generate linked lists for upper BCs
    upper_lst = {}
    for ipoly in all_poly:
        upper_lst[ipoly] = []
        #  find columns  in polygon
        for iy in range(ny):
            for ix in range(nx):
                point = Point((x[ix],y[iy]))
                # extract the top active cells
                if point.within(poly_shapes[ipoly]):
                    iz = np.max(np.where(zid_array[ix,iy,:]>0))
                    line = [ix+1,iy+1,iz+1,fid]
                    upper_lst[ipoly].append(" ".join(map(str,line)))
        fname = open(ipoly.split(".")[0]+".lst",'w')
        fname.write("\n".join(upper_lst[ipoly]))
        fname.close()

#     fig = plt.figure()
#     ax=fig.add_subplot(111)
#     for ipoly in all_poly:
#         print(ipoly)
#         xxx,yyy = poly_shapes[ipoly].exterior.xy
#         plt.plot(xxx,yyy)
# #    plt.plot([xo,xe,xe,xo,xo],[yo,yo,ye,ye,yo],"b")
#     plt.show()
