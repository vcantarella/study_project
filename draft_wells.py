# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 12:36:35 2021

@author: mgome
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:18:14 2021

@author: vcant , mgomezo, alejavillaa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter

class Model:
    xmin, xmax=  0, 200
    ymin, ymax= 0, 200
    steps= 50
    def __init__(self, k, H, h0, n, river = None, x_ref = 0, y_ref = 0, Qx=0, Qy=0):
        self.k = k
        self.H = H
        self.h0 = h0
        self.Qx=Qx  #baseflow in the x direction
        self.Qy= Qy
        self.n=n
        self.aem_elements = []
        self.well_df = pd.DataFrame({'wellid' : [],
                                     'Discharge': [],
                                     'X': [],
                                     'Y': []})
        
        #Mesh
        self.xvec=np.linspace(Model.xmin, Model.xmax, Model.steps)
        self.yvec=np.linspace(Model.ymin, Model.ymax, Model.steps)
        self.xmesh, self.ymesh =np.meshgrid(self.xvec, self.yvec) 
        
        
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
                
    
    def calc_phi_well(self):
        """
        Method to calculate the discharge potential for a mesh:

        Parameters
        ----------
        x,y location of interest.

        Returns
        -------
        phi(x,y) float.

        """
        phi= - self.Qx * self.xmesh - self.Qy * self.ymesh   #baseflow
        if self.h0 < self.H:
            phi00 = -phi + 0.5 * self.k * self.h0 **2
        else:
            phi00 = -phi + self.k * self.H * self.h0 - 0.5 * self.k * self.H **2
        
        for element in self.aem_elements:
            r= np.sqrt((self.xmesh - element.x)**2 + (self.xmesh - element.y)**2)
            phi= phi + (element.Qwell / (2 * np.pi)) * np.arctan2((self.ymesh - element.y), (self.xmesh -element.x))
 
        return phi00, phi00 + phi
    
    def calc_psi_well(self): 
        psi= - self.Qx * self.ymesh + self.Qy * self.xmesh
        for element in self.aem_elements:
            psi= psi + (element.Qwell / (2 * np.pi)) * np.arctan2((self.ymesh - element.y), (self.xmesh -element.x))
        return psi  
    
    
    def head(self):
        phi00 = self.calc_phi_well()[0]
        phi = self.calc_phi_well()[1]
        phicrit = phi00 + 0.5 * self.k * self.H **2 
        conditional= phi >= phicrit
        hc = 0.5 * self.H + (1 / self.k / self.H) *phi
        hu = np.sqrt((2 / self.k) * (phi)) 
        h=conditional * hc+ ~conditional * hu
        return h , conditional   # head
    
    def discharge_vector(self):
        h= self.head()[0]
        phi = self.calc_psi_well()
        [u,v] = np.gradient(-phi)   
        conditional= self.head()[1]                    # discharge vector  
        Hh = conditional * self.H + ~conditional *h                   # aquifer depth  
        u = u / Hh / (Model.xmax- Model.xmin)/Model.steps / self.n
        v = v / Hh / (Model.ymax- Model.ymin)/Model.steps / self.n       
        return u, v
   
         
class Well:
    """
    Element to create Well for the model
    """
    xcoor=[]
    ycoor=[]
    def __init__(self, model,Qwell, rw, x,y):
        self.x = x
        self.y = y
        self.Qwell=Qwell
        self.rw = rw
        model.aem_elements.append(self)
        Well.xcoor.append(self.x)
        Well.ycoor.append(self.y)
        
    def add_coor(self):
        self.xcoor.append(self.x)
        return print(self.xcoor)


aem_model = Model(k = 10, H = 20,n=0.3, h0 = 18, Qx=10, Qy=0)
well = Well(aem_model, Qwell = 10, rw = 0.2, x = 30, y = 50)
well2 = Well(aem_model, Qwell = 20,  rw = 0.2, x = 40, y = 60)
aem_model.calc_phi_well()

 

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(aem_model.xmesh, aem_model.ymesh, aem_model.head()[0],
                    cmap=cm.coolwarm,
                    linewidth=0,
                    antialiased=True)                         # surface 
plt.gca().zaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
#ax.set_title('3-Plot')
# set z (h)-axis invisible for better visibilty if colorbar is active
#if fig.colorbar:
#    ax.set_zticks([])
#else:
ax.set_zlabel('drawdown [m]')
fig.colorbar(surf, shrink=.8, ax=[ax], location = "left") # ax=[ax], location='left' for left side

    
fig2, ax = plt.subplots()
    
contour = plt.contour(aem_model.xmesh, aem_model.ymesh, aem_model.head()[0],
        10,
        cmap = cm.Blues)
        #colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
# fig2, ax = plt.subplots()
contour2 = plt.contour(aem_model.xmesh, aem_model.ymesh, aem_model.psi(),
    10,
    #cmap = cm.binary
    colors=['#808080', '#808080', '#808080'], extend='both')
contour.cmap.set_over('red')
contour.cmap.set_under('blue')
contour.changed()
#plt.clabel(contour, inline=1, fontsize=10)
labels = ['Streamline', 'Potentialline']
contour2.collections[6].set_label(labels[0])
contour.collections[7].set_label(labels[1])

plt.legend(loc='upper left')

u=aem_model.discharge_vector()[0]
v=aem_model.discharge_vector()[1]

plt.quiver(aem_model.xmesh, aem_model.ymesh,u,v)                          # arrow field // quiver(x,y,u,v,'y') 
xvec= aem_model.xmesh[0]
yvec= aem_model.ymesh [0]                                  # flowpaths 
xstart = []
ystart = []
for i in range(100):
    if v[1,i] > 0:
        xstart = [xstart, xvec[i]]
        ystart = [ystart, yvec[1]]
    if v[99,i] < 0:
        xstart = [xstart, xvec[i]]
        ystart = [ystart, yvec[99]]
    if u[i,1] > 0:
        xstart = [xstart, xvec[1]]
        ystart = [ystart, yvec[i]]
    if u[i,99] < 0:
        xstart = [xstart, xvec[99]]
        ystart = [ystart, yvec[i]]

h = plt.streamplot(aem_model.xmesh, aem_model.ymesh,u,v,)#,xstart,ystart)
plt.streamplot(aem_model.xmesh, aem_model.ymesh,u,v,color='b')#,xstart,ystart)
 
       

xstart = well.x + well.rw*np.cos(2*np.pi*np.array([1,1,0])/0) 
ystart = well.y + well.rw*np.sin(2*np.pi*np.array([1,1,0])/0)
seed_points = np.array([xstart,ystart])

h = plt.streamplot(aem_model.xmesh, aem_model.ymesh,-u,-v,start_points=seed_points.T)


