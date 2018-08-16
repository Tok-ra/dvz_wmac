#!/share/apps/python/2.7.2/bin/python
# Added 07.19.14 because PIC filesystem had some problems so part of it was set to readonly.
#import os
#import tempfile
#os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
#
"""
   Reads facies field files for WMA-C and writes out to format for ups_facies.f90.

     ML Rockhold, PNNL, 16-Jan-2015 
"""
def main():
   #input_file = 'final_sisim.out.3'
   #output_file = 'sgrfacies_renum_003.zon'
   input_file = 'final_sisim.out.4'
   output_file = 'sgrfacies_renum_004.zon'
   fin = open(input_file,'r')
   fou = open(output_file,'w')
   nn = 0 
   # 3 header lines   
   while(nn<3):
      s = fin.readline().strip('\n\r')
      nn += 1
   while(1):
      end_of_input_file = 1
      s = fin.readline().strip('\n\r')
      w = s.split()
      if len(w) > 0:
         end_of_input_file = 0
         ifac = int(float(w[0]))
         # renumber for use with stomp
         if ifac == 9 or ifac == 1:
            ifac = 0
         elif ifac == 2:
            ifac = 1
         elif ifac == 3:
            ifac = 2
         elif ifac == 4:
            ifac = 3
         elif ifac == 10:
            #ifac = 5
            ifac = 4
         elif ifac == 11:
            #ifac = 6
            ifac = 5
         elif ifac == 12:
            #ifac = 7
            ifac = 6
         elif ifac == 8:
            ifac = 7
         l2p = [ifac]
         print>>fou,''.join(map(str,l2p))
      if end_of_input_file == 1: break
   fin.close() 
   fou.close()

if __name__ == '__main__':
    main()
