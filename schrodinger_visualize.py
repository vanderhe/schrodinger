#!/usr/bin/env python3
"""Visualization module for the schrodinger_solver"""

import sys
import numpy as np
import matplotlib.pyplot as plt

def show(stretchfactor=1, split=False, markersize=10):
    """Visualizes the output of the solver function and saves to schrodinger.pdf

    Args:
        stretchfactor (float): stretches the wavefunctions in y-direction
        split (bool): creates offset to wavefunction, expectationsvalues
        and standard deviation if set to 'True'
        markersize (float): changes markersize of expectations values and standard deviation

    Raises:
        OSError: if input file is not present or has wrong permissions/name

    """
    # Read given parameters
    try:
        xx = np.loadtxt("potential.dat")[:, 0]
        potential = np.loadtxt("potential.dat")[:, 1]
        energies = np.loadtxt("energies.dat")
        wavefunctions = np.loadtxt("wavefuncs.dat")[:, 1:]
        expectation_values = np.loadtxt("expvalues.dat")[:, 0]
        deviation_x = np.loadtxt("expvalues.dat")[:, 1]
    except OSError:
        print("Could not open datafile(s)")
        print("File(s) is/are either not present or exists/existing \
               but has/have wrong permissions\nExiting program")
        sys.exit(1)

    # Plotting
    # plot comparisation of the potentials:
    # Not usung True and False as 0 and 1
    off = 0
    if split:
        off = 1
    interval_x = np.max(xx) - np.min(xx)
    interval_y = np.max(energies) - np.min(energies)
    nn = len(energies)
    # ylim for both plots, adding space on boundaries for nicer look
    ylim = [np.min(potential) - interval_y/20, np.max(energies) + interval_y/5]

    plt.subplot(1, 2, 1)
    plt.plot(xx, potential, "k-", label="interp. Potential")
    plt.xlim([np.min(xx) - interval_x/20, np.max(xx) + interval_x/20])
    plt.ylim(ylim)
    for ii in range(nn):
        # plot eigenvalue lines
        plt.axhline(energies[ii], np.min(xx), np.max(xx), color="gray")
        # plot expectation values
        plt.plot(expectation_values[ii], off*energies[ii], "gx", ms=markersize)
        if ii%2 == 0:
            plt.plot(xx, stretchfactor*wavefunctions[:, ii] + off*energies[ii], "r-")
        else:
            plt.plot(xx, stretchfactor*wavefunctions[:, ii] + off*energies[ii], "b-")

    plt.xlabel("$x$ [Bohr]")
    plt.ylabel("Energy $E$ [Hartree]")
    plt.title("Potential, Eigenvalues, \n Expectationvalues")
    # plt.legend()

    # plot uncertainty
    plt.subplot(1, 2, 2)
    plt.xlim([0, np.max(deviation_x) + interval_x/20])
    plt.ylim(ylim)
    for ii in range(nn):
        plt.axhline(energies[ii], np.min(xx), np.max(xx), color="gray")
        #plot uncertainty
        plt.plot(deviation_x[ii], off*energies[ii], "m+", ms=markersize)

    plt.xlabel(r"$\sigma_\mathrm{x}$ [Bohr]")
    plt.title(r"Standard Deviation $\sigma_\mathrm{x}$")
    plt.savefig("schrodinger.pdf")
    