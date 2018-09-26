# SUMMARY:      map zonation to new material
# USAGE:        this is only a temperoary tool to read grids from two models
# ORG:          Pacific Northwest National Laboratory
# AUTHOR:       Xuehang Song
# E-MAIL:       xuehang.song@pnnl.gov
# ORIG-DATE:    July-2018
# DESCRIPTION:
# DESCRIP-END.
# COMMENTS:
#
# Last Change: 2018-08-05

import sys
import numpy as np
import re

template_zon = sys.argv[1]
mapping_zon = sys.argv[2]
output_zon = sys.argv[3]
ori_value = sys.argv[4]
map_drift = sys.argv[5]

# template_zon = "/people/song884/wmac/fy18/fine_model_setup/ehm/wma_c_pre_hanford_ehm_89x93x330.zon"
# mapping_zon = "/people/song884/wmac/fy18/fine_model_setup/facies/scale/renum_001.ups"
# output_zon = "/people/song884/wmac/fy18/fine_model_setup/facies/wma_c_pre_hanford_facies001_89x93x330.zon"
# ori_value = "5,6,7"

ori_value = np.asarray([int(x) for x in ori_value.split(",")])
print(ori_value)

map_drift = np.asarray([int(x) for x in map_drift.split(",")])
print(map_drift)

with open(template_zon) as f:
    template = f.read()
template = np.asarray([int(x) for x in re.split(" |\n", template) if x])

with open(mapping_zon) as f:
    mapping = f.read()
mapping = np.asarray([int(x) for x in re.split(" |\n", mapping) if x])

output = template

for ivalue in ori_value:
    value_index = np.where(template == ivalue)
    output[value_index] = mapping[value_index]+map_drift

fout = open(output_zon, 'w')
fout.write("\n".join(map(str, output)))
fout.close()
