# SUMMARY:      change_oppc_zonation_to_prehanford
# USAGE:        change z index of lst files
# ORG:          Pacific Northwest National Laboratory
# AUTHOR:       Xuehang Song
# E-MAIL:       xuehang.song@pnnl.gov
# ORIG-DATE:    July-2018
# DESCRIPTION:
# DESCRIP-END.
# COMMENTS:     
#
# Last Change: 2018-07-24


import glob
import numpy as np

old_lst = np.sort(glob.glob("/people/song884/wmac/fy18/fine_model/model_setup/ehm/recharge_lst_old/*lst"))
for ilst in old_lst:
    old_data = np.genfromtxt(ilst).astype(int)
    print(np.mean(old_data,axis=0))
