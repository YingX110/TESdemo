import pandas as pd
import numpy as np
from numpy.linalg import inv
from SP_Func import sharing_principle
import matplotlib.pyplot as plt
from demo1 import f_matrix, get_matrix, Cal_S
from CarbonData import *


NumofScales = int(input("Enter the number of scales: "))
NumofProcess = int(input("Enter the number of processes: "))
FinalDemand = int(input("Enter the final demand of products: "))

ProcessInfo = pd.read_csv('Pinfo.csv')
pname = ProcessInfo['Process'].tolist()
pcounty = ProcessInfo['County (FIPS)'].tolist()
pstate = ProcessInfo['State'].tolist()
pnation = ProcessInfo['Country'].tolist()
pworld = ['World'] * NumofProcess

local = pd.read_csv('Local_C.csv')
AA = pd.read_csv('A_test.csv')
DD = pd.read_csv('D_test.csv')