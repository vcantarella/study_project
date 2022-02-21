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


well = model_proposal.Well(aem_model, Q = 300, rw = 0.2, x = 20, y = 50)


solv = solvers.river_length(aem_model)

print("River Capture Length, Capture position and contribution to discharge is:")
print(solv.solve_river_length())

length, riv_coords, capture_fraction = solv.solve_river_length()
tt,ys,abgtt,mintt, traj_array = solv.time_travel(0.2, calculate_trajectory = True)

#%%
from plot import *

plot=plotting(0, 60, riv_coords, 100)
plot.plot2d(aem_model, tt=tt, ys = ys, traj_array = traj_array,levels=8)
plot.plot2d(aem_model, tt=tt,ys = ys, levels=8, quiver=False, streams=True)
plot.plot2d(aem_model, tt=tt,ys = ys, levels=8, quiver=True, streams=False)
plot.plot3d(aem_model)


#%%

print("Time of Travel: ")
print(tt)

#%%
### Example 0: Multiple Wells:
#-------------------------------------------

well3 = model_proposal.Well(aem_model, Q = 150, rw = 0.2, x = 10, y = 30)

well4 = model_proposal.Well(aem_model, Q = 50, rw = 0.2, x = 50, y = 10)


plot=plotting(0, 60, riv_coords, 100)
plot.plot2d(aem_model, levels=15, quiver=False, streams=False)
