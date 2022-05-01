import pandas as pd
import numpy as np
from numpy.linalg import inv
from SP_Func import sharing_principle
import matplotlib.pyplot as plt

'''create objectives, gather info from attributes then search it in data inventory and generate matrix'''

class Process:
    def __init__(self, name='', county='', state='', country=''):
        self.name = name
        self.county = county
        self.state = state
        self.country = country

def create_process(n):
    lst = []
    namel = []
    countyl = []
    statel = []
    countryl = []
    for i in range(n):
        name = input('Process: ')
        county = input('County: ')
        state = input('State: ')
        country = input('Country: ')
        ele = Process(name, county, state, country)
        namel.append(name)
        countyl.append(county)
        statel.append(state)
        countryl.append(country)
        lst.append(ele)
    return namel, countyl, statel, countryl, lst

def f_matrix(A, D, demand):
    Ft = np.zeros((A.shape[0], 1))
    Ft[-1, -1] = demand
    Fe = np.zeros((D.shape[0], 1))
    return np.vstack((Ft, Fe))

def get_matrix(df, name):
    lst = []
    for i in name:
        lst.append(df.at[0, i])
    matrix = np.diag(lst)
    return matrix

def Cal_S(n, Sup, SP):
    St = Sup[0]
    for j in range(1, n):
        P = np.identity(n)
        for m in range(j):
            P = P * SP[m]
        St = St + Sup[j] * P
    return(St)

NumofScales = int(input("Enter the number of scales: "))
FinalDemand = int(input("Enter the final demand of products: "))
pname, pcounty, pstate, pcountry, processes = create_process(NumofScales)
pworld = ['World'] * len(pname)

#############################################################################################
'''load data '''
#WorldInfo = {'Emission': 4.21E10, 'Sink': 9.64E9, 'Population': 7.59E9, 'Area': 1.49E8, 'GDP': 8.63E13} # units: ton/yr, ton/yr, people, km^2, $
locS = pd.read_csv('localS_test.csv')
county = pd.read_csv('CountyCO2.csv')
state = pd.read_csv('StateCO2.csv')
country = pd.read_csv('CountryCO2.csv')
world = pd.read_csv('WorldCO2.csv')
local = pd.read_csv('LocalCO2.csv')
# Coty2loc = pd.read_csv('SP_Coty2Loc.csv')
# stat2coty = pd.read_csv('SP_Stat2Coty.csv')
AA = pd.read_csv('A_test.csv')
DD = pd.read_csv('D_test.csv')


'''Sharing Principle Data'''
state_gdp = pd.read_csv('state_gdp.csv')
state_pop = pd.read_csv('state_pop.csv')
state_area = pd.read_csv('state_area.csv')
state_emission = pd.read_csv('State_Emi.csv')
state_invgdp = pd.read_csv('state_invgdp.csv')

county_area = pd.read_csv('county_area.csv')
county_pop = pd.read_csv('county_pop.csv')
county_emission = pd.read_csv('county_emission.csv')

region_area = pd.read_csv('region_area.csv', encoding='unicode_escape')
region_emission = pd.read_csv('Region_Emi.csv', encoding='unicode_escape')
region_gdp = pd.read_csv('region_gdp.csv', encoding='unicode_escape')
region_invgdp = pd.read_csv('region_invgdp.csv', encoding='unicode_escape')
region_pop = pd.read_csv('region_pop.csv', encoding='unicode_escape')

local_emission = pd.read_csv('Local_Emi.csv')
world_emission = pd.read_csv('Global_Emi.csv')

World = {'gdp': 8.67e7, 'emission': world_emission, 'invgdp': 7.236e-2, 'pop': 7.628e9, 'area': 1.361e8} # unit: million $, ton/yr, 1/million $, km^2
Nation = {'gdp': region_gdp, 'emission': region_emission, 'invgdp': region_invgdp, 'pop': region_pop, 'area': region_area} #data based on year 2018
State = {'gdp': state_gdp, 'emission': state_emission, 'invgdp': state_invgdp, 'pop': state_pop, 'area': state_area} #data based on year 2018
County = {'gdp': '', 'emission': county_emission, 'invgdp': '', 'pop': county_pop, 'area': county_area} #data based on year 2018
Local = {'emission': local_emission, 'invgdp': '', 'area': ''} #user input

SPinfo = {'world': World, 'nation': Nation, 'state': State, 'county': County, 'local': Local}
# loc = {'world': pworld, 'nation': pcountry, 'state': pstate, 'county': pcounty}
loc = {'world': pworld, 'nation': pcountry, 'state': pstate, 'county': pcounty, 'local': pname}



######################################################################################################
'''generate A, D, C, m and f martix'''
Amatrix = np.matrix(AA.values)
Dmatrix = np.matrix(DD.values)
Fmatrix = f_matrix(Amatrix, Dmatrix, FinalDemand)
Imatrix = -np.identity(Dmatrix.shape[0])
C_c = Amatrix.shape[0] + Dmatrix.shape[0] - Amatrix.shape[1]
Cmatrix = np.zeros((Amatrix.shape[0], C_c))


'''generate eco martix'''
# localS = np.matrix(locS.values)
localS = get_matrix(local, pname)
countyS = get_matrix(county, pcounty)
stateS = get_matrix(state, pstate)
countryS = get_matrix(country, pcountry)
worldS = get_matrix(world, pworld)
# county2local = get_matrix(Coty2loc, pname)
# state2county = get_matrix(stat2coty, pname)

S = [localS, stateS, countryS, worldS]
# SP = [county2local, state2county]
SP = sharing_principle(loc, NumofScales, SPinfo)

Smatrix = Cal_S(NumofScales, S, SP)
me = 1 + np.zeros((Smatrix.shape[0], 1))


'''generate big martix'''
Zeromatrix = np.zeros((Amatrix.shape[0], Imatrix.shape[1]))
A0 = np.hstack((Amatrix, Zeromatrix))
DI = np.hstack((Dmatrix, Imatrix))
CS = np.vstack((Cmatrix, -Smatrix))

Lmatrix = np.vstack((A0, DI))
Rmatrix = Fmatrix - CS * me


'''Calculation of scaling factor and '''
res = inv(Lmatrix) * Rmatrix
print(res)

'''plot the vk'''

def bar_plot(vector, name):
    m = np.split(vector, [Amatrix.shape[1]])[0]
    VecD = Dmatrix * m
    VecS = VecD - np.split(vector, [Amatrix.shape[1]])[1]
    name = np.transpose(np.matrix(name))
    matrix = np.hstack((name, VecD, VecS))
    df = pd.DataFrame(matrix, columns=['ProcName', 'Demand', 'Supply'])
    df = df.set_index('ProcName')
    df['Demand'] = df['Demand'].astype(float)
    df['Supply'] = df['Supply'].astype(float)
    df.plot(y=["Demand", "Supply"], kind="bar")
    plt.show()

bar_plot(res, pname)


print('done')