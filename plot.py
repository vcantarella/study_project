# -*- coding: utf-8 -*-
"""
@author: mgome
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter


class plotting:
    def __init__(self,xmin, ymin, xmax, ymax, steps):
        self.xmin=xmin
        self.ymin=ymin
        self.xmax=xmax
        self.ymax=ymax
        self.steps=steps
        
    def mesh(self):
        xvec=np.linspace(self.xmin, self.xmax, self.steps)
        yvec = np.linspace(self.ymin, self.ymax, self.steps)
        xvec, yvec = np.meshgrid(xvec,yvec)
        return xvec, yvec
    
    def fix_to_mesh(self,model):
        hl=[]
        psil=[]
        for x,y in zip(self.mesh()[0].flatten(),self.mesh()[1].flatten()):
            head = model.calc_head(x, y)
            psi_0 = model.calc_psi(x, y)
            hl.append(head)
            psil.append(psi_0)
        h= np.array(hl).reshape((self.steps,self.steps))
        psi=np.array(psil).reshape((self.steps,self.steps))
        return h , psi
    
    def plot2d(self,model,levels):
        fig2, ax = plt.subplots(figsize = (15,20))
        contour = plt.contourf(self.mesh()[0], self.mesh()[1], self.fix_to_mesh(model)[0],
            levels,
            cmap = cm.Blues)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        fig2.colorbar(contour, ax=ax, shrink=0.9)
        contour_psi = plt.contour(self.mesh()[0], self.mesh()[1],self.fix_to_mesh(model)[1],
                                  levels,
                                  colors=('darkgrey',),
                                  linewidths=(1,))
        return ax
    
    def plot3d(self, model):
        fig, ax = plt.subplots(figsize = (15,20),subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(self.mesh()[0], self.mesh()[1], self.fix_to_mesh(model)[0],
                            cmap=cm.coolwarm,
                            linewidth=0,
                            antialiased=True)                        
        plt.gca().zaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('drawdown [m]')
        fig.colorbar(surf, shrink=.8, ax=[ax], location = "left") 
        return ax
    
#%%
        

plot=plotting(0,0,150,150,100)
plotmesh=plot.fix_to_mesh(aem_model)
plot2dmodel=plot.plot2d(aem_model, 10)
plot3dmodel=plot.plot3d(aem_model)




