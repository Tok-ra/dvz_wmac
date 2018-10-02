import numpy as np
"""

   Uses similar media scaling to estimate hydraulic parameters from
   field-measured volumetric water content using an assumed mean tension
   and reference Ks and water retention function.

   Written by ML Rockhold, 14-Sept-2015.
   Project WMA C Alternative Conceptual Models, client WRPS.

"""

# example useage: Kh.append(MualemVG_Kh(p,h[nf]))


def MualemVG_Kh(p, h):
    vga, vgn, ks, ell = p
    vgm = 1.0 - 1.0/vgn
    den = (1.0 + (vga*h)**vgn)**(vgm*ell)
    num = (1.0 - (vga*h)**(vgn-1.0)*(1.0+(vga*h)**vgn)**(-vgm))**2
    return ks*num/den


def VG_htheta(p, w):
    vga, vgn, ts, tr = p
    sub = 5.e-3
    add = 1.5e-2
    if w <= tr:
        # wold = w
        w = tr + add
        # print 'resetting w from',wold,' to ',w
    if w >= ts:
        # wold = w
        w = ts - sub
        # print 'resetting w from',wold,' to ',w
    se = (w-tr)/(ts-tr)
    vgm = 1.0 - 1.0/vgn
    # print 'w, tr, ts, se, vgm ',w, tr, ts, se,vgm
    h = 1.0/vga*(se**(-1.0/vgm)-1.0)**(1.0/vgn)
    return h


