# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 11:11:07 2021

@author: vcant
"""

import model_proposal
import solvers
import numpy as np
import matplotlib.pyplot as plt

### Example 01: One well: River capture length, percentage of discharge
#-------------------------------------------

aem_model = model_proposal.Model(k = 3, H = 20, h0 = 18)


well = model_proposal.Well(aem_model, Q = 250, rw = 0.2, x = 30, y = 50)

solv = solvers.river_length(aem_model)

print("River Capture Length, Capture position and contribution to discharge is:")
print(solv.solve_river_length())

length, riv_coords, capture_fraction = solv.solve_river_length()
tt = solv.time_travel(0.2)
#%%
xvec = np.linspace(0, 60, 100)
rivmin=riv_coords[0]-int(riv_coords[0]*0.9)
rivmax=riv_coords[1]+int(riv_coords[0]*0.9)
yvec = np.linspace(rivmin, rivmax, 100)

xvec, yvec = np.meshgrid(xvec,yvec)

h = []
psi = []
for x,y in zip(xvec.flatten(),yvec.flatten()):
    
    head = aem_model.calc_head(x, y)
    psi_0 = aem_model.calc_psi(x, y)
    
    h.append(head)
    psi.append(psi_0)

h = np.array(h).reshape((100,100))
psi = np.array(psi).reshape((100,100))
from matplotlib import cm
fig2, ax = plt.subplots(1,2,figsize = (18,12),gridspec_kw={'width_ratios': [1, 3.5]})
contour = plt.contourf(xvec, yvec, h,
    8,
    cmap = cm.Blues, alpha = 0.5)
    #colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
plt.rcParams['contour.negative_linestyle'] = 'solid'
ax[1].set_xlabel('x [m]')
ax[1].set_ylabel('y [m]')

fig2.colorbar(contour, ax=ax, shrink=0.9)
contour_psi = ax[1].contour(xvec,yvec,psi,
                          20,
                          colors=('#848482',),
                          linewidths=(1,),
                          linestyle = ('-',))

#ax[1].streamplot(xvec[:,0], yvec[0,:], psi[:,0], psi[0,:], color='0.8', density=2)
dy, dx = np.gradient(-h) # Flow goes down gradient (thus -zi)
#
widths = 0.00001
e=1
#qui=ax[1].quiver(xvec, yvec, dx, dy, linewidths=0.1, alpha=0.5,width=0.001)
qui=ax[1].quiver(xvec[::e,::e], yvec[::e,::e], dx[::e,::e], dy[::e,::e], linewidths=0.1, alpha=0.5,width=0.001)
#stream_points = np.array(zip(np.arange(-9,9,.5), -np.arange(-9,9,.5)))
#ax[1].streamplot(xvec[::e,::e], yvec[::e,::e], dx[::e,::e], dy[::e,::e], color='#4169e1', 
#           linewidth=1, density=0.7,arrowsize=1)
#ax[1].quiverkey(qui, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E',
#                   coordinates='figure')
psi_0 = aem_model.calc_psi(0,riv_coords[0])
psi_1 = aem_model.calc_psi(0,riv_coords[1])
psi[((psi > psi_0) & (psi < psi_1))] = np.nan

contour_psi_river = ax[1].contour(xvec,yvec,psi,
                          50,
                          colors=('darkred',),
                          linewidths=(2,))

river_line = ax[1].plot([0,0],[np.min(yvec),np.max(yvec)], color = '#4169e1', linestyle = '-', linewidth = 20)
river_capture = ax[1].plot([0, 0], [riv_coords[0], riv_coords[1]], color='r', linestyle='-', linewidth=8)

loc=[np.nan]*int((len(yvec[:,0])-len(tt))/2)
ax[0].plot(loc+tt+loc,yvec[:,0],  '--o',color="#0592D0", markersize=3)
ax[0].set_xlabel('Travel time - Days')
ax[0].set_ylabel('y [m]')
ax[0].set_ylim(0,100)
#ax[0].set_xlim(ax[0].get_xlim()[::-1])
ax[0].grid(alpha=0.2)
fig2.delaxes(ax[0])
#%%
from plot import *

plot=plotting(0, 90, riv_coords, 100)
plot.plot2d(aem_model, tt=tt,levels=8)
plot.plot2d(aem_model, tt=tt,levels=8, quiver=False, streams=True)
plot.plot2d(aem_model, tt=tt,levels=8, quiver=True, streams=False)
plot.plot3d(aem_model)


#%%

<<<<<<< HEAD
tt = solv.time_travel(0.3)
=======
>>>>>>> 5c42dcfecae208a568529784681432079dfb6aa1
print("Time of Travel: ")
print(tt)

#%%
### Example 0: Multiple Wells:
#-------------------------------------------

well3 = model_proposal.Well(aem_model, Q = 150, rw = 0.2, x = 10, y = 30)

well4 = model_proposal.Well(aem_model, Q = 50, rw = 0.2, x = 50, y = 10)

xvec = np.linspace(0, 60, 100)
yvec = np.linspace(00, 60, 100)

xvec, yvec = np.meshgrid(xvec,yvec)

h = []
psi = []
for x,y in zip(xvec.flatten(),yvec.flatten()):
    
    head = aem_model.calc_head(x, y)
    psi_0 = aem_model.calc_psi(x, y)
    
    h.append(head)
    psi.append(psi_0)

h = np.array(h).reshape((100,100))
psi = np.array(psi).reshape((100,100))
from matplotlib import cm
fig2, ax = plt.subplots(figsize = (15,15))
contour = plt.contourf(xvec, yvec, h,
    8,
    cmap = cm.Blues, alpha = 0.7)
    #colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
fig2.colorbar(contour, ax=ax, shrink=0.9)
contour_psi = plt.contour(xvec,yvec,psi,
                          20,
                          colors=('darkgrey',),
                          linewidths=(4,),
                          linestyle = ('-',))
river_line = plt.plot([0,0],[np.min(yvec),np.max(yvec)], color = 'blue', linestyle = '-', linewidth = 16)
