# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 17:20:28 2021

@author: vcant
"""

import model_proposal

import numpy as np
import matplotlib.pyplot as plt



aem_model = model_proposal.Model(k = 10, H = 20, h0 = 18)

well = model_proposal.Well(aem_model, Q = 10, rw = 0.2, x = 30, y = 50)


xvec = np.linspace(0, 300, 100)
yvec = np.linspace(0, 300, 100)


h = []
for x,y in zip(xvec,yvec):
    head = aem_model.head(x, y)
    h.append(h)
    
from matplotlib import cm
fig2, ax = plt.subplots()
contour = plt.contour(xvec, yvec, h,
    5,
    cmap = cm.Blues)
    #colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
# fig2, ax = plt.subplots()
#contour2 = plt.contour(xvec ,yvec, psi,
    #gstream,
    #cmap = cm.binary
    #colors=['#808080', '#808080', '#808080'], extend='both')
contour.cmap.set_over('red')
contour.cmap.set_under('blue')
contour.changed()
#plt.clabel(contour, inline=1, fontsize=10)
labels = ['Streamline', 'Potentialline']
#contour2.collections[6].set_label(labels[0])
contour.collections[7].set_label(labels[1])

plt.legend(loc='upper left')
