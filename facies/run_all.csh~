# initial upscaling and writing of cell face coordinates 
module load tecplot
module load python/2.7.8
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist1" >> temp
./ups_facies_cellfaces.x < temp
rm temp
echo "grid.stompmod" >> temp
echo "grid.gslib" >> temp
echo "n" >> temp
echo "filelist2" >> temp
./ups_facies_cellfaces.x < temp
rm temp
#
# overwriting regions occupied by tanks
#./insert_tanks.py
#
# this version accounts for curvature of tank domes 
./insert_tanks2.py
mv sgrfacies_renum_003_plustanks.ups sgrfacies_renum_003_plustanks.zon
mv sgrfacies_renum_004_plustanks.ups sgrfacies_renum_004_plustanks.zon
#
# calling ups_facies just to write out tecplot files for checking results.
# no upscaling/downscaling is performed since input and output grids are the same.
# ups_facies will recreate *.ups files that were renamed above.
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
