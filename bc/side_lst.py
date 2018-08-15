# SUMMARY:      side_lnk.py
# USAGE:        generate lnk files from side boundary
# ORG:          Pacific Northwest National Laboratory
# AUTHOR:       Xuehang Song
# E-MAIL:       xuehang.song@pnnl.gov
# ORIG-DATE:    Jun-2018
# DESCRIPTION:
# DESCRIPTION:
# DESCRIP-END.
# COMMENTS:     only deal cartesian sturtured grids
#
# Last Change: 2018-07-29

# below is MLR's original description
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
    poly_dir = "/people/song884/wmac/fy18/fine_model/model_setup/polygons/"
    zonation = "/people/song884/wmac/fy18/fine_model/model_setup/ehm/wma_c_pre_hanford_ehm_89x93x330.zon"

    # boundary type
    fid_east = 1
    fid_west = -1

    # read x, y, z coordinates
    xo, yo, zo, xe, ye, ze, dx, dy, dz, nx, ny, nz, x, y, z = retrieve_grids(
        grid_card)

    # z range in west/east boundary
    z_east = np.arange(0, nz)
    z_west = np.arange(0, nz)

    # read zonation file
    zid = np.genfromtxt(zonation).flatten(order="C").astype(int)
    zid_array = zid.reshape((nx, ny, nz), order="F")

    west_lowest = nz
    # generate lst file for west boundary
    west_lst = []
    for iz in z_west:
        for iy in range(ny):
            for ix in [0]:
                if zid_array[ix, iy, iz] != 0:
                    line = [ix+1, iy+1, iz+1, fid_west]
                    west_lst.append(" ".join(map(str, line)))
                    west_lowest = min(west_lowest, iz)
    fname = open(poly_dir+"wmac_west_aquifer.lst", 'w')
    fname.write("\n".join(west_lst))
    fname.close()

    east_lowest = nz
    # generate lst file for east boundary
    east_lst = []
    for iz in z_east:
        for iy in range(ny):
            for ix in [nx-1]:
                if zid_array[ix, iy, iz] != 0:
                    line = [ix+1, iy+1, iz+1, fid_east]
                    east_lst.append(" ".join(map(str, line)))
                    east_lowest = min(east_lowest, iz)
    fname = open(poly_dir+"wmac_east_aquifer.lst", 'w')
    fname.write("\n".join(east_lst))
    fname.close()
