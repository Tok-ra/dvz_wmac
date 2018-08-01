Questions  
do we need prepare seperated one to distingguish pre/op???  
coarse model only has one resurface_file, but there're two resurface polygons  
use two resurface file in the fine scale model, need check with MLR  
same side boudnary for pre-hanford and oppc period?  
There should be scripts/data to automaticlly generate the sources, ask MLR  
Need attension:how MLR choose the model origin? why it's slightly different from xpiv and ypiv  


**eSTOMP constant**  

> gravity: 9.81  
> water density: 998.32  
> air pressure: 101325  

# DVZ WMA-C FY2018

## Target 
1) Remapping material types and parameters used in PNNL-24740 to a finer model, this finer model is developed by Intera with more details in shape of geologic units.  
2) Rerun the simulation and compare results from 4 models (EHM, two facies based, and one water content based model)  

## Need to 
1) Generate/compare new source regions for the refined grid 
2) Replace the zonation files in the EHM model with intera one
3) Regenerate zonation files for facies case
4) with 3) results, generate zonation files for water content model. 

## Model simulation scenario
Tank residual scenario: pre-hanford (ss); operational (op), and post-closure (pc)  
Tank leak scenario: pre-hanford (ss); operational-post-closure (oppc)  

There were multiple versions of model inputs  
My revision is based on the inputs in folder **simu_upr2** and **simu_tank_residual2**  
**simu_upr2** tank leak scenario  
**simu_tank_residual2** tank residual scenario   

Four groups of simulations are conducted  

> **upr_ss** model spin-up period (from 0~1944) for both scenario  
> **upr_oppc** operational-post-closure period for **tank leak scenario**  
> **op** operational period for **Tank residual scenario**
> **pc** post-closure period for **Tank residual scenario**


## Summary of case setup

### 1. model zonation ###
**In MLR's base model, there is no tanks in zonation file, might be a mistake.**
#### 1.1 EHM model ####

> the original file was sent by Nazmul Hasan (Intera) on 06/28/2018 as "newgridehm89x93x330original.zon"  
> this zonation is for past leak simulations

Based on Intera's refined zoantion file. Two zonation files are created for EHM model  
1. pre_hanford: "wma_c_pre_hanford_ehm_89x93x330.zon"  
   replace all tanks and backfills with H1 in Intera's file  
   **change_oppc_zonation_to_hanford.py**
2. pc,op,oppc:  "wma_c_oppc_ehm_89x93x330.zon",this is the same as Intera's file 

#### 1.2 Facies Models ####
**I mainly used MLR's scripts to genearte the facies zonation file**  
The grids setup in facies/grid.gslib of coarse scale model setup has a bug

> facies/grid.gslib   
> Cartesian,  
> 148,160,116,  
> 574656,m,148@5,m,  
> **136454**,m,160@5,m,  
> 95,m,116@1,m,

it should be 

> watercontent/ups/grid.gslib  
> Cartesian,  
> 148,160,116,  
> 574656,m,148@5,m,  
> **136464**,m,160@5,m,  
> 95,m,116@1,m,  

This has been confirmed by MLR.


### 2. initial condtion ###


The revision is maded based the following differences between the fine and coarse model  
a. the fine scale model is thiner than coarse model  

> fine scale model z = [110,209.99]  
> coarse scale model z = [95,211]  
> This requires to change the reference points for initial condtion, side condtions  

b. the z index changed  

> fine scale model z = [1,89]  
> scale model z = [1,330]  
> requires to change anything related to Z index  


##### 2.1 Coarse scale model #####

IC is defined by using two condtions, saturated part and unsaturated part  

> Aqueous Pressure,325106.932,Pa,,,,,-9793.52,1/m,1,89,1,93,1,17,  
> Aqueous Pressure, 73000.,Pa,,,,,-97.9352,1/m,1,89,1,93,18,95,  

For the saturated part.  

> z[1] = 97.5m  
> The water table is at (325106.932-101325)/9793.52+97.5 = 120.35m  
> At z=110.1515m, the pressure is "325106.932-9793.52(110.1515-97.5)=201204.21372  

For the unsaturated part.  

> z[18] = 123.25m  
> At z=123.1805m, the pressure is 73000-97.9352(123.1805-123.25)=73006.80650  

##### 2.2 Setup of Fine scale model #####

> Aqueous Pressure,201204.21372,Pa,,,,,-9793.52,1/m,1,89,1,93,1,43,  
> Aqueous Pressure,73006.80650,Pa,,,,,-97.9352,1/m,1,89,1,93,44,330,  

For the saturated part.  

> z[1] = 110.1515m  
> The water table is at (201204.21372-101325)/9793.52+110.1515 = 120.35m  

For the unsaturated part  

> z[44] = 123.1805m  


### 3 boundary condtions ###
   
#### 3.1 uppper recharge boundary  ####

##### 3.1.1 remap the recharge area #####
**upper_lst.py** is written with **wmac_bc.py** as reference.  
**upper_lst.py** use polygon functions from shapele package  

##### 3.1.2 pre_hanford period #####

3.5mm/yr for all polygons  
remove tank areas from MLR's input, the original setup might be reducdant  

##### 3.1.3 oppc period #####
The recharge amount was adjusted based on the coarse scale model setup  

#### 3.2 side boundary  ####
##### 3.2.1 pre_hanford period #####
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

**side_lst.py** is used to generate the **west_aquifer.lst** and **east_aquifer.lst**

##### 3.2.2 oppc period #####
the same as the prehanford period based on the coarse scale model setup  

#### 3.3 source term  ####
##### 3.3.1 pre_hanford period #####
No source term for steady state simulation period (pre-hanford)
##### 3.3.2 oppc period #####
Because the horizontal resolution doesn't change, so only change z-index to the top cell below tanks

### 4. output
revise the aquifer surface flux coords to keep consistant with the finer grid  
**Need double check the screen interval of 299-E27-14, 299-E17-15**



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
**make_poly.py**: read tank coordinates and elevation, generate polygon points for each tanks  

### bc
**wmac_bc.py**: read in zonation file, face file, surface area polygon; generate different source region  

### Facies

#### Post-processing of SISIM ####

**extract_sisim.py**:read SISIM file and generate zonation file (without tanks), the output resolution of zonation files is the same as SISIM configuration, which is higher than final model setup in this case.  

#### Modify zonation file ####

Workflow is controlled by a csh file  

> 1) **ups_facies_cellfaces.x** to do the scaling   
> 2) **insert_tanks2.py** to add tanks   
> 3) **ups_facies.x** to generate files only for plotting and then use Tecplot to generate figure.  

### Watercontent

#### Scale water content data ####

**ups/ups_theta.x** to convert gslib to pflotran zonation files for water content data  

#### Convert water content data to hydraulic conductivity ####

**Param/wmac_param_step1.py** apply the PTF (use srf to regenerate material)  
**Param/wmac_param_step3.py** write estomp input (borrow tanks locations from facies case)  

### Data folders

#### Surfaces ####

Store some Tecplot files to generate geologic surface  

#### Theta ####

Store results from GSLIB  


=========================================================================================================================
## This is the index of updated model.
**upr/**                 upr model
**upr/base_ss**          model spin-up for base model, revised from upr_base_ss  
**upr/base_oppc**        oppc simulation, revsied from upr_base_oppc  
**upr/facies003_ss**     model spin-up for facies-based model (realization 003)  
**upr/facies003_oppc**   oppc simulation for facies-based model (realization 003)  
**upr/facies004_ss**     model spin-up for facies-based model (realization 004)  
**upr/facies004_oppc**   oppc simulation for facies-based model (realization 004)  
