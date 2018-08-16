#!/bin/bash -l

module remove python*
module load python/anaconda3.6

scripts_dir=/people/song884/github/dvz_wmac/facies/

nreaz=5
for ireaz in $(seq 1 $nreaz)
do
    echo $ireaz
    s_ireaz=$(printf "%03d" $ireaz)
    python3 $scripts_dir"mapping_zonation.py" \
    	    /people/song884/wmac/fy18/fine_model_setup/ehm/wma_c_pre_hanford_ehm_89x93x330.zon \
    	    /people/song884/wmac/fy18/fine_model_setup/facies/scale/renum_"$s_ireaz".ups \
    	    /people/song884/wmac/fy18/fine_model_setup/facies/wma_c_pre_hanford_facies"$s_ireaz"_89x93x330.zon \
    	    "5,6,7" \
	    "4"

    python3 $scripts_dir"mapping_zonation.py" \
    	    /people/song884/wmac/fy18/fine_model_setup/ehm/wma_c_oppc_ehm_89x93x330.zon \
    	    /people/song884/wmac/fy18/fine_model_setup/facies/scale/renum_"$s_ireaz".ups \
    	    /people/song884/wmac/fy18/fine_model_setup/facies/wma_c_oppc_facies"$s_ireaz"_89x93x330.zon \
    	    "5,6,7" \
	    "4"
done



