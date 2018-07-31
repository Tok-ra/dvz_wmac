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

oppc_zon = "/people/song884/wmac/fy18/fine_model/model_setup/ehm/wma_c_oppc_ehm_89x93x330.zon"
pre_hanford_zon = "/people/song884/wmac/fy18/fine_model/model_setup/ehm/wma_c_pre_hanford_ehm_89x93x330.zon"

oppc = np.genfromtxt(oppc_zon).flatten(order="C").astype(int)

oppc_array = oppc.reshape((nx, ny, nz), order="F")
oppc_0 = np.asarray(np.where(oppc_array == 0))

# find tank locations
tank_cells = []
for ipoint in range(len(oppc_0[0, ])):
    bottom_material = oppc_array[oppc_0[0, ipoint],
                                      oppc_0[1, ipoint],
                                      np.arange(0,oppc_0[2, ipoint])]
    top_material = oppc_array[oppc_0[0, ipoint],
                                   oppc_0[1, ipoint],
                    np.arange(oppc_0[2, ipoint]+1, nz)]
    if (any(bottom_material != 0) and any(top_material != 0)):
        print(ipoint)
        tank_cells.append(ipoint)
tank_index = oppc_0[:,tank_cells]
tank_index = tank_index[0,:]+tank_index[1,:]*nx+tank_index[2,:]*nx*ny


# find backfill locations
backfill_index = np.asarray(np.where(oppc == 9))

pre_hanford = oppc
pre_hanford[tank_index] = 7
pre_hanford[backfill_index] = 7

fout = open(pre_hanford_zon,'w')
fout.write("\n".join(map(str,pre_hanford)))
fout.close()
