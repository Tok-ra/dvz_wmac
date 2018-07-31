**eSTOMP constant**  

> gravity: 9.81  
> water density: 998.32  
> air pressure: 101325  

# DVZ WMA-C FY2018

## Target 
1) Remapping material types and parameters used in PNNL-24740 to a finer model, this finer model is developed by Intera with more details in shape of geologic units.  
2) Rerun the simulation and compare results from 4 models (EHM, two facies based, and one water content based model)  


## Model simulation scenario
Tank residual scenario: pre-hanford (ss); operational (op), and post-closure (pc)  
thank leak scenario: pre-hanford (ss); operational-post-closure (oppc)  

## Summary of case setup
### EHM model
#### 1. zonation file 

> the original file was sent by Nazmul Hasan (Intera) on 06/28/2018 as "newgridehm89x93x330original.zon"  
> this zonation is for past leak simulations

Based on Intera's refined zoantion file. Two zonation files are created for EHM model  
1. pre_hanford: "wma_c_pre_hanford_ehm_89x93x330.zon"  
   replace all tanks and backfills with H1 in Intera's file  
   **change_oppc_zonation_to_hanford.py**
2. pc,op,oppc:  "wma_c_oppc_ehm_89x93x330.zon",this is the same as Intera's file 
## do we need prepare seperated one to distingguish pre/op??? 

#### 2. boundary condtions
The revisions are based on two differences between the fine and coarse model  
a. the fine scale model is thiner than coarse model  

> fine scale model z = [110,209.99]  
> coarse scale model z = [95,211]  
> This requires to change the reference points for initial condtion, side condtions  

b. the z index changed  

> fine scale model z = [1,89]  
> scale model z = [1,330]  
> requires to change anything related to Z index  

##### 2.1 revision for Initial Condition (IC) #####

###### Coarse scale model ######

IC is set using two condtions, saturated part and unsaturated part  

> Aqueous Pressure,325106.932,Pa,,,,,-9793.52,1/m,1,89,1,93,1,17,  
> Aqueous Pressure, 73000.,Pa,,,,,-97.9352,1/m,1,89,1,93,18,95,  

For the saturated part.  

> z[1] = 97.5m  
> The water table is at (325106.932-101325)/9793.52+97.5 = 120.35m  
> At z=110.1515m, the pressure is "325106.932-9793.52(110.1515-97.5)=201204.21372  

For the unsaturated part.  

> z[18] = 123.25m  
> At z=123.1805m, the pressure is 73000-97.9352(123.1805-123.25)=73006.80650  

###### Setup of Fine scale model ######

> Aqueous Pressure,201204.21372,Pa,,,,,-9793.52,1/m,1,89,1,93,1,43,  
> Aqueous Pressure,73006.80650,Pa,,,,,-97.9352,1/m,1,89,1,93,44,330,  

For the saturated part.  

> z[1] = 110.1515m  
> The water table is at (201204.21372-101325)/9793.52+110.1515 = 120.35m  

For the unsaturated part  

> z[44] = 123.1805m  
   
##### 2.2 revision for uppper recharge boundary  #####

###### remap the recharge area ######

**upper_lst.py** is written with **wmac_bc.py** as reference.  
**upper_lst.py** use polygon functions from shapele package  


###### pre_hanford period ######

3.5mm/yr for all polygons  
remove tank areas from MLR's input, the original setup might be reducdant  

# coarse model only has one resurface_file, but there're two resurface polygons #
use two resurface file in the fine scale model, need check with MLR  


###### oppc period ######

##### 2.3 revision for side boundary  #####

###### pre_hanford period ######
Map MLR and ZFZ's setup to the new grids  
from MLR and ZFZ's input file:  

> From Bill McMahon:  
> dh/dx {northwest - southeast}  =  0.2000E-04 m/m (= 0.195870 pa/m)  
> distance(I-direction) = 737.90  m  
> MLR and ZFZ: Water table elev is at 122.25 m  
> GW elevation at west boundary = 122.25 m  
> GW elevation at east boundary = 122.25 - 737.90*2E-5 = 122.235242 m  

Then the pressure at the center of bottom cell (110m)  along west boundary is  

> 101325+(122.25-110)*9793.52 = 221295.62 pa  

the pressure at the center of bottom cell (110m) along east boundary is  

> 101325+(122.235242-110)*9793.52 = 221151.08723184 pa  

It should be fine to just use entire west/east boundary as seepage  
however, here I still follow MLR and ZFZ's setup to define the saturated region  

> Both east/east lst file end at  z[41] = 122.2715

**side_lst.py** is used to generate the **westaquifer.lst** and **eastaquifer.lst**


#### 3. output
revise the aquifer surface flux coords to keep consistant with the finer grid
**Need double check the screen interal of 299-E27-14, 299-E17-15**



# Need attension:how MLR choose the model origin? why it's slightly different from xpiv and ypiv #

## Need to 
1) Generate/compare new source regions for the refined grid 
2) Replace the zonation files in the EHM model with intera one
3) Regenerate zonation files for facies case
4) with 3) results, generate zonation files for water content model. 

## Other changes
### the final tank shapes were taken from intera
1) Change tank regions to curved domes (done by Mark)  
   Use insert_tanks2.py in. /facies: generate tank regions with curved domes.  
2) Make tank regions inactive   
   Change material id of tanks from 8 to 0 and comment out corresponding sections in input files  

## Input files from Mark
### InteraFiles
Inputs from intera, including input deck, zonation file, source region 

### Simulations
No file
### Tank_polygons
Use make_poly.py: read tank coordinates and elevation, generate polygon points for each tanks

### bc
Use wmac_bc.py: read in zonation file, face file, surface area polygon; generate different source region.

### Facies
Post-processing of SISIM
extract_sisim.py to read SISIM file and generate zonation file (without tanks), the output resolution of zonation files is the same as SISIM configuration, which is higher than final model setup in this case.
Modify zonation file 
The workflow is controlled by a csh file.
1) ups_facies_cellfaces.x to do the scaling 
2) insert_tanks2.py to add tanks (new from last meeting)
3) ups_facies.x to generate files only for plotting and then use Tecplot to generate figure.

### Watercontent
Scale water content data
ups/ups_theta.x to convert gslib to pflotran zonation files for water content data
Convert water content data to hydraulic conductivity 
Param/wmac_param_step1.py apply the PTF (use srf to regenerate material)
Param/wmac_param_step3.py write estomp input (borrow tanks locations from facies case)

### Data folders
1) Surfaces 
Store some Tecplot files to generate geologic surface
2) Theta
Store results from GSLIB 



=========================================================================================================================
## This is the index of updated model.
upr/                 #upr model <br />
upr/base_ss          #model spin-up for base model, revised from upr_base_ss <br />
upr/base_oppc        #oppc simulation, revsied from upr_base_oppc <br />
upr/facies003_ss     #model spin-up for facies-based model (realization 003) <br />
upr/facies003_oppc   #oppc simulation for facies-based model (realization 003) <br />
upr/facies004_ss     #model spin-up for facies-based model (realization 004) <br />
upr/facies004_oppc   #oppc simulation for facies-based model (realization 004) <br />
