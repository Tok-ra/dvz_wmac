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

nx = 89
ny = 93
nz = 330

ss_zon = file1 = "/people/song884/wmac/fy18/fine_model_setup/bin/new_grid_heterogeneous_ss_89x93x330.zon"

file1 = "/people/song884/wmac/fy18/fine_model_setup/bin/new_grid_heterogeneous_89x93x330.zon"
file2_1 = "/people/song884/wmac/fy18/for_vicky/Fine_grid_with_polmann/ss/new_grid_heterogeneous_vz_ss.zon"
file2_2 = "/people/song884/wmac/fy18/for_vicky/Fine_grid_with_polmann/C-105-leak/new_grid_heterogeneous_vz.zon"


zon1 = np.genfromtxt(file1).flatten(order="C").astype(int)
zon2_1 = np.genfromtxt(file2_1).flatten(order="C").astype(int)
zon2_2 = np.genfromtxt(file2_2).flatten(order="C").astype(int)


zon1[zon2_1 != zon2_2] = zon2_1[zon2_1 != zon2_2]

fout = open(ss_zon, 'w')
fout.write("\n".join(map(str, zon1)))
fout.close()
