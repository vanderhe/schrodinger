#!/usr/bin/env python3
"""Module that reads the input data, processed by the schrodinger solver"""

import sys
import numpy as np

def read_input(file):
    """Read given parameters and potential data of 'schrodinger.inp'

    Args:
        file (str): path to input file schrodinger.inp

    Returns:
        obtained_input (dict): obtained input from 'file'

    Raises:
        OSError: if input file is not present or has wrong permissions/name

    """
    try:
        schrodingerinp = open(file, "r")
        schrodingerlines = schrodingerinp.readlines()
        # print(schrodingerlines)
    except OSError:
        print("Could not open specified inputfile: {}".format(file))
        print("File is either not present or it exists but has wrong permissions\nExiting program")
        sys.exit(1)

    massentry = schrodingerlines[0].split()[0]
    mass = float(massentry)
    print("\nobtained parameters: ")
    print("mass: ", mass)

    xminentry = schrodingerlines[1].split()[0]
    xmin = float(xminentry)
    #print("xmin: ", xmin)

    xmaxentry = schrodingerlines[1].split()[1]
    xmax = float(xmaxentry)
    print("xmin, xmax: ", xmin, ", ", xmax)

    npointentry = schrodingerlines[1].split()[2]
    npoint = int(npointentry)
    print("number of interpolation points: ", npoint)

    firsteigventry = schrodingerlines[2].split()[0]
    firsteigv = int(firsteigventry)
    #print("first eigenvalue to print: ", firsteigv)

    lasteigventry = schrodingerlines[2].split()[1]
    lasteigv = int(lasteigventry)
    print("first, last eigenvalue to print: ", firsteigv, ", ", lasteigv)

    intertype = schrodingerlines[3].split()[0]
    #print("interpolation type: ", intertype)

    potlen = len(schrodingerlines) - 5
    # print("\nnr. of pot-values:\n", potlen)
    xpot = np.zeros(potlen)
    ypot = np.zeros(potlen)
    for ii in range(5, potlen + 5):
        xpot[ii - 5] = float(schrodingerlines[ii].split()[0])
        ypot[ii - 5] = float(schrodingerlines[ii].split()[1])
    xypot = np.hstack((xpot.reshape((-1, 1)), ypot.reshape((-1, 1))))

    schrodingerinp.close()

    obtained_input = {"mass": mass, "xmin": xmin, "xmax": xmax, "npoint": npoint,
                      "firsteigv": firsteigv, "lasteigv": lasteigv, "intertype": intertype,
                      "potlen": potlen, "xypot": xypot}

    return obtained_input

def output(data):
    """Write calculated data to files

    Args:
        data (dict): dictionary with calculated data from solve1d

    """
    np.savetxt("potential.dat", data["potential"])
    np.savetxt("energies.dat", data["energies"])
    np.savetxt("wavefuncs.dat", data["wavefuncs"])
    np.savetxt("expvalues.dat", data["expvalues"])
