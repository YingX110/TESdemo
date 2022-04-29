import pandas as pd
import numpy as np

state_gdp = pd.read_csv('state_gdp.csv')
state_pop = pd.read_csv('state_pop.csv')
state_area = pd.read_csv('state_area.csv')
state_emission = pd.read_csv('state_emission.csv')
state_invgdp = pd.read_csv('state_invgdp.csv')

county_area = pd.read_csv('county_area.csv')
county_pop = pd.read_csv('county_pop.csv')
county_emission = pd.read_csv('county_emission.csv')

region_area = pd.read_csv('region_area.csv', encoding='unicode_escape')
region_emission = pd.read_csv('region_emission.csv', encoding='unicode_escape')
region_gdp = pd.read_csv('region_gdp.csv', encoding='unicode_escape')
region_invgdp = pd.read_csv('region_invgdp.csv', encoding='unicode_escape')
region_pop = pd.read_csv('region_pop.csv', encoding='unicode_escape')

Global = {'gdp': 8.67e7, 'emission': 4.726e10, 'invgdp': 7.236e-2, 'pop': 7.628e9, 'area': 1.361e8} # unit: million $, ton/yr, 1/million $, km^2
Nation = {'gdp': region_gdp, 'emission': region_emission, 'invgdp': region_invgdp, 'pop': region_pop, 'area': region_area} #data based on year 2018
State = {'gdp': state_gdp, 'emission': state_emission, 'invgdp': state_invgdp, 'pop': state_pop, 'area': state_area} #data based on year 2018
County = {'gdp': '', 'emission': county_emission, 'invgdp': '', 'pop': county_pop, 'area': county_area} #data based on year 2018

SPinfo = {'global': Global, 'nation': Nation, 'state': State, 'county': County}


def sharing_principle(Nation, State, County, nScales):
    lst = []
    #num_of_scales = input('Number of scales (Local, County, State, Nation, Global): ')
    SP = input('Sharing Principle (gdp, inverse of gdp, emission, area, population): ')
    for i in range(nScales):
        scale = input('Geo-scale' + str(i) + ': ')
        #lst.append(SPinfo[scale])
        lst.append(scale)

'''get sharing principles between scales
e.g. list = [global, national]
principle = 'emission'
loc = {'global': gname, 'nation': nname, 'state': sname, 'county': cname}
'''
def SP_CAL(list, principle, loc):
    d1 = SPinfo[list[0]][principle] #nation
    d2 = SPinfo[list[1]][principle] #global
    s1 = loc[list[0]] #[n1, n2, n3 ...]
    s2 = loc[list[1]] #[g1, g2, g3 ...]
    sp_lst = []
    for i in range(len(s1)):
        sp = d1.at[0, s1[i]] / d2.at[0, s2[i]]
        sp_lst.append(sp)
    return np.diag(sp_lst)




