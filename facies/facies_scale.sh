#!/bin/bash -l

# ---- this scripts is converted from MLR's csh
# generate the zonation file for facies based WMAC model

module remove tecplot*
module load tecplot/2015r2


scripts_dir=/people/song884/github/dvz_wmac/facies/
setup_dir=/people/song884/wmac/fy18/fine_model_setup/facies/scale/


#--- convert sisim outputs to stomp zonation file
#!!!!!!!!!!!!!!!!! double check if the remapping of material ids is correct
# module remove python*
# module load python/2.7.8
# python $scripts_dir"extract_sisim_v2.py"


gfortran -o $setup_dir"ups_facies_cellfaces.x" $scripts_dir"/ups_facies_cellfaces.f90"


# #--- 001
cd $setup_dir
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist1" >> temp
./ups_facies_cellfaces.x < temp

# # #--- 002
cd $setup_dir
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist2" >> temp
./ups_facies_cellfaces.x < temp


# # #--- 003
cd $setup_dir
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist3" >> temp
./ups_facies_cellfaces.x < temp


# # #--- 004
cd $setup_dir
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist4" >> temp
./ups_facies_cellfaces.x < temp
rm temp


# # #--- 005
cd $setup_dir
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist5" >> temp
./ups_facies_cellfaces.x < temp
rm temp

# mapping to 
