**eSTOMP constant**  fLyMd-mAkEr

> gravity: 9.81  
> water density: 998.32  
> air pressure: 101325  

# DVZ WMA-C FY2018

## Target 
1) Remap material types and parameters used in PNNL-24740 to a finer model, this finer model is developed by Intera with more details in shape of geologic units.  
2) Rerun the simulation and compare results from 4 models (EHM, two facies based, and one water content based model)  

## Need to 
1) Generate/compare new source regions/boundaries for the refined grid 
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
> **op** operational period for **Tank residual scenario (not included)**
> **pc** post-closure period for **Tank residual scenario (not included)**

## Summary of case setup

### 1. model zonation ###
**In MLR's base model, there is no tanks in zonation file, might be a different setup?**
#### 1.1 EHM model ####

> the original file was sent by Nazmul Hasan (Intera) on 06/28/2018 as "newgridehm89x93x330original.zon"  
> this zonation is for past leak simulations

Based on Intera's refined zonation file. Two zonation files are created for EHM model  
1. pre_hanford: "wma_c_pre_hanford_ehm_89x93x330.zon"  
   replace all tanks and backfills with H1 in Intera's file  
   **change_oppc_zonation_to_hanford.py**
2. pc,op,oppc:  "wma_c_oppc_ehm_89x93x330.zon",this is the same as Intera's file  

#### 1.2 Facies Models ####

##### 1.2.1 sisim realization #####

Regenerate the facies realizations using Zhuangshuang (Jason) Hou's files  

> Initial thoughts was to use Jason's SISIM.exe files  
> while it failed since there's is a fixed array limit for nx, ny, nz in sisim.inc  
> We don't have the orginal source code to recomplile the sisim.exe  
> So I took the lastest GSLIB from www.gslib.com and compile new sisim (linux version)  
> The lastest GSLIB produce the same results as the old one, the major difference is the lastest Gslib use allocatable array  
> The format of the input files were slightly different and modifiled.  

sisim dimention  
> 148     0.0     5  
> 160     0.0     5  
> 464    95.0    0.25  

##### 1.2.2 map the facies to zonation #####

The orginal workflow is  

> 1 The sisim realization is generated on a uniform grids for three new facies (runsisim.pl).  
> 2 use **replace_v2.pl** to replace H1, H2 sand, H2 coarse sand with the three new facies in the uniform grids.  
> 3  **ups_facies_cellfaces.x** to do the scaling from uniform grids to nonuniform grids  
> 4  **insert_tanks2.py** to add tanks   
> 5 **ups_facies.x** to generate files only for plotting and then use Tecplot to generate figure.

The new workflow is

> 1 The sisim realization is generated on a uniform grids for three new facies (runsisim.pl).  
> 2  **ups_facies_cellfaces.x** to do the scaling   
> 3 use **replace_v2.pl** to replace H1, H2 sand, H2 coarse sand with the three new facies in the nonuniform grids.  
> 4 repeat 3 for prehanford and oppc period  

*The grids setup in facies/grid.gslib of coarse scale model has a bug*  

> facies/grid.gslib   
> Cartesian,  
> 148,160,116,  
> 574656,m,148@5,m,  
> **136454**,m,160@5,m,  
> 95,m,116@1,m,

*it should be*  

> watercontent/ups/grid.gslib  
> Cartesian,  
> 148,160,116,  
> 574656,m,148@5,m,  
> **136464**,m,160@5,m,  
> 95,m,116@1,m,  

*This has been confirmed by MLR*  

The final coordinates used is  

> watercontent/ups/grid.gslib  
> Cartesian,  
> 148,160,340,  
> 0,m,148@5,m,  
> 0,m,160@5,m,  
> 110,m,340@0.3,m,  

One import tips to use ups_facies_cellfaces.f90  
The number of indicator classes should be n+1  

> This is a potential bug after MLR revised the original scripts for 0 material
#### 1.3 MLR's water content model ####




#### 1.4 Intera's binned models ####
Intera sent two set of soil moisture model

> (1) forwarded by Vicky 06/27/2018, email title "Intera zonation file", file name "n**ew_grid_heterogenous_89*93*330.zon**"  
> (2) forward by Vikcy 06/20/2018, email title **"eSTOMP installation testing on Tellus"**,file name "**new_grid_heterogeneous_vz_ss.zon**" and **new_grid_heterogeneous_vz.zon**

(1) and (2) was compared using script bin/check_zonation.py, the results clearly showd the units "Aquifer" (1) was set to be inactive (0) in set (2), and the zonation file in **"new_grid_heterogenous_89*93*330.zon"** is for oppc period.  

In the simulation, use **new_grid_heterogenous_89*93*330.zon** in (2) is used for oppc period  
the difference between "**new_grid_heterogeneous_vz_ss.zon**" and **new_grid_heterogeneous_vz.zon** in (1)  was extracted and assigned to **new_grid_heterogenous_89*93*330.zon** in (2) to create a new zonation file named as **new_grid_heterogenous_89*93*330.zon**, this file is used for ss period.





### 2. initial condtion   

The revision is made based the following differences between the fine and coarse model  
a. the fine scale model is thiner than coarse model  

> fine scale model z = [110,209.99]  
> coarse scale model z = [95,211]  
> This requires to change the reference points for initial condtion, side condtions  

b. the z index changed  

> coarse scale model z = [1,89]  
> fine scale model z = [1,330]  
> requires to change anything related to Z index  


##### 2.1 Coarse scale model #####

IC was defined by  

> Aqueous Pressure, 331472.7,Pa,,,,,-9793.5192,1/m,1,89,1,93,1,89,  

Based on this IC  

> z[1] = 97.5m  
> The water table is at (331472.7-101325)/9793.52+97.5 = 121  
> At z=110.1515m (bottom cell center of fine scale model), the pressure is 331472.7-9793.52*(110.1515-97.5) = 207569.98172000004  

##### 2.2 Setup of Fine scale model #####  

IC was defined by  
> Aqueous Pressure, 207569.98,Pa,,,,,-9793.5192,1/m,1,89,1,93,1,330,  


The following part is deprecated, as it's reivsed based on coarse scale EHM model  
Now we follows setups from coarse scale facies model  

//////////////////////////////////////////////////////////////////////////////////////////
The revision is made based the following differences between the fine and coarse model  
a. the fine scale model is thiner than coarse model  

> fine scale model z = [110,209.99]  
> coarse scale model z = [95,211]  
> This requires to change the reference points for initial condtion, side condtions  

b. the z index changed  

> fine scale model z = [1,95]  
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
///////////////////////////////////////////////////////////////////////////////////////

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

Then the pressure at the center of bottom cell (110.1515 m)  along west boundary is  

> 101325+(122.25-110.1515)*9793.52 = 219811.9017 pa  

the pressure at the center of bottom cell (110m) along east boundary is  

> 101325+(122.235242-110.1515)*9793.52 = 219667.36895 pa  

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

### 5. Other changes
### the final tank shapes were taken from intera
1) Change tank regions to curved domes (done by Mark)  
   Use insert_tanks2.py in. /facies: generate tank regions with curved domes.  
2) Make tank regions inactive   
   Change material id of tanks from 8 to 0 and comment out corresponding sections in input files  

======================================================================================  

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

**ups/ups_theta.x** to convert gslib to estomp zonation files for water content data  

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
