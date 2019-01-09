#!/usr/bin/env python
import pandas as pd
from scipy import *
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt



x=linspace(0,1,100)
print(x[::10])
plt.figure(0)
plt.plot(sin(x))
plt.figure(1)
plt.plot(cos(x))
plt.show()
