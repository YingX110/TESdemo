import pandas as pd

'''
load supply data
*for county scale assume all public land
'''
county = pd.read_csv('CountyCO2.csv')
state = pd.read_csv('State_PubC.csv')
nation = pd.read_csv('Nation_PubC.csv')
world = pd.read_csv('World_PubC.csv')


'''load sharing principle data'''
state_gdp = pd.read_csv('State_GDP.csv')
state_pop = pd.read_csv('State_Pop.csv')
state_area = pd.read_csv('State_Area.csv')
state_emission = pd.read_csv('State_Emi.csv')
state_invgdp = pd.read_csv('State_invGDP.csv')

county_area = pd.read_csv('County_Area.csv')
county_pop = pd.read_csv('County_Pop.csv')
county_emission = pd.read_csv('County_Emi.csv')

nation_area = pd.read_csv('Nation_Area.csv')
nation_emission = pd.read_csv('Nation_Emi.csv')
nation_gdp = pd.read_csv('Nation_GDP.csv')
nation_invgdp = pd.read_csv('Nation_invGDP.csv')
nation_pop = pd.read_csv('Nation_Pop.csv')

world_emission = pd.read_csv('World_Emi.csv')
world_gdp = pd.read_csv('World_GDP.csv')
world_invgdp = pd.read_csv('World_invGDP.csv')
world_area = pd.read_csv('World_Area.csv')
world_pop = pd.read_csv('World_Pop.csv')

local_emission = pd.read_csv('Local_Emi.csv')

''' 
unit: million $, ton/yr, 1/million $, km^2
data based on year 2018
'''
World = {'gdp': world_gdp, 'emission': world_emission, 'invgdp': world_invgdp, 'pop': world_pop, 'area': world_area}
Nation = {'gdp': nation_gdp, 'emission': nation_emission, 'invgdp': nation_invgdp, 'pop': nation_pop, 'area': nation_area}
State = {'gdp': state_gdp, 'emission': state_emission, 'invgdp': state_invgdp, 'pop': state_pop, 'area': state_area}
County = {'gdp': '', 'emission': county_emission, 'invgdp': '', 'pop': county_pop, 'area': county_area}
