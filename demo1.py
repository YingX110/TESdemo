import pandas as pd
import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt

'''create objectives, gather info from attributes then search it in data inventory and generate matrix'''

class Process:
    def __init__(self, name='', county='', state='', country=''):
        self.name = name
        self.county = county
        self.state = state
        self.country = country
