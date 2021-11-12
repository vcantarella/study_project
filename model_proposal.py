# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:18:14 2021

@author: vcant
"""

import numpy as np
import pandas as pd

class Model:
    def __init__(self, k, H, ho):
        self.k = k
        self.H = H
        self.ho = ho
        self.aem_elements = []
        self.well_df = pd.DataFrame({wellid})

class Well:
    """
    Element to create Well for the model
    """
    def __init__(self, model,Q, rw, x,y):
        self.x = x
        self.y = y
        self.Q = Q
        self.rw = rw
        model.aem_elements.append(self)
      def phi(self):
          self.Q/2*pi

aem_model = Model(10, 20, 18)

well = Well(aem_model, 10, 0.2, 30, 50)

print(aem_model.aem_elements)
