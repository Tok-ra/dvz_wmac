## here is to

import numpy as np
import matplotlib.pyplot as plt
import glob
"""

"""


setup_dir = "/people/song884/wmac/fy18/fine_model_setup/watercontent/scale/"
ss_vga = np.genfromtxt(glob.glob(setup_dir+"*ss_vga.dat")[0])
oppc_vga = np.genfromtxt(glob.glob(setup_dir+"*oppc_vga.dat")[0])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(ss_vga[ss_vga > 10], bins=100)
ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
ax.set_ylabel("Frequency")
ax.set_xlabel('Alpha')
fig.tight_layout()
fig.set_size_inches(5, 5)
fig.savefig(setup_dir+"ss_vga.png", dpi=600, transparent=False)
plt.clf()
fig.clf()


mlr_vga = np.genfromtxt(
    "/people/song884/wmac/fy18/fine_model_setup/watercontent/coarse_params/vga.dat")
mlr_vga2 = np.genfromtxt(
    "/people/song884/wmac/fy18/fine_model_setup/watercontent/coarse_params/vga2.dat")

# nx = 89

# ny = 93
# nz = 330
# output = np.repeat(0.036, nx*ny*nz)
# fout = open(
#     "/people/song884/wmac/fy18/fine_model_setup/watercontent/scale/vga2.dat", 'w')
# fout.write("\n".join(map(str, output)))
# fout.close()
