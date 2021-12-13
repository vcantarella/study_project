# -*- coding: utf-8 -*-
"""
Script with the solvers implemented in the RBF model.
This initial implementation is based on automatic root finding from the sympy package.

Current implementations:
    
    - River intercepted length:
        This is the length of the river intercepted by the rbf well
    - Stream flow contribution:
        This is the percentage of the pumping discharge that comes from river water.
    
Limitations:
    - Streams must be located in the y-axis
    - Only one well allowed, located in the positive x,y quadrant

@author: vcant
"""
import numpy as np
import sympy


class river_length():
    """
    Class to solve the river_length and base flow calculations in the RBF model.
    
    Current implementations:
        
        - River intercepted length:
            This is the length of the river intercepted by the rbf well
        - Stream flow contribution:
            This is the percentage of the pumping discharge that comes from river water.
        
    Limitations:
        - Streams must be located in the y-axis
        - Only one well allowed, located in the positive x,y quadrant
        
    Inputs:
        Model: The RBF model class, already set up with the aquifer characteristics and the well placement.
    
    """
    def __init__(self, model):
        self.model = model
    
    def solve_river_length(self):
        """
        Method to calculate intercepted river length and river-flow contribution to well discharge.
        
        Currently checks whether the model well element inputs are correct.
        Inputs
        -------
        None

        Returns
        -------
        length: river length intercepted by the well
        location of the river legnth (y-coordinates of the intercepted river length)
        contribution of river-water to discharge: the percentage of the pumping-rate that comes from river water (the rest is aquifer water)

        """
        if (len(self.model.aem_elements) > 1) | (len(self.model.aem_elements) == 0):
            return "Failed to derive solution. Check current implementation limitiations or model mistakes./nHave you added exactly one well to your model?"
        else:
            
            y = sympy.symbols('y')
            elem = self.model.aem_elements[0]
            Q = elem.Q
            xw = elem.x
            yw = elem.y
            d = np.abs(self.model.river_a *xw + self.model.river_b*yw + self.model.river_c)/np.sqrt(self.model.river_a**2+ self.model.river_b**2)
            Qx = self.model.Qo_x
      
            ## Checking if stagnation points exists for the solution:
            ex_st_points = Q/(np.pi*d*Qx)
            
            if ex_st_points <= 1:
                return print(" There are no stagnation points, check model inputs")
            else:
                equation = sympy.Eq(-d**2 + d*Q/(np.pi*Qx)-y**2,0) # Equation assumes the well is at y = 0, it is corrected later below.
                sols = sympy.solveset(equation, y, domain = sympy.S.Reals)
                sol_el = []
                for i in sols: #Transforming solution that is in a set to a list
                    sol_el.append(np.float64(i+yw)) # Correcting the solution to the well y position
                length = np.abs(sol_el[0]-sol_el[1]) # River capture  length
                Q_river = self.model.calc_psi(0,sol_el[0]) - self.model.calc_psi(0,sol_el[1])+ Q
                contrib = Q_river/Q
            
                return length,sol_el, contrib
        
        



