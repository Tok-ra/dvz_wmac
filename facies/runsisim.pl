#-------------------------------------------------------------
# runsisim.pl
#-------------------------------------------------------------
# The script executes the following tasks:
# x(1) Check if a blank grid is used, if yes, split it by row.
# (2) Run SGSIM by changing the random seeds
# x(3) If Step (2) is yes, split SGSIM output file. 
# x    If no, go to Step (4).
# x(4) Calculate the number of non-blanked grid values
#     exceeding a specified cutoff.
# x(5) Output the number of cells vs. number of simulations
#-------------------------------------------------------------
# Note: All variables need to be declared in the first part
#       the script.
# Note: Modified to incorporate LVM files, and no counting.
#-------------------------------------------------------------

#----------------------------
# Variables
#----------------------------
$simfl = "sisim.out";
$nheader1 = 3;                     #-- header for $simfl        --#
$tempfl = "sisim.tmp";             #-- template file            --#
$seedfl = "seeds2.txt";            #-- no header                --#
#$lvmfl = "lvm10.txt";             #-- no header                --#
$word1 = "#SEED";                  #-- keyword for random seeds --#
#$word2 = "#LVMFL";                #-- keyword for lvm file     --#

#--------------------------
# (0) Read in random seeds
#--------------------------
open (SEEDFL, $seedfl) || die "can't open $seedfl: $!";

$i = 0;
while (<SEEDFL>)
{
   chomp;
   $seeds[$i] = $_;
   $i++;
}
close (SEEDFL);
$nseed = @seeds;
print "Number of random seeds: $nseed\n";

#--------------------------
# (1) Read in LVM files
#--------------------------
#open (LVMFL, $lvmfl) || die "can't open $lvmfl: $!";
#
#$i = 0;
#while (<LVMFL>)
#{
#   chomp;
#   $lvmfl[$i] = $_;
#   $i++;
#}
#close (LVMFL);
#$nlvm = @lvmfl;
#print "Number of LVM files: $nlvm\n";
#
#if ($nlvm != $nseed)
#{
#   die "Numbers of LVM and random seeds do not match: $!";
#}

#-------------------------------
# (2) Execute SISIM for $nseed
#-------------------------------
print "Start SISIM...\n";
print "\n";

for ($i=0; $i<$nseed; $i++)
{
   $isim = $i + 1;

   open (TEMPFL, "$tempfl") || die "can't open $tempfl: $!";
   open (PARFL, ">sisim.par") || die "can't create sisim.par: $!";
   
   while (<TEMPFL>)
   {
         chomp;
         $_ =~ s/$word1/$seeds[$i]/;
         #$_ =~ s/$word2/$lvmfl[$i]/;
         print PARFL "$_\n";   
   }
   close (TEMPFL);
   close (PARFL);
   print "Run SISIM no. $isim...\n";
   system("./sisim")==0 || die "system sisim failed: $!";
   unlink("sisim.par");  
   
   rename ("$simfl", "$simfl.$isim");
   rename ("sisim.dbg", "sisim.dbg.$isim");

}

#----------------------------------
print "\n*** END of SCRIPT ***\n";
#----------------------------------
