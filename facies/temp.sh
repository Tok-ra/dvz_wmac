#!/bin/bash -l

# ---- this scripts is converted from MLR's csh
# generate the zonation file for facies based WMAC model

module remove tecplot*
module load tecplot/2015r2


scripts_dir=/people/song884/github/dvz_wmac/facies/
setup_dir=/people/song884/wmac/fy18/fine_model_setup/facies/scale/


#--- convert sisim outputs to stomp zonation file
#!!!!!!!!!!!!!!!!! double check if the remapping of material ids is correct
module remove python*
module load python/2.7.8
python $scripts_dir"extract_sisim_v2.py"
