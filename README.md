# DVZ WMA-C
## Target
1) Remapping material types and parameters used in PNNL-24740 to a finer model, this finer model is developed by Intera with more details in shape of geologic units.
2) Rerun the simulation and compare results from 4 models (EHM, two facies based, and one water content based model)

## Other changes to the model
1) Change tank regions to curved domes (done by Mark)
     Use insert_tanks2.py in. /facies: generate tank regions with curved domes.
2) Make tank regions inactive 
     Change material id of tanks from 8 to 0 and comment out corresponding sections in input files

## Workflow to generate new models
1) Generate/compare new source regions for the refined grid 
2) Replace the zonation files in the EHM model with intera one
3) Regenerate zonation files for facies case
4) with 3) results, generate zonation files for water content model. 

## Input files from Mark
### InteraFiles
Inputs from intera, including input deck, zonation file, source region 

### Simulations
No file

### Tank_polygons
Use make_poly.py: read tank coordinates and elevation, generate polygon points for each tanks

### BC
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
