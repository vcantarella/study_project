# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:18:14 2021

@author: vcant
"""

import numpy as np
import pandas as pd

class River:
    """
    Optional class to input the river coordinates.
    If given, will output the rotation matrix for the coordinates with the rot_matrix method
    Inputs: x,y coordinates for two river nodes (x1,y1) and (x2,y2)
    """
    def __init__(self,x1,y1,x2,y2):
        self.m = (y2-y1)/(x2-x1)
        self.theta = np.where(np.arctan(self.m)> 0, np.pi - np.arctan(self.m),
                              -np.pi - np.arctan(self.m))
    def rot_matrix(self):
        """
        returns the rotation matrix (2d numpy array) that guarantee the river is parallel to y axis
        
        """
        t = self.theta
        return(np.array([np.cos(t), -np.sin(t)],
                        [np.sin(t), np.cos(t)]))
    
    def operator(self,x,y):
        """
        returns the rotated and translated coordinates for the river system:
        input (x, y)
        outputs: translated (x', y')
        """
        return None


class Model:
    def __init__(self, k, H, h0, river = None, x_ref = 0, y_ref = 0):
        self.k = k
        self.H = H
        self.h0 = h0
        self.aem_elements = []
        self.well_df = pd.DataFrame({'wellid' : [],
                                     'Discharge': [],
                                     'X': [],
                                     'Y': []})
        if river == None:
            # If undeclared river line equation will be assumed to be located at the y-axis
            self.river_a = 1
            self.river_b = 0
            self.river_c = 0
        else: # river line imported from river class
            self.river_a = river.river_a
            self.river_b = river.river_b
            self.river_c = river.river_c
        if self.h0 < self.H:
            self.phi0 = 0.5 * self.k * self.h0 **2
        else:
            self.phi0 = self.k * self.H * self.h0 - 0.5 * self.k * self.H **2
    
    def calc_phi(self, x, y):
        """
        Method to calculate the discharge potential at given location:

        Parameters
        ----------
        x,y location of interest.

        Returns
        -------
        phi(x,y) float.

        """
        
        phi_well = 0
        for element in self.aem_elements:
            d = np.abs(self.river_a *element.x + self.river_b*element.y + self.river_c)/np.sqrt(self.river_a**2+ self.river_b**2)
            phi_q = (element.Q/(4*np.pi))*np.log(((x + d)**2 + y**2)/((x-d)**2+y**2))
            phi_well += phi_q
        return self.phi0 + phi_well
    def head(self,x,y):
        phi = self.calc_phi(x,y)
        phicrit = self.phi0 + 0.5 * self.k * self.H **2 
        if phi >= phicrit:
            h = 0.5 * self.H + (1 / self.k / self.H) *phi
        else:
            h = np.sqrt((2 / self.k) * (phi)) 
        return h# head
            
    

class Well:
    """
    Element to create Well for the model
    """
    def __init__(self, model,Q, rw, x,y):
        self.x = x
        self.y = y
        self.Q = Q
        self.rw = rw
        model.aem_elements.append(self)
        def phi(self):
            self.Q/2*np.pi



aem_model = Model(k = 10, H = 20, h0 = 18)

well = Well(aem_model, Q = 10, rw = 0.2, x = 30, y = 50)


print(aem_model.head(1, 1))