# def main():
if 1 == 1:

    # ksx[cm/s],ksy,ksz,thetas,thetar,alpha[1/cm],n,ellx,elly,ellz,href
    # h1 and h3 are the same here

    # setup directory
    setup_dir = "/people/song884/wmac/fy18/fine_model_setup/watercontent/scale/"
    water_content_data_file = setup_dir+'sgsim1.ups'
    zon_file = setup_dir + "wma_c_pre_hanford_ehm_89x93x330.zon"
    output_prefix = "theta001_ss_"

    zon_file = setup_dir + "wma_c_oppc_ehm_89x93x330.zon"
    output_prefix = "theta001_oppc_"

    # read data file
    ehm_id = np.genfromtxt(zon_file).flatten(order="C").astype(int)
    wc = np.genfromtxt(water_content_data_file).flatten(
        order="C").astype(float)/100.0

    # name id
    zon_id = dict()
    zon_id["Basalt"] = 1
    zon_id["Aquifer"] = 2
    zon_id["H3 Gravelly Sand"] = 3
    zon_id["H2 Fine Sand"] = 4
    zon_id["H2 Coarse Sand"] = 5
    zon_id["H2 Sand"] = 6
    zon_id["H1 Gravelly Sand"] = 7
    zon_id["Backfill"] = 8

    # which id to map
    hete_ids = [5, 6, 7]

    # parameter to calculate hydraulic property
    params = dict()
    params[zon_id["H2 Coarse Sand"]] = [9.40e-3, 9.40e-3, 9.40e-3, 0.367,
                                        0.025, 0.140, 1.80, -1.0, -1.0, -0.2, 245.0]
    params[zon_id["H2 Sand"]] = [9.40e-3, 9.40e-3, 9.40e-3, 0.367,
                                 0.025, 0.140, 1.80, -1.0, -1.0, -0.2, 245.0]
    params[zon_id["H1 Gravelly Sand"]] = [4.79e-3, 4.79e-3, 1.60e-3, 0.200,
                                          0.025, 0.120, 1.60, -1.2, -1.2, -1.2, 446.0]

    homos = dict()
    homos[zon_id["Basalt"]] = dict()
    homos[zon_id["Aquifer"]] = dict()
    homos[zon_id["H3 Gravelly Sand"]] = dict()
    homos[zon_id["H2 Fine Sand"]] = dict()
    homos[zon_id["H2 Coarse Sand"]] = dict()
    homos[zon_id["H2 Sand"]] = dict()
    homos[zon_id["H1 Gravelly Sand"]] = dict()
    homos[zon_id["Backfill"]] = dict()

    # Ksx,Ksy,Ksz
    homos[zon_id["Basalt"]]["perm"] = [1.27e+1, 1.27e+1, 1.27]
    homos[zon_id["Aquifer"]]["perm"] = [1.27e+1, 1.27e+1, 1.27]
    homos[zon_id["H3 Gravelly Sand"]]["perm"] = [7.7e-4, 7.7e-4, 7.7e-4]
    homos[zon_id["H2 Fine Sand"]]["perm"] = [4.15e-3, 4.15e-3, 4.15e-3]
    homos[zon_id["H2 Coarse Sand"]]["perm"] = [4.15e-3, 4.15e-3, 4.15e-3]
    homos[zon_id["H2 Sand"]]["perm"] = [4.15e-3, 4.15e-3, 4.15e-3]
    homos[zon_id["H1 Gravelly Sand"]]["perm"] = [7.7e-4, 7.7e-4, 7.7e-4]
    homos[zon_id["Backfill"]]["perm"] = [1.56e-3, 1.56e-3, 1.56e-3]

    # vga[1/cm],vgn,Sr
    homos[zon_id["Basalt"]]["sat"] = [0.036, 1.491, 0.064]
    homos[zon_id["Aquifer"]]["sat"] = [0.036, 1.491, 0.064]
    homos[zon_id["H3 Gravelly Sand"]]["sat"] = [0.036, 1.491, 0.064]
    homos[zon_id["H2 Fine Sand"]]["sat"] = [0.063, 2.047, 0.124]
    homos[zon_id["H2 Coarse Sand"]]["sat"] = [0.063, 2.047, 0.124]
    homos[zon_id["H2 Sand"]]["sat"] = [0.063, 2.047, 0.124]
    homos[zon_id["H1 Gravelly Sand"]]["sat"] = [0.036, 1.491, 0.064]
    homos[zon_id["Backfill"]]["sat"] = [0.081, 2.18, 0.088]

    # rhos,difpor,totpor,compress
    homos[zon_id["Basalt"]]["mech"] = [2.47, 0.2, 0.2, 1.e-7]
    homos[zon_id["Aquifer"]]["mech"] = [2.47, 0.2, 0.2, 1.e-7]
    homos[zon_id["H3 Gravelly Sand"]]["mech"] = [2.47, 0.171, 0.171, 1.e-7]
    homos[zon_id["H2 Fine Sand"]]["mech"] = [2.49, 0.315, 0.315, 1.e-7]
    homos[zon_id["H2 Coarse Sand"]]["mech"] = [2.49, 0.315, 0.315, 1.e-7]
    homos[zon_id["H2 Sand"]]["mech"] = [2.49, 0.315, 0.315, 1.e-7]
    homos[zon_id["H1 Gravelly Sand"]]["mech"] = [2.47, 0.171, 0.171, 1.e-7]
    homos[zon_id["Backfill"]]["mech"] = [2.72, 0.34, 0.34, 1.e-7]

    # ell_x, ell_y, ell_z
    homos[zon_id["Basalt"]]["kerl"] = [0.5, 0.5, 0.5]
    homos[zon_id["Aquifer"]]["kerl"] = [0.5, 0.5, 0.5]
    homos[zon_id["H3 Gravelly Sand"]]["kerl"] = [0.5, 0.5, 0.5]
    homos[zon_id["H2 Fine Sand"]]["kerl"] = [0.5, 0.5, 0.5]
    homos[zon_id["H2 Coarse Sand"]]["kerl"] = [0.5, 0.5, 0.5]
    homos[zon_id["H2 Sand"]]["kerl"] = [0.5, 0.5, 0.5]
    homos[zon_id["H1 Gravelly Sand"]]["kerl"] = [0.5, 0.5, 0.5]
    homos[zon_id["Backfill"]]["kerl"] = [0.5, 0.5, 0.5]

    # output fields
    fields = dict()
    fields["ksx"] = np.zeros(len(ehm_id))
    fields["ksy"] = np.zeros(len(ehm_id))
    fields["ksz"] = np.zeros(len(ehm_id))
    fields["por"] = np.zeros(len(ehm_id))
    fields["sr"] = np.zeros(len(ehm_id))
    fields["vga"] = np.zeros(len(ehm_id))
    fields["vgn"] = np.zeros(len(ehm_id))
    fields["rhos"] = np.zeros(len(ehm_id))
    fields["ellx"] = np.zeros(len(ehm_id))
    fields["elly"] = np.zeros(len(ehm_id))
    fields["ellz"] = np.zeros(len(ehm_id))

    for id_type in zon_id.values():
        print(id_type)
        if id_type in hete_ids:
            ksx = params[id_type][0]
            ksy = params[id_type][1]
            ksz = params[id_type][2]
            ts = params[id_type][3]
            tr = params[id_type][4]
            vga = params[id_type][5]
            vgn = params[id_type][6]
            ellx = params[id_type][7]
            elly = params[id_type][8]
            ellz = params[id_type][9]
            href = params[id_type][10]

            cell_index = np.where(ehm_id == id_type)[0]
            for icell in cell_index:
                p = [vga, vgn, ts, tr]
                h = VG_htheta(p, wc[icell])
                sfh = h/href
                sfk = sfh
                hb = 1.0/vga/sfh
                vga_new = 1.0/hb
                ksz_new = ksz*sfk**2
                ksx_new = ksz_new*(ksx/ksz)
                ksy_new = ksz_new*(ksy/ksz)

                fields["ksx"][icell] = ksx_new
                fields["ksy"][icell] = ksy_new
                fields["ksz"][icell] = ksz_new
                fields["por"][icell] = ts
                fields["sr"][icell] = tr/ts
                fields["vga"][icell] = vga_new
                fields["vgn"][icell] = vgn
                #!!!!!!!!!!!!!!!!!!!!!!!!
                fields["rhos"][icell] = 2.72
                fields["ellx"][icell] = ellx
                fields["elly"][icell] = elly
                fields["ellz"][icell] = ellz
        else:
            cell_index = np.where(ehm_id == id_type)
            fields["ksx"][cell_index] = homos[id_type]["perm"][0]
            fields["ksy"][cell_index] = homos[id_type]["perm"][1]
            fields["ksz"][cell_index] = homos[id_type]["perm"][2]
            fields["por"][cell_index] = homos[id_type]["mech"][1]
            fields["sr"][cell_index] = homos[id_type]["sat"][2]
            fields["vga"][cell_index] = homos[id_type]["sat"][0]
            fields["vgn"][cell_index] = homos[id_type]["sat"][1]
            fields["rhos"][cell_index] = homos[id_type]["mech"][0]
            fields["ellx"][cell_index] = homos[id_type]["kerl"][0]
            fields["elly"][cell_index] = homos[id_type]["kerl"][1]
            fields["ellz"][cell_index] = homos[id_type]["kerl"][2]

    for ifield in fields.keys():
        fout = open(setup_dir+output_prefix+ifield+".dat", 'w')
        fout.write("\n".join(map(str, fields[ifield])))
        fout.close()

        # # if __name__ == '__main__':
        # #     main()
