#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 2022
@author: pbelange
Description :
"""
#-------------------------------

import numpy as np
import matplotlib.pyplot as plt

import Backend.Charging  as chg
import Backend.Objects   as obj
import Backend.Constants as cst
import Backend.Materials as mat


#========================================
# Showing SEY curves
#========================================

# Main function: dust.material.get_SEY(EVec*cst.elec)

# Energy vector in eV
EVec = np.linspace(0,2000,3000)

plt.figure('SEY')

for material in ['Cu','Al2O3']:
    dust = obj.DustObject(material = material,R = 0,Q = 0)
    plt.plot(EVec,dust.material.get_SEY(EVec),label=material) 

plt.axhline(1,linestyle='--',alpha=0.5,color='k')
plt.ylim([0,4.9])
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.xlabel('Primary electron energy (eV)',fontsize=16)
plt.ylabel(r'Secondary electron yield, $\delta(E)$',fontsize=16)

plt.legend(fontsize=15,loc='center right')
plt.tight_layout()
plt.savefig('figures/SEY_curve.png',format='png',dpi=400)
plt.show()



#========================================
# Showing charging currents w.r.t phi
#========================================

# Main function: chg.get_Je,chg.get_Js,chg.get_Jhv

# Initialize with 0 charge, the potential will be varied after
dust = obj.DustObject(material = 'Cu',
                             R = 30e-6,
                             Q = 0)


# Electron cloud parameters
ne_total = 10**(12)

# Beam parameters
Np = 1.15e11*2808


# Plotting for electron energies: 
Te_Vec = [10,300] 


# Plotting
f, axes = plt.subplots(len(Te_Vec), 1, gridspec_kw={'height_ratios': [1, 1]},figsize=(6.4, 6.4))
letterLabel = iter(['(a)','(b)'])
props = dict(boxstyle='round', facecolor='white',edgecolor='lightgrey', linestyle = '-',alpha=0.8)

for idx,Te in enumerate(Te_Vec):


    phi_vec = np.linspace(-40,10,1000)

    J_capture   = chg.get_Je(phi_vec,ne_total,Te)
    J_secondary = chg.get_Js(phi_vec,ne_total,Te,SEY=dust.material.get_SEY)
    J_photo     = chg.get_Jhv(phi_vec,Np,Thv = 6)

    J_tot = J_capture+J_secondary+J_photo


    plt.sca(axes[idx])
    plt.axhline(0,color='k',alpha=0.5)
    plt.axvline(0,color='k',alpha=0.5)
    plt.plot(phi_vec,J_capture/cst.elec*1e-19  ,linestyle = (0, (1, 4)),linewidth=2,color='C0',label=r'$J_e (\Phi)$')
    plt.plot(phi_vec,J_secondary/cst.elec*1e-19,linestyle = (0, (4, 4)),linewidth=2,color='C0',label=r'$J_s (\Phi)$')
    plt.plot(phi_vec,J_photo/cst.elec*1e-19    ,linestyle=(0, (4, 4, 1, 4)),linewidth=2,color='C0',label=r'$J_{h\nu} (\Phi)$')
    plt.plot(phi_vec,J_tot/cst.elec*1e-19       ,'-',linewidth=2,color='C3',label=r'$J_e+J_s+J_{h\nu}$')
    
    plt.text(0.02, 0.91, next(letterLabel)+ r' $k_{_B}T_e = %d$ eV' %Te,fontsize=15, bbox=props,horizontalalignment='left',verticalalignment='center', transform=plt.gca().transAxes)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    
    plt.ylabel(' \n ',fontsize=16)


plt.sca(axes[0])
plt.xticks([])
plt.legend(fontsize=15,loc='lower left')
plt.ylim([-0.08,0.04])

plt.sca(axes[1])
plt.ylim([-0.4,0.6])


f.text(0.05, 0.5, r'Current density ($\times 10^{19}$ e$^{-}$ s$^{-1}$ m$^{-2}$)',fontsize=16, va='center', ha='center', rotation='vertical')
plt.xlabel(r'Surface potential, $\Phi$ (V)',fontsize=16)
plt.tight_layout()
plt.subplots_adjust(hspace=.1)


plt.savefig('figures/Charging_currents.png',format='png',dpi=400)
plt.show()     


    
