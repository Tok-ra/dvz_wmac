#------------------------------------------------------------
# replace.pl
#------------------------------------------------------------
# The script reads in a list of simulation files, and a index
# file with upper and lower facies to replace the simulated 
# facies in the simulation files. That is, if the values
# at the nodes are negative, the simulated values are used.
# Otherwise, the values in the index file will be used.
#
# Note1: Declare the variables in the first part of the script.
# Note2: In case of duplicate of simulated values with 
#    the index values, add a factor to the simulated values.
#-------------------------------------------------------------

#--------------------------
# (0) Variables
#---------------------------
$idfl = "blk_LayerCode_Grid.txt";       #- Index filename
$nheader1 = 1;                          #- Number of headers in $infl
$col1 = 1;                              #- Column of the index variable
$listfl = "list2.txt";                  #- List of simulation file
$nheader2 = 3;                          #- Number of headers in simulation files
$col2 = 1;                              #- Column of variable in simulation files
$factor = 9;                            #- Factor to be added to the simulated value
$outfl = "final_sisim.out";             #- Output filename
$length = 6;                            #- Length ofthe printout value
$digit = 1;                             #- Decimal of the printout value

#----------------------------
print "(1) Read the list of simulation files\n";
#----------------------------
open (LISTFL, $listfl) || die "Cannot open $listfl: $!";

$isim = 0;
@simfl = 0;
while (<LISTFL>)
{
  chomp;
  $simfl[$isim] = $_;
  $isim++;
}
close(LISTFL);

$nsim = $isim;
print "Number of simulation files: $nsim\n";

#-----------------------------
print "\n(2) Read the index file: $idfl\n";
#-----------------------------
open (IDFL, $idfl) || die "Cannot open $idfl: $!";

$irow = 0;
$idat = 0;
@id = 0;
while (<IDFL>)
{
  chomp;
  $irow++;
  if ($irow>$nheader1)
  {
    @dummy = split;
    $tmpid = $dummy[$col1-1];
    $id[$idat] = $tmpid;
    $idat++;
  }
}
close (IDFL);
$ndat1 = $idat;
print "Number of index values: $ndat1\n";

#----------------------------
print "\n(3) Generate the final files\n";
#----------------------------
for ($i=0; $i<$nsim; $i++)
{
  $isim = $i + 1;
  $tmpinfl = $simfl[$i];
  $tmpoutfl = "$outfl.$isim";
  
  print "...(3.1) Reading $tmpinfl...\n";
  open (TMPIN, $tmpinfl) || die "Cannot open $tmpinfl: $!";
  $irow = 0;
  $idat = 0;
  @simval = 0;
  while (<TMPIN>)
  {
    chomp;
    $irow++;
    if ($irow>$nheader2)
    {
      @dummy = $_;
      $simval[$idat] = $dummy[$col2-1];
      $idat++;
    }
  }
  close (TMPIN);
  
  $ndat2 = $idat;
  if ($ndat1 != $ndat2)
  {
    die "Number of index values $ndat1 is not equal to number of simulated values $ndat2: $!";
  }
  
  print "...(3.2) Creating $tmpoutfl...\n";
  open (TMPOUT, ">$tmpoutfl") || die "Cannot create $tmpoutfl: $!";
  print TMPOUT "Simulation no.$isim: final\n";
  print TMPOUT "1\n";
  print TMPOUT "value\n";
  
  for ($idat=0; $idat<$ndat1; $idat++)
  {
    if ($id[$idat]<0)
    {
      $tmpval = $simval[$idat] + $factor;
    }
    else
    {
      $tmpval = $id[$idat];
    }
    
    printf TMPOUT "%${length}.${digit}f\n",$tmpval;
  }
   
  close (TMPOUT);
}

#-----------------------
print "\n*** END OF SCRIPT: replace_v2.pl ***\n";
#-----------------------