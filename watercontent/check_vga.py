## here is to

import numpy as np
import matplotlib.pyplot as plt
import glob
"""

"""


setup_dir = "/people/song884/wmac/fy18/fine_model_setup/watercontent/scale/theta001_ss_"
param_ss = dict()
param_ss["vga"] = np.genfromtxt(setup_dir+"vga.dat")
param_ss["ksx"] = np.genfromtxt(setup_dir+"ksx.dat")
param_ss["ksy"] = np.genfromtxt(setup_dir+"ksy.dat")
param_ss["ksz"] = np.genfromtxt(setup_dir+"ksz.dat")


# ss_vga = np.genfromtxt(glob.glob(setup_dir+"*ss_vga.dat")[0])
# oppc_vga = np.genfromtxt(glob.glob(setup_dir+"*oppc_vga.dat")[0])

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.hist(ss_vga[ss_vga > 10], bins=100)
# ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
# ax.set_ylabel("Frequency")
# ax.set_xlabel('Alpha')
# fig.tight_layout()
# fig.set_size_inches(5, 5)
# fig.savefig(setup_dir+"ss_vga.png", dpi=600, transparent=False)
# plt.clf()
# fig.clf()

# mlr_vga = np.genfromtxt(
#     "/people/song884/wmac/fy18/fine_model_setup/watercontent/coarse_params/vga.dat")
# mlr_vga2 = np.genfromtxt(
#     "/people/song884/wmac/fy18/fine_model_setup/watercontent/coarse_params/vga2.dat")

model_param_dir = "/people/song884/wmac/fy18/fine_model_setup/watercontent/coarse_params/used_in_model/"
script_param_dir = "/people/song884/wmac/fy18/fine_model_setup/watercontent/coarse_params/generated_from_scripts/"

param_model = dict()
param_script = dict()


param_script["vga"] = np.genfromtxt(script_param_dir+"vga.dat")
param_script["ksx"] = np.genfromtxt(script_param_dir+"ksx.dat")
param_script["ksy"] = np.genfromtxt(script_param_dir+"ksy.dat")
param_script["ksz"] = np.genfromtxt(script_param_dir+"ksz.dat")
param_script["ksx_tanks"] = np.genfromtxt(script_param_dir+"ksx_tanks.dat")
param_script["ksy_tanks"] = np.genfromtxt(script_param_dir+"ksy_tanks.dat")
param_script["ksz_tanks"] = np.genfromtxt(script_param_dir+"ksz_tanks.dat")
param_script["zon"] = np.genfromtxt(script_param_dir+"zonation.dat")


param_model["vga"] = np.genfromtxt(model_param_dir+"vga2.dat")
param_model["ksx"] = np.genfromtxt(model_param_dir+"ksx.dat")
param_model["ksy"] = np.genfromtxt(model_param_dir+"ksy.dat")
param_model["ksz"] = np.genfromtxt(model_param_dir+"ksz.dat")
param_model["ksx_tanks"] = np.genfromtxt(model_param_dir+"ksx_tanks.dat")
param_model["ksy_tanks"] = np.genfromtxt(model_param_dir+"ksy_tanks.dat")
param_model["ksz_tanks"] = np.genfromtxt(model_param_dir+"ksz_tanks.dat")
param_model["zon"] = np.genfromtxt(model_param_dir+"zonation.dat")

max(param_model["vga"][np.where(param_script["vga"] >= 0.25)])
min(param_model["vga"][np.where(param_script["vga"] >= 0.25)])


ksx_diff_index = np.where(param_model["ksx"] != param_script["ksx"])
ksy_diff_index = np.where(param_model["ksy"] != param_script["ksy"])
ksz_diff_index = np.where(param_model["ksz"] != param_script["ksz"])

min(param_model["ksx"][ksx_diff_index]/param_script["ksx"][ksx_diff_index])
max(param_model["ksx"][ksx_diff_index]/param_script["ksx"][ksx_diff_index])
np.unique(param_model["ksx"][ksx_diff_index])
np.unique(param_script["ksx"][ksx_diff_index])

np.unique(param_model["ksx"][ksx_diff_index] /
          param_script["ksx"][ksx_diff_index])
min(param_model["ksz"][ksz_diff_index]/param_script["ksz"][ksz_diff_index])
max(param_model["ksz"][ksz_diff_index]/param_script["ksz"][ksz_diff_index])
np.unique(param_model["ksz"][ksz_diff_index])
np.unique(param_script["ksz"][ksz_diff_index])


# scripts
# for ikey in param_script.keys():
#     param_script[ikey] = np.asarray(
#         [np.float(np.format_float_scientific(x, exp_digits=1)) for x in param_script[ikey]])
# # model
# for ikey in param_model.keys():
#     param_model[ikey] = np.asarray(
#         [np.float(np.format_float_scientific(x, exp_digits=1)) for x in param_model[ikey]])

# nx = 89

# ny = 93
# nz = 330
# output = np.repeat(0.036, nx*ny*nz)
# fout = open(
#     "/people/song884/wmac/fy18/fine_model_setup/watercontent/scale/vga2.dat", 'w')
# fout.write("\n".join(map(str, output)))
# fout.close()
