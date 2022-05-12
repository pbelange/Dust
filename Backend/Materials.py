#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 2022
@author: pbelange
"""

import numpy as np
import Backend.Constants as cst

class Material:
    def __init__(self,materialConfig):
        self.materialConfig = materialConfig
        self.type           = self.materialConfig['material']
        self.SEY_name       = self.materialConfig['SEY']

        # Material dictionnary
        loadMaterial = {'custom' : self.custom,
                        'C'      : self.Carbon,
                        'Cu'     : self.Copper,
                        'Al2O3'  : self.Alumine,
                        'Al'     : self.Aluminium,
                        'Si'     : self.Silicon,
                        'O'      : self.Oxygen}
        loadMaterial[self.type]()

        # Calculate electron density
        self.n = cst.Na*self.Z*self.rho/(self.A*cst.Mu)
        self.macroscopicCS = self.crossSection*cst.Na*self.rho/(self.A*cst.Mu)

    def custom(self):
        self.rho          = self.materialConfig.getfloat('rho')
        self.Z            = self.materialConfig.getfloat('Z')
        self.A            = self.materialConfig.getfloat('A')                       
        self.c            = self.materialConfig.getfloat('c')                         
        self.crossSection = self.materialConfig.getfloat('crossSection')             

        # SEY
        self.deltaMax     = self.materialConfig.getfloat('deltaMax')     
        self.Emax         = self.materialConfig.getfloat('Emax')     
        self.E_elas       = self.materialConfig.getfloat('E_elas') 
        self.R0           = self.materialConfig.getfloat('R0') 

    def Carbon(self):
        self.rho = 2000                     # Density [kg/m^3]
        self.Z = 6                          # Atomic number
        self.A = 12                         # Mass number
        self.c = 710.6                      # Specific heat [J/kg*K]
        self.crossSection = 266e-31         # Atomic cross section [m^2]  (mbarn = 1e-31 m^2)

    def Copper(self):
        self.rho = 8960                     # Density [kg/m^3]
        self.Z = 29                         # Atomic number
        self.A = 64                         # Mass number
        self.c = 384.56                     # Specific heat [J/kg*K]
        self.crossSection = 850e-31         # Atomic cross section [m^2]  (mbarn = 1e-31 m^2)

        # SEY
        self.deltaMax = 1.7
        self.Emax     = 332                 # in eV
        self.E_elas   = 150                 # in eV
        self.R0       = 0.7

    def Alumine(self):
        # TODO: find alumine parameters
        self.rho = 0                        # Density [kg/m^3]
        self.Z = 0                          # Atomic number
        self.A = 1                          # Mass number
        self.c = 1                          # Specific heat [J/kg*K]
        self.crossSection = 1               # Atomic cross section [m^2]  (mbarn = 1e-31 m^2)

        # SEY
        self.deltaMax = 4.7
        self.Emax     = 600
        self.E_elas   = 150
        self.R0       = 0.7

    def Aluminium(self):
        self.rho = 2700                     # Density [kg/m^3]
        self.Z = 13                         # Atomic number
        self.A = 27                         # Mass number
        self.c = 898.7                      # Specific heat [J/kg*K]
        self.crossSection = 470e-31         # Atomic cross section [m^2]  (mbarn = 1e-31 m^2)

    def Silicon(self):
        self.rho = 2328                     # Density [kg/m^3]
        self.Z = 14                         # Atomic number
        self.A = 28                         # Mass number
        self.c = 898.7                      # Specific heat [J/kg*K]
        self.crossSection = 530e-31         # Atomic cross section [m^2]  (mbarn = 1e-31 m^2)

    def Oxygen(self):
        self.rho = 1310                     # Density [kg/m^3]
        self.Z = 8                          # Atomic number
        self.A = 16                         # Mass number
        self.c = 1861                       # Specific heat [J/kg*K]
        self.crossSection = 335e-31         # Atomic cross section [m^2]  (mbarn = 1e-31 m^2)


    def get_SEY(self,E):
        # All SEY curves assume E in eV
        SEY_fun = { 'sternglass':self.SEY_sternglass,
                    'jonker'    :self.SEY_jonker,
                    'zimm'      :self.SEY_zimm,
                    'LHC'       :self.SEY_LHC}[self.SEY_name]
        return SEY_fun(E)



    def SEY_sternglass(self,E):
        deltaMax,Emax = self.deltaMax,self.Emax
        return deltaMax*(E/Emax)*np.exp(-2*np.sqrt(E/Emax)+2)

    
    def SEY_jonker(self,E):
        s_delta  = 1.8
        deltaMax,Emax = self.deltaMax,self.Emax

        x = E/Emax
        return deltaMax*(s_delta*x/(s_delta-1+x**s_delta))

    
    def SEY_LHC(self,E):
        s_delta  = 1.35
        deltaMax,Emax = self.deltaMax,self.Emax
        E0,R0 = self.E_elas,self.R0
        
        x = E/Emax
        delta_elas = R0*((np.sqrt(E)-np.sqrt(E+E0))/(np.sqrt(E)+np.sqrt(E+E0)))**2
        return deltaMax*(s_delta*x/(s_delta-1+x**s_delta)) + delta_elas
        
    
    def SEY_zimm(self,E):
        deltaMax,Emax = self.deltaMax,self.Emax
        x = E/Emax
        return deltaMax*1.11*(x**(-0.35))*(1-np.exp(-2.3*(x**1.35)))