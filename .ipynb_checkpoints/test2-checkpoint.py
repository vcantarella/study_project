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

xvec = np.linspace(0, 60, 100)
yvec = np.linspace(riv_coords[0]-10, riv_coords[1]+10, 100)

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
psi_0 = aem_model.calc_psi(0,riv_coords[0])
psi_1 = aem_model.calc_psi(0,riv_coords[1])
psi[((psi > psi_0-5) & (psi < psi_1+5))] = np.nan

contour_psi_river = plt.contour(xvec,yvec,psi,
                          40,
                          colors=('darkred',),
                          linewidths=(7,))

river_line = plt.plot([0,0],[np.min(yvec),np.max(yvec)], color = 'blue', linestyle = '-', linewidth = 16)
river_capture = plt.plot([0, 0], [riv_coords[0], riv_coords[1]], color='r', linestyle='-', linewidth=8)

tt = solv.time_travel(0.4)
print("Time of Travel: ")
print(tt)
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
