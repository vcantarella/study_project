# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 17:20:28 2021

@author: vcant
"""

import model_proposal

import numpy as np
import matplotlib.pyplot as plt



aem_model = model_proposal.Model(k = 3, H = 20, h0 = 18)


well = model_proposal.Well(aem_model, Q = 200, rw = 0.2, x = 30, y = 50)


xvec = np.linspace(0, 150, 100)
yvec = np.linspace(-100, 100, 100)

xvec, yvec = np.meshgrid(xvec,yvec)


h = []
psi = []
for x,y in zip(xvec.flatten(),yvec.flatten()):
    print(x)
    print(y)
    head = aem_model.calc_head(x, y)
    psi_0 = aem_model.calc_psi(x, y)
    print(head)
    h.append(head)
    psi.append(psi_0)
print(h)
h = np.array(h).reshape((100,100))
psi = np.array(psi).reshape((100,100))
from matplotlib import cm
fig2, ax = plt.subplots(figsize = (15,20))
contour = plt.contourf(xvec, yvec, h,
    8,
    cmap = cm.Blues)
    #colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
fig2.colorbar(contour, ax=ax, shrink=0.9)
contour_psi = plt.contour(xvec,yvec,psi,
                          10,
                          colors=('darkgrey',),
                          linewidths=(2,))

## Add NEW WELL:
    
well2 = model_proposal.Well(aem_model, Q = 200, rw = 0.2, x = 10, y = 30)


h = []
psi = []
for x,y in zip(xvec.flatten(),yvec.flatten()):
    print(x)
    print(y)
    head = aem_model.calc_head(x, y)
    psi_0 = aem_model.calc_psi(x, y)
    print(head)
    h.append(head)
    psi.append(psi_0)
print(h)
h = np.array(h).reshape((100,100))
psi = np.array(psi).reshape((100,100))
from matplotlib import cm
fig2, ax = plt.subplots(figsize = (15,20))
contour = plt.contourf(xvec, yvec, h,
    8,
    cmap = cm.Blues)
    #colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
fig2.colorbar(contour, ax=ax, shrink=0.9)
contour_psi = plt.contour(xvec,yvec,psi,
                          10,
                          colors=('darkgrey',),
                          linewidths=(2,))
