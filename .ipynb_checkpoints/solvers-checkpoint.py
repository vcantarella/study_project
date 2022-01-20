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
        
        ys = np.linspace(sol_el[0]+0.1,sol_el[1]-0.1,int(sol_el[1]-sol_el[0]-1))
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
        def qx(x,y):
            return -1*(-Qx + Q/(4*np.pi)*((2*(x-xw)/((x-xw)**2+(y-yw)**2))-(2*(x-(xw-2*d)))/((x-(xw-2*d))**2+(y-yw)**2)))/self.model.calc_head(x, y)
        
        def qy(x,y):
            return -1*(Q/(4*np.pi)*((2*(y-yw)/((x-xw)**2+(y-yw)**2))-(2*(y-yw))/((x-(xw-2*d))**2+(y-yw)**2)))/self.model.calc_head(x, y)
        
        '''
        Formulas for correction of the trajectory (stream function)
        '''
        def equation_x(x_a, psi):
                    return Qx*y_2 + (Q/(2*np.pi))*(np.arctan2((y_2-yw),(x_a-xw))- np.arctan2((y_2-yw),(x_a-(xw-2*d))))-psi
        
        def equation_y(y_a, psi) :
                    return Qx*y_a + (Q/(2*np.pi))*(np.arctan2((y_a-yw),(x_2-xw))- np.arctan2((y_a-yw),(x_2-(xw-2*d))))-psi
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
                qx1 = qx(x1,y1)
                qy1 = qy(x1,y1)
                vx = qx1/ne
                vy = qy1/ne
                v_i = np.sqrt(vx**2+vy**2)
                
                
                #Part 2: estimating second point
                
                x_2 = np.float(x1 + delta_s*vx/v_i)
                y_2 = np.float(y1 + delta_s*vy/v_i)
                
                
                
                
                ## Adjust for psi:
                #x_a = sympy.symbols('x_a')
                #y_a = sympy.symbols('y_a')
                
                sols = fsolve(equation_x, x_2, (psi))
                sol_el_x = sols[0]
                
                
                sols_y = fsolve(equation_y, y_2, (psi))
                sol_el_y = sols_y[0]
                
                pos_locs_y = [(sol_el_x,y_2)]
                pos_locs_x = [(x_2,sol_el_y)]
                pos_locs = pos_locs_x + pos_locs_y

                dista = 1e9 #Initial distance to be updated in the loop
                #print(pos_locs)
                #Calculating distance and correcting second point:
                for xp,yp in pos_locs:
                    dist = np.sqrt((xp-x1)**2+(yp-y1)**2)
                    if dist < dista:
                        x_2 = xp
                        y_2 = yp
                        dista = dist #Distance updated with new point
                #dis_arr.append(dista)
                #print('distancia da particula:')
                #print(np.sqrt((x1-xw)**2+(y1-yw)**2))
                #Looping
                x1 = x_2
                y1 = y_2
                dista_2 = np.sqrt((x1-xw)**2+(y1-yw)**2)
                if dista_2 > dista1:
                    breakin_dists.append(dista_2)
                    break
                    
                qx2 = qx(x_2,y_2)
                qy2 = qy(x_2,y_2)
                vx2 = qx2/ne
                vy2 = qy2/ne
                               
                v_i2 = np.sqrt(vx2**2+vy2**2)
                logv = np.log(v_i2/v_i)
                A = (v_i2-v_i)/dista
                t_arr.append((1/A)*logv)
            
            #Adding time of travel estimate
            #dis_arr = np.array(dis_arr)
            #v_arr = np.array(v_arr)
            tt.append(np.sum(np.array(t_arr)))
            #print("Essa particula CHEGOU!!!")
            
        return tt#, breakin_dists
            
            
            
                
            
            
            
            
            
            
            
            
        
        



