#!/share/apps/python/2.7.2/bin/python
import numpy as np
#import matplotlib as mpl
#import matplotlib.pyplot as plt
import csv
"""
    Purpose:
       Merges property fields for two files.
       Actually need two sets of property field files: 
         one without and one with tank regions and backfill. 

    Author: 
       Mark Rockhold, PNNL, 02.12.15 

    Project:
       WMA-C Support Task

    Last update, keep H2_fine_sand as constant, Xuehang Song 09/26/2018
"""


def main():

    # Just need to replace values for cells that lie
    # in aquifer, H3, backfill, and tank regions.

    # 1.1e+4 m/d = 1.27e+1 cm/s
    # Ksx,Ksy,Ksz
    aquifer_perm = [1.27e+1, 1.27e+1, 1.27]
    H3_gravelly_sand_perm = [7.7e-4, 7.7e-4, 7.7e-4]
    H2_fine_sand_perm = [4.15e-3, 4.15e-3, 4.15e-3]
    H2_coarse_sand_perm = [4.15e-3, 4.15e-3, 4.15e-3]
    H2_sand_perm = [4.15e-3, 4.15e-3, 4.15e-3]
    H1_gravelly_sand_perm = [7.7e-4, 7.7e-4, 7.7e-4]
    backfill_perm = [1.56e-3, 1.56e-3, 1.56e-3]

    # vga[1/cm],vgn,Sr
    aquifer_sat = [0.036, 1.491, 0.064]
    H3_gravelly_sand_sat = [0.036, 1.491, 0.064]
    H2_fine_sand_sat = [0.063, 2.047, 0.124]
    H2_coarse_sand_sat = [0.063, 2.047, 0.124]
    H2_sand_sat = [0.063, 2.047, 0.124]
    H1_gravelly_sand_sat = [0.036, 1.491, 0.064]
    backfill_sat = [0.081, 2.18, 0.088]

    # rhos,difpor,totpor,compress
    aquifer_mech = [2.47, 0.2, 0.2, 1.e-7]
    H3_gravelly_sand_mech = [2.47, 0.171, 0.171, 1.e-7]
    H2_fine_sand_mech = [2.49, 0.315, 0.315, 1.e-7]
    H2_coarse_sand_mech = [2.49, 0.315, 0.315, 1.e-7]
    H2_sand_mech = [2.49, 0.315, 0.315, 1.e-7]
    H1_gravelly_sand_mech = [2.47, 0.171, 0.171, 1.e-7]
    backfill_mech = [2.72, 0.34, 0.34, 1.e-7]

    # ell_x, ell_y, ell_z
    aquifer_krel = [0.5, 0.5, 0.5]
    H3_gravelly_sand_krel = [0.5, 0.5, 0.5]
    H2_fine_sand_krel = [0.5, 0.5, 0.5]
    H2_coarse_sand_krel = [0.5, 0.5, 0.5]
    H2_sand_krel = [0.5, 0.5, 0.5]
    H1_gravelly_sand_krel = [0.5, 0.5, 0.5]
    backfill_krel = [0.5, 0.5, 0.5]

    zone_file_list = 'zonefilelist'
    parameter_file = 'wmac_param_step1.out'

    xcell_face_coords_file = 'cfxc.dat'
    ycell_face_coords_file = 'cfyc.dat'
    zcell_face_coords_file = 'cfzc.dat'

    print 'reading x cell face coordinates'
    fin = open(xcell_face_coords_file, 'r')
    xcf = []
    i = 0
    while(1):
        end_of_xcell_face_coords_file = 1
        w = fin.readline().split()
        if len(w) > 0:
            end_of_xcell_face_coords_file = 0
            xcf.append(float(w[0]))
            i += 1
        if end_of_xcell_face_coords_file == 1:
            break
    fin.close()

    print 'reading y cell face coordinates'
    fin = open(ycell_face_coords_file, 'r')
    ycf = []
    j = 0
    while(2):
        end_of_ycell_face_coords_file = 1
        w = fin.readline().split()
        if len(w) > 0:
            end_of_ycell_face_coords_file = 0
            ycf.append(float(w[0]))
            j += 1
        if end_of_ycell_face_coords_file == 1:
            break
    fin.close()

    print 'reading z cell face coordinates'
    fin = open(zcell_face_coords_file, 'r')
    zcf = []
    k = 0
    while(3):
        end_of_zcell_face_coords_file = 1
        w = fin.readline().split()
        if len(w) > 0:
            end_of_zcell_face_coords_file = 0
            zcf.append(float(w[0]))
            k += 1
        if end_of_zcell_face_coords_file == 1:
            break
    fin.close()

    print 'reading theta-based parameter file'
    p = []
    with open(parameter_file, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            p.append(row)

    nx = len(xcf) - 1
    ny = len(ycf) - 1
    nz = len(zcf) - 1
    print 'reading zonation file list'
    fin1 = open(zone_file_list, 'r')
    #
    # Read zonation files, one at a time
    while(5):
        n = 0
        zid = []
        end_of_zonation_file_list = 1
        w1 = fin1.readline().split()
        if len(w1) > 0:
            infile = w1[0]
            zid = np.genfromtxt(infile).flatten(order="C").astype(int)
            #             end_of_zonation_file_list = 0
            #             #
            #             # Read zone ids for all grid blocks
            #             infile = w1[0]
            #             print 'infile= ', infile
            #             #name_parts = infile.split('.')
            #             fin2 = open(infile, 'r')
            #             #outfile = name_parts[0] + '_plustanks_clip3.ups'
            #             #fou2 = open(outfile,'w')
            #             # print infile,' ',outfile
            #             while(6):
            #                 end_of_zone_file = 1
            #                 w2 = fin2.readline().split()
            #                 if len(w2) > 0:
            #                     end_of_zone_file = 0
            # #                    zid.append(int(w2[0]))
            #                     zid = zid+[int(x) for x in w2]
            #                     n += 1
            #                     print(n)
            #                 if end_of_zone_file == 1:
            #                     break
            #             fin2.close()
            #
            # need two sets of parameter fields, one pre-hanford (no tanks or backfill)
            fou2 = open('ksx.dat', 'w')
            fou3 = open('ksy.dat', 'w')
            fou4 = open('ksz.dat', 'w')
            fou5 = open('por.dat', 'w')
            fou6 = open('sr.dat', 'w')
            fou7 = open('vga.dat', 'w')
            fou8 = open('vgn.dat', 'w')
            fou9 = open('rhos.dat', 'w')
            fou10 = open('ellx.dat', 'w')
            fou11 = open('elly.dat', 'w')
            fou12 = open('ellz.dat', 'w')
            fou13 = open('zonation.dat', 'w')
            #fou14 = open('zonation_all.dat','w')
            #
            # Loop over grid blocks
            nzon = 2
            for k in range(len(zcf)-1):
                zc = (zcf[k] + zcf[k+1])*0.5
                for j in range(len(ycf)-1):
                    yc = (ycf[j] + ycf[j+1])*0.5
                    for i in range(len(xcf)-1):
                        xc = (xcf[i] + xcf[i+1])*0.5
                        i1 = i + 1
                        j1 = j + 1
                        k1 = k + 1
                        nn = (k1 - 1)*nx*ny + (j1-1)*nx + i1
                        n0 = nn - 1
                        zid2 = zid[n0]
                        l2p = [zid2]
                        # zonation files
                        print>>fou13, ''.join(map(str, l2p))
                        #l2p = nzon
                        # print>>fou14,''.join(map(str,l2p))
                        #nzon += 1
                        #
                        # property files
                        if zid2 <= 2:
                            # print constant values for zid2 = 1
                            l2p = [float(aquifer_perm[0])]
                            print>>fou2, ''.join(map(str, l2p))
                            l2p = [float(aquifer_perm[1])]
                            print>>fou3, ''.join(map(str, l2p))
                            l2p = [float(aquifer_perm[2])]
                            print>>fou4, ''.join(map(str, l2p))
                            l2p = [float(aquifer_mech[1])]
                            print>>fou5, ''.join(map(str, l2p))
                            l2p = [float(aquifer_sat[2])]
                            print>>fou6, ''.join(map(str, l2p))
                            l2p = [float(aquifer_sat[0])]
                            print>>fou7, ''.join(map(str, l2p))
                            l2p = [float(aquifer_sat[1])]
                            print>>fou8, ''.join(map(str, l2p))
                            l2p = [float(aquifer_mech[0])]
                            print>>fou9, ''.join(map(str, l2p))
                            l2p = [float(aquifer_krel[0])]
                            print>>fou10, ''.join(map(str, l2p))
                            l2p = [float(aquifer_krel[1])]
                            print>>fou11, ''.join(map(str, l2p))
                            l2p = [float(aquifer_krel[2])]
                            print>>fou12, ''.join(map(str, l2p))
                        elif zid2 == 3:
                            l2p = [float(H3_gravelly_sand_perm[0])]
                            print>>fou2, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_perm[1])]
                            print>>fou3, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_perm[2])]
                            print>>fou4, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_mech[1])]
                            print>>fou5, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_sat[2])]
                            print>>fou6, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_sat[0])]
                            print>>fou7, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_sat[1])]
                            print>>fou8, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_mech[0])]
                            print>>fou9, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_krel[0])]
                            print>>fou10, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_krel[1])]
                            print>>fou11, ''.join(map(str, l2p))
                            l2p = [float(H3_gravelly_sand_krel[2])]
                            print>>fou12, ''.join(map(str, l2p))
                        elif zid2 == 3:
                            l2p = [float(H2_fine_sand_perm[0])]
                            print>>fou2, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_perm[1])]
                            print>>fou3, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_perm[2])]
                            print>>fou4, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_mech[1])]
                            print>>fou5, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_sat[2])]
                            print>>fou6, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_sat[0])]
                            print>>fou7, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_sat[1])]
                            print>>fou8, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_mech[0])]
                            print>>fou9, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_krel[0])]
                            print>>fou10, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_krel[1])]
                            print>>fou11, ''.join(map(str, l2p))
                            l2p = [float(H2_fine_sand_krel[2])]
                            print>>fou12, ''.join(map(str, l2p))
                        elif zid2 == 8:
                            l2p = [float(backfill_perm[0])]
                            print>>fou2, ''.join(map(str, l2p))
                            l2p = [float(backfill_perm[1])]
                            print>>fou3, ''.join(map(str, l2p))
                            l2p = [float(backfill_perm[2])]
                            print>>fou4, ''.join(map(str, l2p))
                            l2p = [float(backfill_mech[1])]
                            print>>fou5, ''.join(map(str, l2p))
                            l2p = [float(backfill_sat[2])]
                            print>>fou6, ''.join(map(str, l2p))
                            l2p = [float(backfill_sat[0])]
                            print>>fou7, ''.join(map(str, l2p))
                            l2p = [float(backfill_sat[1])]
                            print>>fou8, ''.join(map(str, l2p))
                            l2p = [float(backfill_mech[0])]
                            print>>fou9, ''.join(map(str, l2p))
                            l2p = [float(backfill_krel[0])]
                            print>>fou10, ''.join(map(str, l2p))
                            l2p = [float(backfill_krel[1])]
                            print>>fou11, ''.join(map(str, l2p))
                            l2p = [float(backfill_krel[2])]
                            print>>fou12, ''.join(map(str, l2p))
                        else:
                            # ksx
                            l2p = [float(p[n0][2])]
                            print>>fou2, ''.join(map(str, l2p))
                            # ksy
                            l2p = [float(p[n0][3])]
                            print>>fou3, ''.join(map(str, l2p))
                            # ksz
                            l2p = [float(p[n0][4])]
                            print>>fou4, ''.join(map(str, l2p))
                            # por
                            l2p = [float(p[n0][5])]
                            print>>fou5, ''.join(map(str, l2p))
                            # Sr
                            l2p = [float(p[n0][6])/float(p[n0][5])]
                            print>>fou6, ''.join(map(str, l2p))
                            # alpha
                            l2p = [float(p[n0][7])]
                            print>>fou7, ''.join(map(str, l2p))
                            # n
                            l2p = [float(p[n0][8])]
                            print>>fou8, ''.join(map(str, l2p))
                            # rhos
                            rhos = 2.72
                            l2p = [rhos]
                            print>>fou9, ''.join(map(str, l2p))
                            # ellx
                            l2p = [float(p[n0][9])]
                            print>>fou10, ''.join(map(str, l2p))
                            # elly
                            l2p = [float(p[n0][10])]
                            print>>fou11, ''.join(map(str, l2p))
                            # ellz
                            l2p = [float(p[n0][11])]
                            print>>fou12, ''.join(map(str, l2p))

            fou2.close()
            fou3.close()
            fou4.close()
            fou5.close()
            fou6.close()
            fou7.close()
            fou8.close()
            fou9.close()
            fou10.close()
            fou11.close()
            fou12.close()
            fou13.close()
            # fou14.close()

        if end_of_zonation_file_list == 1:
            break

    fin1.close()


if __name__ == '__main__':
    main()
