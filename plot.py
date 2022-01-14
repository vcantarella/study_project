# -*- coding: utf-8 -*-
"""
@author: mgome
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter


class plotting:
    def __init__(self,xmin, xmax, riv_coords, steps):
        self.xmin=xmin
        self.ymin=riv_coords[0]-int(0.9*riv_coords[0])
        self.xmax=xmax
        self.ymax=riv_coords[1]+int(0.9*riv_coords[0])
        self.steps=steps
        self.riv_coords=riv_coords
        
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
    
    def plot2d(self,model,tt=None,levels=10, alpha=0.6, quiver=False, streams=False):
        
        h=self.fix_to_mesh(model)[0]
        psi=self.fix_to_mesh(model)[1]
        
        psiriv=self.fix_to_mesh(model)[1]
        psi_riv0= model.calc_psi(0, self.riv_coords[0])
        psi_riv1= model.calc_psi(0, self.riv_coords[1])
        psiriv[((psiriv > psi_riv0) & (psiriv < psi_riv1))] = np.nan
        
        dy, dx = np.gradient(-h)
        e=1
                
        fig, ax = plt.subplots(1,2,figsize = (18,12),gridspec_kw={'width_ratios': [1, 3.5]})
        contour = plt.contourf(self.mesh()[0], self.mesh()[1], h,
            levels,
            cmap = cm.Blues,alpha=alpha)
        ax[1].set_xlabel('x [m]')
        ax[1].set_ylabel('y [m]')
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        fig.colorbar(contour, ax=ax[1], shrink=0.9)
        
        if not (quiver) and not(streams):
            ax[1].contour(self.mesh()[0], self.mesh()[1],psi,
                                      int(levels*2.5),
                                      colors=('#848482',),
                                      linewidths=(1,))
        elif quiver:
            ax[1].quiver(self.mesh()[0][::e,::e], self.mesh()[1][::e,::e], 
                         dx[::e,::e], dy[::e,::e], 
                         linewidths=0.1, alpha=0.5,width=0.001)
        if streams:
            ax[1].streamplot(self.mesh()[0][::e,::e], self.mesh()[1][::e,::e], 
                             dx[::e,::e], dy[::e,::e], color='#003366', 
                              linewidth=0.8, density=0.6,arrowsize=1.2,zorder=0)
        if tt is not None:   
            ax[1].contour(self.mesh()[0], self.mesh()[1],psiriv,
                                      int((levels*3.5)),
                                      colors=('darkred',),
                                      linewidths=(1,))
        
        ax[1].plot([0,0],[np.min(self.mesh()[1]),np.max(self.mesh()[1])], 
                   color = '#4169e1', linestyle = '-', linewidth = 20) #river line
        ax[1].plot([0, 0], [self.riv_coords[0], self.riv_coords[1]], 
                   color='r', linestyle='-', linewidth=8) #River capture


        if tt is not None:
        #Travel times plot
            loc=[np.nan]*int((len(self.mesh()[1])-len(tt))/2)
            ax[0].plot(loc+tt+loc,self.mesh()[1],  '--o',color="#0592D0", markersize=3)
            ax[0].set_xlabel('Travel time - Days')
            ax[0].set_ylabel('y [m]')
            ax[0].set_ylim(0,100)
            ax[0].grid(alpha=0.2)
        else:
            fig.delaxes(ax[0])
        #plt.tight_layout()

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
    





