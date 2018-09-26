# SUMMARY:      read water moisture data cleaned by intera
# USAGE:
# ORG:          Pacific Northwest National Laboratory
# AUTHOR:       Xuehang Song
# E-MAIL:       xuehang.song@pnnl.gov
# ORIG-DATE:    Step-2018
# DESCRIPTION:
# DESCRIP-END.
# COMMENTS:
#
# Last Change: 2018-09-17

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pre_krig_csv = "/people/song884/wmac/fy18/ROCSAN_Moisture_Geology/Moisture_Database_files/7_One_ft_Interval_Max_to_Krig.csv"
img_dir = '/people/song884/wmac/fy18/fine_model_setup/watercontent/'

# xpiv = 574667.0
# ypiv = 136453.0
# deg = -45.0
# xoffset = -1.85
# yoffset = 8.0
# rot = deg*np.pi/180.0

# x = 574762.1
# y = 136464

# xdis = x - xpiv
# ydis = y - ypiv
# x_new = xdis*np.cos(rot) + ydis*np.sin(rot) + xpiv + xoffset
# y_new = -xdis*np.sin(rot) + ydis*np.cos(rot) + ypiv + yoffset


wm_data = pd.read_csv(pre_krig_csv)

## wm_loc = wm_data.iloc[:, [0, 1, 2]].drop_duplicates()
wm_loc = wm_data.drop_duplicates(subset="WELL_ID").iloc[:, [0, 1, 2]]


imgfile = img_dir+"wm_loc.png"
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(wm_loc.iloc[:, 1],
           wm_loc.iloc[:, 2],
           s=1, color="darkblue")
# ax.set_title(sample_name[sample_index], fontsize=20)
# ax.set_ylabel('Scale factor (-)', fontsize=20)
# ax.set_xlabel('# sample', fontsize=20)
# ax.tick_params(axis="both", which="major", labelsize=20)
# ax.tick_params(axis="both", which="minor", labelsize=20)
fig.set_size_inches(4, 3)
fig.tight_layout()
fig.savefig(imgfile, bbox_inches=0)
plt.close(fig)
