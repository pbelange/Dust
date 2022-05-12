#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 2022
@author: pbelange
Description :
"""

import numpy as np

import Backend.Constants as cst
import Backend.Materials as mat


#=============================
# Class needed
#=============================
class DustObject:
    def __init__(self,material,R,Q):
        self.__type__ = 'DustObject'
        
        # Main properties
        self.material = mat.Material({'material': material,
                                      'SEY'     : 'LHC' })
        self.shape    =        shape({'type'    : 'sphere',
                                      'radius'  : R})


        # Initializing macroscopic properties
        self.R = R
        self.m = self.material.rho*self.shape.volume
        self.Q = Q


    # Linking charge with surface potential
    @property
    def phi(self):
        return self.Q/(4*np.pi*cst.eps0*self.R)

    @phi.setter
    def phi(self, value):
        self.Q = value*(4*np.pi*cst.eps0*self.R)


class shape:
    def __init__(self,shape_config):
        self.shapeConfig = shape_config
        self.type = shape_config['type']

        # Shape dictionnary
        loadShape = {'sphere'    : self.sphere}
        loadShape[self.type]()

    def sphere(self):
        self.r = self.shapeConfig['radius']
        self.area = np.pi*(self.r)**2
        self.volume = 4*np.pi*(self.r)**3/3
