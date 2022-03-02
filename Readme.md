# RBF AEM Model

This is the repository of the River Bank Filtration Analytic Element Model developed by Cantarella V., Gómez M. and Villa A. for the Study Project Assignment from TU-Dresden Hydro Science Deparment

The work has been done under supervision of Dr. Prabhas Yadav.

The model is contained in three scripts:

* [model_proposal.py](https://github.com/vcantarella/study_project/blob/main/model_proposal.py) : The AEM model framework with the classes and calculation methods for developing a river bank filtration. Description is included in the file. The main methods implemented are:
    - initiate model and add wells
    - calculate potential and stream function
    - calculate aquifer hydraulic heads
* [solvers.py](https://github.com/vcantarella/study_project/blob/main/solvers.py) : This script contain the solver class used to calculate the advanced results for River Bank Filtration Assessment. The implemented methods are:
    - calculate river capture length and bank filtrate proportion
    - calculate travel time of particle from the river to the well. this include travel time in multiple locations of the river capture length, minimum travel time and flow averaged travel time.
* [plot.py](https://github.com/vcantarella/study_project/blob/main/plot.py): This script contain methods for easy plotting of model results in 2d or 3d.

The user is encouraged to check the Jupyter notebooks that contain the results and model validation with MODFLOW:

* [Model Validation](https://github.com/vcantarella/study_project/blob/main/model_verification.ipynb): Notebook with concurrent implementation of a RBF AEM model and an identical MODFLOW model for validation. Requires flopy and MODFLOW and MODPATH executables.

* [Model Exploration](https://github.com/vcantarella/study_project/blob/main/model_exploration.ipynb): Notebook with model exploration of variables and results.

* [Case Studies](https://github.com/vcantarella/study_project/blob/main/case_studies.ipynb): Notebook with comparison of RBF AEM model results and real world case studies and results (including MODFLOW simulation)

Below we briefly explain how to run a simple RBF model and extract the main results:



```python
import pandas as pd
model_params = pd.DataFrame({'parameter' : [], 'value' : [], 'unit' : []})
model_params.loc[0] = ['Hydraulic Conductivity', 0.12e-3, 'm/s']
model_params.loc[1] = ['River Reference Head', 80, 'm']
model_params.loc[2] = ['Well Distance to the river', 63, 'm']
model_params.loc[3] = ['Well Pumping Rate', 0.044, 'm3/s']
model_params.loc[4] = ['Hydraulic Gradient', 0.001, '']
model_params.loc[5] = ['Reference Specific Baseflow', 0.12e-3*0.001*85*3600*24, 'm/d']

model_params


```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>parameter</th>
      <th>value</th>
      <th>unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Hydraulic Conductivity</td>
      <td>0.00012</td>
      <td>m/s</td>
    </tr>
    <tr>
      <th>1</th>
      <td>River Reference Head</td>
      <td>80.00000</td>
      <td>m</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Well Distance to the river</td>
      <td>63.00000</td>
      <td>m</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Well Pumping Rate</td>
      <td>0.04400</td>
      <td>m3/s</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Hydraulic Gradient</td>
      <td>0.00100</td>
      <td></td>
    </tr>
    <tr>
      <th>5</th>
      <td>Reference Specific Baseflow</td>
      <td>0.88128</td>
      <td>m/d</td>
    </tr>
  </tbody>
</table>
</div>



## Step 1. Import the required libraries


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import model_proposal #AEM model location
import solvers #Solvers for some analysis from the aem model
```

## Step 2. Create and define the model

This step we:
* create the model with the ```Model``` class
* define the well with the ```Well``` class
* find the river length problem with the ```solvers.river_length``` class.
* find the travel time results with the ```time_travel``` method.


```python
# Define model with hydraulic condutivity = 0.12e-3 m/s, height = 85, reference river head = 80

aem_model = model_proposal.Model(k = 0.12e-3*3600*24, H = 85, h0 = 80)

aem_model.Qo_x = -0.12e-3*3600*24*0.001*85

# Add well at position x = 63, y = 50 and pumping rate of 0.044 m3/s, well radius = 0.01 m

well = model_proposal.Well(aem_model, Q = 0.005*3600*24, rw = 0.01, x = 63, y = 50)

# Solver for river length and river water capture fraction.

solv = solvers.river_length(aem_model)

print("River Capture Length, Capture position and contribution to discharge is:")
print(solv.solve_river_length())

# Here we collect all results from the first solve method:
#length: River capture lenght
# riv_coords: end point coordinates of the captured length
# capture_fraction: fraction of pumped water that is derived from the river.
length, riv_coords, capture_fraction = solv.solve_river_length()

#Here we collect all the results from the travel time method:
#tt: travel time array of particles
# ys: initial particle location
# avgtt: flow averaged time of travel
# mintt: minimum travel time
#traj_array: x and y location of the calculated trajectory of the particles (used for plotting) 
tt, ys, avgtt, mintt, traj_array = solv.time_travel(0.2, delta_s = 0.4, calculate_trajectory = True)

print("Flow Averaged Time of Travel: "+str(np.round(avgtt,2)) + " [d]")
print("Minimum Time of Travel: "+str(np.round(mintt,2)) + " [d]")


```

    River Capture Length, Capture position and contribution to discharge is:
    (153.11640342946325, [-26.558201714731624, 126.55820171473162], 0.24929722047129896)
    Flow Averaged Time of Travel: 716.58 [d]
    Minimum Time of Travel: 463.1 [d]
    

## Step 3. Plotting the results with the plot method

The ```plotting``` class was created to simplify the plotting of results of the RBF model.
Below there is an example on how to use the method to plot model results


```python
import plot

img = plot.plotting(0,100,-30,130,100,riv_coords)

# The plot 2d method optionally can contain the trajectory of the sampled particles and their travel time:
img.plot2d(aem_model, tt=tt, ys = ys, traj_array = traj_array, levels=8, quiver=False, streams=True);
```


    
![png](output_7_0.png)
    

