#!/bin/bash -l

# ---- this scripts is converted from MLR's csh
# generate the zonation file for facies based WMAC model

module remove tecplot*
module load tecplot/2015r2


scripts_dir=/people/song884/github/dvz_wmac/facies/
setup_dir=/people/song884/wmac/fy18/fine_model/model_setup/facies/

cd $setup_dir


#--- convert sisim outputs to stomp zonation file
#!!!!!!!!!!!!!!!!! double check if the remapping of material ids is correct
module remove python*
module load python/2.7.8
python extract_sisim.py


#--- do the scaling
#!!!!!!!!!!!!!!!!! modify model dimensions in ups_facies_cellfaces.f90
gfortran -o ups_facies_cellfaces.x $scripts_dir"/ups_facies_cellfaces.f90"

#--- 003
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist1" >> temp
./ups_facies_cellfaces.x < temp

#--- 004
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist2" >> temp
./ups_facies_cellfaces.x < temp
rm temp

#--- extract tanks from Intera files
#--- revise the zonation file
#--- module remove python*
#--- module load python/anaconda3.6
python $scripts_dir"extract_intera_tanks_to_zon.py"
python $scripts_dir"extract_intera_tanks_to_zon.py"
mv sgrfacies_renum_003_plustanks.ups sgrfacies_renum_003_plustanks.zon
mv sgrfacies_renum_004_plustanks.ups sgrfacies_renum_004_plustanks.zon


#--- calling ups_facies just to write out tecplot files for checking results.
#--- no upscaling/downscaling is performed since input and output grids are the same.
#--- ups_facies will recreate *.ups files that were renamed above.

gfortran -o ups_facies.x $scripts_dir"/ups_facies.f90"
rm temp
echo "grid.stompmod" >> temp
echo "grid.stompmod" >> temp
echo "y" >> temp
echo "filelist3" >> temp
./ups_facies.x < temp
mv grid-in.tec real003-grid-in.tec
mv grid-out.tec real003-grid-out.tec
preplot real003-grid-in.tec
preplot real003-grid-out.tec
rm temp
echo "grid.stompmod" >> temp
echo "grid.stompmod" >> temp
echo "y" >> temp
echo "filelist4" >> temp
./ups_facies.x < temp
mv grid-in.tec real004-grid-in.tec
mv grid-out.tec real004-grid-out.tec
preplot real004-grid-in.tec
preplot real004-grid-out.tec
rm temp
