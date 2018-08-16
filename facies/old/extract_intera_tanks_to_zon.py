# ----------------
# extract tank location from intera zonation file and
# insert the tanks into other zonation file
# written by XHS 06/18/2018


import numpy as np

setup_dir = "/people/song884/wmac/fy18/fine_model/model_setup/facies/"
intera_zon = setup_dir+"new_grid_heterogeneous_vz.zon"

old_zon = setup_dir+"sgrfacies_renum_003.ups"
new_zon = setup_dir+"sgrfacies_renum_003_plustanks.ups"

old_zon = setup_dir+"sgrfacies_renum_004.ups"
new_zon = setup_dir+"sgrfacies_renum_004_plustanks.ups"


nx = 89
ny = 93
nz = 330

# ---- here we're using materials from sisim realizations
# ---- need compare intera model with sisim
intera_material = np.genfromtxt(intera_zon).flatten(order="C").astype(int)
intera_material = intera_material.reshape((nx, ny, nz), order="F")
intera_material_0 = np.asarray(np.where(intera_material == 0))
tank_cells = []
for ipoint in range(len(intera_material_0[0, ])):
    bottom_material = intera_material[intera_material_0[0, ipoint],
                                      intera_material_0[1, ipoint],
                                      np.arange(0,intera_material_0[2, ipoint])]
    top_material = intera_material[intera_material_0[0, ipoint],
                                   intera_material_0[1, ipoint],
                    np.arange(intera_material_0[2, ipoint]+1, nz)]
    if (any(bottom_material != 0) and any(top_material != 0)):
        print(ipoint)
        tank_cells.append(ipoint)
tank_index = intera_material_0[:,tank_cells]
tank_index = tank_index[0,:]+tank_index[1,:]*nx+tank_index[2,:]*nx*ny

old_material = np.genfromtxt(old_zon).flatten(order="C").astype(int)
new_material = old_material
new_material[tank_index] = 0


fout = open(new_zon,'w')
fout.write("\n".join(map(str,new_material)))
fout.close()


# grids = np.meshgrid(range(nz), range(ny), range(nx),indexing="ij")
# grids = np.array(grids).reshape(3,nx*ny*nz)
# grids = grids[(2,1,0),:]

