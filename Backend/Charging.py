#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 2022
@author: pbelange
Description :
"""

import numpy as np
import scipy.integrate as integrate
import scipy.optimize as sciOpt

import Backend.Constants as cst



#==================================================
# Charging currents

#-------------------
# Electron capture
def get_Je(phi,ne,Te):
    """
    
    phi: Surface potential          [V]
    ne : electron density           [e/m^3] 
    Te : Electron cloud temperature [eV]

    """
    if np.size(ne)>1 or np.size(Te)>1:
        raise ValueError('only phi can be a vector')
    phi = np.array(phi)

    J0 = ne*cst.elec*np.sqrt(Te*cst.elec/(2*np.pi*cst.m_e))

    # Case where phi>=0
    Je = -J0*(1 + phi/Te)

    # Case where phi<0
    Je[phi<0] = -J0*np.exp(phi[phi<0]/Te)

    return Je


#-------------------
# SEE current
def get_Js(phi,ne,Te,SEY,Ts = 3):
    """

    phi: Surface potential          [V]
    ne : electron density           [e/m^3] 
    Te : Electron cloud temperature [eV]
    SEY: SEY function
    Ts : temperature of SEE         [eV]

    """
    if np.size(ne)>1 or np.size(Te)>1:
        raise ValueError('only phi can be a vector')
    phi = np.array(phi)

    J0 = ne*cst.elec*np.sqrt(Te*cst.elec/(2*np.pi*cst.m_e))

    # Computing Js based on the integral
    Js = np.nan*np.ones(len(phi)) 

    # Case where phi<0
    integratedFactor = integrate.quad(lambda E: E*SEY(E)*np.exp(-E/Te), 0, np.inf)[0]
    Js[phi<0] = J0*(1/Te**2)*np.exp(phi[phi<0]/Te)*integratedFactor

    # Case where phi>=0
    integratedFactor = np.array([integrate.quad(lambda E: E*SEY(E)*np.exp(-E/Te), _phi, np.inf)[0] for _phi in phi[phi>=0]]) 
    Js[phi>=0] = J0*(1/Te**2)*np.exp(phi[phi>=0]/Te)*np.exp(-phi[phi>=0]/Ts)*(1+phi[phi>=0]/Ts)*integratedFactor

    return Js




#-------------------
# Photoelectric current
def get_Jhv(phi,Np,Thv,E_Beam=6.5e12,Qhv = 1,deltahv = 0.3,fraction_phot=1.08423/3.24759):
    """

    phi          : Surface potential                          [V]
    Np           : Num of protons in beam                     [p+] 
    Thv          : Photoelectron temperature                  [eV]
    E_Beam       : Beam energy                                [eV]
    Qhv          : Absorption efficiention                    [_]
    deltahv      : photoelectric yield                        [_]
    fraction_phot: fraction of photons with sufficient energy [_]

    """
    
    if np.size(Np)>1 or np.size(Thv)>1:
        raise ValueError('only phi can be a vector')
    phi = np.array(phi)

    # Computing Gamma_tot
    rho = cst.LHC_RHO_ARC
    ndot = (5/2/np.sqrt(3))*(1+E_Beam/cst.m_p_eV)*(cst.c/rho)* (1/137) * (23*2*cst.LHC_L_ARC_CELL*8)/(2*np.pi*rho)
    Gamma_tot = ndot/(cst.LHC_PERIMETER_BEAM_SCREEN*cst.LHC_C) * Np

    # Using "fraction_phot" value computed separately for the LHC
    Gamma_dot = fraction_phot * Gamma_tot

    # Saturation current
    J_sat = cst.elec*Gamma_dot*Qhv*deltahv

    # Case where phi<0
    Jhv = J_sat*np.ones(len(phi))

    # Case where phi>=0
    Jhv[phi>=0] = J_sat*np.exp(-phi[phi>=0]/Thv)


    return Jhv



