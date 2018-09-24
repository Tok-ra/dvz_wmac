# SUMMARY:      change_oppc_zonation_to_prehanford.py
# USAGE:        convert tanks and backfill material to hanford
# ORG:          Pacific Northwest National Laboratory
# AUTHOR:       Xuehang Song
# E-MAIL:       xuehang.song@pnnl.gov
# ORIG-DATE:    July-2018
# DESCRIPTION:
# DESCRIP-END.
# COMMENTS:
#
# Last Change: 2018-07-24

import numpy as np
import pandas as pd

nx = 89
ny = 93
nz = 330

ehm_zon = "/people/song884/wmac/fy18/fine_model_setup/ehm/wma_c_pre_hanford_ehm_89x93x330.zon"
# bin_zon = "/people/song884/wmac/fy18/fine_model_setup/bin/new_grid_heterogeneous_vz_ss.zon"


# ehm_zon = "/people/song884/wmac/fy18/InteraFiles/new_grid_ehm_89x93x330_original.zon"
ehm_zon = "/people/song884/wmac/fy18/InteraFiles/new_grid_heterogeneous_89x93x330.zon"
# ehm_zon = "/people/song884/wmac/fy18/InteraFiles/new_grid_heterogeneous_vz.zon"

#ehm_zon = "/people/song884/wmac/fy18/for_vicky/Fine_grid_with_polmann/ss/new_grid_heterogeneous_vz_ss.zon"
bin_zon = "/people/song884/wmac/fy18/for_vicky/Fine_grid_with_polmann/C-105-leak/new_grid_heterogeneous_vz.zon"

ehm = np.genfromtxt(ehm_zon).flatten(order="C").astype(int)
ehm_array = ehm.reshape((nx, ny, nz), order="F")
ehm_0 = np.asarray(np.where(ehm_array == 0))

bin = np.genfromtxt(bin_zon).flatten(order="C").astype(int)
bin_array = bin.reshape((nx, ny, nz), order="F")
bin_0 = np.asarray(np.where(bin_array == 0))


print(pd.Series(bin).value_counts(sort=False))
print(pd.Series(ehm).value_counts(sort=False))


# # find tank locations
# tank_cells = []
# for ipoint in range(len(oppc_0[0, ])):
#     bottom_material = oppc_array[oppc_0[0, ipoint],
#                                  oppc_0[1, ipoint],
#                                  np.arange(0, oppc_0[2, ipoint])]
#     top_material = oppc_array[oppc_0[0, ipoint],
#                               oppc_0[1, ipoint],
#                               np.arange(oppc_0[2, ipoint]+1, nz)]
#     if (any(bottom_material != 0) and any(top_material != 0)):
#         print(ipoint)
#         tank_cells.append(ipoint)
# tank_index = oppc_0[:, tank_cells]
# tank_index = tank_index[0, :]+tank_index[1, :]*nx+tank_index[2, :]*nx*ny


# # find backfill locations
# backfill_index = np.asarray(np.where(oppc == 8))

# pre_hanford = oppc
# pre_hanford[tank_index] = 7
# pre_hanford[backfill_index] = 7

# fout = open(pre_hanford_zon, 'w')
# fout.write("\n".join(map(str, pre_hanford)))
# fout.close()
