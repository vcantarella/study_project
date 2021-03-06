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
import itertools
from scipy.optimize import fsolve

#For the time of travel calculation using ttcrpy package:


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
        sol_el: location of the river legnth (y-coordinates of the intercepted river length)
        contrib: contribution of river-water to discharge: the percentage of the pumping-rate that comes from river water (the rest is aquifer water)

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
            Qx = -self.model.Qo_x
      
            ## Checking if stagnation points exists for the solution:
            ex_st_points = Q/(np.pi*d*Qx)
            
            if ex_st_points <= 1:
                return print("There are no stagnation points, check model inputs")
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
    
    def time_travel(self, ne, delta_s = 0.1):
        """
        Method to derive the time of travel of selected paths from the river to the well
        
        

        Returns
        -------
        time of travel array : numpy array, dimensions: (length of river capture length,1)

        """
        
        length, sol_el, contrib = self.solve_river_length()
        
        ys = np.linspace(sol_el[0]+0.1,sol_el[1]-0.1,20)
        #print(ys.shape)
        xs = np.repeat(0.1,ys.shape[0])
        tt = []
        
        '''
        initial parameters from the model:
            
        '''
        elem = self.model.aem_elements[0]
        Q = elem.Q
        xw = elem.x
        yw = elem.y
        d = np.abs(self.model.river_a *xw + self.model.river_b*yw + self.model.river_c)/np.sqrt(self.model.river_a**2+ self.model.river_b**2)
        Qx = self.model.Qo_x
        rw = elem.rw
        
        '''
        general qx, qy formulas (general potential)
        '''
        def qx(x,y, Q, Qx, xw, yw, d):
            return -1*(-Qx + Q/(4*np.pi)*((2*(x-xw)/((x-xw)**2+(y-yw)**2))-(2*(x-(xw-2*d)))/((x-(xw-2*d))**2+(y-yw)**2)))/self.model.calc_head(x,y)
        
        def qy(x,y, Q, Qx, xw, yw, d):
            return -1*(Q/(4*np.pi)*((2*(y-yw)/((x-xw)**2+(y-yw)**2))-(2*(y-yw))/((x-(xw-2*d))**2+(y-yw)**2)))/self.model.calc_head(x,y)
        
        '''
        Formulas for correction of the trajectory (stream function)
        '''
        def equation_x(x_a, psi, y_2, Q, Qx, xw, yw, d):
                    return -Qx*y_2 + (Q/(2*np.pi))*(np.arctan2((y_2-yw),(x_a-xw))- np.arctan2((y_2-yw),(x_a-(xw-2*d))))-psi
        
        def equation_y(y_a, psi, x_2, Q, Qx, xw, yw, d) :
                    return -Qx*y_a + (Q/(2*np.pi))*(np.arctan2((y_a-yw),(x_2-xw))- np.arctan2((y_a-yw),(x_2-(xw-2*d))))-psi
        ''' 
        calculation of streamline and time of travel
        '''
        for x,y in zip(xs,ys):
            
            #dis_arr = []
            #v_arr = []
            t_arr = []
            x1 = x
            y1 = y
            psi = self.model.calc_psi(x,y)
            breakin_dists = []
            while np.sqrt((x1-xw)**2+(y1-yw)**2) > 1*delta_s :
                #Part 1 calculating velocity:
                dista1 = np.sqrt((x1-xw)**2+(y1-yw)**2)
                #print(x1)
                #print(y1)
                qx1 = qx(x1,y1, Q, Qx, xw, yw, d)
                qy1 = qy(x1,y1, Q, Qx, xw, yw, d)
                vx = qx1/ne
                vy = qy1/ne
                v_i = np.sqrt(vx**2+vy**2)
                
                
                #Part 2: estimating second point
                
                
                y_2 = np.float(y1 + delta_s*vy/v_i)
                x_2 = np.float(x1 + delta_s*vx/v_i)
                
                ## correcting the point location based on the psi value:
                
                if vx > vy :
                    sols_y = fsolve(equation_y, y_2, (psi, x_2, Q, Qx, xw, yw, d))
                    sol_el_y = sols_y[0]
                    y_2 = sol_el_y
                else:
                    sols = fsolve(equation_x, x_2, (psi, y_2, Q, Qx, xw, yw, d))
                    sol_el_x = sols[0]
                    x_2 = sol_el_x
                
                ## Calculating distance:
                dist = np.sqrt((x_2-x1)**2+(y_2-y1)**2)
                
                # Calculating velocities for the second point:
                
                qx2 = qx(x_2,y_2, Q, Qx, xw, yw, d)
                qy2 = qy(x_2,y_2, Q, Qx, xw, yw, d)
                vx2 = qx2/ne
                vy2 = qy2/ne
                
                # Calculating mean velocity: 
                
                vxm = np.mean([vx,vx2])
                vym = np.mean([vy,vy2])
                
                vm = np.sqrt(vxm**2+vym**2)
                
                #Calculating time of travel of the particle (deltaS/deltaV) and appending to array:
                t_arr.append(dist/vm)
                
                #Looping
                x1 = x_2
                y1 = y_2
                #dista_2 = np.sqrt((x1-xw)**2+(y1-yw)**2)
                #if dista_2 > dista1:
                #    breakin_dists.append(dista_2)
                #    break
            
            #Adding time of travel estimate
            #dis_arr = np.array(dis_arr)
            #v_arr = np.array(v_arr)
            tt.append(np.sum(np.array(t_arr)))
            #print("Essa particula CHEGOU!!!")
            
        return tt#, breakin_dists

    
        
        
                
            
            
            
            
            
            
            
            
        
        



